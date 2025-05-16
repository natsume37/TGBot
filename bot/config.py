import os
import logging
import logging.config

# 读取环境变量
ENV = os.getenv("ENV", "production").lower()
GLOBAL_LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

IS_DEV = ENV == "development"

# 日志文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 这里以 config.py 所在目录为基准，你可根据需要调整
INFO_LOG_DIR = os.path.join(BASE_DIR, "log", 'info.log')
ERROR_LOG_DIR = os.path.join(BASE_DIR, "log", 'error.log')
DEBUG_LOG_DIR = os.path.join(BASE_DIR, "log", 'debug.log')


def ensure_log_dirs_exist():
    """
    确保日志目录存在，不存在则创建
    """
    for file_path in [INFO_LOG_DIR, ERROR_LOG_DIR, DEBUG_LOG_DIR]:
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)


LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(threadName)s:%(thread)d [%(name)s] %(levelname)s [%(pathname)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(asctime)s [%(name)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'sqlalchemy': {
            'format': '[SQLALCHEMY] %(asctime)s %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console_debug_handler': {
            'level': 'DEBUG' if IS_DEV else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file_info_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': INFO_LOG_DIR,
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
        'file_debug_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': DEBUG_LOG_DIR,
            'encoding': 'utf-8',
            'formatter': 'simple',
        },
        'file_error_handler': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ERROR_LOG_DIR,
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
        'sqlalchemy_handler': {
            'level': 'INFO' if IS_DEV else 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'sqlalchemy',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console_debug_handler', 'file_info_handler', 'file_error_handler'],
            'level': GLOBAL_LOG_LEVEL,
            'propagate': False,
        },
        'sqlalchemy.engine': {
            'handlers': ['sqlalchemy_handler'],
            'level': 'INFO' if IS_DEV else 'WARNING',
            'propagate': False,
        },
    },
}


def setup_logging():
    ensure_log_dirs_exist()
    logging.config.dictConfig(LOGGING_DIC)
    # 运行时确保 sqlalchemy.engine 日志级别正确
    sqlalchemy_level = logging.INFO if IS_DEV else logging.WARNING
    logging.getLogger("sqlalchemy.engine").setLevel(sqlalchemy_level)
    logger = logging.getLogger(__name__)

