from datetime import datetime as _datetime_datetime

from mocktime import _time_new, _time_old
from mocktime.unsafe_magic import patch_builtin_class

_datetime_now_old = _datetime_datetime.now


def now(tz=None) -> _datetime_datetime:
    return _datetime_datetime.fromtimestamp(_time_old(), tz)


def _datetime_now_new(tz=None) -> _datetime_datetime:
    return _datetime_datetime.fromtimestamp(_time_new(), tz)


patch_builtin_class(_datetime_datetime, 'now', _datetime_now_new)
