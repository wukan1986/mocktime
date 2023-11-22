# 以下代码要放在datetime.datetime patch 之前，是否要防止这里用的改版后的datetime.now?
from loguru._datetime import datetime as _loguru_datetime

from mocktime._time import _time_new

_loguru_now_old = _loguru_datetime.now


def _loguru_now_new(cls, tz=None) -> _loguru_datetime:
    return _loguru_datetime.fromtimestamp(_time_new(), tz)


_loguru_datetime.now = classmethod(_loguru_now_new)
