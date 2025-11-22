import requests
import json

from common.log import logger

# 飞书机器人 Webhook 地址
WEBHOOK_URL = ""


def feishu_send_text(webhook_url: str, text):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msg_type": "text",  # 消息类型
        "content": {
            "text": text
        }
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        logger.info("飞书消息发送成功: {}".format(response.json()))
    else:
        logger.error("飞书消息发送失败: {}".format(response.text))


if __name__ == '__main__':
    feishu_send_text(WEBHOOK_URL, "message test")
