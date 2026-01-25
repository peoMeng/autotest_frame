import argparse


def parse():
    parser = argparse.ArgumentParser(description="自动化测试参数(可选 默认读取config.yaml)")
    parser.add_argument("--device_id", type=str, help="设备号")
    parser.add_argument("--test_type", type=str, help="测试类型")
    parser.add_argument("--test_platform", type=str, help="测试平台")
    parser.add_argument("--tester", type=str, help="测试人")
    args, _ = parser.parse_known_args()
    return args
