import pytest

from util.setter import argsetter
from util.log import logger


def main():
    try:
        pytest.main([argsetter.path_run, "-m", argsetter.test_platform])
    except Exception as e:
        logger.exception(f"运行测试异常:{e}")


if __name__ == '__main__':
    main()
