from db.get_db import init_create_table
from utils.config_file import check_base_dir


import asyncio

async def main():
    # 初始化数据库
    await init_create_table()
    # 检查基础目录
    check_base_dir()

if __name__ == "__main__":
    main()
