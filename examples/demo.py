from datetime import datetime

import mocktime

if __name__ == '__main__':
    # 打印真实时间
    print('mocktime.now:', mocktime.now())

    # 打印默认伪造时间
    print('datetime.now, is_mock = True:', datetime.now())
    # 还原
    mocktime.is_mock = False
    print('datetime.now, is_mock = False:', datetime.now())

    # 更新伪造时间
    mocktime.time_update(datetime(2020, 1, 1, 1, 1, 1))
    print('datetime.now, is_mock = False:', datetime.now())
    mocktime.is_mock = True
    print('datetime.now, is_mock = True:', datetime.now())

    # 增加伪造时间
    mocktime.time_add(5)
    print('datetime.now, is_mock = True:', datetime.now())
