# Cloud-Genshin-Impact

云●原神 每日自动签到送15分钟脚本。

## 介绍

- 云原神自动签到
- 多账号自动签到
- 定时任务
- 接入WXPusher微信推送状态


## 使用说明

1. 安装依赖库：在运行代码之前，请确保已安装以下依赖库：
- requests

```bash
pip install requests
```
如果你使用python3，你可能需要使用pip3来安装依赖库。
```bash
pip3 install requests
```
- 如果您使用的是虚拟环境，请确保已经激活了虚拟环境再执行上述命令。
- 设置配置信息，将config.py.example重命名为config.py。
- 填写对应信息

```
cp config.py.example config.py
```

## 使用

使用以下命令运行代码：
```
python app.py
```
如果你使用python3，你可能需要使用python3来运行代码。
```
python3 app.py
```



### 代码基于 [Cloud-Genshin-Impact 项目](https://github.com/fves1997/Cloud-Genshin-Impact) 修改。

### 本项目已经内置定时器如您使用云函数尝试部署
请注意以下几点：

1. 在云函数中，不需要手动运行`main_handler`函数或设置定时器。云函数会根据事件触发自动执行代码。

2. 在云函数中，日志将会自动打印到云函数的日志系统中，您可以在云函数的日志中查看日志信息。

3. 请确保您的云函数环境已经正确配置了`config.py`文件中的配置项，并且可以正常访问WxPusher的API。

4. 在云函数中，建议将`sign_in`函数作为云函数的入口函数，并在函数代码中调用`sign_in`函数。

