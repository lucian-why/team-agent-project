# AGENTS.md - 跨平台 AI 入口

> 本文件是所有 AI 编码工具（Claude Code、Cursor、Copilot、Gemini）的统一入口。

## 项目概览

**Open Notebook** 是一个开源、隐私优先的 AI 研究助手，支持上传多模态内容（PDF、音频、视频、网页）、生成笔记、语义搜索、AI 对话和播客生成。

**架构**：Next.js 前端（端口 3000）→ FastAPI 后端（端口 5055）→ SurrealDB 图数据库（端口 8000）。

**核心价值**：隐私优先、多提供商 AI 支持（18+ 提供商）、完全自托管。

---

## 阅读顺序

1. **先读本文件**（AGENTS.md）— 了解项目全貌
2. **再读 CLAUDE.md** — 了解架构细节和编码规范
3. **按需读 features/ 下的 README** — 了解具体功能模块

---

## 项目结构

```
team-agent-project/
├── AGENTS.md                    # 本文件（跨平台入口）
├── CLAUDE.md                    # Claude Code 专用指令
├── .claude/                     # Claude Code 配置
├── .github/                     # GitHub 配置（CODEOWNERS、CI/CD）
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

---

## 核心命令

### 后端（Python）

| 命令 | 说明 |
|------|------|
| `make api` | 启动 FastAPI 开发服务器 |
| `make database` | 通过 Docker 启动 SurrealDB |
| `make worker` | 启动后台任务处理器 |
| `make start-all` | 启动所有服务 |
| `make stop-all` | 停止所有服务 |
| `uv run pytest tests/` | 运行后端测试 |

### 前端（TypeScript/Next.js）

| 命令 | 说明 |
|------|------|
| `cd frontend && npm run dev` | 启动 Next.js 开发服务器 |
| `cd frontend && npm run build` | 生产构建 |
| `cd frontend && npm test` | 运行测试 |

---

## 红线（绝对不能做）

1. **不要直接推送到 main 分支** — 必须通过 PR
2. **不要修改 shared/ 层的接口** — 需要通知所有人
3. **不要提交敏感信息** — .env、密钥、密码
4. **不要跳过测试** — 所有代码必须有测试
5. **不要使用 AI 自动 push** — push 必须是人工操作

---

## 检索地图

| 想了解... | 去哪里看 |
|-----------|----------|
| 项目架构 | `CLAUDE.md` 的"高级架构"部分 |
| API 接口 | `features/*/api/router.py` |
| 数据库模型 | `shared/database/models.py` |
| AI 提供商 | `shared/ai/provider.py` |
| 前端组件 | `features/*/components/` |
| 测试 | `features/*/tests/` |
| 部署 | `docker-compose.yml`、`Dockerfile` |
| 团队协作 | `docs-ai/architecture.md` |

---

## AI 工具特定配置

### Claude Code
- 读取 `CLAUDE.md` 获取详细指令
- 配置文件：`.claude/settings.json`

### Cursor
- 规则文件：`.cursor/rules/*.mdc`（可从 CLAUDE.md 派生）

### Copilot
- 指令文件：`.github/copilot-instructions.md`（可从 CLAUDE.md 派生）

### Gemini
- 配置文件：`GEMINI.md`（可从 CLAUDE.md 派生）

---

## 团队协作

- **分支策略**：简化的 GitHub Flow
- **代码所有权**：`.github/CODEOWNERS`
- **质量门禁**：Git Hooks + CI/CD
- **文档同步**：每次改完需求跑一次 `/neat-freak`

---

## 最后更新

- 日期：2026-05-15
- 维护者：tech-lead
