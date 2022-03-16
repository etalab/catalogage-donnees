"""
Datetime utilities focused on manipulating tz-aware datetimes only.

See: https://julien.danjou.info/python-and-timezones/
"""

import datetime as dt

UTC = dt.timezone.utc


def now(tz: dt.tzinfo = UTC) -> dt.datetime:
    return dt.datetime.now(tz)


def parse(text: str) -> dt.datetime:
    return dt.datetime.fromisoformat(text)
