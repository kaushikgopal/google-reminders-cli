# google-reminders-cli

**google-reminders-cli** is a simple tool for interacting with _Google reminders_ from the command line.
It allows creating, deleting and watching reminders

Run with `-h` to see all supported actions, acceptable time formats, etc.


## Installation

```
pip3 install requirements.txt
```

On the first run, a consent screen will open in the browser to aquire permission
to access the user's reminders.

App API keys are provided in a separate file, so you may either use them or easily change
them with your own keys.


## Usage examples

Create a reminder interactively:
```
$ python3 remind.py -i
What's the reminder: Pay bills
When do you want to be reminded: tomorrow at 4pm

"Pay bills" on Sun, Jun 02 2019, 16:00

Do you want to save this? [Y/n] y
Reminder set successfully:
2019-06-02 16:00: Pay bills ; id="cli-reminder-1559389411.7416472"
```

or using command line arguments:
```
$ python3 remind.py -c "Pay bills" "tomorrow 17:45"
Reminder set successfully:
2019-06-02 17:45: Pay bills ; id="cli-reminder-1559389443.0839736"
```


**Disclaimer**: Currently there is no official API for _Google Reminders_, so instead,
this tool imitates a browser request. This may cause google-reminders-cli to stop
function correctly at any time.



# Todos

* If a time is not supplied, assume it to be all_day event
* Add concept of end_date
* Add recurring reminders
* Add option to remove confirmation


Notes on recurrence:
```
'recurring': 'https://reminders-pa.clients6.google.com/v1internalOP/reminders/recurrence/create',

Request

{
  "1": {
    "4": "WRP / /WebCalendar/calendar.web_20211214.09_p0"
  },
  "2": {
    "1": 7
  },
  "3": {
    "1": "1640205493557_212712925"
  },
  "4": {
    "3": "CC: pay balances on all cards for good credit score",
    "8": 0
  },
  "5": {
    "1": 2,
    "2": 1,
    "3": {
      "1": {
        "1": 2021,
        "2": 12,
        "3": 22,
        "4": {
          "1": 10,
          "2": 0,
          "3": 0
        }
      }
    },
    "5": {
      "1": {
        "1": 10,
        "2": 0,
        "3": 0
      },
      "3": 0
    },
    "7": {
      "1": [
        22
      ]
    }
  }
}

Response
Body

{
  "1": {
    "1": 2,
    "2": 1,
    "3": {
      "1": {
        "1": 2021,
        "2": 12,
        "3": 22,
        "4": {
          "1": 10,
          "2": 0,
          "3": 0
        }
      }
    },
    "4": {
      "1": {
        "1": 2022,
        "2": 12,
        "3": 22
      },
      "4": 1
    },
    "5": {
      "1": {
        "1": 10,
        "2": 0,
        "3": 0
      },
      "3": 0
    },
    "7": {
      "1": [
        22
      ]
    }
  },
  "2": {
    "1": "11306912",
    "2": "synthesized-version-info"
  }
}


```
