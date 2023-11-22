import time
from datetime import datetime

import mocktime

if __name__ == '__main__':
    mocktime.configure(mock=True, tick=False)
    print('真实时间:', mocktime.now())
    print('默认模拟时间:', datetime.now())

    mocktime.configure(mock=False, tick=False)
    print('还原成真实时间:', datetime.now())

    mocktime.configure(mock=True, tick=False)
    mocktime.time_update(datetime(2023, 1, 2, 3, 4, 5))
    print('更新模拟时间:', datetime.now())

    mocktime.time_add(5.1)
    print('模拟时间+5.1s:', datetime.now())

    mocktime.configure(mock=True, tick=True)
    time.sleep(5)
    print('开启时间流逝，等5s:', datetime.now())
    mocktime.configure(mock=True, tick=False)
    time.sleep(5)
    print('关闭时间流逝，等5s:', datetime.now())
