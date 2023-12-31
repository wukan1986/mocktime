"""演示schedule库的使用

pip install schedule -U

1. 代码简洁，实现历史回测功能特别方便
2. 结构简单，运行速度快
2. 复杂条件很难实现，比如周一到周五的开盘时间运行就很难，需要多条job配合，或job中进行判断
    https://github.com/dbader/schedule/pull/581

"""
import logging  # LogRecord使用的time.time()将被替换
import time
from datetime import datetime  # datetime.now()将被替换

from schedule import Scheduler

import mocktime
from strategy import add_jobs

# 修改日志级别，可观察`schedule`的日志，方便调试
logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(filename)s:%(funcName)s:%(lineno)d - %(message)s')
logging.getLogger('schedule').setLevel(logging.WARNING)


def backtest_main_loop(scheduler: Scheduler):
    """回测主循环"""
    while True:
        scheduler.run_pending()
        # 更新时间
        next_run = scheduler.get_next_run()
        if next_run is None:
            break
        mocktime.time_update(next_run.timestamp())


def live_main_loop(scheduler: Scheduler):
    """实盘主循环"""
    while True:
        scheduler.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    # TODO 开始时间
    start_date = datetime(2023, 1, 2, 3, 4, 5, 6000)
    # 将时间改成起始时间
    mocktime.time_update(start_date)
    # TODO 模式配置。共有三种模式，按需设置
    mocktime.configure(mock=False, tick=True)

    # TODO 结束时间
    end_date = datetime(2023, 1, 3) if mocktime.is_mock() else mocktime.max
    logging.warning('mock time:{}, real time:{}'.format(datetime.now(), mocktime.now()))

    scheduler = Scheduler()
    scheduler = add_jobs(scheduler, end_date)

    print('Press Ctrl+C to exit')

    try:
        if mocktime.is_tick():
            live_main_loop(scheduler)
        else:
            backtest_main_loop(scheduler)
    except (KeyboardInterrupt, SystemExit):
        pass
