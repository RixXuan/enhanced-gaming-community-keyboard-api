#!/bin/bash
set -e

# 显示欢迎信息
echo "=== FlorisBoard Enhancement API 安装脚本 ==="
echo "本脚本将设置项目开发环境"

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python -m venv venv
else
    echo "虚拟环境已存在"
fi

# 激活虚拟环境
if [ -f "venv/bin/activate" ]; then
    echo "激活虚拟环境..."
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    echo "激活虚拟环境 (Windows)..."
    source venv/Scripts/activate
else
    echo "无法找到激活脚本，请手动激活虚拟环境"
    exit 1
fi

# 安装依赖
echo "安装项目依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 创建环境变量文件
if [ ! -f ".env" ]; then
    echo "创建 .env 文件模板..."
    cat > .env << EOF
# 项目设置
PROJECT_NAME="FlorisBoard Enhancement API"
API_V1_STR="/api/v1"

# 安全设置
SECRET_KEY="请更改为长而复杂的随机字符串"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 天

# 数据库设置 - PostgreSQL
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=florisboard_db

# Discord 设置
DISCORD_CLIENT_ID="你的Discord应用ID"
DISCORD_CLIENT_SECRET="你的Discord应用密钥"
DISCORD_REDIRECT_URI="http://localhost:8000/api/v1/auth/discord/callback"

# CORS 设置
CORS_ORIGINS='["http://localhost:3000","http://localhost:8000"]'
EOF
    echo "已创建 .env 文件模板，请修改其中的设置值"
else
    echo ".env 文件已存在，跳过创建"
fi

# 创建数据库目录结构
echo "创建项目目录结构..."
mkdir -p app/{api/endpoints,core,crud,models,schemas,services,utils}
mkdir -p alembic
mkdir -p tests

# 创建基础文件
echo "创建基础文件..."

# 创建 __init__.py 文件
touch app/__init__.py
touch app/api/__init__.py
touch app/api/endpoints/__init__.py
touch app/core/__init__.py
touch app/crud/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
touch app/utils/__init__.py
touch tests/__init__.py

# 初始化 Alembic (数据库迁移)
if [ ! -f "alembic.ini" ]; then
    echo "初始化 Alembic..."
    alembic init alembic
    # 修改 alembic.ini 中的连接字符串，使用环境变量
    sed -i 's/sqlalchemy.url = driver:\/\/user:pass@localhost\/dbname/sqlalchemy.url = postgresql:\/\/\${POSTGRES_USER}:\${POSTGRES_PASSWORD}@\${POSTGRES_SERVER}\/\${POSTGRES_DB}/g' alembic.ini
    echo "已初始化 Alembic，请检查配置"
else
    echo "alembic.ini 已存在，跳过初始化"
fi

echo "=== 安装完成 ==="
echo "要启动应用，请运行: uvicorn app.main:app --reload"
echo "确保先修改 .env 文件中的设置"