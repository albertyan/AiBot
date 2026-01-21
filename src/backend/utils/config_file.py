import os
from pathlib import Path


def check_base_dir():
    """
    检查用户目录是否存在，不存在则创建
    """
    # 找到用户目录
    user_dir = Path.home()
    base_dir = os.path.join(user_dir, ".aiBot")
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
