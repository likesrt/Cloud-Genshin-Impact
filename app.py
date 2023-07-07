import logging
import time
import requests
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from config import USERS, ADMIN_UID, WX_APP_TOKEN

# 定义日志格式
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 创建日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建命令行日志处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

# 创建文件日志处理器
file_handler = RotatingFileHandler('app.log', maxBytes=10*1024*1024, backupCount=5, encoding='utf-8')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)


host = 'https://api-cloudgame.mihoyo.com'

headers = {
    "x-rpc-client_type": "2",
    "x-rpc-app_version": "1.3.0",
    "x-rpc-sys_version": "11",
    "x-rpc-channel": "mihoyo",
    "x-rpc-device_name": "Xiaomi Mi 10 Pro",
    "x-rpc-device_model": "Mi 10 Pro",
    "x-rpc-app_id": "1953439974",
    "Referer": "https://app.mihoyo.com",
    "Content-Length": "0",
    "Host": "api-cloudgame.mihoyo.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/3.14.9"
}


def send_wxpusher_notification(content, uids):
    data = {
        "appToken": WX_APP_TOKEN,
        "content": content,
        "contentType": 1,
        "uids": uids
    }
    response = requests.post("https://wxpusher.zjiecode.com/api/send/message", json=data)
    response_data = response.json()
    if response_data["code"] == 1000:
        logging.info("WxPusher通知发送成功")
    else:
        logging.error("WxPusher通知发送失败")


def process_user(user):
    token = user["token"]
    device_id = user["device_id"]
    remark = user["remark"]
    notification_uid = user["notification_uid"]

    user_headers = {
        "x-rpc-combo_token": token,
        "x-rpc-device_id": device_id,
        **headers
    }

    try:
        # 登录
        rsp = requests.post(f'{host}/hk4e_cg_cn/gamer/api/login', headers=user_headers)
        logging.debug(f"Login -> {rsp.text}")

        # 获取钱包信息
        rsp = requests.get(f'{host}/hk4e_cg_cn/wallet/wallet/get', headers=user_headers)
        coins = rsp.json()['data']['coin']
        free_times = rsp.json()['data']['free_time']
        total_time = rsp.json()['data']['total_time']
        logging.debug(f"Wallet -> {rsp.json()}")

        return "签到成功", f"{remark} - 米云币:{coins['coin_num']},免费时长:{free_times['free_time']}分钟,总免费时长:{total_time}分钟"
    except Exception as e:
        logging.error(f"{remark} - 处理失败: {str(e)}")
        return "签到失败", ""


def sign_in():
    now = datetime.now()
    content = f"签到通知 - {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
    success_users = []

    for user in USERS:
        status, sign_in_info = process_user(user)
        remark = user["remark"]
        if status == "签到成功":
            success_users.append(remark)

        user_content = f"{remark} - {status}\n{sign_in_info}"
        send_wxpusher_notification(user_content, [user["notification_uid"]])


        content += f"{remark} - {status}\n"

    content += f"成功签到用户数: {len(success_users)}\n"
    if len(success_users) > 0:
        content += "成功签到的用户:\n"
        for user in success_users:
            content += f"- {user}\n"

    send_wxpusher_notification(content, [ADMIN_UID])


def main():
    while True:
        try:
            sign_in()
            logging.info("处理成功")
        except Exception as e:
            logging.error(f"处理失败: {str(e)}")
            send_wxpusher_notification("处理失败，请检查日志", [ADMIN_UID])

        # 设置定时器，每天零点40分执行一次签到
        now = datetime.now()
        target_time = now.replace(hour=0, minute=40, second=0, microsecond=0)
        if now > target_time:
            target_time += timedelta(days=1)
        delta = target_time - now
        delay_seconds = delta.total_seconds()

        logging.info(f"等待 {delay_seconds} 秒后再次执行签到")
        time.sleep(delay_seconds)


if __name__ == '__main__':
    main()
