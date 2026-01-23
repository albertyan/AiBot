import os
from pathlib import Path
from loguru import logger


def check_base_dir():
    """
    检查用户目录是否存在，不存在则创建
    """
    try:
        # 找到用户目录
        user_dir = Path.home()
        base_dir = os.path.join(user_dir, ".aiBot")
        if not os.path.exists(base_dir):
            logger.info(f"create it: {base_dir}")
            os.makedirs(base_dir)
    except Exception as e:
        logger.error(f"[check_base_dir] check base dir error: {e}")
        raise e

def get_base_dir():
    """
    获取用户目录
    """
    try:
        # 找到用户目录
        user_dir = Path.home()
        base_dir = os.path.join(user_dir, ".aiBot")
        logger.info(f"base dir: {base_dir}")
        return base_dir
    except Exception as e:
        logger.error(f"[get_base_dir] get base dir error: {e}")
        raise e

if __name__ == "__main__":
    check_base_dir()