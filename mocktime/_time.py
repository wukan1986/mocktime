import time as _time

from datetime import datetime as _datetime_datetime

# 是否伪造时间，默认只要导入就生效
is_mock: bool = True
# 是否时间流逝
is_tick: bool = False

# 源函数
_time_old = _time.time
_tm: float = 0.0
_offset: float = 0.0


def time_update(t) -> float:
    """更新模拟时间"""
    global _tm
    if isinstance(t, _datetime_datetime):
        _tm = t.timestamp()
        return _tm
    if isinstance(t, (int, float)):
        _tm = t
        return _tm
    if t is None:
        _tm = _time.time()
        return _tm
    if isinstance(t, tuple):
        _tm = _time.mktime(t)
        return _tm


def time_add(t: float) -> float:
    """模拟时间自加"""
    global _tm
    if t is not None:
        _tm += t
    return _tm


def _offset_update() -> None:
    """更新偏移。用于时间流逝"""
    global _offset
    _offset = _tm - _time_old()


def _time_new() -> float:
    global _tm
    if is_tick:
        _tm = _time_old() + _offset
    if is_mock:
        return _tm
    else:
        return _time_old()


_time.time = _time_new
