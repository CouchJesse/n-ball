#!/bin/bash
set -e

# 临时禁用 BuildKit 以解决 gRPC 'x-docker-expose-session-sharedkey' 报错问题
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

# ==========================================
# N-Ball 自动化回滚脚本
# 用法: ./scripts/rollback.sh [环境] (例如: ./scripts/rollback.sh dev, ./scripts/rollback.sh prod)
# ==========================================

ENV=$1
if [ -z "$ENV" ]; then
    echo "❌ 错误: 未指定回滚环境。"
    echo "用法: $0 [dev|test|prod]"
    exit 1
fi

COMPOSE_FILE="docker-compose.${ENV}.yml"

if [ ! -f "$COMPOSE_FILE" ]; then
    echo "❌ 错误: 找不到对应的配置文件 $COMPOSE_FILE"
    exit 1
fi

echo "⚠️ 准备对 [$ENV] 环境执行回滚操作..."

if [ "$ENV" = "prod" ]; then
    if [ ! -f ".env.prod" ]; then
        echo "❌ 错误: 生产环境回滚需要 .env.prod 文件！"
        exit 1
    fi
    ENV_OPT="--env-file .env.prod"
else
    ENV_OPT=""
fi

# 1. 确认回滚
echo "=========================================="
echo "⚠️ 警告：数据库降级可能会导致数据丢失！"
echo "=========================================="
read -p "❓ 确定要回滚数据库迁移 (向下迁移 1 个版本) 吗？ (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "🔙 执行 Alembic downgrade -1..."
    docker-compose -f $COMPOSE_FILE $ENV_OPT exec -T web alembic downgrade -1
    echo "✅ 数据库降级成功！"
else
    echo "⏭️ 跳过数据库降级。"
fi

# 2. 代码回滚与重启
echo "🔙 请手动将代码切换到上一个稳定版本标签 (git checkout <tag>)，或确认已经切回。"
read -p "❓ 代码是否已就绪并准备好重启服务？ (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "🔄 重新构建并启动服务..."
    export DOCKER_BUILDKIT=0
    docker build -t nball-app:latest .
    docker-compose -f $COMPOSE_FILE $ENV_OPT down
    docker-compose -f $COMPOSE_FILE $ENV_OPT up -d --no-build
    echo "✅ 服务回滚并重启成功！"
else
    echo "⏹️ 操作已取消。"
    exit 0
fi

echo "你可以通过 docker-compose -f $COMPOSE_FILE ps 查看运行状态。"
