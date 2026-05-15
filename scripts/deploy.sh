#!/bin/bash

# 阿里云 ECS 部署脚本
# 服务器: 123.57.173.158

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}开始部署到阿里云 ECS...${NC}"

# 服务器信息
SERVER_IP="123.57.173.158"
SERVER_USER="root"
PROJECT_DIR="/home/agent/team-agent-project"

# 1. 同步代码到服务器
echo -e "${YELLOW}1. 同步代码到服务器...${NC}"
rsync -avz --exclude 'node_modules' --exclude '.git' --exclude '__pycache__' --exclude '.venv' \
    ./ ${SERVER_USER}@${SERVER_IP}:${PROJECT_DIR}/

# 2. 在服务器上执行部署
echo -e "${YELLOW}2. 在服务器上执行部署...${NC}"
ssh ${SERVER_USER}@${SERVER_IP} << 'EOF'
cd /home/agent/team-agent-project

# 停止现有容器
echo "停止现有容器..."
docker-compose down || true

# 拉取最新镜像（如果使用远程镜像）
# docker-compose pull

# 构建并启动容器
echo "构建并启动容器..."
docker-compose up -d --build

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 检查服务状态
echo "检查服务状态..."
docker-compose ps

# 检查 API 健康状态
echo "检查 API 健康状态..."
curl -s http://localhost:5055/health || echo "API 服务未就绪"

echo "部署完成！"
EOF

echo -e "${GREEN}部署完成！${NC}"
echo -e "${GREEN}API 地址: http://${SERVER_IP}:5055${NC}"
echo -e "${GREEN}前端地址: http://${SERVER_IP}:3000${NC}"
