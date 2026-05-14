# 多阶段构建
FROM python:3.11-slim as base

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装依赖
RUN uv sync --frozen --no-dev

# 复制源代码
COPY . .

# 暴露端口
EXPOSE 5055

# 启动命令
CMD ["uv", "run", "run_api.py"]
