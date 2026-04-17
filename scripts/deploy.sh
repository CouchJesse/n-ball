#!/bin/bash
set -e

# ==========================================
# N-Ball 自动化部署脚本
# 用法: ./scripts/deploy.sh [环境] (例如: ./scripts/deploy.sh dev, ./scripts/deploy.sh prod)
# ==========================================

ENV=$1
if [ -z "$ENV" ]; then
    echo "❌ 错误: 未指定部署环境。"
    echo "用法: $0 [dev|test|prod]"
    exit 1
fi

COMPOSE_FILE="docker-compose.${ENV}.yml"

if [ ! -f "$COMPOSE_FILE" ]; then
    echo "❌ 错误: 找不到对应的配置文件 $COMPOSE_FILE"
    exit 1
fi

echo "🚀 开始部署 [$ENV] 环境..."

# 1. 如果是 prod 环境，检查环境变量文件
if [ "$ENV" = "prod" ]; then
    if [ ! -f ".env.prod" ]; then
        echo "⚠️ 警告: 生产环境需要 .env.prod 文件！"
        echo "正在为您创建一个示例文件 .env.prod..."
        cat << 'ENVEOF' > .env.prod
POSTGRES_USER=nball_admin
POSTGRES_PASSWORD=nball_secure_pass
POSTGRES_DB=nball_prod
SECRET_KEY=super_secret_production_key_change_me
ENVEOF
        echo "✅ 已生成 .env.prod，请修改其中的敏感信息后再重新执行部署。"
        exit 1
    fi
    ENV_OPT="--env-file .env.prod"
else
    ENV_OPT=""
fi

# 2. 拉取最新代码 (可选，默认注释掉，如果需要可以直接解开)
# echo "📦 拉取最新代码..."
# git pull origin main

# 3. 停止旧容器
echo "🛑 停止并移除旧容器..."
docker-compose -f $COMPOSE_FILE $ENV_OPT down

# 4. 构建并启动新容器
echo "🏗️ 构建并启动容器..."
docker-compose -f $COMPOSE_FILE $ENV_OPT up -d --build

# 5. 等待数据库启动就绪
echo "⏳ 等待数据库就绪 (等待 10 秒)..."
sleep 10 # 给予一些初始化时间，也可以通过检查健康状态循环判断

# 6. 执行数据库迁移
echo "🗄️ 执行数据库迁移 (Alembic)..."
docker-compose -f $COMPOSE_FILE $ENV_OPT exec -T web alembic upgrade head

echo "✅ [$ENV] 环境部署成功！"
echo "你可以通过 docker-compose -f $COMPOSE_FILE ps 查看运行状态。"
