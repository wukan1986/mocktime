from mocktime._version import __version__

_ = __version__

# ==========================================
# time.time patch
import mocktime._time as _mocktime_time
from mocktime._time import time_update, time_add, _offset_update


def configure(*, mock: bool = True, tick: bool = False):
    """设置参数

    Parameters
    ----------
    mock: bool
        模拟时间
    tick: bool
        时间流逝

    """
    _mocktime_time.is_tick = tick
    if tick:
        _offset_update()
        mock = True
    _mocktime_time.is_mock = mock


def is_mock():
    """是否模拟时间"""
    return _mocktime_time.is_mock


def is_tick():
    """是否时间流逝"""
    return _mocktime_time.is_tick


# ==========================================
# loguru._datetime补丁一定要在datetime补丁之前
try:
    from mocktime._loguru import *
except ImportError:
    pass

# ==========================================
# datetime.datetime补丁一定要在最后
from mocktime._datetime import now

# ==========================================
# 顺序乱了可能报错如下
#
#  File "site-packages\loguru\_datetime.py", line 90, in aware_now
#     timestamp = now.timestamp()
# OSError: [Errno 22] Invalid argument
