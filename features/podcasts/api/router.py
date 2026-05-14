"""
播客 API 路由

提供播客生成功能。
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel

from shared.auth.middleware import AuthMiddleware, User
from ..service.podcast_service import PodcastService
from ..domain.episode import Episode, EpisodeCreate

router = APIRouter(prefix="/podcasts", tags=["podcasts"])

# 依赖注入
podcast_service = PodcastService()


@router.post("/episodes", response_model=Episode)
async def create_episode(
    data: EpisodeCreate,
    current_user: User = Depends(AuthMiddleware.get_current_user)
):
    """
    创建播客剧集

    Args:
        data: 剧集数据
        current_user: 当前用户

    Returns:
        创建的剧集
    """
    try:
        episode = await podcast_service.create_episode(data, current_user.id)
        return episode
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/episodes", response_model=List[Episode])
async def list_episodes(
    limit: int = 100,
    offset: int = 0,
    current_user: User = Depends(AuthMiddleware.get_current_user)
):
    """
    列出播客剧集

    Args:
        limit: 返回数量限制
        offset: 偏移量
        current_user: 当前用户

    Returns:
        剧集列表
    """
    episodes = await podcast_service.list_episodes(current_user.id, limit, offset)
    return episodes
