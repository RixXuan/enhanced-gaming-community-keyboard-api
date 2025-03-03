# app/core/middleware.py
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import log_request

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    日志中间件，记录所有请求
    """
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        # 计算执行时间（毫秒）
        execution_time = (time.time() - start_time) * 1000
        
        # 记录请求
        log_request(request, response.status_code, execution_time)
        
        return response