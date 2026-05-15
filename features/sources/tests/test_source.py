"""
资料源领域模型测试
"""

import pytest
from ..domain.source import (
    Asset,
    SourceBase,
    SourceCreate,
    SourceUpdate,
    Source,
    SourceList,
    SourceInsight,
    CreateInsightRequest,
    InsightCreationResponse,
    SourceStatusResponse,
)


class TestAsset:
    """资源资产模型测试"""

    def test_asset_with_file_path(self):
        """测试文件路径资产"""
        asset = Asset(file_path="/uploads/test.pdf")

        assert asset.file_path == "/uploads/test.pdf"
        assert asset.url is None

    def test_asset_with_url(self):
        """测试 URL 资产"""
        asset = Asset(url="https://example.com/article")

        assert asset.url == "https://example.com/article"
        assert asset.file_path is None


class TestSource:
    """资料源模型测试"""

    def test_source_base_defaults(self):
        """测试基础模型默认值"""
        base = SourceBase(title="Test Source")

        assert base.title == "Test Source"
        assert base.topics == []
        assert base.asset is None
        assert base.full_text is None

    def test_source_create_link(self):
        """测试创建链接类型资料源"""
        request = SourceCreate(
            type="link",
            url="https://example.com",
            title="Example Article",
        )

        assert request.type == "link"
        assert request.url == "https://example.com"
        assert request.embed is False

    def test_source_create_upload(self):
        """测试创建上传类型资料源"""
        request = SourceCreate(
            type="upload",
            title="My PDF",
        )

        assert request.type == "upload"
        assert request.async_processing is False

    def test_source_create_text(self):
        """测试创建文本类型资料源"""
        request = SourceCreate(
            type="text",
            content="This is the content.",
            title="My Notes",
        )

        assert request.type == "text"
        assert request.content == "This is the content."

    def test_source_update_partial(self):
        """测试更新资料源部分更新"""
        update = SourceUpdate(title="New Title")

        assert update.title == "New Title"
        assert update.topics is None

    def test_source_complete(self):
        """测试完整资料源模型"""
        source = Source(
            id="source-123",
            title="Test Source",
            topics=["AI", "ML"],
            asset=Asset(url="https://example.com"),
            full_text="Full text content",
            owner_id="user-1",
            embedded=True,
            embedded_chunks=10,
            file_available=True,
            created="2024-01-01T00:00:00",
            updated="2024-01-02T00:00:00",
            command_id="cmd-123",
            status="completed",
            notebooks=["nb-1", "nb-2"],
            insights_count=5,
        )

        assert source.id == "source-123"
        assert source.embedded is True
        assert source.embedded_chunks == 10
        assert len(source.notebooks) == 2

    def test_source_list_item(self):
        """测试资料源列表项模型"""
        item = SourceList(
            id="source-123",
            title="Test Source",
            topics=["AI"],
            embedded=False,
            embedded_chunks=0,
            insights_count=0,
        )

        assert item.id == "source-123"
        assert item.status is None


class TestSourceInsight:
    """资料源洞察模型测试"""

    def test_source_insight_create(self):
        """测试创建洞察"""
        insight = SourceInsight(
            id="insight-123",
            source_id="source-456",
            insight_type="summary",
            content="This is a summary.",
            created="2024-01-01T00:00:00",
            updated="2024-01-02T00:00:00",
        )

        assert insight.id == "insight-123"
        assert insight.source_id == "source-456"
        assert insight.insight_type == "summary"

    def test_create_insight_request(self):
        """测试创建洞察请求"""
        request = CreateInsightRequest(transformation_id="trans-123")

        assert request.transformation_id == "trans-123"

    def test_insight_creation_response(self):
        """测试洞察创建响应"""
        response = InsightCreationResponse(
            status="pending",
            message="Insight generation started",
            source_id="source-123",
            transformation_id="trans-456",
            command_id="cmd-789",
        )

        assert response.status == "pending"
        assert response.command_id == "cmd-789"


class TestSourceStatus:
    """资料源状态模型测试"""

    def test_source_status_response(self):
        """测试状态响应"""
        response = SourceStatusResponse(
            status="completed",
            message="Processing completed",
            processing_info={"started_at": "2024-01-01", "completed_at": "2024-01-02"},
            command_id="cmd-123",
        )

        assert response.status == "completed"
        assert response.command_id == "cmd-123"
        assert response.processing_info is not None
