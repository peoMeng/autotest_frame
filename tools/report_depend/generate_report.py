import subprocess
import os

from common.task_info import base_dir


def generate_allure_report():
    results_dir = os.path.join(base_dir, "allure_results")
    report_dir = os.path.join(base_dir, "allure_report")

    allure_bat = base_dir + os.sep + "tools" + os.sep + "allure-2.35.1" + os.sep + "bin" + os.sep + "allure.bat"

    # 生成报告
    subprocess.run([allure_bat, "generate", results_dir, "-o", report_dir, "--clean"], check=True)


if __name__ == "__main__":
    generate_allure_report()
