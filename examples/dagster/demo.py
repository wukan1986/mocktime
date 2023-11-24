"""
dagster示例

dagster会启动多个进程，但`mocktime.configure`仅是单进程内有效
1. 使用`mocktime.multiprocess`可实现多个进程共享同一套模拟时间
2. 多个进程需要使用同一时间配置文件，要保证每个进程都能导入`mocktime`
3. 一般的项目都有`__init__.py`，规范的项目必有`__version__`
4. 由于`version.py`中只有一行，额外代码放这清晰易管理
5. 用完后一定要还原此处

"""

# 在IDE中，按`Ctrl`, 鼠标移动到`__version__`,可跳转到`version.py`
from dagster.version import __version__

_ = __version__
# =================================
# 复制以下代码到`version.py`中。按常规用法使用`dagster`。不需要时删除即可

from datetime import datetime

import mocktime

# TODO 自定义配置文件和启动时间
# 强烈建议使用绝对路径
mocktime.multiprocess(r'd:\a.pkl', datetime(2022, 1, 1).timestamp())
