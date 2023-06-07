# coding: utf-8


import os
import sys
import logging


BASE_DIR = os.path.dirname(__file__)


# 参数
options = {
    "port": 9000,
}


# 基本配置信息
settings = {
    "debug": True,
}


# ip白名单
white_list = ['39.105.112.224', '39.106.105.172']


# 日志配置
logger = logging.getLogger('ai_analysis')
logger.setLevel(logging.INFO)

# 创建handler
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

MAX_BYTES = 500 * 1024 * 1024
log_path = BASE_DIR + "/logs/aitools.log"
# file_handler = logging.FileHandler(log_path)
file_handler = logging.handlers.RotatingFileHandler(log_path, maxBytes=MAX_BYTES, backupCount=3)
file_handler.setLevel(logging.INFO)

# 创建formatter
formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(pathname)s - %(lineno)d - %(message)s")
handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 为日志器logger添加上面创建的处理器handler
logger.addHandler(handler)
logger.addHandler(file_handler)
