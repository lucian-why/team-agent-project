"""
学习画像服务层

提供学习画像的业务逻辑。
"""

from typing import List, Optional
from datetime import datetime

from shared.database.repository import Repository
from ..domain.profile import Profile, ProfileCreate, ProfileUpdate


class ProfileService:
    """学习画像服务"""

    def __init__(self):
        self.repository = Repository("profiles")

    async def create(self, data: ProfileCreate, user_id: str) -> Profile:
        """
        创建学习画像

        Args:
            data: 画像数据
            user_id: 用户 ID

        Returns:
            创建的画像
        """
        # 准备数据
        profile_data = {
            **data.dict(),
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # 创建记录
        result = await self.repository.create(profile_data)

        # 返回画像对象
        return Profile(**result)

    async def get(self, profile_id: str, user_id: str) -> Optional[Profile]:
        """
        获取学习画像

        Args:
            profile_id: 画像 ID
            user_id: 用户 ID

        Returns:
            画像数据，如果不存在返回 None
        """
        # 查询记录
        result = await self.repository.get(profile_id)

        # 检查所有权
        if not result or result.get("user_id") != user_id:
            return None

        return Profile(**result)

    async def update(
        self,
        profile_id: str,
        data: ProfileUpdate,
        user_id: str
    ) -> Optional[Profile]:
        """
        更新学习画像

        Args:
            profile_id: 画像 ID
            data: 更新数据
            user_id: 用户 ID

        Returns:
            更新后的画像，如果不存在返回 None
        """
        # 检查是否存在且属于当前用户
        existing = await self.get(profile_id, user_id)
        if not existing:
            return None

        # 准备更新数据
        update_data = {
            **data.dict(exclude_unset=True),
            "updated_at": datetime.utcnow()
        }

        # 更新记录
        result = await self.repository.update(profile_id, update_data)

        return Profile(**result)

    async def delete(self, profile_id: str, user_id: str) -> bool:
        """
        删除学习画像

        Args:
            profile_id: 画像 ID
            user_id: 用户 ID

        Returns:
            是否删除成功
        """
        # 检查是否存在且属于当前用户
        existing = await self.get(profile_id, user_id)
        if not existing:
            return False

        # 删除记录
        return await self.repository.delete(profile_id)

    async def list(
        self,
        user_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[Profile]:
        """
        列出学习画像

        Args:
            user_id: 用户 ID
            limit: 返回数量限制
            offset: 偏移量

        Returns:
            画像列表
        """
        # 查询记录
        filters = {"user_id": user_id}
        results = await self.repository.list(filters, limit, offset)

        # 转换为画像对象
        return [Profile(**result) for result in results]
