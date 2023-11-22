# mocktime

通过对`time.time()`和`datetime.now()`的修改，实现模拟时间功能

## 项目起源

1. 本项目来自于使用定时任务调度框架实现程序化交易回测的一个设想
2. 策略一般由行情事件驱动，但在开盘前和收盘后无行情，只能靠定时任务来驱动。如：`before_trading`,`after_trading`
3. K线行情事件本质上可认为也是固定频率的定时任务。如：`on_bar`
4. 定时任务框架一般只能用于实盘，因为它的时间机制是**基于操作系统**，而回测的时间是**基于历史数据**
5. 框架中大量的使用到`datetime.now()`, 它无法根据历史进行修改，而本项目就是为了打破这个限制而做的尝试
6. 最先支持了`apscheduler`，之后支持了日志库`logging`和`loguru`
7. 编写了`schedule`的示例后，想到可能还有其它调度库需要模拟时间
8. 后来还想到模拟时间功能可以快速的检测任务规则是否编写正确，很有必要独立成一个项目

## 原理

1. `datetime.datetime`打补丁，使其可以修改成任意时间，这样其它模块就可以取到历史时间
2. `datetime.now()`中使用了`time.time()`，替换它成历史时间
3. 每个任务执行完后更新`time.time()`为下次任务的触发时间

## 安装

```bash
pip install mocktime -U
```

# 示例

```python
import time
from datetime import datetime

import mocktime

if __name__ == '__main__':
    mocktime.configure(mock=True, tick=False)
    print('真实时间:', mocktime.now())
    print('默认模拟时间:', datetime.now())

    mocktime.configure(mock=False, tick=False)
    print('还原成真实时间:', datetime.now())

    mocktime.configure(mock=True, tick=False)
    mocktime.time_update(datetime(2023, 1, 2, 3, 4, 5))
    print('更新模拟时间:', datetime.now())

    mocktime.time_add(5.1)
    print('模拟时间+5.1s:', datetime.now())

    mocktime.configure(mock=True, tick=True)
    time.sleep(5)
    print('开启时间流逝，等5s:', datetime.now())
    mocktime.configure(mock=True, tick=False)
    time.sleep(5)
    print('关闭时间流逝，等5s:', datetime.now())
```

输出如下

```text
真实时间: 2023-11-22 14:42:02.505068
默认模拟时间: 1970-01-01 08:00:00
还原成真实时间: 2023-11-22 14:42:02.505068
更新模拟时间: 2023-01-02 03:04:05
模拟时间+5.1s: 2023-01-02 03:04:10.100000
开启时间流逝，等5s: 2023-01-02 03:04:15.103451
关闭时间流逝，等5s: 2023-01-02 03:04:15.103451
```

## 调度任务示例

### apscheduler `examples/apscheduler/demo.py`

1. 导入`mocktime`后，设置好过去的开始与结束时间，但任务并没有继续执行。因为模拟时间是固定不变的
2. 需继承`BlockingScheduler`，在每批次的任务执行完后立即更新时间`mocktime.time_add`

### schedule `examples/schedule/demo.py`

1. 同样遇到需更新模拟时间问题
2. 在循环中取`get_next_run`，然后更新时间`mocktime.time_update`

## 参考资料

1.《深度剖析CPython解释器》34.
侵入Python虚拟机，动态修改底层数据结构和运行时 - https://www.cnblogs.com/traditional/p/15489296.html