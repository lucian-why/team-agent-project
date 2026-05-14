.PHONY: help api database worker start-all stop-all status lint ruff test clean-cache

# 默认目标
help:
	@echo "Available commands:"
	@echo "  make api          - Start FastAPI dev server"
	@echo "  make database     - Start SurrealDB via Docker"
	@echo "  make worker       - Start background job worker"
	@echo "  make start-all    - Start all services"
	@echo "  make stop-all     - Stop all services"
	@echo "  make status       - Check which services are running"
	@echo "  make lint         - Run mypy type checking"
	@echo "  make ruff         - Run ruff linter with auto-fix"
	@echo "  make test         - Run all tests"
	@echo "  make test-feature - Run feature tests"
	@echo "  make clean-cache  - Clean cache files"

# 启动 FastAPI 开发服务器
api:
	uv run --env-file .env run_api.py

# 启动 SurrealDB
database:
	docker-compose up -d surrealdb

# 启动后台任务处理器
worker:
	uv run --env-file .env python -m open_notebook.commands.worker

# 启动所有服务
start-all:
	docker-compose up -d
	uv run --env-file .env run_api.py &

# 停止所有服务
stop-all:
	docker-compose down
	pkill -f "run_api.py" || true

# 检查服务状态
status:
	@echo "=== Docker Services ==="
	docker-compose ps
	@echo "\n=== API Server ==="
	curl -s http://localhost:5055/health || echo "API server not running"
	@echo "\n=== Frontend ==="
	curl -s http://localhost:3000 || echo "Frontend not running"

# 运行 mypy 类型检查
lint:
	uv run mypy .

# 运行 ruff linter
ruff:
	uv run ruff check . --fix

# 运行所有测试
test:
	uv run pytest tests/ -v --tb=short
	uv run pytest features/ -v --tb=short

# 运行 feature 测试
test-feature:
	uv run pytest features/ -v --tb=short

# 清理缓存
clean-cache:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
