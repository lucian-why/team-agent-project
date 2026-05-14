"""
学习画像 API 路由

提供学习画像的 CRUD 操作。
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel

from shared.auth.middleware import AuthMiddleware, User
from ..service.profile_service import ProfileService
from ..domain.profile import Profile, ProfileCreate, ProfileUpdate

router = APIRouter(prefix="/profiles", tags=["profiles"])

# 依赖注入
profile_service = ProfileService()


@router.post("/", response_model=Profile)
async def create_profile(
    data: ProfileCreate,
    current_user: User = Depends(AuthMiddleware.get_current_user)
):
    """
    创建学习画像

    Args:
        data: 画像数据
        current_user: 当前用户

    Returns:
        创建的画像
    """
    try:
        profile = await profile_service.create(data, current_user.id)
        return profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{profile_id}", response_model=Profile)
async def get_profile(
    profile_id: str,
    current_user: User = Depends(AuthMiddleware.get_current_user)
):
    """
    获取学习画像

    Args:
        profile_id: 画像 ID
        current_user: 当前用户

    Returns:
        画像数据
    """
    profile = await profile_service.get(profile_id, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/{profile_id}", response_model=Profile)
async def update_profile(
    profile_id: str,
    data: ProfileUpdate,
    current_user: User = Depends(AuthMiddleware.get_current_user)
):
    """
    更新学习画像

    Args:
        profile_id: 画像 ID
        data: 更新数据
        current_user: 当前用户

    Returns:
        更新后的画像
    """
    try:
        profile = await profile_service.update(profile_id, data, current_user.id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{profile_id}")
async def delete_profile(
    profile_id: str,
    current_user: User = Depends(AuthMiddleware.get_current_user)
):
    """
    删除学习画像

    Args:
        profile_id: 画像 ID
        current_user: 当前用户

    Returns:
        删除结果
    """
    success = await profile_service.delete(profile_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted successfully"}


@router.get("/", response_model=List[Profile])
async def list_profiles(
    limit: int = 100,
    offset: int = 0,
    current_user: User = Depends(AuthMiddleware.get_current_user)
):
    """
    列出学习画像

    Args:
        limit: 返回数量限制
        offset: 偏移量
        current_user: 当前用户

    Returns:
        画像列表
    """
    profiles = await profile_service.list(current_user.id, limit, offset)
    return profiles
