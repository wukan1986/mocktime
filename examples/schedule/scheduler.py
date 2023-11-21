from schedule import Scheduler

import mocktime


def backtest_main_loop(scheduler: Scheduler):
    """回测主循环"""
    while True:
        scheduler.run_pending()
        # 更新时间
        next_run = scheduler.get_next_run()
        if next_run is None:
            break
        mocktime.time_update(next_run.timestamp())
