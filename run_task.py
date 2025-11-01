import pytest

from common import task_info
from common.log import logger
from common.send_report import send_report


def main():
    rerun_mark = ['--reruns', '1', '--reruns-delay', '5']
    try:
        if 'smoke' in task_info.test_type:
            pytest.main([task_info.path_run, "-m", task_info.test_project, *rerun_mark])
    except Exception as e:
        logger.exception(f"运行测试异常:{e}")

    logger.info("开始发送测试报告")
    send_report()


if __name__ == '__main__':
    main()
