# N-Ball 部署引导手册

欢迎使用 N-Ball 项目！本文档旨在引导您从零开始将本项目部署到您的服务器或本地环境。项目基于 `Docker` 和 `Docker Compose` 进行容器化管理，并提供了自动化部署脚本以简化流程。

## 1. 部署前准备

### 1.1 系统要求
- 操作系统：Linux (推荐 Ubuntu 20.04+ 或 CentOS 8+) / macOS / Windows (WSL2)
- 内存：至少 2GB RAM
- 磁盘：至少 10GB 可用空间

### 1.2 环境依赖
确保您的服务器上已安装以下软件：
- **Git**: 用于拉取代码。
- **Docker**: 用于运行容器化应用。
  - [Docker 官方安装指南](https://docs.docker.com/engine/install/)
- **Docker Compose**: 用于编排多容器应用。
  - [Docker Compose 官方安装指南](https://docs.docker.com/compose/install/)

### 1.3 验证环境
运行以下命令确保依赖已正确安装：
```bash
docker --version
docker-compose --version
git --version
```

---

## 2. 获取代码

将项目代码克隆到您的服务器上，并进入项目目录：
```bash
git clone <your-repository-url>
cd <project-directory>
```

---

## 3. 环境配置与部署

本项目支持三种环境部署：**开发 (dev)**、**测试 (test)** 和 **生产 (prod)**。您可以根据实际需求选择。

### 3.1 开发环境 (Dev)
适合本地开发调试，支持代码热重载。数据库和 Redis 端口会映射到宿主机。

```bash
# 执行自动化部署脚本
./scripts/deploy.sh dev
```
> **提示**：开发环境的数据库文件会持久化在名为 `postgres_dev_data` 的 Docker Volume 中。

### 3.2 测试环境 (Test)
适合 CI/CD 自动化集成测试使用。环境纯净，不映射多余端口。

```bash
# 执行自动化部署脚本
./scripts/deploy.sh test
```

### 3.3 生产环境 (Prod)
适合线上正式运行，配置了服务自动重启、日志限制以及生产级别的环境变量注入。

#### 步骤一：初始化生产环境变量
第一次部署生产环境时，脚本会拦截并自动生成一个 `.env.prod` 示例文件。
```bash
./scripts/deploy.sh prod
```
您会看到如下提示：
```
⚠️ 警告: 生产环境需要 .env.prod 文件！
正在为您创建一个示例文件 .env.prod...
✅ 已生成 .env.prod，请修改其中的敏感信息后再重新执行部署。
```

#### 步骤二：修改环境变量配置
打开 `.env.prod` 文件，修改其中的敏感信息（如密码、密钥）：
```bash
vim .env.prod
```
*建议：将 `SECRET_KEY` 替换为一个随机生成的长字符串，可以使用 `openssl rand -hex 32` 生成。*

#### 步骤三：正式部署
配置修改完成后，再次运行部署脚本：
```bash
./scripts/deploy.sh prod
```

---

## 4. 验证部署

部署完成后，您可以通过以下方式验证服务是否正常运行：

### 4.1 检查容器状态
```bash
# 查看指定环境的容器状态 (例如 prod)
docker-compose -f docker-compose.prod.yml ps
```
确保 `web`、`worker`、`db`、`redis` 四个容器的状态均为 `Up (healthy)`。

### 4.2 访问健康检查接口
通过 `curl` 或浏览器访问系统的 Health 接口：
```bash
# 如果是本地或开发环境，访问 8000 端口
curl http://localhost:8000/api/v1/system/health

# 如果是生产环境（默认映射到 80 端口），直接访问服务器 IP 或域名
curl http://<your-server-ip>/api/v1/system/health
```
如果返回 `{"status": "ok"}`，则说明 Web 服务已成功启动并能正常响应。

### 4.3 查看服务日志
如果服务运行异常，可以查看日志进行排查：
```bash
# 查看所有容器的日志
docker-compose -f docker-compose.prod.yml logs -f

# 仅查看 web 容器的日志
docker-compose -f docker-compose.prod.yml logs -f web

# 仅查看 worker (Celery) 容器的日志
docker-compose -f docker-compose.prod.yml logs -f worker
```

---

## 5. 版本更新与回滚

### 5.1 更新服务 (发布新版本)
当有新代码需要发布时，只需拉取最新代码并重新运行部署脚本即可：
```bash
git pull origin main
./scripts/deploy.sh prod
```
*脚本会自动停止旧容器、构建新镜像、启动新容器并执行必要的数据库迁移。*

### 5.2 故障回滚
如果您发布了新版本后发现严重 Bug，可以使用提供的交互式回滚脚本进行回滚：

```bash
./scripts/rollback.sh prod
```
**回滚流程：**
1. 脚本会首先询问您是否需要降级数据库（向下迁移 1 个版本）。**请注意，这可能会导致新写入的数据丢失，请谨慎操作！**
2. 随后，脚本会提示您手动将代码切换到上一个稳定的版本标签（例如 `git checkout v1.0.0`）。
3. 当您确认代码已就绪后，脚本会重新构建并启动上一个稳定版本的服务。

---

## 6. 常见问题 (FAQ)

**Q1: 部署脚本提示 `Permission denied`？**
**A**: 请确保脚本具有执行权限。运行 `chmod +x scripts/*.sh`。

**Q2: `web` 容器启动失败，日志显示连接数据库超时？**
**A**: 通常是因为数据库容器还在初始化。自动化脚本已经添加了 10 秒的等待时间，如果您的服务器性能较低，可以尝试修改 `scripts/deploy.sh` 中的 `sleep 10` 为更长的时间。或者，直接等待片刻后再次运行 `./scripts/deploy.sh prod`。

**Q3: 如何进入容器内部执行命令？**
**A**: 可以使用 `docker-compose exec` 命令。例如，进入生产环境的 web 容器：
```bash
docker-compose -f docker-compose.prod.yml exec web /bin/bash
```

**Q4: 我想清除所有容器和数据，重新部署怎么办？**
**A**: 可以使用 `down -v` 命令清除容器和对应的 Volumes（**警告：这会删除所有数据库数据！**）：
```bash
docker-compose -f docker-compose.prod.yml down -v
```

