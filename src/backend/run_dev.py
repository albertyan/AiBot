import os
import sys
import subprocess
import time
import asyncio
import webview
from threading import Thread

# 将项目根目录添加到 sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.insert(0, CURRENT_DIR)
sys.path.insert(0, PROJECT_ROOT)
import backend_init
# 尝试导入 backend_init，如果失败则提示

def start_backend_process():
    """
    启动 uvicorn 子进程，开启热重载
    """
    # 构造环境变量，确保子进程能找到模块
    env = os.environ.copy()
    python_path = env.get("PYTHONPATH", "")
    # 将项目根目录和 src/backend 加入 PYTHONPATH
    env["PYTHONPATH"] = f"{PROJECT_ROOT}{os.pathsep}{CURRENT_DIR}{os.pathsep}{python_path}"
    
    # 启动命令：python -m uvicorn src.backend.app:app --reload --host 127.0.0.1 --port 8090
    # 使用 8090 端口避免与默认端口冲突
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "src.backend.app:app", 
        "--host", "127.0.0.1", 
        "--port", "8090", 
        "--reload"
    ]
    
    print(f"Starting backend with command: {' '.join(cmd)}")
    process = subprocess.Popen(cmd, cwd=PROJECT_ROOT, env=env)
    return process

def main():
    # 1. 执行初始化逻辑 (数据库建表等)
    print("Initializing application...")
    try:
        asyncio.run(backend_init.main())
    except Exception as e:
        print(f"Initialization warning: {e}")

    # 2. 启动后端服务
    backend_proc = start_backend_process()
    
    try:
        # 等待服务启动
        print("Waiting for backend to start...")
        time.sleep(3) 
        
        # 3. 启动前端窗口
        # 指向后端端口 8000
        print("Starting WebView window...")
        webview.create_window('AiBot (Dev Mode - Auto Reload)', 'http://localhost:8090', width=1024, height=768)
        webview.start(debug=True)
        
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        # 4. 清理子进程
        if backend_proc.poll() is None:
            print("Terminating backend process...")
            backend_proc.terminate()
            backend_proc.wait()
            print("Backend stopped.")

if __name__ == "__main__":
    main()
