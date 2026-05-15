"""
聊天服务层

提供聊天会话的业务逻辑。
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from shared.database.repository import Repository
from ..domain.message import (
    ChatSession,
    ChatSessionCreate,
    ChatSessionUpdate,
    ChatMessage,
    ExecuteChatRequest,
    ExecuteChatResponse,
    BuildContextRequest,
    BuildContextResponse,
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


class ChatService:
    """聊天服务"""

    def __init__(self):
        self.repository = Repository("chat_session")

    async def get_sessions(
        self,
        notebook_id: str,
        owner_id: str = "",
        limit: int = 50,
        offset: int = 0,
    ) -> List[ChatSession]:
        """
        获取笔记本的聊天会话列表

        Args:
            notebook_id: 笔记本 ID
            owner_id: 所有者 ID
            limit: 返回数量限制
            offset: 偏移量

        Returns:
            会话列表
        """
        rows = await self.repository.list(
            filters={"notebook_id": notebook_id, "owner_id": owner_id},
            limit=limit,
            offset=offset,
        )
        return [ChatSession.model_validate(_normalize_record(row)) for row in rows]

    async def get_session(
        self,
        session_id: str,
        owner_id: str = "",
    ) -> ChatSession:
        """
        获取聊天会话

        Args:
            session_id: 会话 ID
            owner_id: 所有者 ID

        Returns:
            聊天会话

        Raises:
            NotFoundError: 会话不存在
        """
        row = await self.repository.get(session_id)
        if not row:
            raise NotFoundError(f"Chat session {session_id} not found")
        return ChatSession.model_validate(_normalize_record(row))

    async def create_session(
        self,
        notebook_id: str,
        request: ChatSessionCreate,
        owner_id: str = "",
    ) -> ChatSession:
        """
        创建聊天会话

        Args:
            notebook_id: 笔记本 ID
            request: 创建请求
            owner_id: 所有者 ID

        Returns:
            创建的会话
        """
        data = {
            "notebook_id": notebook_id,
            "title": request.title or f"Chat Session {_now_iso()}",
            "model_override": request.model_override,
            "owner_id": owner_id,
        }
        record = await self.repository.create(data)
        return ChatSession.model_validate(_normalize_record(record))

    async def update_session(
        self,
        session_id: str,
        request: ChatSessionUpdate,
        owner_id: str = "",
    ) -> ChatSession:
        """
        更新聊天会话

        Args:
            session_id: 会话 ID
            request: 更新请求
            owner_id: 所有者 ID

        Returns:
            更新后的会话

        Raises:
            NotFoundError: 会话不存在
        """
        # 验证会话存在且属于当前用户
        await self.get_session(session_id, owner_id)

        update_data = request.model_dump(exclude_unset=True)
        update_data["updated"] = _now_iso()

        result = await self.repository.update(session_id, update_data)
        record = result[0] if isinstance(result, list) else result
        return ChatSession.model_validate(_normalize_record(record))

    async def delete_session(
        self,
        session_id: str,
        owner_id: str = "",
    ) -> bool:
        """
        删除聊天会话

        Args:
            session_id: 会话 ID
            owner_id: 所有者 ID

        Returns:
            是否删除成功

        Raises:
            NotFoundError: 会话不存在
        """
        # 验证会话存在且属于当前用户
        await self.get_session(session_id, owner_id)
        return await self.repository.delete(session_id)


class NotFoundError(Exception):
    """资源不存在异常"""
    pass
