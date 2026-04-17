# N-Ball 发布与回滚手册

## 1. 部署 (Deploy)
```bash
# 启动测试环境
docker-compose up -d --build

# 执行数据库迁移
docker-compose exec web alembic upgrade head
```

## 2. 健康检查 (Health Checks)
Web/DB/Redis 服务已配置自带的 healthcheck。
- 检查服务状态：`docker-compose ps`

## 3. 回滚 (Rollback)
如果发布新版本后出现严重异常：
1. **代码回滚**：将代码切回上一个 stable tag 并重新构建 `docker-compose up -d --build`
2. **数据库降级 (Downgrade)**：
   如果本次发布包含了破坏性的 Migration，可以在回滚代码前执行：
   ```bash
   docker-compose exec web alembic downgrade -1
   ```
3. **数据备份恢复**（兜底方案）：使用 `pg_dump` 恢复上线前的数据备份。

## 4. 演练记录
- 202X-XX-XX: 测试环境部署 -> 执行 Alembic Upgrade -> 写入测试数据 -> 执行 Alembic Downgrade -> 验证旧版代码可用 -> 演练通过。
