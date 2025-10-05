# 自动化测试框架

## 1. 介绍

基于`pytest`编写自动化测试框架，集成`allure`测试报告和飞书消息通知，支持按照测试类型（如冒烟测试）、测试项目（如op项目）、单个用例文件等执行，
目前使用`uiautomator2`作为UI自动化工具集，默认读取`config.yaml`文件作为配置参数，也可在`run.py`入口文件重新指定配置参数，
与`jenkins`工具无缝集成，实现参数更新触发自动化测试并生成报告。

## 2. 项目结构

```
autotest_frame/
├── common/                 # 公共模块
│   ├── common_api.py       # 通用业务
│   ├── feishu_api.py       # 飞书通知
│   ├── log.py              # 日志配置
│   └── read_parse.py       # 配置传入参数
│   └── task_info.py        # 任务信息
│   └── ui2_util.py         # uiautomator2方法集
├── log/                    # 日志文件目录
├── testcase/               # 测试用例
│   └── test_smoke/         # 冒烟测试集
│       └── test_phone/     # 手机端测试
├── tools/                  # 外部工具
│   └── allure-2.35.1/      # allure命令行工具
│   └── report_depend/      # 报告依赖脚本
├── .gitignore              # git忽略配置
├── .python-version         # python版本
├── config.yaml             # 全局配置文件
├── main.bat                # 本地执行入口文件
├── pyproject.toml          # 项目依赖项 (uv)
├── pytest.ini              # pytest配置文件
├── run.py                  # CI/CD执行入口
├── run_task.py             # 测试任务执行入口脚本
├── uv.lock                 # 锁定的依赖版本 
└── uv_env.bat              # uv管理虚拟环境 
```

## 3. 环境准备

在开始之前，请确保您的系统已安装以下软件：

   **python**: 建议版本与 `.python-version` 文件中指定的版本一样。

   **java**: allure报告生成需要java环境。

## 4. 配置

4.1 **选择配置 `config.yaml`**：这是框架的核心配置文件，默认读取这个yaml文件作为配置参数。
   ```yaml
   device_id: '96a38567'  # 设备号
   test_type: 'test_smoke\test_phone'  # 测试类型
   test_project: 'vi'  # 测试项目平台
   case_name: 'all'  # 是否指定测试文件，默认为all
   tester_name: 'meng.peo'  # 测试人
   send_message: 'yes'  # 是否发送报告
   run_number: '1' # 压测次数
   ```
4.2 **`run.py`文件重新指定配置参数**：可在`CI/CD`或本地执行时，通过`run.py`指定任意配置参数覆盖`config.yaml`
   ```text
   usage: run.py [-h] [--device_id DEVICE_ID] [--test_type TEST_TYPE] [--test_project TEST_PROJECT]
              [--case_name CASE_NAME] [--tester_name TESTER_NAME] [--send_message {yes,no}]       
              [--run_number RUN_NUMBER]
   
   自动化测试参数(可选 默认读取config.yaml)
   
   options:
     -h, --help            show this help message and exit
     --device_id DEVICE_ID
                           设备号
     --test_type TEST_TYPE
                           测试类型
     --test_project TEST_PROJECT
                           测试平台
     --case_name CASE_NAME
                           指定测试文件名
     --tester_name TESTER_NAME
                           测试人
     --send_message {yes,no}
                           是否发送消息
     --run_number RUN_NUMBER
                           测试次数

   ```
4.3 **扩展配置参数**：可在`config.yaml`文件增加扩展的参数，并在`common\task_info.py``common\read_parse.py`文件配置新增的参数，满足业务需求扩展。
   
## 5. 运行测试

   **通过主入口 `run.py` (推荐)**：该脚本封装了配置和激活虚拟环境，也可以指定配置参数。
   ```bash
   python run.py
   ```