"""
学习画像 API 路由

提供学习画像的 CRUD 操作，从现有项目迁移并重构。
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel

from shared.auth.middleware import AuthMiddleware, User
from ..service.profile_service import ProfileService, LearningPathService, NotFoundError
from ..domain.profile import (
    StudentProfile,
    StudentProfileCreate,
    StudentProfileUpdate,
    LearningPath,
    LearningPathCreate,
    LearningPathUpdate,
)

router = APIRouter(prefix="/learning", tags=["learning"])

# 依赖注入
profile_service = ProfileService()
learning_path_service = LearningPathService()


# ==================== 学生画像 ====================

@router.get("/notebooks/{notebook_id}/profile", response_model=StudentProfile)
async def get_student_profile(
    notebook_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user)
):
    """
    获取学生画像

    Args:
        notebook_id: 笔记本 ID
        current_user: 当前用户

    Returns:
        学生画像
    """
    try:
        profile = await profile_service.get_profile(
            notebook_id,
            owner_id=current_user.get("sub", "")
        )
        return profile
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/notebooks/{notebook_id}/profile", response_model=StudentProfile)
async def upsert_student_profile(
    notebook_id: str,
    request: StudentProfileCreate,
    current_user: dict = Depends(AuthMiddleware.get_current_user)
):
    """
    创建或更新学生画像

    Args:
        notebook_id: 笔记本 ID
        request: 画像数据
        current_user: 当前用户

    Returns:
        学生画像
    """
    try:
        profile = await profile_service.upsert_profile(
            notebook_id,
            request,
            owner_id=current_user.get("sub", "")
        )
        return profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/notebooks/{notebook_id}/profile", response_model=StudentProfile)
async def update_student_profile(
    notebook_id: str,
    request: StudentProfileUpdate,
    current_user: dict = Depends(AuthMiddleware.get_current_user)
):
    """
    更新学生画像

    Args:
        notebook_id: 笔记本 ID
        request: 更新数据
        current_user: 当前用户

    Returns:
        学生画像
    """
    try:
        profile = await profile_service.update_profile(
            notebook_id,
            request,
            owner_id=current_user.get("sub", "")
        )
        return profile
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/notebooks/{notebook_id}/profile")
async def delete_student_profile(
    notebook_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user)
):
    """
    删除学生画像

    Args:
        notebook_id: 笔记本 ID
        current_user: 当前用户

    Returns:
        删除结果
    """
    try:
        success = await profile_service.delete_profile(
            notebook_id,
            owner_id=current_user.get("sub", "")
        )
        if success:
            return {"message": "Profile deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete profile")
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ==================== 学习路径 ====================

@router.get("/notebooks/{notebook_id}/learning-path", response_model=LearningPath)
async def get_learning_path(
    notebook_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user)
):
    """
    获取学习路径

    Args:
        notebook_id: 笔记本 ID
        current_user: 当前用户

    Returns:
        学习路径
    """
    try:
        path = await learning_path_service.get_path(
            notebook_id,
            owner_id=current_user.get("sub", "")
        )
        return path
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/notebooks/{notebook_id}/learning-path", response_model=LearningPath)
async def upsert_learning_path(
    notebook_id: str,
    request: LearningPathCreate,
    current_user: dict = Depends(AuthMiddleware.get_current_user)
):
    """
    创建或更新学习路径

    Args:
        notebook_id: 笔记本 ID
        request: 路径数据
        current_user: 当前用户

    Returns:
        学习路径
    """
    try:
        path = await learning_path_service.upsert_path(
            notebook_id,
            request,
            owner_id=current_user.get("sub", "")
        )
        return path
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/notebooks/{notebook_id}/learning-path", response_model=LearningPath)
async def update_learning_path(
    notebook_id: str,
    request: LearningPathUpdate,
    current_user: dict = Depends(AuthMiddleware.get_current_user)
):
    """
    更新学习路径

    Args:
        notebook_id: 笔记本 ID
        request: 更新数据
        current_user: 当前用户

    Returns:
        学习路径
    """
    try:
        path = await learning_path_service.update_path(
            notebook_id,
            request,
            owner_id=current_user.get("sub", "")
        )
        return path
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
