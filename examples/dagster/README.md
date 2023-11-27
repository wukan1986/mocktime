# dagster示例

dagster会启动多个进程，但`mocktime.configure`仅是单进程内有效

1. 使用`mocktime.multiprocess`可实现多个进程共享同一套模拟时间
2. 多个进程需要使用同一时间配置文件，要保证每个进程都能导入`mocktime`

## 方案一

1. 只对虚拟环境下单个库产生影响
2. 一般的项目都有`__init__.py`，规范的项目必有`__version__`，由于`version.py`中只有一行，额外代码放这清晰易管理
3. 将`usercustomize.py`内的**代码**，复制到`dagster\version.py`中，可按需求修改此代码
4. 运行`dagster`项目。用完后一定要还原此处

## 方案二

1. 对虚拟环境下所有库产生影响
2. python解释器支持`site`. 默认会导入`usercustomize.py`和`sitecustomize.py`。可通过`python -s`临时禁用
3. 将`usercustomize.py`**文件**复制到当前环境的`site-packages`目录下，可按需求修改其中的代码
4. 运行`dagster`项目。用完后一定要还原此处

- 可通过`python -m site`得到当前环境中的`site-packages`目录。例如：
    - `D:\Users\Xxx\miniconda3\envs\py311\Lib\site-packages`

## 参考链接

https://docs.python.org/zh-cn/3/library/site.html#module-usercustomize