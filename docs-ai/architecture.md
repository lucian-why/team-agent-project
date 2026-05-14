# 架构设计文档

## 概述

本文档描述 Open Notebook 团队协作版的架构设计，采用垂直切片架构（Vertical Slices），支持 4 人团队并行开发。

---

## 核心设计原则

### 1. 垂直切片（Vertical Slices）

按业务功能组织代码，不按技术层（前端/后端）组织。

**优势**：
- AI 上下文范围小（只看一个 feature）
- 人与人耦合度低（各 feature 独立）
- 并行开发效率高（互不阻塞）
- AI 出错率低（上下文精准）

### 2. 接口锁死（Interface Lock）

shared/ 层的接口一旦定义，所有人依赖，不能随意修改。

**规则**：
- shared/ 层接口定义后，需要所有人 review
- 修改 shared/ 层接口需要通知所有人
- feature/ 层可以独立修改自己的接口

### 3. 端到端闭环（End-to-End）

每个功能模块包含完整的 UI + API + 测试，不跨 feature 修改代码。

**结构**：
```
features/learning-profile/
├── components/          # UI 组件
├── api/                 # API 路由
├── service/             # 业务逻辑
├── domain/              # 领域模型
└── tests/               # 测试
```

---

## 目录结构

```
team-agent-project/
├── AGENTS.md                    # 跨平台 AI 入口（< 100 行）
├── CLAUDE.md                    # 项目级 AI 指令（< 200 行）
├── .claude/
│   ├── settings.json            # 团队共享配置（提交到 git）
│   └── settings.local.json      # 个人覆盖（自动 gitignore）
├── .github/
│   ├── CODEOWNERS               # 代码所有权定义
│   └── workflows/
│       └── ci.yml               # CI/CD 配置
├── shared/                      # 公共层（接口锁死，所有人依赖）
│   ├── database/                # 数据库连接、模型、迁移
│   │   ├── repository.py        # CRUD 操作
│   │   ├── async_migrate.py     # 异步迁移
│   │   └── models.py            # 数据模型
│   ├── auth/                    # 认证中间件
│   │   ├── middleware.py
│   │   └── jwt.py
│   └── ai/                      # AI 模型封装
│       ├── provider.py          # AI 提供商接口
│       └── models.py            # 模型管理
├── features/                    # 功能切片（每人负责 1-2 个）
│   ├── learning-profile/        # 成员 A
│   ├── chat/                    # 成员 B
│   ├── sources/                 # 成员 C
│   └── podcasts/                # 成员 D
├── frontend/                    # 前端公共部分
├── docs-ai/                     # AI 参考文档
├── docker-compose.yml
├── Dockerfile
└── Makefile
```

---

## 接口契约

### shared 层接口（锁死）

```python
# shared/database/repository.py
class Repository:
    async def create(self, data: dict) -> dict
    async def get(self, id: str) -> dict
    async def update(self, id: str, data: dict) -> dict
    async def delete(self, id: str) -> bool
    async def list(self, filters: dict = None) -> list[dict]

# shared/ai/provider.py
class AIProvider:
    async def generate(self, prompt: str, **kwargs) -> str
    async def stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]

# shared/auth/middleware.py
class AuthMiddleware:
    async def verify_token(self, token: str) -> dict
    async def get_current_user(self, request: Request) -> User
```

### feature 层接口（独立）

每个 feature 模块定义自己的 API 接口，详见 `features/*/api/router.py`。

---

## Git 分支策略

```
main（锁死，只允许 PR 合并）
├── feature/learning-profile    ← 成员 A
├── feature/chat                ← 成员 B
├── feature/sources             ← 成员 C
├── feature/podcasts            ← 成员 D
├── refactor/shared             ← 共享层重构（串行）
└── infra/ci-cd                 ← CI/CD 配置
```

**分支规则**：
- `main` 通过 Protected Branch 禁止直接推送
- 每个任务一个分支，小而聚焦
- 分支命名：`feature/<name>`、`fix/<issue>`、`refactor/<name>`
- 用完即弃，合并后删除分支

---

## 三层质量门禁

| 层级 | 工具 | 时机 | 作用 |
|------|------|------|------|
| **L1** | Claude Code Hooks | 编码会话中 | AI 生成代码后立即验证 |
| **L2** | Git Hooks (Husky) | commit 前 | 最终守门人，进版本控制前检查 |
| **L3** | CI/CD Pipeline | PR 创建时 | 服务端强制执行 |

---

## 团队分工

**建议分工模式**（按 feature 垂直切片）：

| 角色 | 负责模块 | 职责范围 |
|------|----------|----------|
| 成员 A | learning-profile + learning-path | 学生画像、学习路径的前后端 |
| 成员 B | chat + multi-agent | 对话、多智能体编排的前后端 |
| 成员 C | sources + podcasts | 资料源、播客生成的前后端 |
| 成员 D | xingyu + 其他 | 自定义助手、辅助功能 |
| tech-lead | 基础设施 + shared 层 | AGENTS.md、CLAUDE.md、CODEOWNERS、CI/CD、shared 层设计 |

**协作原则**：
- 每人在自己的 feature 目录下**端到端闭环**（UI + API + 测试）
- 不跨 feature 修改代码
- shared 层接口锁死，改接口需要通知所有人

---

## 参考资料

- [团队协作方案文档](../agent-文档/团队协作.md)
- [团队协作方案文档 2](../agent-文档/团队协作2.md)
- [团队架构展示页面](https://lucian-why.github.io/team-skills/team-architecture.html)
