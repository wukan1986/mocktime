"""
复制到`site-packages`目录下，并修改代码

可通过`python -m site`得到当前环境中的`site-packages`目录
"""
print('__file__:', __file__)

from datetime import datetime

import mocktime

# TODO 自定义配置文件和启动时间
mocktime.multiprocess(r'd:\a.pkl', datetime(2022, 1, 1).timestamp())
