import os

from common.feishu_api import feishu_send_text
from common.log import logger
from common.task_info import path_run, send_message, test_project, tester_name
from tools.report_depend.generate_report import get_pytest_summary

WEBHOOK_URL_OP = "https://open.feishu.cn/open-apis/bot/v2/hook/8981a01b-46fa-44f4-830d-3f9b65485a7d"


def send_text(text):
    try:
        if test_project == 'vi':
            feishu_send_text(WEBHOOK_URL_OP, text)
    except Exception as e:
        logger.exception(f"发送消息异常:{e}")


def send_report():
    try:
        if send_message == "yes":
            test_summary = get_pytest_summary()
            executed_total = test_summary.get("executed_total", 0)
            passed = test_summary.get("passed", 0)
            failed = test_summary.get("failed", 0) + test_summary.get("errors", 0)  # 失败=failed+errors
            rate = test_summary.get("pass_rate_excl_skipped", 0.0)

            test_message = (
                f"测试项目：{test_project}\n"
                f"测试人：{tester_name}\n"
                f"通过数：{passed}\n"
                f"失败数：{failed}\n"
                f"执行总数：{executed_total}\n"
                f"通过率：{rate}%\n"
            )
            logger.info(f"发送测试概要")
            send_text(test_message)

            logger.info(f"测试执行路径: {path_run}")
            if "Jenkins" in path_run:
                report_url = os.environ.get("BUILD_URL", "") + "allure/"
                logger.info(f"发送测试报告链接：{report_url}")
                send_text(f"测试报告链接：{report_url}")
    except Exception as e:
        logger.exception(f"发送测试报告异常:{e}")
