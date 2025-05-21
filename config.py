# logger_config.py
import os
import logging
import logging.config

# 环境变量配置
GLOBAL_LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# 日志目录和文件
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "log")
INFO_LOG_PATH = os.path.join(LOG_DIR, "info.log")
ERROR_LOG_PATH = os.path.join(LOG_DIR, "error.log")
DEBUG_LOG_PATH = os.path.join(LOG_DIR, "debug.log")
USER_LOG_PATH = os.path.join(LOG_DIR, "user.log")


def ensure_log_dirs_exist():
    os.makedirs(LOG_DIR, exist_ok=True)


LOGGING_DIC = {
    'version': 1.0,
    'disable_existing_loggers': False,
    # 日志格式
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(threadName)s:%(thread)d [%(name)s] %(levelname)s [%(pathname)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(asctime)s [%(name)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'test': {
            'format': '%(asctime)s %(message)s',
        },
    },
    'filters': {},
    # 日志处理器
    'handlers': {
        'console_debug_handler': {
            'level': 'DEBUG',  # 日志处理的级别限制
            'class': 'logging.StreamHandler',  # 输出到终端
            'formatter': 'simple'  # 日志格式
        },
        'file_info_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
            'filename': f'{USER_LOG_PATH}',
            'maxBytes': 1024 * 1024 * 10,  # 日志大小 10M
            'backupCount': 10,  # 日志文件保存数量限制
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
        'file_debug_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',  # 保存到文件
            'filename': f'{DEBUG_LOG_PATH}',  # 日志存放的路径
            'encoding': 'utf-8',  # 日志文件的编码
            'formatter': 'test',
        },
        'file_error_handler': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
            'filename': f'{ERROR_LOG_PATH}',
            'maxBytes': 1024 * 1024 * 10,  # 日志大小 10M
            'backupCount': 10,  # 日志文件保存数量限制
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
    },
    # 日志记录器
    'loggers': {
        'admin': {  # 导入时logging.getLogger时使用的app_name
            'handlers': ['console_debug_handler'],  # 日志分配到哪个handlers中
            'level': 'DEBUG',  # 日志记录的级别限制
            'propagate': False,  # 默认为True，向上（更高级别的logger）传递，设置为False即可，否则会一份日志向上层层传递
        },
        'user_info': {
            'handlers': ['console_debug_handler', 'file_info_handler', 'file_error_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'httpx': {
            'handlers': ['console_debug_handler'],
            # 'level': 'INFO',
            'level': 'WARNING',
            'propagate': False,
        },
        # 万能日志记录器
        '': {
            'handlers': ['console_debug_handler'],  # 及答应到终端、也保存到文件
            'level': 'INFO',
            'propagate': False,
        },
    }
}


def setup_logging():
    """项目启动时调用一次，建立日志系统。"""
    ensure_log_dirs_exist()
    logging.config.dictConfig(LOGGING_DIC)

    logging.getLogger('config').info("日志系统已初始化")
