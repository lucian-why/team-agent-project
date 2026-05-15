"""
播客 API 路由

提供播客的 CRUD 操作和生成功能。
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional

from shared.auth.middleware import AuthMiddleware
from ..service.podcast_service import PodcastService, NotFoundError
from ..domain.episode import (
    PodcastEpisode,
    PodcastGenerationRequest,
    PodcastGenerationResponse,
    PodcastJobStatus,
)

router = APIRouter(prefix="/podcasts", tags=["podcasts"])

# 依赖注入
podcast_service = PodcastService()


@router.get("/episodes", response_model=List[PodcastEpisode])
async def get_episodes(
    limit: int = Query(50, ge=1, le=100, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    获取播客剧集列表

    Args:
        limit: 返回数量限制
        offset: 偏移量
        current_user: 当前用户

    Returns:
        剧集列表
    """
    try:
        episodes = await podcast_service.get_episodes(
            owner_id=current_user.get("sub", ""),
            limit=limit,
            offset=offset,
        )
        return episodes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/episodes/{episode_id}", response_model=PodcastEpisode)
async def get_episode(
    episode_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    获取播客剧集详情

    Args:
        episode_id: 剧集 ID
        current_user: 当前用户

    Returns:
        剧集详情
    """
    try:
        episode = await podcast_service.get_episode(
            episode_id=episode_id,
            owner_id=current_user.get("sub", ""),
        )
        return episode
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/episodes/{episode_id}")
async def delete_episode(
    episode_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    删除播客剧集

    Args:
        episode_id: 剧集 ID
        current_user: 当前用户

    Returns:
        删除结果
    """
    try:
        success = await podcast_service.delete_episode(
            episode_id=episode_id,
            owner_id=current_user.get("sub", ""),
        )
        if success:
            return {"message": "Episode deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete episode")
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate", response_model=PodcastGenerationResponse)
async def generate_podcast(
    request: PodcastGenerationRequest,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    生成播客

    Args:
        request: 生成请求
        current_user: 当前用户

    Returns:
        生成响应
    """
    try:
        response = await podcast_service.submit_generation_job(
            request=request,
            owner_id=current_user.get("sub", ""),
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{job_id}", response_model=PodcastJobStatus)
async def get_job_status(
    job_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    获取任务状态

    Args:
        job_id: 任务 ID
        current_user: 当前用户

    Returns:
        任务状态
    """
    try:
        status = await podcast_service.get_job_status(job_id=job_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/episodes/{episode_id}/retry", response_model=PodcastGenerationResponse)
async def retry_episode(
    episode_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    重试播客剧集

    Args:
        episode_id: 剧集 ID
        current_user: 当前用户

    Returns:
        生成响应
    """
    try:
        response = await podcast_service.retry_episode(
            episode_id=episode_id,
            owner_id=current_user.get("sub", ""),
        )
        return response
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/episodes/{episode_id}/audio")
async def get_episode_audio(
    episode_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    获取剧集音频

    Args:
        episode_id: 剧集 ID
        current_user: 当前用户

    Returns:
        音频文件
    """
    # TODO: 实现音频文件返回逻辑
    raise HTTPException(status_code=501, detail="Not implemented yet")
