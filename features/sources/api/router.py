"""
资料源 API 路由

提供资料源的 CRUD 操作和处理功能。
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional

from shared.auth.middleware import AuthMiddleware
from ..service.source_service import SourceService, NotFoundError
from ..domain.source import (
    Source,
    SourceCreate,
    SourceUpdate,
    SourceList,
    SourceInsight,
    CreateInsightRequest,
    InsightCreationResponse,
    SourceStatusResponse,
)

router = APIRouter(prefix="/sources", tags=["sources"])

# 依赖注入
source_service = SourceService()


@router.get("/", response_model=List[SourceList])
async def get_sources(
    notebook_id: Optional[str] = Query(None, description="笔记本 ID"),
    limit: int = Query(50, ge=1, le=100, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    sort_by: str = Query("updated", description="排序字段"),
    sort_order: str = Query("desc", description="排序顺序"),
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    获取资料源列表

    Args:
        notebook_id: 笔记本 ID（可选）
        limit: 返回数量限制
        offset: 偏移量
        sort_by: 排序字段
        sort_order: 排序顺序
        current_user: 当前用户

    Returns:
        资料源列表
    """
    try:
        sources = await source_service.get_sources(
            owner_id=current_user.get("sub", ""),
            notebook_id=notebook_id,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return sources
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=Source)
async def create_source(
    request: SourceCreate,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    创建资料源

    Args:
        request: 创建请求
        current_user: 当前用户

    Returns:
        创建的资料源
    """
    try:
        source = await source_service.create_source(
            request=request,
            owner_id=current_user.get("sub", ""),
        )
        return source
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{source_id}", response_model=Source)
async def get_source(
    source_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    获取资料源详情

    Args:
        source_id: 资料源 ID
        current_user: 当前用户

    Returns:
        资料源详情
    """
    try:
        source = await source_service.get_source(
            source_id=source_id,
            owner_id=current_user.get("sub", ""),
        )
        return source
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{source_id}", response_model=Source)
async def update_source(
    source_id: str,
    request: SourceUpdate,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    更新资料源

    Args:
        source_id: 资料源 ID
        request: 更新请求
        current_user: 当前用户

    Returns:
        更新后的资料源
    """
    try:
        source = await source_service.update_source(
            source_id=source_id,
            request=request,
            owner_id=current_user.get("sub", ""),
        )
        return source
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{source_id}")
async def delete_source(
    source_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    删除资料源

    Args:
        source_id: 资料源 ID
        current_user: 当前用户

    Returns:
        删除结果
    """
    try:
        success = await source_service.delete_source(
            source_id=source_id,
            owner_id=current_user.get("sub", ""),
        )
        if success:
            return {"message": "Source deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete source")
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{source_id}/status", response_model=SourceStatusResponse)
async def get_source_status(
    source_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    获取资料源处理状态

    Args:
        source_id: 资料源 ID
        current_user: 当前用户

    Returns:
        处理状态
    """
    try:
        status = await source_service.get_source_status(
            source_id=source_id,
            owner_id=current_user.get("sub", ""),
        )
        return status
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{source_id}/retry", response_model=Source)
async def retry_source(
    source_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    重试资料源处理

    Args:
        source_id: 资料源 ID
        current_user: 当前用户

    Returns:
        更新后的资料源
    """
    # TODO: 实现重试逻辑
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{source_id}/insights", response_model=List[SourceInsight])
async def get_source_insights(
    source_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    获取资料源洞察列表

    Args:
        source_id: 资料源 ID
        current_user: 当前用户

    Returns:
        洞察列表
    """
    try:
        insights = await source_service.get_insights(
            source_id=source_id,
            owner_id=current_user.get("sub", ""),
        )
        return insights
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{source_id}/insights", response_model=InsightCreationResponse, status_code=202)
async def create_source_insight(
    source_id: str,
    request: CreateInsightRequest,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    创建资料源洞察

    Args:
        source_id: 资料源 ID
        request: 创建请求
        current_user: 当前用户

    Returns:
        创建响应
    """
    try:
        response = await source_service.create_insight(
            source_id=source_id,
            request=request,
            owner_id=current_user.get("sub", ""),
        )
        return response
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
