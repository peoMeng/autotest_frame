import json
import subprocess
import os

from common.log import logger
from common.task_info import base_dir

results_dir = os.path.join(base_dir, "allure_results")
report_dir = os.path.join(base_dir, "allure_report")

current_dir = os.path.abspath(os.path.dirname(__file__))


def get_pytest_summary():
    """读取 pytest_terminal_summary 写入的汇总文件"""
    summary_path = os.path.join(results_dir, "pytest_summary.json")
    if not os.path.exists(summary_path):
        logger.error("未找到 pytest_summary.json")
        return {}

    with open(summary_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_allure_report():
    allure_bat = current_dir + os.sep + "allure-2.35.1" + os.sep + "bin" + os.sep + "allure.bat"

    # 生成报告
    subprocess.run([allure_bat, "generate", results_dir, "-o", report_dir, "--clean"], check=True)


if __name__ == "__main__":
    generate_allure_report()
