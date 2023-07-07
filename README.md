# Cloud-Genshin-Impact

云●原神 每日自动签到送15分钟脚本。

## 介绍

- 云原神自动签到
- 多账号自动签到
- 定时任务
- 接入WXPusher微信推送状态
[WXPusher](https://wxpusher.zjiecode.com/admin/)地址 根据提示注册并获取UID和APP_TOKEN填入config.py中

## 使用说明  

> 注意： 本项目是使用Python 3.x语法编写的，其中包括了一些Python 3.x才引入的功能和语法。如果您使用的是Python 2.x版本，其中某些部分可能无法直接运行。
> 
> 若要在Python 2.x中运行代码，您需要进行一些适应性修改，以兼容Python 2.x的语法和库。


1. 安装依赖库：在运行代码之前，请确保已安装以下依赖库：
- requests

```bash
pip install requests
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




### 代码基于 [Cloud-Genshin-Impact 项目](https://github.com/fves1997/Cloud-Genshin-Impact) 修改。

### 本项目已经内置定时器.

### 如您需要云函数部署,可能需要自定义入口函数，并修改代码中的定时器部分。本人未尝试过云函数部署，如有问题请自行解决。