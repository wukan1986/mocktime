from datetime import datetime

from loguru import logger  # loguru._datetime.datetime将被替换
from schedule import Scheduler

import mocktime


class Strategy:
    def __init__(self, sched: Scheduler) -> None:
        self.sched: Scheduler = sched

    def before_trading(self) -> None:
        logger.info('{}, {}', datetime.now(), mocktime.now())

    def after_trading(self) -> None:
        logger.info('{}, {}', datetime.now(), mocktime.now())

    def on_bar(self, info) -> None:
        logger.info('{}, {}, {}, {}', datetime.now(), mocktime.now(), info, len(self.sched.get_jobs()))


def add_jobs(sched: Scheduler, end_date: datetime) -> None:
    strategy = Strategy(sched)

    # 无法写复杂外触发条件
    sched.every().days.at('09:20').until(end_date).do(strategy.before_trading)
    sched.every().days.at('14:55').until(end_date).do(strategy.after_trading)
    sched.every(30).minutes.until(end_date).do(strategy.on_bar, info='test')
