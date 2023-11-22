"""演示apscheduler库的使用

pip install apscheduler -U

1. 支持cron，条件灵活

"""
import logging  # LogRecord使用的time.time()将被替换
from datetime import datetime  # datetime.now()将被替换

from apscheduler.executors.debug import DebugExecutor
from apscheduler.schedulers.base import STATE_STOPPED
from apscheduler.schedulers.blocking import BlockingScheduler

import mocktime
from examples.apscheduler.strategy import add_jobs

# 修改日志级别，可观察`apscheduler`的日志，方便调试
logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(filename)s:%(funcName)s:%(lineno)d - %(message)s')
logging.getLogger('apscheduler').setLevel(logging.WARNING)


class BacktestBlockingScheduler(BlockingScheduler):
    """删除事件等待，回测速度快"""

    def _main_loop(self):
        import mocktime

        while self.state != STATE_STOPPED:
            wait_seconds = self._process_jobs()
            if wait_seconds is None:
                # 设置了end_date后，由于运行到最后无任务了，此值返回None退出
                self.shutdown()
            else:
                # 将时间更新放到所有任务执行完后再更新，防止第一个任务修改了时间后，后续同批任务由于时间已过而跳过
                # 但多线程模式下，这个时间已经改了，子任务还没执行，所以必需要使用一个线程来跑
                mocktime.time_add(wait_seconds)


if __name__ == '__main__':
    # TODO 实盘与回测开关
    mocktime.configure(mock=True, tick=False)

    # TODO 开始时间，结束时间
    start_date = datetime(2023, 1, 2, 3, 4, 5, 6000)
    end_date = datetime(2023, 1, 3) if mocktime.is_mock() else datetime(2099, 12, 31)

    # 将时间改成起始时间
    mocktime.time_update(start_date)
    logging.warning('mock time:{}, real time:{}'.format(datetime.now(), mocktime.now()))

    # 添加任务
    kwargs = {
        'max_instances': 2,  # 使用DebugExecutor时，此参数无实际意义
        'end_date': end_date,  # TODO 回测结束时间必须加，时间到会自动退出，否则会一直运行下去
    }

    if mocktime.is_mock():
        # 只能同一线程，否则因为datetime快于job会报错
        executors = {"default": DebugExecutor(), }
        scheduler = BacktestBlockingScheduler(executors=executors)
    else:
        scheduler = BlockingScheduler()

    # 可以向策略传递信息，免去使用全局变量
    add_jobs(scheduler, kwargs)

    print('Press Ctrl+C to exit')

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
