# Cloud-Genshin-Impact

云●原神 每日自动签到送15分钟脚本。

## 介绍



## 使用说明

1. 安装依赖库：在运行代码之前，请确保已安装以下依赖库：
- requests
- email
- apscheduler
- python-dotenv

```bash
pip install requests email apscheduler python-dotenv
```
如果你使用python3，你可能需要使用pip3来安装依赖库。
```bash
pip3 install requests email apscheduler python-dotenv
```
- 如果您使用的是虚拟环境，请确保已经激活了虚拟环境再执行上述命令。
设置环境变量：
```
cp .env.example .env 
```

在运行代码之前，请确保已设置以下环境变量：

```
# 用户token,用逗号分隔
TOKEN= '1', '2', '3'  # 抓包 header中的x-rpc-combo_token
# 用户DEVICE_ID，用逗号分隔，顺序与用户token对应
DEVICE_ID= '1', '2', '3'  # 抓包 header中的x-rpc-device_id
# 备注信息，顺序与用户token对齐
TOKEN_REMARKS=1,2,3
# 通知邮箱，顺序与用户token对齐
NOTIFICATION_EMAILS==1,2,3

# 管理员邮箱，接受所有账号的通知信息
ADMIN_EMAIL=9

# SMTP配置
# SMTP 服务器地址
SMTP_SERVER=smtp.qq.com
# SMTP 服务器端口号
SMTP_PORT=465
# 邮箱用户名
SMTP_USERNAME=yscpush@qq.cn
# 邮箱密码/授权码
SMTP_PASSWORD=dtvATih69e4
# 发件人邮箱
SENDER_EMAIL=yscpush@qq.cn
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

## 定时任务

代码中已包含定时任务的设置，可以根据需要进行调整。

## 代码基于 https://github.com/fves1997/Cloud-Genshin-Impact 修改 增加邮件通知功能，多账号签到。定时任务






