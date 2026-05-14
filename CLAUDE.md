# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Open Notebook** 是一个开源、隐私优先的 AI 研究助手，支持上传多模态内容（PDF、音频、视频、网页）、生成笔记、语义搜索、AI 对话和播客生成。

**架构**：Next.js 前端（端口 3000）→ FastAPI 后端（端口 5055）→ SurrealDB 图数据库（端口 8000）。

**核心价值**：隐私优先、多提供商 AI 支持（18+ 提供商）、完全自托管。

---

## 垂直切片架构

本项目采用**垂直切片架构**（Vertical Slices），按功能模块组织代码，不按技术层（前端/后端）组织。

### 目录结构

```
team-agent-project/
├── AGENTS.md                    # 跨平台 AI 入口
├── CLAUDE.md                    # 本文件
├── .claude/                     # Claude Code 配置
├── .github/                     # GitHub 配置
├── shared/                      # 公共层（接口锁死）
│   ├── database/                # 数据库连接、模型、迁移
│   ├── auth/                    # 认证中间件
│   └── ai/                      # AI 模型封装
├── features/                    # 功能切片（垂直架构）
│   ├── learning-profile/        # 学生画像
│   ├── chat/                    # AI 对话
│   ├── sources/                 # 资料源管理
│   └── podcasts/                # 播客生成
├── frontend/                    # 前端公共部分
├── docs-ai/                     # AI 参考文档
└── scripts/                     # 脚本工具
```

### 为什么这样设计

| 维度 | 垂直切片（功能） | 水平分层（前后端） |
|------|------------------|-------------------|
| AI 上下文范围 | 小（只看一个 feature） | 大（整个 frontend/ 或 api/） |
| 人与人耦合度 | 低（各 feature 独立） | 高（前端等后端接口） |
| 并行开发效率 | 高（互不阻塞） | 低（需要协调接口） |
| AI 出错率 | 低（上下文精准） | 高（上下文污染） |

---

## Development Setup

- **Requirements**: Python 3.11+, `uv` package manager, Node.js/npm, Docker (for SurrealDB).
- **Install Python deps**: `uv sync`
- **Install frontend deps**: `cd frontend && npm install`
- **Environment**: Copy `.env.example` to `.env` and set `OPEN_NOTEBOOK_ENCRYPTION_KEY`.

---

## Common Commands

### Backend (Python)

| Command | Description |
|---------|-------------|
| `make api` | Start FastAPI dev server |
| `make database` | Start SurrealDB via Docker |
| `make worker` | Start background job worker |
| `make start-all` | Start all services |
| `make stop-all` | Stop all services |
| `uv run pytest tests/` | Run all backend tests |
| `uv run pytest features/learning-profile/tests/` | Run feature tests |
| `make lint` | Run mypy type checking |
| `make ruff` | Run ruff linter with auto-fix |

### Frontend (TypeScript/Next.js)

| Command | Description |
|---------|-------------|
| `cd frontend && npm run dev` | Start Next.js dev server |
| `cd frontend && npm run build` | Production build |
| `cd frontend && npm test` | Run vitest once |
| `cd frontend && npm run test:watch` | Run vitest in watch mode |

---

## High-Level Architecture

### Shared Layer (`shared/`)

公共层，接口锁死，所有人依赖。

#### Database (`shared/database/`)

SurrealDB async driver with repository pattern:

- **`repository.py`**: Raw CRUD operations. Auto-timestamps `created`/`updated`.
- **`async_migrate.py`**: Schema migrations on API startup.
- **`models.py`**: Data models.

#### Auth (`shared/auth/`)

Multi-user JWT authentication:

- **`middleware.py`**: `PasswordAuthMiddleware` validates JWT tokens.
- **`jwt.py`**: JWT token generation and validation.

#### AI (`shared/ai/`)

Multi-provider AI support:

- **`provider.py`**: Unified interface to 18+ AI providers.
- **`models.py`**: Model management and fallback logic.

### Feature Layer (`features/`)

每个功能模块独立，端到端闭环（UI + API + 测试）。

#### Learning Profile (`features/learning-profile/`)

学生画像模块：

- `components/`: React 组件
- `api/router.py`: FastAPI 路由
- `service/profile_service.py`: 业务逻辑
- `domain/profile.py`: 领域模型
- `tests/`: 单元测试和集成测试

#### Chat (`features/chat/`)

AI 对话模块：

- `components/`: React 组件
- `api/router.py`: FastAPI 路由
- `service/chat_service.py`: 业务逻辑
- `domain/message.py`: 领域模型
- `tests/`: 单元测试和集成测试

#### Sources (`features/sources/`)

资料源管理模块：

- `components/`: React 组件
- `api/router.py`: FastAPI 路由
- `service/source_service.py`: 业务逻辑
- `domain/source.py`: 领域模型
- `tests/`: 单元测试和集成测试

#### Podcasts (`features/podcasts/`)

播客生成模块：

- `components/`: React 组件
- `api/router.py`: FastAPI 路由
- `service/podcast_service.py`: 业务逻辑
- `domain/episode.py`: 领域模型
- `tests/`: 单元测试和集成测试

### Frontend (`frontend/`)

Next.js 16 (React 19), TypeScript, Tailwind CSS + Shadcn/ui.

- `src/app/`: Next.js App Router
- `src/components/ui/`: 公共 UI 组件
- `src/lib/utils.ts`: 公共工具函数

---

## Coding Principles

### Think Before Coding

Don't assume silently. When uncertain, state assumptions explicitly, present multiple interpretations, and ask for clarification before implementing.

### Surgical Changes

Every changed line should trace directly to the user's request. When editing existing code:

- Don't "improve" adjacent code, comments, or formatting that wasn't asked about
- Match existing style, even if you'd do it differently
- If your changes create unused imports/variables/functions, remove them

### Goal-Driven Execution

Transform imperative tasks into verifiable goals. Instead of vague instructions, define success criteria:

| Instead of... | Use... |
|---|---|
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |

---

## Important Quirks & Gotchas

- **Migrations auto-run on startup** but must be manually registered.
- **SurrealDB must be running before API starts**. Use `make database`.
- **Worker required for podcasts**. Without `make worker`, episodes stay queued.
- **API must start before frontend**. The UI has no standalone data layer.
- **LangGraph async workaround**: `source_chat.py` spins up a new event loop inside sync graph nodes.
- **CORS wide open in dev**: Restrict before production.
- **Multi-user data isolation**: When `AUTH_ENABLED=true`, each user's data is isolated via `owner_id`.

---

## Git Workflow

### Branch Strategy

```
main（锁死，只允许 PR 合并）
├── feature/learning-profile    ← 功能开发
├── feature/chat                ← 功能开发
├── feature/sources             ← 功能开发
├── feature/podcasts            ← 功能开发
├── fix/<issue>                 ← Bug 修复
└── refactor/<name>             ← 重构
```

### Commit Convention

使用 Conventional Commits：

```
feat: 添加学生画像模块
fix: 修复 RAG 检索空结果问题
refactor: 拆分 chat service 为独立文件
docs: 更新 API 文档
test: 添加 learning-path 单元测试
```

### PR 规范

- 每个 PR < 500 行
- 每个 PR 只解决一个问题
- PR 描述说明 AI 贡献
- CODEOWNERS 自动分配 reviewer

---

## Sub-Module Documentation

- **[`shared/database/CLAUDE.md`](shared/database/CLAUDE.md)**: 数据库层
- **[`shared/auth/CLAUDE.md`](shared/auth/CLAUDE.md)**: 认证层
- **[`shared/ai/CLAUDE.md`](shared/ai/CLAUDE.md)**: AI 层
- **[`features/learning-profile/CLAUDE.md`](features/learning-profile/CLAUDE.md)**: 学生画像模块
- **[`features/chat/CLAUDE.md`](features/chat/CLAUDE.md)**: AI 对话模块
- **[`features/sources/CLAUDE.md`](features/sources/CLAUDE.md)**: 资料源模块
- **[`features/podcasts/CLAUDE.md`](features/podcasts/CLAUDE.md)**: 播客模块

---

## 最后更新

- 日期：2026-05-15
- 维护者：tech-lead
