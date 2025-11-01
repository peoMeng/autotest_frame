import os
import shutil
import subprocess

from common.read_parse import args


def main():
    # 保证模块搜索包含根目录
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))

    # 删除测试前的日志信息
    shutil.rmtree("log", ignore_errors=True)

    # 把 args 转换成命令行形式的字符串
    params_list = []
    for k, v in vars(args).items():
        if v is not None:
            # argparse 里的参数名是 test_project -> --test_project
            params_list.append(f"--{k} {v}")
    # 保存指定的参数传入主入口main.bat-run_task.py
    params = " ".join(params_list)
    # 运行测试入口
    subprocess.run(fr".\main.bat {params}", shell=True, env=env)


if __name__ == "__main__":
    main()
