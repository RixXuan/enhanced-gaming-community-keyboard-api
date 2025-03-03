import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict, Optional

from app.core.config import settings

# 日志格式
class CustomFormatter(logging.Formatter):
    def format(self, record):
        iso_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        log_record = {
            "timestamp": iso_time,
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # 添加异常信息（如果有）
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        
        # 添加额外字段
        for key, value in record.__dict__.items():
            if key not in ["args", "asctime", "created", "exc_info", "exc_text", "filename",
                          "funcName", "id", "levelname", "levelno", "lineno", "module",
                          "msecs", "message", "msg", "name", "pathname", "process",
                          "processName", "relativeCreated", "stack_info", "thread", "threadName"]:
                log_record[key] = value
        
        return json.dumps(log_record)

# 创建 logger
def setup_logger(name: str = "app") -> logging.Logger:
    """
    设置和配置日志器
    """
    logger = logging.getLogger(name)
    
    # 设置日志级别
    logger.setLevel(logging.INFO)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    
    # 添加处理器到日志器
    logger.addHandler(console_handler)
    
    # 设置日志文件（如果需要）
    # file_handler = logging.FileHandler("app.log")
    # file_handler.setFormatter(CustomFormatter())
    # logger.addHandler(file_handler)
    
    return logger

# 创建全局日志器实例
logger = setup_logger()

# 日志函数
def log_info(msg: str, extra: Optional[Dict[str, Any]] = None) -> None:
    """
    记录信息级别日志
    """
    logger.info(msg, extra=extra or {})

def log_error(msg: str, exc_info: bool = False, extra: Optional[Dict[str, Any]] = None) -> None:
    """
    记录错误级别日志
    """
    logger.error(msg, exc_info=exc_info, extra=extra or {})

def log_warning(msg: str, extra: Optional[Dict[str, Any]] = None) -> None:
    """
    记录警告级别日志
    """
    logger.warning(msg, extra=extra or {})

def log_critical(msg: str, exc_info: bool = False, extra: Optional[Dict[str, Any]] = None) -> None:
    """
    记录严重级别日志
    """
    logger.critical(msg, exc_info=exc_info, extra=extra or {})

def log_debug(msg: str, extra: Optional[Dict[str, Any]] = None) -> None:
    """
    记录调试级别日志
    """
    logger.debug(msg, extra=extra or {})

def log_request(request, response_status: int, execution_time: float) -> None:
    """
    记录 HTTP 请求日志
    """
    log_info(
        f"Request: {request.method} {request.url.path} - Status: {response_status} - Time: {execution_time:.2f}ms",
        extra={
            "request_method": request.method,
            "request_path": request.url.path,
            "request_query": str(request.query_params),
            "response_status": response_status,
            "execution_time_ms": execution_time,
            "client_ip": request.client.host if request.client else None,
        }
    )