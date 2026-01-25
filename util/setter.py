import os
import yaml

from util.read_parse import parse

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(base_dir, "config.yaml")


class ArgSetter:
    """
    参数管理单例
    - 默认读取 config.yaml
    - 支持 parse 覆盖
    """
    _instance = None
    _inited = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.device_id = None
        self.test_type = None
        self.test_platform = None
        self.tester = None
        self.base_dir = None
        self.path_run = None
        self._build_args()
        self._inited = True

    def _build_args(self):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            _data = yaml.safe_load(f) or {}

        # argparse 覆盖
        args = parse()
        for k, v in vars(args).items():
            if v is not None:
                _data[k] = v

        self.device_id = _data["device_id"]
        self.test_type = _data["test_type"]
        self.test_platform = _data["test_platform"]
        self.tester = _data["tester"]
        self.base_dir = base_dir
        self.path_run = os.path.join(self.base_dir, "testcase", self.test_type)


argsetter = ArgSetter()
