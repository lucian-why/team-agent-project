"""
聊天领域模型测试
"""

import pytest
from ..domain.message import (
    ChatMessage,
    ChatSessionBase,
    ChatSessionCreate,
    ChatSessionUpdate,
    ChatSession,
    ChatSessionWithMessages,
    ExecuteChatRequest,
    ExecuteChatResponse,
    BuildContextRequest,
    BuildContextResponse,
)


class TestChatMessage:
    """聊天消息模型测试"""

    def test_chat_message_create(self):
        """测试创建聊天消息"""
        message = ChatMessage(
            id="msg-1",
            type="human",
            content="Hello, how are you?",
            timestamp="2024-01-01T00:00:00",
            citations=[],
        )

        assert message.id == "msg-1"
        assert message.type == "human"
        assert message.content == "Hello, how are you?"
        assert message.citations == []

    def test_chat_message_with_citations(self):
        """测试带引用的聊天消息"""
        message = ChatMessage(
            id="msg-2",
            type="ai",
            content="Based on the source...",
            citations=[
                {"sourceId": "src-1", "content": "relevant text"},
            ],
        )

        assert len(message.citations) == 1
        assert message.citations[0]["sourceId"] == "src-1"


class TestChatSession:
    """聊天会话模型测试"""

    def test_chat_session_base_defaults(self):
        """测试基础模型默认值"""
        base = ChatSessionBase()

        assert base.title == "Untitled Session"
        assert base.model_override is None
        assert base.notebook_id is None

    def test_chat_session_create(self):
        """测试创建会话请求"""
        request = ChatSessionCreate(
            notebook_id="nb-123",
            title="My Chat",
            model_override="gpt-4",
        )

        assert request.notebook_id == "nb-123"
        assert request.title == "My Chat"
        assert request.model_override == "gpt-4"

    def test_chat_session_create_required_fields(self):
        """测试创建会话请求必填字段"""
        with pytest.raises(Exception):
            ChatSessionCreate()  # notebook_id 是必填的

    def test_chat_session_update_partial(self):
        """测试更新会话请求部分更新"""
        update = ChatSessionUpdate(title="New Title")

        assert update.title == "New Title"
        assert update.model_override is None

    def test_chat_session_complete(self):
        """测试完整会话模型"""
        session = ChatSession(
            id="session-123",
            title="My Chat",
            notebook_id="nb-456",
            model_override="gpt-4",
            owner_id="user-1",
            created="2024-01-01T00:00:00",
            updated="2024-01-02T00:00:00",
            message_count=10,
        )

        assert session.id == "session-123"
        assert session.owner_id == "user-1"
        assert session.message_count == 10

    def test_chat_session_with_messages(self):
        """测试带消息的会话模型"""
        messages = [
            ChatMessage(id="msg-1", type="human", content="Hello"),
            ChatMessage(id="msg-2", type="ai", content="Hi there!"),
        ]

        session = ChatSessionWithMessages(
            id="session-123",
            title="My Chat",
            notebook_id="nb-456",
            owner_id="user-1",
            messages=messages,
        )

        assert len(session.messages) == 2
        assert session.messages[0].type == "human"
        assert session.messages[1].type == "ai"


class TestExecuteChat:
    """聊天执行模型测试"""

    def test_execute_chat_request(self):
        """测试聊天执行请求"""
        request = ExecuteChatRequest(
            session_id="session-123",
            message="What is Python?",
            context={"sources": [], "notes": []},
            model_override="gpt-4",
            notebook_id="nb-456",
            assistant_id="assistant-789",
        )

        assert request.session_id == "session-123"
        assert request.message == "What is Python?"
        assert request.model_override == "gpt-4"

    def test_execute_chat_response(self):
        """测试聊天执行响应"""
        response = ExecuteChatResponse(
            session_id="session-123",
            messages=[
                ChatMessage(id="msg-1", type="human", content="Hello"),
                ChatMessage(id="msg-2", type="ai", content="Hi!"),
            ],
            agent_triggered=None,
        )

        assert response.session_id == "session-123"
        assert len(response.messages) == 2
        assert response.agent_triggered is None


class TestBuildContext:
    """构建上下文模型测试"""

    def test_build_context_request(self):
        """测试构建上下文请求"""
        request = BuildContextRequest(
            notebook_id="nb-123",
            context_config={
                "sources": {"src-1": "full content", "src-2": "not in"},
                "notes": {"note-1": "full content"},
            },
        )

        assert request.notebook_id == "nb-123"
        assert "sources" in request.context_config

    def test_build_context_response(self):
        """测试构建上下文响应"""
        response = BuildContextResponse(
            context={"sources": [], "notes": []},
            token_count=100,
            char_count=400,
        )

        assert response.token_count == 100
        assert response.char_count == 400
