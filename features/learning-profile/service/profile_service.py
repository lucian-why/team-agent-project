"""
学习画像服务层

提供学习画像的业务逻辑，从现有项目迁移并重构。
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from shared.database.repository import Repository
from ..domain.profile import (
    StudentProfile,
    StudentProfileCreate,
    StudentProfileUpdate,
    LearningPath,
    LearningPathCreate,
    LearningPathUpdate,
    WrongQuestionGroup,
)


def _now_iso() -> str:
    """获取当前时间的 ISO 格式字符串"""
    return datetime.now(timezone.utc).isoformat()


def _normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """标准化记录格式"""
    normalized = dict(record)
    if "created_at" in normalized and "created" not in normalized:
        normalized["created"] = normalized.pop("created_at")
    if "updated_at" in normalized and "updated" not in normalized:
        normalized["updated"] = normalized.pop("updated_at")
    if normalized.get("created") is not None:
        normalized["created"] = str(normalized["created"])
    if normalized.get("updated") is not None:
        normalized["updated"] = str(normalized["updated"])
    return normalized


def _with_defaults(notebook_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """添加默认值"""
    return {
        "notebook_id": notebook_id,
        "schema_version": 1,
        "source_ids": [],
        "created_by": "user",
        "metadata": {},
        **payload,
    }


class ProfileService:
    """学习画像服务"""

    def __init__(self):
        self.repository = Repository("student_profile")

    async def get_profile(
        self, notebook_id: str, owner_id: str = ""
    ) -> StudentProfile:
        """
        获取学生画像

        Args:
            notebook_id: 笔记本 ID
            owner_id: 所有者 ID

        Returns:
            学生画像

        Raises:
            NotFoundError: 画像不存在
        """
        rows = await self.repository.list(
            filters={"notebook_id": notebook_id},
            limit=1
        )
        if not rows:
            raise NotFoundError(f"Student profile for notebook {notebook_id} not found")
        return StudentProfile.model_validate(_normalize_record(rows[0]))

    async def upsert_profile(
        self,
        notebook_id: str,
        request: StudentProfileCreate,
        owner_id: str = ""
    ) -> StudentProfile:
        """
        创建或更新学生画像

        Args:
            notebook_id: 笔记本 ID
            request: 画像数据
            owner_id: 所有者 ID

        Returns:
            学生画像
        """
        data = _with_defaults(
            notebook_id,
            request.model_dump(exclude_unset=True),
        )
        if owner_id:
            data["owner_id"] = owner_id

        # 查找现有记录
        rows = await self.repository.list(
            filters={"notebook_id": notebook_id},
            limit=1
        )

        if rows:
            # 更新现有记录
            result = await self.repository.update(rows[0]["id"], data)
            record = result[0] if isinstance(result, list) else result
        else:
            # 创建新记录
            record = await self.repository.create(data)

        return StudentProfile.model_validate(_normalize_record(record))

    async def update_profile(
        self,
        notebook_id: str,
        request: StudentProfileUpdate,
        owner_id: str = ""
    ) -> StudentProfile:
        """
        更新学生画像

        Args:
            notebook_id: 笔记本 ID
            request: 更新数据
            owner_id: 所有者 ID

        Returns:
            学生画像
        """
        # 获取现有画像
        existing = await self.get_profile(notebook_id, owner_id)

        # 准备更新数据
        update_data = request.model_dump(exclude_unset=True)
        update_data["updated"] = _now_iso()

        # 更新记录
        result = await self.repository.update(existing.id, update_data)
        record = result[0] if isinstance(result, list) else result

        return StudentProfile.model_validate(_normalize_record(record))

    async def delete_profile(
        self,
        notebook_id: str,
        owner_id: str = ""
    ) -> bool:
        """
        删除学生画像

        Args:
            notebook_id: 笔记本 ID
            owner_id: 所有者 ID

        Returns:
            是否删除成功
        """
        existing = await self.get_profile(notebook_id, owner_id)
        return await self.repository.delete(existing.id)


class LearningPathService:
    """学习路径服务"""

    def __init__(self):
        self.repository = Repository("learning_path")

    async def get_path(
        self, notebook_id: str, owner_id: str = ""
    ) -> LearningPath:
        """
        获取学习路径

        Args:
            notebook_id: 笔记本 ID
            owner_id: 所有者 ID

        Returns:
            学习路径

        Raises:
            NotFoundError: 路径不存在
        """
        rows = await self.repository.list(
            filters={"notebook_id": notebook_id},
            limit=1
        )
        if not rows:
            raise NotFoundError(f"Learning path for notebook {notebook_id} not found")
        return LearningPath.model_validate(_normalize_record(rows[0]))

    async def upsert_path(
        self,
        notebook_id: str,
        request: LearningPathCreate,
        owner_id: str = ""
    ) -> LearningPath:
        """
        创建或更新学习路径

        Args:
            notebook_id: 笔记本 ID
            request: 路径数据
            owner_id: 所有者 ID

        Returns:
            学习路径
        """
        data = _with_defaults(
            notebook_id,
            request.model_dump(mode="json", exclude_unset=True),
        )
        if owner_id:
            data["owner_id"] = owner_id

        # 查找现有记录
        rows = await self.repository.list(
            filters={"notebook_id": notebook_id},
            limit=1
        )

        if rows:
            # 更新现有记录
            result = await self.repository.update(rows[0]["id"], data)
            record = result[0] if isinstance(result, list) else result
        else:
            # 创建新记录
            record = await self.repository.create(data)

        return LearningPath.model_validate(_normalize_record(record))

    async def update_path(
        self,
        notebook_id: str,
        request: LearningPathUpdate,
        owner_id: str = ""
    ) -> LearningPath:
        """
        更新学习路径

        Args:
            notebook_id: 笔记本 ID
            request: 更新数据
            owner_id: 所有者 ID

        Returns:
            学习路径
        """
        # 获取现有路径
        existing = await self.get_path(notebook_id, owner_id)

        # 准备更新数据
        update_data = request.model_dump(mode="json", exclude_unset=True)
        update_data["updated"] = _now_iso()

        # 更新记录
        result = await self.repository.update(existing.id, update_data)
        record = result[0] if isinstance(result, list) else result

        return LearningPath.model_validate(_normalize_record(record))


class NotFoundError(Exception):
    """资源不存在异常"""
    pass
