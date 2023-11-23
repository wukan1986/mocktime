from datetime import datetime

from apscheduler.schedulers.base import BaseScheduler
from loguru import logger  # loguru._datetime.datetime将被替换

import mocktime


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


def add_jobs(sched: BaseScheduler, kwargs) -> BaseScheduler:
    strategy = Strategy(sched)

    sched.add_job(strategy.before_trading, 'cron', hour=9, minute=20, **kwargs)
    sched.add_job(strategy.after_trading, 'cron', hour=14, minute=55, **kwargs)
    sched.add_job(strategy.on_bar, 'cron', hour='0-23', minute='*', **kwargs, args=('test',))

    return sched
