import logging.config
import os

import colorlog

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 构造日志目录路径
log_dir = os.path.join(base_dir, "log")
# 创建目录
os.makedirs(log_dir, exist_ok=True)

# 日志配置字典
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,  # 保留已经配置好的 logger 设置，同时加载你自己新增的日志配置
    'formatters': {
        'standard_formatter': {  # 标准输出
            'format': '%(asctime)s | %(filename)s:%(lineno)d | '
                      '%(levelname)s | %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'color_formatter': {  # 颜色格式化标准输出
            '()': colorlog.ColoredFormatter,
            'format': '%(log_color)s%(asctime)s | %(filename)s:%(lineno)d | '
                      '%(levelname)s | %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        },
    },
    'filters': {},  # 日志过滤器
    'handlers': {
        'console': {  # 输出到日志控制台
            'level': 'DEBUG',  # 日志等级
            'class': 'logging.StreamHandler',  # 输出到控制台
            'formatter': 'standard_formatter',  # 颜色格式化标准输出
        },
        'pro_env': {  # 输出到文件
            'level': 'INFO',  # 日志等级
            'formatter': 'standard_formatter',  # 标准输出
            'class': "logging.handlers.TimedRotatingFileHandler",  # 按日期自动轮转日志，保留历史记录
            'filename': os.path.join(log_dir, "production.log"),  # 输出日志的文件
            'when': 'D',  # 按天分割
            'interval': 1,  # 间隔1天
            'backupCount': 5,  # 保留天数
            'encoding': 'utf-8',  # utf-8编码
        }
    },
    'loggers': {  # 根据loggers.getLogger(__name__)获取logger配置
        'logger': {
            'handlers': ['console', 'pro_env'],
            'level': 'DEBUG',
            'propagate': False  # 冒泡到上级（最终到达 root）→ 再打印一次
        }
    },
    "root": {  # <<< 在这里配置 root
        "level": "INFO",
        "handlers": ["console"]
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('logger')


if __name__ == '__main__':
    logger.debug("this is a debug message")
    logger.info("this is a info message")
    logger.warning("this is a warning message")
    logger.error("this is a error message")
