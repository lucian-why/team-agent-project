"""
FastAPI 主应用入口

注册所有 feature 模块的路由。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入各 feature 模块的路由
from features.learning_profile.api.router import router as learning_profile_router
from features.chat.api.router import router as chat_router
from features.sources.api.router import router as sources_router
from features.podcasts.api.router import router as podcasts_router

app = FastAPI(
    title="Open Notebook - Team Agent Project",
    description="AI 时代的团队开发协作架构 - 垂直切片架构，支持 4 人团队并行开发",
    version="1.0.0",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(learning_profile_router)
app.include_router(chat_router)
app.include_router(sources_router)
app.include_router(podcasts_router)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Open Notebook - Team Agent Project",
        "version": "1.0.0",
        "architecture": "Vertical Slices",
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}
