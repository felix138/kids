import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from ..config import settings

def setup_logger(name: str = __name__) -> logging.Logger:
    """配置日志记录器"""
    
    # 创建日志目录
    log_dir = Path(os.path.dirname(settings.LOG_FILE))
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    
    # 创建格式化器
    formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # 创建文件处理器
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=settings.LOG_MAX_SIZE,
        backupCount=settings.LOG_BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# 创建默认日志记录器
logger = setup_logger() 