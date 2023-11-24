"""
由于grpc有部分取时间功能是在C层内部实现的，
客户端会生成一个截止时间，如果返回信息差距太大会报错，
但服务端的时间是底层做的判断，所以不得不进行处理，

所以不得不在上层保持原版time
"""
from typing import Optional

import grpc._channel

import mocktime

_deadline_old = grpc._channel._deadline


def _deadline_new(timeout: Optional[float]) -> Optional[float]:
    return None if timeout is None else mocktime.time() + timeout


grpc._channel._deadline = _deadline_new
