# Open Notebook - 团队协作版

> AI 时代的团队开发协作架构 - 垂直切片架构，支持 4 人团队并行开发

## 项目概览

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
├── CLAUDE.md                    # Claude Code 专用指令
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

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 20+
- Docker
- uv（Python 包管理器）

### 安装

```bash
# 克隆仓库
git clone https://github.com/lucian-why/team-agent-project.git
cd team-agent-project

# 安装后端依赖
uv sync

# 安装前端依赖
cd frontend && npm install && cd ..

# 复制环境变量
cp .env.example .env
# 编辑 .env 设置 OPEN_NOTEBOOK_ENCRYPTION_KEY

# 启动数据库
make database

# 启动后端
make api

# 启动前端（新终端）
cd frontend && npm run dev
```

### 使用 Docker

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

---

## 团队协作

### 分支策略

```
main（锁死，只允许 PR 合并）
├── feature/learning-profile    ← 功能开发
├── feature/chat                ← 功能开发
├── feature/sources             ← 功能开发
├── feature/podcasts            ← 功能开发
├── fix/<issue>                 ← Bug 修复
└── refactor/<name>             ← 重构
```

### 代码所有权

每个功能模块有对应的负责人，详见 `.github/CODEOWNERS`。

### 质量门禁

- **L1**: Claude Code Hooks（编码会话中）
- **L2**: Git Hooks（commit 前）
- **L3**: CI/CD Pipeline（PR 创建时）

---

## 开发指南

### 创建新功能

1. 创建功能分支：`git checkout -b feature/my-feature`
2. 在 `features/` 下创建功能目录
3. 实现功能（UI + API + 测试）
4. 提交 PR，等待 review
5. 合并后删除分支

### 运行测试

```bash
# 运行所有测试
make test

# 运行 feature 测试
make test-feature

# 运行单个测试
uv run pytest features/learning-profile/tests/test_profile.py -v
```

### 代码检查

```bash
# 类型检查
make lint

# 代码格式化
make ruff
```

---

## 部署

### 阿里云 ECS

- **服务器**：123.57.173.158
- **配置**：2 vCPU, 4 GiB, Ubuntu 22.04
- **登录**：`ssh root@123.57.173.158`

### 部署步骤

```bash
# 登录服务器
ssh root@123.57.173.158

# 克隆仓库
git clone https://github.com/lucian-why/team-agent-project.git
cd team-agent-project

# 启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

---

## 文档

- [AGENTS.md](AGENTS.md) - 跨平台 AI 入口
- [CLAUDE.md](CLAUDE.md) - Claude Code 专用指令
- [docs-ai/architecture.md](docs-ai/architecture.md) - 架构设计
- [docs-ai/api-specs/](docs-ai/api-specs/) - API 接口规范

---

## 贡献

1. Fork 仓库
2. 创建功能分支
3. 提交 PR
4. 等待 review

---

## 许可证

MIT License

---

## 联系方式

- **GitHub**: [lucian-why/team-agent-project](https://github.com/lucian-why/team-agent-project)
- **Email**: tech@example.com
