from mocktime._version import __version__

_ = __version__

# ==========================================
# time.time patch

import time as _time
from datetime import datetime as _datetime_datetime

# 是否伪造时间，默认只要导入就生效
is_mock: bool = True

_time_old = _time.time
_t: float = 0.0


def time_update(t) -> float:
    global _t
    if isinstance(t, _datetime_datetime):
        _t = t.timestamp()
        return _t
    if isinstance(t, (int, float)):
        _t = t
        return _t
    if t is None:
        _t = _time.time()
        return _t
    if isinstance(t, tuple):
        _t = _time.mktime(t)
        return _t


def time_add(t: float) -> float:
    global _t
    if t is not None:
        _t += t
    return _t


def _time_new() -> float:
    return _t if is_mock else _time_old()


_time.time = _time_new

# ==========================================
# loguru._datetime patch must before datetime patch
try:
    from mocktime._loguru import *
except ImportError:
    pass
# ==========================================
# datetime.datetime patch must after loguru patch
from mocktime._datetime import now

# ==========================================
# if loguru._datetime patch after datetime patch
#
#  File "site-packages\loguru\_datetime.py", line 90, in aware_now
#     timestamp = now.timestamp()
# OSError: [Errno 22] Invalid argument
