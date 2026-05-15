"""
聊天领域模型

定义聊天相关的数据结构。
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """聊天消息模型"""
    id: str = Field(..., description="消息 ID")
    type: str = Field(..., description="消息类型 (human|ai)")
    content: str = Field(..., description="消息内容")
    timestamp: Optional[str] = Field(None, description="消息时间戳")
    citations: List[Dict[str, Any]] = Field(
        default_factory=list, description="引用的来源"
    )


class ChatSessionBase(BaseModel):
    """聊天会话基础模型"""
    title: str = Field("Untitled Session", description="会话标题")
    model_override: Optional[str] = Field(None, description="模型覆盖")
    notebook_id: Optional[str] = Field(None, description="关联的笔记本 ID")


class ChatSessionCreate(ChatSessionBase):
    """创建聊天会话请求模型"""
    notebook_id: str = Field(..., description="笔记本 ID")


class ChatSessionUpdate(BaseModel):
    """更新聊天会话请求模型"""
    title: Optional[str] = None
    model_override: Optional[str] = None


class ChatSession(ChatSessionBase):
    """聊天会话完整模型"""
    id: str = Field(..., description="会话 ID")
    owner_id: str = Field(..., description="所有者 ID")
    created: Optional[str] = Field(None, description="创建时间")
    updated: Optional[str] = Field(None, description="更新时间")
    message_count: Optional[int] = Field(None, description="消息数量")

    class Config:
        from_attributes = True


class ChatSessionWithMessages(ChatSession):
    """带消息的聊天会话模型"""
    messages: List[ChatMessage] = Field(default_factory=list, description="会话消息")


class ExecuteChatRequest(BaseModel):
    """执行聊天请求模型"""
    session_id: str = Field(..., description="会话 ID")
    message: str = Field(..., description="用户消息")
    context: Dict[str, Any] = Field(..., description="上下文（sources 和 notes）")
    model_override: Optional[str] = Field(None, description="模型覆盖")
    notebook_id: Optional[str] = Field(None, description="笔记本 ID")
    assistant_id: Optional[str] = Field(None, description="自定义助手 ID")


class ExecuteChatResponse(BaseModel):
    """执行聊天响应模型"""
    session_id: str = Field(..., description="会话 ID")
    messages: List[ChatMessage] = Field(..., description="更新后的消息列表")
    agent_triggered: Optional[Dict[str, Any]] = Field(
        None, description="触发的 agent 信息"
    )


class BuildContextRequest(BaseModel):
    """构建上下文请求模型"""
    notebook_id: str = Field(..., description="笔记本 ID")
    context_config: Dict[str, Any] = Field(..., description="上下文配置")


class BuildContextResponse(BaseModel):
    """构建上下文响应模型"""
    context: Dict[str, Any] = Field(..., description="构建的上下文数据")
    token_count: int = Field(..., description="预估 token 数量")
    char_count: int = Field(..., description="字符数量")
