# 命令行参数覆盖 yaml 配置
import argparse

parser = argparse.ArgumentParser(description="自动化测试参数(可选 默认读取config.yaml)")
parser.add_argument("--device_id", type=str, help="设备号")
parser.add_argument("--test_type", type=str, help="测试类型")
parser.add_argument("--test_project", type=str, help="测试平台")
parser.add_argument("--tester_name", type=str, help="测试人")
parser.add_argument("--send_message", choices=["yes", "no"], help="是否发送消息")
parser.add_argument("--run_number", type=int, help="测试次数")
args, _ = parser.parse_known_args()

