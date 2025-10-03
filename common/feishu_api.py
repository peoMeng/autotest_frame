import requests
import json

from common.log import logger

# 飞书机器人 Webhook 地址
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/8981a01b-46fa-44f4-830d-3f9b65485a7d"


def send_text(text, webhook_url: str):
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
    send_text("message test", WEBHOOK_URL)
