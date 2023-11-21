from apscheduler.schedulers.base import STATE_STOPPED
from apscheduler.schedulers.blocking import BlockingScheduler


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
