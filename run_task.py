import os

import pytest

from common import task_info
from common.log import logger
from tools.report_depend.generate_report import generate_allure_report


def main():
    rerun_mark = ['--reruns', '1', '--reruns-delay', '5']
    try:
        if 'smoke' in task_info.test_type:
            if task_info.case_name == 'all':
                test_path = task_info.path_run
            else:
                test_path = os.path.join(task_info.path_run, task_info.case_name)
                # 设置环境变量
            pytest.main([test_path, "-m", task_info.test_project, test_path, *rerun_mark])
    except Exception as e:
        logger.exception(f"运行测试异常:{e}")

    generate_allure_report()


if __name__ == '__main__':
    main()
