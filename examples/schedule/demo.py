"""演示schedule库的使用

pip install schedule -U


1. 代码简洁，实现历史回测功能特别方便
2. 复杂条件很难实现，比如周一到周五的开盘时间运行就很难，需要多条job配合，或job中进行判断
    https://github.com/dbader/schedule/pull/581

"""
import mocktime

# TODO 实盘与回测开关
mocktime.is_mock = True

import time
import logging  # LogRecord使用的time.time()将被替换
from datetime import datetime  # datetime.now()将被替换
from loguru import logger  # loguru._datetime.datetime将被替换
from schedule import Scheduler

# 修改日志级别，可观察`schedule`的日志，方便调试
logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(filename)s:%(funcName)s:%(lineno)d - %(message)s')
logging.getLogger('schedule').setLevel(logging.WARNING)


class Strategy:
    def __init__(self, sched: Scheduler) -> None:
        self.sched: Scheduler = sched

    def before_trading(self) -> None:
        logger.info('{}, {}', datetime.now(), mocktime.now())

    def after_trading(self) -> None:
        logger.info('{}, {}', datetime.now(), mocktime.now())

    def on_bar(self, info) -> None:
        logger.info('{}, {}, {}, {}', datetime.now(), mocktime.now(), info, len(self.sched.get_jobs()))


if __name__ == '__main__':
    # TODO 将时间改成起始时间
    mocktime.time_update(datetime(2023, 1, 2, 3, 4, 5, 6))
    print('mock time:{}, real time:{}'.format(datetime.now(), mocktime.now()))

    if mocktime.is_mock:
        # 结束时间，测试用
        end_date = datetime(2023, 1, 3)
    else:
        end_date = datetime(2030, 12, 31)

    scheduler = Scheduler()

    # 可以向策略传递信息，免去使用全局变量
    strategy = Strategy(scheduler)

    # 任务，无法写复杂外触发条件
    scheduler.every().days.at('09:20').until(end_date).do(strategy.before_trading)
    scheduler.every().days.at('14:55').until(end_date).do(strategy.after_trading)
    scheduler.every(30).minutes.until(end_date).do(strategy.on_bar, info='test')

    print('Press Ctrl+C to exit')

    if mocktime.is_mock:
        from examples.schedule.scheduler import backtest_main_loop

        backtest_main_loop(scheduler)
    else:
        while True:
            scheduler.run_pending()
            time.sleep(1)
