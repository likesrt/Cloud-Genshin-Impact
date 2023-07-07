import logging
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

def send_email(subject, message, receiver):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("SENDER_EMAIL")

    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender_email
    msg['To'] = receiver

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        server.quit()
        logger.info(f"电子邮件已发送到: {receiver}")
    except Exception as e:
        logger.error(f"邮件发送失败: {str(e)}")

def process_account(token, device_id, token_remark, notification_email):
    app_id = '1953439974'
    host = 'https://api-cloudgame.mihoyo.com'

    headers = {
        "x-rpc-client_type": "2",
        "x-rpc-app_version": "1.3.0",
        "x-rpc-sys_version": "11",
        "x-rpc-channel": "mihoyo",
        "x-rpc-device_name": "Xiaomi Mi 10 Pro",
        "x-rpc-device_model": "Mi 10 Pro",
        "x-rpc-app_id": app_id,
        "Referer": "https://app.mihoyo.com",
        "Content-Length": "0",
        "Host": "api-cloudgame.mihoyo.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.14.9"
    }

    try:
        headers["x-rpc-combo_token"] = token
        headers["x-rpc-device_id"] = device_id

        logger.info(f"正在处理: {token}")
        logger.info(f"备注: {token_remark}")
        logger.info(f"通知邮箱: {notification_email}")

        rsp = requests.post(f'{host}/hk4e_cg_cn/gamer/api/login', headers=headers)
        logger.debug(f"Login->{rsp.text}")

        rsp = requests.get(f'{host}/hk4e_cg_cn/wallet/wallet/get', headers=headers)
        coins = rsp.json()['data']['coin']
        free_times = rsp.json()['data']['free_time']
        total_time = rsp.json()['data']['total_time']
        logger.debug(f"Wallet->{rsp.json()}")
        logger.info(f"米云币:{coins['coin_num']},免费时长:{free_times['free_time']}分钟,总免费时长:{total_time}分钟")

        rsp = requests.get(f'{host}/hk4e_cg_cn/gamer/api/listNotifications?status=NotificationStatusUnread'
                           f'&type=NotificationTypePopup&is_sort=true', headers=headers)
        logger.debug(f"ListNotifications->{rsp.text}")
        rewards = rsp.json()['data']['list']
        logger.info(f"总共有{len(rewards)}个奖励待领取。")

        for reward in rewards:
            reward_id = reward['id']
            reward_msg = reward['msg']
            rsp = requests.post(f'{host}/hk4e_cg_cn/gamer/api/ackNotification',
                                json={
                                    "id": reward_id
                                },
                                headers=headers)
            logger.info(f"领取奖励,ID:{reward_id},Msg:{reward_msg}")
            logger.debug(f"AckNotification->{rsp.text}")

        rsp = requests.get(f'{host}/hk4e_cg_cn/wallet/wallet/get', headers=headers)
        coins = rsp.json()['data']['coin']
        free_times = rsp.json()['data']['free_time']
        total_time = rsp.json()['data']['total_time']
        logger.debug(f"Wallet->{rsp.json()}")
        logger.info(f"米云币:{coins['coin_num']},免费时长:{free_times['free_time']}分钟,总免费时长:{total_time}分钟")

        logger.debug("处理成功")
        result = "处理成功"
    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        result = "处理失败"

    # 发送签到结果通知
    subject = f"{token_remark}-签到结果"
    message = f"账号备注: {token_remark}\n签到结果: {result}"
    send_email(subject, message, notification_email)

def main_handler():
    tokens = os.getenv("TOKEN").split(',')
    device_ids = os.getenv("DEVICE_ID").split(',')
    token_remarks = os.getenv("TOKEN_REMARKS").split(',')
    notification_emails = os.getenv("NOTIFICATION_EMAILS").split(',')
    admin_email = os.getenv("ADMIN_EMAIL")

    for token, device_id, token_remark, notification_email in zip(tokens, device_ids, token_remarks, notification_emails):
        process_account(token, device_id, token_remark, notification_email)

    # 发送管理员通知
    subject = "云原神所有账号签到情况"
    message = f"签到时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    for token_remark in token_remarks:
        message += f"账号备注: {token_remark}\n签到结果: 未知\n\n"
    send_email(subject, message, admin_email)

if __name__ == '__main__':
    main_handler()

    # 创建定时任务调度器
    scheduler = BlockingScheduler()
    scheduler.add_job(main_handler, 'cron', hour=0, minute=05)  
    # 启动调度器
    scheduler.start()
