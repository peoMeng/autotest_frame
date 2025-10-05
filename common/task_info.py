import os

import yaml

from common.log import logger
from common.read_parse import args

# 获取根目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Arg:
    """
    默认读取config.yaml配置参数
    可在run.py指定配置参数
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_data"):
            self._data = {}

    def load(self):
        config_yaml = os.path.join(base_dir, "config.yaml")
        with open(config_yaml, "r", encoding="utf-8") as f:
            self._data = yaml.safe_load(f)

        for k, v in vars(args).items():
            if v is not None:
                self._data[k] = v

        self._data["path_run"] = os.path.join(base_dir, "testcase", self._data["test_type"])
        return self._data

    @property
    def config(self):
        if not self._data:
            return self.load()
        return self._data


# 单例对象
arg = Arg()
config = arg.config
logger.info(f"配置参数：{config}")
# 设备号
device_id = config['device_id']
# 测试类型
test_type = os.path.normpath(config['test_type'])
# 测试项目平台
test_project = config['test_project']
# 测试用例路径
path_run = config['path_run']
# 指定测试文件
case_name = config['case_name']
# 测试人
tester_name = config['tester_name']
# 发生消息
send_message = config['send_message']
# 压测次数
run_number = int(config['run_number'])

if __name__ == '__main__':
    print(config)
