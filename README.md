# pywebview + FastApi+Vue

# 1.介绍  

**桌面应用开发，打包的环境整合**，**开发时**可使用node作为前端服务器，fastapi作为后端服务器（在pywebview启动时启动）。此时需要分别启动前后端的服务器。打包时只需启动pywebview即可（此时vue生成的dist会被挂在fastapi的服务器（uvicorn）上）



**项目目录：**

----AIBOT

├─dist 打包成exe的输出文件

├─gui vue打包后的静态文件
├─src
│  ├─backend  python代码
│  └─frontend vue项目所在文件





# 2.使用

## 2.1安装依赖



## （推荐）conda下使用

**conda下安装python,node ** 

```cmd
#安装python
conda create -n py38 python=3.8
# 激活python环境
conda activate py38
#在 Conda 环境中安装 Node.js
conda install -c conda-forge nodejs=v22.9.0
#
验证
python --version  # 检查 Python 版本
node -v           # 检查 Node.js 版本
npm -v            # 检查 npm 版本

```

**安装项目依赖**  

python的依赖

```cmd
pip install -r requirements.txt

```

node依赖

```cmd
npm install  --registry=http://registry.npmmirror.com  
```



# 3.启动

 main.py

```python
if __name__ == '__main__':
    find_port()
    uviconserverThread()
    fastServer("prod") # 值若为prod模拟打包后的启动，为dev则是开发环境启动。
```

**prod和dev的区别**

prod 此时启动项目后gui下的文件会被挂载到fastapi服务下，同时启动pywenview, 此时前端不用单独服务器了如（node）  

dev 此时启动项目仅仅启动fastapi和webview,前端需要使用npm run dev 单独启动。好处：方便前端页面开发  





# 4.打包

修改main.py 如下

```
fastServer("prod") 


```

```


npm   run build 

pyinstaller .\main.spec


```

执行build.bat

**详见build.bat**



# todo...

## 新版项目文档

### 项目概述
- 桌面外壳：`pywebview`；后端：`FastAPI`（`uvicorn`）；前端：`Vue 3 (Vite)`。
- 模式：`dev` 前后端分离开发；`prod` 前端静态资源挂载到后端并打包为 `exe`。

### 目录结构
```
AiBot
├─ dist/                 # 打包产物（main.exe、gui 静态资源）
│  └─ gui/               # 前端构建后拷贝到此目录
├─ src/
│  ├─ backend/
│  │  ├─ app.py          # FastAPI 应用与静态资源挂载
│  │  ├─ main.py         # 启动 uvicorn 与 pywebview（入口）
│  │  ├─ environment.py  # 环境模式 dev/prod
│  │  ├─ router/         # 根路由（返回 index.html）
│  │  ├─ api/            # 业务 API（微信初始化/自动回复）
│  │  ├─ pywechat/       # 微信自动化与机器人能力
│  │  ├─ data/           # SQLite 封装与 schema
│  │  └─ utils/          # 通用工具
│  └─ frontend/          # Vue 前端工程
│     ├─ src/            # 前端源码
│     ├─ dist/           # 前端构建产物（中转）
│     └─ package.json    # 前端依赖与脚本
├─ AIBOT.spec            # PyInstaller 打包配置
├─ build.bat             # 一键前端构建并打包脚本
├─ requirements.txt      # 后端依赖
├─ baseUtil.py           # 路径/打包相关工具
└─ nginx.py              # 打包场景下的内置 Nginx 控制
```

### 安装依赖
- Python 依赖（根目录）：
```
pip install -r requirements.txt
```
- 前端依赖（进入前端目录）：
```
cd src\frontend
npm install
```
- 使用 `pnpm`：
```
pnpm install
```

### 开发模式运行（dev）
- 后端 + 桌面外壳（根目录执行）：
```
python src\backend\main.py
```
- 默认后端端口：`8000`（`src/backend/main.py:55`）。
- 开发模式 webview 加载地址：`http://localhost:800`（`src/backend/main.py:49`）。
- 前端独立开发（进入前端目录）：
```
cd src\frontend
npm run dev
```

### 生产模式运行（prod）
- 设置环境为 `prod`，webview 指向本地后端并挂载静态资源：
```
# src/backend/main.py
envMode.set_mode(EnvMode.PROD)            # src/backend/main.py:58
uviconserverThread()                      # 启动 FastAPI（uvicorn）
fastServer(envMode.envMode)               # 根据模式创建 webview 窗口
```
- 根路由返回 `index.html`（`src/backend/router/router_manager.py:23-27`）。
- 静态资源挂载：`/assets`（`src/backend/app.py:28`）。

### 打包发布
- 使用根目录脚本：
```
build.bat
```
- 手动执行：
```
cd src\frontend && pnpm run build
xcopy .\dist ..\..\dist\gui /E
pyinstaller .\AIBOT.spec
```

### API 示例
- `GET /api/init`：初始化微信客户端并返回当前用户信息，位置：`src/backend/api/home.py:16-30`。

### 重要说明
- 内置 Nginx 控制（打包路径兼容）：路径解析 `nginx.py:10-18`；启动 `nginx.py:29-45`；停止 `nginx.py:46-55`。
- 端口与地址可按需调整；默认后端端口为 `8000`。






