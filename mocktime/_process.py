import os
import pathlib
import pickle
from datetime import datetime

from mocktime import configure
from mocktime._time import _time_old, offset_update, time_update


def _dump(path, start_time: float):
    """记录真实时间与模拟时间，将给其它进程使用"""
    with open(path, 'wb') as f:
        d = {'start_time': start_time, 'create_time': _time_old()}
        _start = datetime.fromtimestamp(d['start_time'])
        _create = datetime.fromtimestamp(d['create_time'])
        print('pid:{} save time to `{}`, start:{}, create:{}, offset:{}'.format(
            os.getpid(), path,
            _start, _create, _start - _create))
        pickle.dump(d, f)


def _load(path):
    with open(path, 'rb') as f:
        d = pickle.load(f)
    create_time = d['create_time']
    start_time = d['start_time']
    _create = datetime.fromtimestamp(create_time)
    _start = datetime.fromtimestamp(start_time)
    _offset = start_time - create_time
    _now = datetime.fromtimestamp(_time_old() + _offset)
    print('pid:{} load time from `{}`, start:{}, create:{}, now:{}'.format(
        os.getpid(), path,
        _start, _create, _now))
    return _offset


def multiprocess(path: str, t: float):
    """多进程共享模拟时间

    Parameters
    ----------
    path: str
        时间信息保存路径。由于不同进程的当前目录可能不同，强列建议使用绝对路径
    t: float
        模拟时间戳。创建时有效，加载时忽略

    Notes
    -----
    多进程时间模拟只有`configure(mock=True, tick=True)`一种模式。
    而由一个进程修改时间后其它进程时间也变动的模式暂不支持

    """
    path = pathlib.Path(path)
    # 为防止用户误用相对路径，导致多个项目启动产生无处不在的文件
    assert path.is_absolute(), 'path must be absolute'

    if path.exists():
        configure(mock=True, tick=True)
        offset = _load(path)
        offset_update(offset)
    else:
        assert isinstance(t, (int, float))

        time_update(t)
        configure(mock=True, tick=True)
        _dump(path, t)
