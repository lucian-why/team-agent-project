"""
聊天 API 路由

提供聊天会话的 CRUD 操作和聊天执行功能。
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional

from shared.auth.middleware import AuthMiddleware
from ..service.chat_service import ChatService, NotFoundError
from ..domain.message import (
    ChatSession,
    ChatSessionCreate,
    ChatSessionUpdate,
    ChatSessionWithMessages,
    ExecuteChatRequest,
    ExecuteChatResponse,
    BuildContextRequest,
    BuildContextResponse,
)

router = APIRouter(prefix="/chat", tags=["chat"])

# 依赖注入
chat_service = ChatService()


@router.get("/sessions", response_model=List[ChatSession])
async def get_sessions(
    notebook_id: str = Query(..., description="笔记本 ID"),
    limit: int = Query(50, ge=1, le=100, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    获取笔记本的聊天会话列表

    Args:
        notebook_id: 笔记本 ID
        limit: 返回数量限制
        offset: 偏移量
        current_user: 当前用户

    Returns:
        会话列表
    """
    try:
        sessions = await chat_service.get_sessions(
            notebook_id=notebook_id,
            owner_id=current_user.get("sub", ""),
            limit=limit,
            offset=offset,
        )
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sessions", response_model=ChatSession)
async def create_session(
    request: ChatSessionCreate,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    创建聊天会话

    Args:
        request: 创建请求
        current_user: 当前用户

    Returns:
        创建的会话
    """
    try:
        session = await chat_service.create_session(
            notebook_id=request.notebook_id,
            request=request,
            owner_id=current_user.get("sub", ""),
        )
        return session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sessions/{session_id}", response_model=ChatSessionWithMessages)
async def get_session(
    session_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    获取聊天会话详情

    Args:
        session_id: 会话 ID
        current_user: 当前用户

    Returns:
        会话详情（包含消息）
    """
    try:
        session = await chat_service.get_session(
            session_id=session_id,
            owner_id=current_user.get("sub", ""),
        )
        # TODO: 从 LangGraph 获取消息
        return ChatSessionWithMessages(
            **session.model_dump(),
            messages=[],
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/sessions/{session_id}", response_model=ChatSession)
async def update_session(
    session_id: str,
    request: ChatSessionUpdate,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    更新聊天会话

    Args:
        session_id: 会话 ID
        request: 更新请求
        current_user: 当前用户

    Returns:
        更新后的会话
    """
    try:
        session = await chat_service.update_session(
            session_id=session_id,
            request=request,
            owner_id=current_user.get("sub", ""),
        )
        return session
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    删除聊天会话

    Args:
        session_id: 会话 ID
        current_user: 当前用户

    Returns:
        删除结果
    """
    try:
        success = await chat_service.delete_session(
            session_id=session_id,
            owner_id=current_user.get("sub", ""),
        )
        if success:
            return {"message": "Session deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete session")
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute", response_model=ExecuteChatResponse)
async def execute_chat(
    request: ExecuteChatRequest,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    执行聊天请求

    Args:
        request: 聊天请求
        current_user: 当前用户

    Returns:
        聊天响应
    """
    # TODO: 实现聊天执行逻辑（调用 LangGraph）
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/stream")
async def stream_chat(
    request: ExecuteChatRequest,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    流式聊天响应

    Args:
        request: 聊天请求
        current_user: 当前用户

    Returns:
        SSE 流
    """
    # TODO: 实现流式聊天逻辑
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/context", response_model=BuildContextResponse)
async def build_context(
    request: BuildContextRequest,
    current_user: dict = Depends(AuthMiddleware.get_current_user),
):
    """
    构建聊天上下文

    Args:
        request: 上下文请求
        current_user: 当前用户

    Returns:
        构建的上下文
    """
    # TODO: 实现上下文构建逻辑
    raise HTTPException(status_code=501, detail="Not implemented yet")
