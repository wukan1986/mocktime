import time as _time

from datetime import datetime as _datetime_datetime
from typing import Optional

# 是否伪造时间，默认只要导入就生效
is_mock: bool = True
# 是否时间流逝
is_tick: bool = False

# 源函数
_time_old = _time.time
_tm: float = 0.0
_offset: float = 0.0


def time_update(t) -> float:
    """更新模拟时间

    Notes
    -----
    如果当前是时间流逝模式，将以新时间为起点开始流逝
    """
    global _tm
    while True:
        if isinstance(t, _datetime_datetime):
            _tm = t.timestamp()
            break
        if isinstance(t, (int, float)):
            _tm = t
            break
        if t is None:
            _tm = _time.time()
            break
        if isinstance(t, tuple):
            _tm = _time.mktime(t)
            break
        # 跳出，使用do while模仿goto语法
        break

    if is_tick:
        # 正在流逝模式，需要强行更新_offset
        offset_update(None)
    return _tm


def time_add(t: float) -> float:
    """模拟时间自加"""
    global _tm
    if t is None:
        return _tm

    _tm += t
    if is_tick:
        # 正在流逝模式，需要强行更新_offset
        offset_update(None)
    return _tm


def offset_update(offset: Optional[float] = None) -> None:
    """更新偏移。用于时间流逝"""
    global _offset
    if offset is None:
        # 只在被调用时记录下与模拟时间的偏移
        _offset = _tm - _time_old()
    else:
        _offset = offset


def _time_new() -> float:
    global _tm
    if is_tick:
        # 当时间流逝时，计算新的时间
        _tm = _time_old() + _offset
    if is_mock:
        return _tm
    else:
        return _time_old()


_time.time = _time_new
