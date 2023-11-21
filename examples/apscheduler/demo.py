"""演示apscheduler库的使用

pip install apscheduler -U

1. 支持cron

"""
import mocktime

# TODO 实盘与回测开关
mocktime.is_mock = True

import logging  # LogRecord使用的time.time()将被替换
from datetime import datetime  # datetime.now()将被替换
from loguru import logger  # loguru._datetime.datetime将被替换
from apscheduler.schedulers.base import BaseScheduler

# 修改日志级别，可观察`apscheduler`的日志，方便调试
logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(filename)s:%(funcName)s:%(lineno)d - %(message)s')
logging.getLogger('apscheduler').setLevel(logging.WARNING)


class Strategy:
    def __init__(self, sched: BaseScheduler) -> None:
        self.sched: BaseScheduler = sched

    def before_trading(self) -> None:
        logger.info('{}, {}', datetime.now(), mocktime.now())

    def after_trading(self) -> None:
        logger.info('{}, {}', datetime.now(), mocktime.now())

    def on_bar(self, info) -> None:
        # 此函数调用比较多，但apscheduler又比较慢，可以考虑当天所有bar一次性处理完
        logger.info('{}, {}, {}, {}', datetime.now(), mocktime.now(), info, self.sched.state)


if __name__ == '__main__':
    # TODO 将时间改成起始时间
    mocktime.time_update(datetime(2023, 1, 2, 3, 4, 5, 6))
    print('mock time:{}, real time:{}'.format(datetime.now(), mocktime.now()))

    # 添加任务
    kwargs = {
        'max_instances': 2,  # 使用DebugExecutor时，此参数无实际意义
    }

    if mocktime.is_mock:
        from apscheduler.executors.debug import DebugExecutor
        from examples.apscheduler.scheduler import BacktestBlockingScheduler

        # TODO 回测结束时间必须加，时间到会自动退出，否则会一直运行下去
        kwargs.update({'end_date': datetime(2023, 1, 3)})

        # 只能同一线程，否则因为datetime快于job会报错
        executors = {"default": DebugExecutor(), }
        scheduler = BacktestBlockingScheduler(executors=executors)
    else:
        from apscheduler.schedulers.blocking import BlockingScheduler

        scheduler = BlockingScheduler()

    # 可以向策略传递信息，免去使用全局变量
    strategy = Strategy(scheduler)

    scheduler.add_job(strategy.before_trading, 'cron', hour=9, minute=20, **kwargs)
    scheduler.add_job(strategy.after_trading, 'cron', hour=14, minute=55, **kwargs)
    scheduler.add_job(strategy.on_bar, 'cron', hour='0-23', minute='*', **kwargs, args=('test',))

    print('Press Ctrl+C to exit')

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
