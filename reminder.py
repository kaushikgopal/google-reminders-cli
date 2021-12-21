import functools
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


def gen_id() -> str:
    """generate a fresh reminder id"""
    # id is set according to the current unix time
    return f'cli-reminder-{time.time()}'


@dataclass
@functools.total_ordering
class Reminder:
    id: str
    title: str
    dt: datetime
    all_day: bool = False
    creation_timestamp_msec: Optional[int] = None
    done: bool = False

    def __repr_title(self):
        """
        if reminder is not done return its title as is. otherwise return
        a strikethrough title
        """
        return (
            self.title if not self.done
            else '̶'.join(c for c in self.title)
        )

    def __lt__(self, other):
        return self.dt < other.dt

    def __repr_date(self):
        return (
            self.dt.strftime('%Y-%m-%d') + ' (All)' if self.all_day
            else  self.dt.strftime('%Y-%m-%d %H:%M')
        )

    def __repr__(self):
        return f'{self.__repr_date()}: {self.__repr_title()} ; id="{self.id}"'
