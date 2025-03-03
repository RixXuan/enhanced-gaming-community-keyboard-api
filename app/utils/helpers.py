import re
from typing import Optional
import random
import string
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

def slugify(s: str) -> str:
    """
    生成URL友好的slug
    """
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s

def random_string(length: int = 32) -> str:
    """
    生成指定长度的随机字符串
    """
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def is_valid_object_id(id: str) -> bool:
    """
    检查字符串是否是有效的MongoDB ObjectId
    """
    return bool(re.match(r'^[0-9a-fA-F]{24}$', id))

def format_datetime(dt: datetime) -> str:
    """
    格式化datetime为用户友好的字符串
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def add_time_from_now(minutes: int = 0, hours: int = 0, days: int = 0) -> datetime:
    """
    从现在开始添加指定时间
    """
    return datetime.utcnow() + timedelta(minutes=minutes, hours=hours, days=days)

def model_to_dict(obj):
    """
    将模型对象转换为字典（处理嵌套模型）
    """
    return jsonable_encoder(obj)

def extract_input_context(text: str, max_length: int = 100) -> Optional[str]:
    """
    从输入文本中提取上下文特征
    """
    if not text:
        return None
    # 提取前100个字符作为上下文特征
    return text[:max_length]