import subprocess
from contextlib import contextmanager

import allure

from util.log import logger
from util.setter import argsetter


class AdbUtil:

    @classmethod
    def adb_run(cls, cmd):
        cmd_list = cmd.split(' ', 1)
        cmd_str = cmd_list[0] + ' -s ' + argsetter.device_id + ' ' + cmd_list[1]
        try:
            result = subprocess.run(cmd_str, capture_output=True, text=True, check=True)
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"adb run error: {e}")

    @classmethod
    def back_home(cls):
        cls.adb_run("adb shell input keyevent 3")


class Allure:

    @staticmethod
    @contextmanager
    def step(step_msg):
        with allure.step(step_msg):
            logger.info(step_msg)
            yield
