"""
资料源 API 路由

提供资料源管理功能。
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel

from shared.auth.middleware import AuthMiddleware, User
from ..service.source_service import SourceService
from ..domain.source import Source, SourceCreate, SourceUpdate

router = APIRouter(prefix="/sources", tags=["sources"])

# 依赖注入
source_service = SourceService()


@router.post("/", response_model=Source)
async def create_source(
    data: SourceCreate,
    current_user: User = Depends(AuthMiddleware.get_current_user)
):
    """
    创建资料源

    Args:
        data: 资料源数据
        current_user: 当前用户

    Returns:
        创建的资料源
    """
    try:
        source = await source_service.create(data, current_user.id)
        return source
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{source_id}", response_model=Source)
async def get_source(
    source_id: str,
    current_user: User = Depends(AuthMiddleware.get_current_user)
):
    """
    获取资料源

    Args:
        source_id: 资料源 ID
        current_user: 当前用户

    Returns:
        资料源数据
    """
    source = await source_service.get(source_id, current_user.id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.get("/", response_model=List[Source])
async def list_sources(
    limit: int = 100,
    offset: int = 0,
    current_user: User = Depends(AuthMiddleware.get_current_user)
):
    """
    列出资料源

    Args:
        limit: 返回数量限制
        offset: 偏移量
        current_user: 当前用户

    Returns:
        资料源列表
    """
    sources = await source_service.list(current_user.id, limit, offset)
    return sources
