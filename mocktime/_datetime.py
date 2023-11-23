from datetime import datetime as _datetime_datetime

from mocktime._time import _time_new, _time_old
from mocktime.unsafe_magic import patch_builtin_class

_datetime_now_old = _datetime_datetime.now


def now(tz=None) -> _datetime_datetime:
    return _datetime_datetime.fromtimestamp(_time_old(), tz)


def _datetime_now_new(tz=None) -> _datetime_datetime:
    return _datetime_datetime.fromtimestamp(_time_new(), tz)


patch_builtin_class(_datetime_datetime, 'now', _datetime_now_new)

# 开始时间设为1970年
min = _datetime_datetime.fromtimestamp(0)
# 最大时间如果是int64的最大值取timestamp()会报错，所以设了一个比较大的值
max = _datetime_datetime(3000, 1, 1)
