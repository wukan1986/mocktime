from loguru._datetime import datetime as _loguru_datetime

from mocktime import _time_new

_loguru_now_old = _loguru_datetime.now


def _loguru_now_new(tz=None) -> _loguru_datetime:
    return _loguru_datetime.fromtimestamp(_time_new(), tz)


_loguru_datetime.now = _loguru_now_new
