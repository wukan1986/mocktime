import time
from datetime import datetime

import mocktime

mocktime.multiprocess('a.pkl', datetime(2025, 1, 1).timestamp())
# 多次执行此文件可发现时间会不断增加
print(datetime.now(), time.time())
