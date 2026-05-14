"""
AI 对话 API 路由

提供 AI 对话功能。
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel

from shared.auth.middleware import AuthMiddleware, User
from ..service.chat_service import ChatService
from ..domain.message import Message, MessageCreate

router = APIRouter(prefix="/chat", tags=["chat"])

# 依赖注入
chat_service = ChatService()


@router.post("/messages", response_model=Message)
async def create_message(
    data: MessageCreate,
    current_user: User = Depends(AuthMiddleware.get_current_user)
):
    """
    发送消息并获取 AI 回复

    Args:
        data: 消息数据
        current_user: 当前用户

    Returns:
        AI 回复消息
    """
    try:
        message = await chat_service.create_message(data, current_user.id)
        return message
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/messages", response_model=List[Message])
async def list_messages(
    conversation_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    current_user: User = Depends(AuthMiddleware.get_current_user)
):
    """
    列出消息

    Args:
        conversation_id: 会话 ID（可选）
        limit: 返回数量限制
        offset: 偏移量
        current_user: 当前用户

    Returns:
        消息列表
    """
    messages = await chat_service.list_messages(
        current_user.id,
        conversation_id,
        limit,
        offset
    )
    return messages
