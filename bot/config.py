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


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,  # 保留未在此处显式配置的 logger，但我们后面会手动调整它们的级别

    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(threadName)s:%(thread)d [%(name)s] %(levelname)s [%(pathname)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(asctime)s [%(name)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        },
        'info_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': INFO_LOG_PATH,
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'encoding': 'utf-8',
        },
        'user_info_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': USER_LOG_PATH,
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'encoding': 'utf-8',
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'WARNING',
            'formatter': 'detailed',
            'filename': ERROR_LOG_PATH,
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'encoding': 'utf-8',
        },
        'debug_file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': DEBUG_LOG_PATH,
            'encoding': 'utf-8',
        },
    },

    'loggers': {
        # 你自己项目的日志器
        'userInfo': {
            'handlers': ["user_info_file"],
            'level': 'DEBUG',
            'propagate': False,
        },
        # 第三方库：强制提升到 WARNING
        'sqlalchemy': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'sqlalchemy.engine': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'httpcore': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'httpx': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'telegram': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'openai._base_client': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },

    # 根日志器：所有未单独配置的 logger 都走这里
    'root': {
        'handlers': ['console', 'info_file', 'error_file'],
        'level': GLOBAL_LOG_LEVEL,
        'propagate': False,
    },
}


def setup_logging():
    """项目启动时调用一次，建立日志系统。"""
    ensure_log_dirs_exist()
    logging.config.dictConfig(LOGGING_CONFIG)

    # 终极静默模式、解决一切烦恼
    for name in ('sqlalchemy', 'sqlalchemy.engine', 'httpcore', 'httpx', 'telegram'):
        logging.getLogger(name).setLevel(logging.WARNING)
    logging.getLogger('root').info("日志系统已初始化")
