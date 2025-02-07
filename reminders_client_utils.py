import json
import os
from datetime import datetime, timedelta
from typing import Optional

import httplib2
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

from reminder import Reminder

APP_KEYS_FILE = os.path.expanduser('~/.config/google-reminders/app_keys.json')
USER_OAUTH_DATA_FILE = os.path.expanduser('~/.config/google-reminders/google-reminders-cli-oauth')


def authenticate() -> httplib2.Http:
    """
    returns an Http instance that already contains the user credentials and is
    ready to make requests to alter user data.

    On the first time, this function will open the browser so that the user can
    grant it access to his data
    """
    with open(APP_KEYS_FILE) as f:
        app_keys = json.load(f)
    storage = Storage(USER_OAUTH_DATA_FILE)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(
            flow=OAuth2WebServerFlow(
                client_id=app_keys['APP_CLIENT_ID'],
                client_secret=app_keys['APP_CLIENT_SECRET'],
                scope=['https://www.googleapis.com/auth/reminders'],
                user_agent='google reminders cli tool',
            ),
            storage=storage,
            flags=tools.argparser.parse_args([]),
        )
    auth_http = credentials.authorize(httplib2.Http())
    return auth_http


def create_req_body(reminder: Reminder) -> str:
    """
    returns the body of a create-reminder request
    """
    body = {
        '2': {
            '1': 7
        },
        '3': {
            '2': reminder.id
        },
        '4': {
            '1': {
                '2': reminder.id
            },
            '3': reminder.title,
            '5': {
                '1': reminder.dt.year,
                '2': reminder.dt.month,
                '3': reminder.dt.day,
            },
            '8': 0
        }
    }
    if reminder.all_day:
        body['4']['5']['9'] = 1
    else:
        body['4']['5']['4'] = {
            '1': reminder.dt.hour,
            '2': reminder.dt.minute,
            '3': reminder.dt.second,
        }
    return json.dumps(body)


def get_req_body(reminder_id: str) -> str:
    """
    returns the body of a get-reminder request
    """
    body = {'2': [{'2': reminder_id}]}
    return json.dumps(body)


def delete_req_body(reminder_id: str) -> str:
    """
    returns the body of a delete-reminder request
    """
    body = {'2': [{'2': reminder_id}]}
    return json.dumps(body)


def list_req_body(num_reminders: int, max_timestamp_msec: int = 0) -> str:
    """
    returns the body of a list-reminders request.

    The body corresponds to a request that retrieves a maximum of num_reminders
    reminders, whose creation timestamp is less than max_timestamp_msec.
    max_timestamp_msec is a unix timestamp in milliseconds. if its value is 0, treat
    it as current time.
    """
    body = {
        '5': 1,  # boolean field: 0 or 1. 0 doesn't work ¯\_(ツ)_/¯
        '6': num_reminders,  # number number of reminders to retrieve
    }

    if max_timestamp_msec:
        max_timestamp_msec += int(timedelta(hours=15).total_seconds() * 1000)
        body['16'] = max_timestamp_msec
        # Empirically, when requesting with a certain timestamp, reminders with the given
        # timestamp or even a bit smaller timestamp are not returned. Therefore we increase
        # the timestamp by 15 hours, which seems to solve this...  ~~voodoo~~
        # (I wish Google had a normal API for reminders)

    return json.dumps(body)


def build_reminder(reminder_dict: dict) -> Optional[Reminder]:
    r = reminder_dict
    try:
        id = r['1']['2']
        title = r['3']
        year = r['5']['1']
        month = r['5']['2']
        day = r['5']['3']
        if '9' in r['5']:
            all_day = True
            hour = minute = second = 0
        else:
            all_day = False
            hour = r['5']['4']['1']
            minute = r['5']['4']['2']
            second = r['5']['4']['3']
        creation_timestamp_msec = int(r['18'])
        done = '8' in r and r['8'] == 1

        return Reminder(
            id=id,
            title=title,
            dt=datetime(year, month, day, hour, minute, second),
            creation_timestamp_msec=creation_timestamp_msec,
            all_day=all_day,
            done=done,
        )

    except KeyError:
        print('build_reminder failed: unrecognized reminder dictionary format')
        return None
