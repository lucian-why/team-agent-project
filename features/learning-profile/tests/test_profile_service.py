"""
学习画像服务层测试
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from ..service.profile_service import (
    ProfileService,
    LearningPathService,
    NotFoundError,
    _now_iso,
    _normalize_record,
    _with_defaults,
)
from ..domain.profile import (
    StudentProfileCreate,
    StudentProfileUpdate,
    LearningPathCreate,
    LearningPathUpdate,
)


class TestHelperFunctions:
    """辅助函数测试"""

    def test_now_iso(self):
        """测试获取当前时间 ISO 格式"""
        result = _now_iso()
        assert isinstance(result, str)
        assert "T" in result
        assert "+" in result or "Z" in result or result.count("-") >= 2

    def test_normalize_record_with_created_at(self):
        """测试标准化记录（created_at -> created）"""
        record = {
            "id": "123",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-02T00:00:00",
        }
        result = _normalize_record(record)

        assert "created_at" not in result
        assert "updated_at" not in result
        assert result["created"] == "2024-01-01T00:00:00"
        assert result["updated"] == "2024-01-02T00:00:00"

    def test_normalize_record_with_created(self):
        """测试标准化记录（已有 created 字段）"""
        record = {
            "id": "123",
            "created": "2024-01-01T00:00:00",
            "updated": "2024-01-02T00:00:00",
        }
        result = _normalize_record(record)

        assert result["created"] == "2024-01-01T00:00:00"
        assert result["updated"] == "2024-01-02T00:00:00"

    def test_normalize_record_none_values(self):
        """测试标准化记录（None 值）"""
        record = {
            "id": "123",
            "created": None,
            "updated": None,
        }
        result = _normalize_record(record)

        assert result["created"] is None
        assert result["updated"] is None

    def test_with_defaults(self):
        """测试添加默认值"""
        notebook_id = "nb-123"
        payload = {"major": "计算机科学"}
        result = _with_defaults(notebook_id, payload)

        assert result["notebook_id"] == notebook_id
        assert result["schema_version"] == 1
        assert result["source_ids"] == []
        assert result["created_by"] == "user"
        assert result["metadata"] == {}
        assert result["major"] == "计算机科学"

    def test_with_defaults_override(self):
        """测试默认值可被覆盖"""
        notebook_id = "nb-123"
        payload = {
            "schema_version": 2,
            "created_by": "ai",
            "major": "数据科学",
        }
        result = _with_defaults(notebook_id, payload)

        assert result["schema_version"] == 2
        assert result["created_by"] == "ai"
        assert result["major"] == "数据科学"


class TestProfileService:
    """学生画像服务测试"""

    @pytest.fixture
    def mock_repository(self):
        """模拟 Repository"""
        with patch("..service.profile_service.Repository") as mock:
            repo = AsyncMock()
            mock.return_value = repo
            yield repo

    @pytest.fixture
    def service(self, mock_repository):
        """创建服务实例"""
        return ProfileService()

    @pytest.mark.asyncio
    async def test_get_profile_success(self, service, mock_repository):
        """测试成功获取画像"""
        mock_repository.list.return_value = [
            {
                "id": "profile-123",
                "notebook_id": "nb-456",
                "major": "计算机科学",
                "schema_version": 1,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-02T00:00:00",
            }
        ]

        result = await service.get_profile("nb-456", owner_id="user-1")

        assert result.id == "profile-123"
        assert result.notebook_id == "nb-456"
        assert result.major == "计算机科学"
        mock_repository.list.assert_called_once_with(
            filters={"notebook_id": "nb-456"},
            limit=1,
        )

    @pytest.mark.asyncio
    async def test_get_profile_not_found(self, service, mock_repository):
        """测试获取画像不存在"""
        mock_repository.list.return_value = []

        with pytest.raises(NotFoundError) as exc_info:
            await service.get_profile("nb-456", owner_id="user-1")

        assert "nb-456" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_upsert_profile_create(self, service, mock_repository):
        """测试创建画像（upsert）"""
        mock_repository.list.return_value = []  # 不存在
        mock_repository.create.return_value = {
            "id": "profile-123",
            "notebook_id": "nb-456",
            "major": "计算机科学",
            "schema_version": 1,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-02T00:00:00",
        }

        request = StudentProfileCreate(
            notebook_id="nb-456",
            major="计算机科学",
        )

        result = await service.upsert_profile("nb-456", request, owner_id="user-1")

        assert result.id == "profile-123"
        mock_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_upsert_profile_update(self, service, mock_repository):
        """测试更新画像（upsert）"""
        mock_repository.list.return_value = [
            {"id": "profile-123", "notebook_id": "nb-456"}
        ]
        mock_repository.update.return_value = {
            "id": "profile-123",
            "notebook_id": "nb-456",
            "major": "数据科学",
            "schema_version": 1,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-02T00:00:00",
        }

        request = StudentProfileCreate(
            notebook_id="nb-456",
            major="数据科学",
        )

        result = await service.upsert_profile("nb-456", request, owner_id="user-1")

        assert result.major == "数据科学"
        mock_repository.update.assert_called_once_with("profile-123", request.model_dump(exclude_unset=True))

    @pytest.mark.asyncio
    async def test_update_profile_success(self, service, mock_repository):
        """测试成功更新画像"""
        mock_repository.list.return_value = [
            {"id": "profile-123", "notebook_id": "nb-456"}
        ]
        mock_repository.update.return_value = {
            "id": "profile-123",
            "notebook_id": "nb-456",
            "major": "数据科学",
            "schema_version": 1,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-02T00:00:00",
        }

        request = StudentProfileUpdate(major="数据科学")

        result = await service.update_profile("nb-456", request, owner_id="user-1")

        assert result.major == "数据科学"

    @pytest.mark.asyncio
    async def test_update_profile_not_found(self, service, mock_repository):
        """测试更新画像不存在"""
        mock_repository.list.return_value = []

        request = StudentProfileUpdate(major="数据科学")

        with pytest.raises(NotFoundError):
            await service.update_profile("nb-456", request, owner_id="user-1")

    @pytest.mark.asyncio
    async def test_delete_profile_success(self, service, mock_repository):
        """测试成功删除画像"""
        mock_repository.list.return_value = [
            {"id": "profile-123", "notebook_id": "nb-456"}
        ]
        mock_repository.delete.return_value = True

        result = await service.delete_profile("nb-456", owner_id="user-1")

        assert result is True
        mock_repository.delete.assert_called_once_with("profile-123")

    @pytest.mark.asyncio
    async def test_delete_profile_not_found(self, service, mock_repository):
        """测试删除画像不存在"""
        mock_repository.list.return_value = []

        with pytest.raises(NotFoundError):
            await service.delete_profile("nb-456", owner_id="user-1")


class TestLearningPathService:
    """学习路径服务测试"""

    @pytest.fixture
    def mock_repository(self):
        """模拟 Repository"""
        with patch("..service.profile_service.Repository") as mock:
            repo = AsyncMock()
            mock.return_value = repo
            yield repo

    @pytest.fixture
    def service(self, mock_repository):
        """创建服务实例"""
        return LearningPathService()

    @pytest.mark.asyncio
    async def test_get_path_success(self, service, mock_repository):
        """测试成功获取学习路径"""
        mock_repository.list.return_value = [
            {
                "id": "path-123",
                "notebook_id": "nb-456",
                "title": "Python 学习路径",
                "nodes": [],
                "status": "draft",
                "schema_version": 1,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-02T00:00:00",
            }
        ]

        result = await service.get_path("nb-456", owner_id="user-1")

        assert result.id == "path-123"
        assert result.notebook_id == "nb-456"
        assert result.title == "Python 学习路径"

    @pytest.mark.asyncio
    async def test_get_path_not_found(self, service, mock_repository):
        """测试获取学习路径不存在"""
        mock_repository.list.return_value = []

        with pytest.raises(NotFoundError) as exc_info:
            await service.get_path("nb-456", owner_id="user-1")

        assert "nb-456" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_upsert_path_create(self, service, mock_repository):
        """测试创建学习路径（upsert）"""
        mock_repository.list.return_value = []  # 不存在
        mock_repository.create.return_value = {
            "id": "path-123",
            "notebook_id": "nb-456",
            "title": "Python 学习路径",
            "nodes": [],
            "status": "draft",
            "schema_version": 1,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-02T00:00:00",
        }

        request = LearningPathCreate(
            notebook_id="nb-456",
            title="Python 学习路径",
        )

        result = await service.upsert_path("nb-456", request, owner_id="user-1")

        assert result.id == "path-123"
        mock_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_upsert_path_update(self, service, mock_repository):
        """测试更新学习路径（upsert）"""
        mock_repository.list.return_value = [
            {"id": "path-123", "notebook_id": "nb-456"}
        ]
        mock_repository.update.return_value = {
            "id": "path-123",
            "notebook_id": "nb-456",
            "title": "更新后的路径",
            "nodes": [],
            "status": "active",
            "schema_version": 1,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-02T00:00:00",
        }

        request = LearningPathCreate(
            notebook_id="nb-456",
            title="更新后的路径",
        )

        result = await service.upsert_path("nb-456", request, owner_id="user-1")

        assert result.title == "更新后的路径"
        mock_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_path_success(self, service, mock_repository):
        """测试成功更新学习路径"""
        mock_repository.list.return_value = [
            {"id": "path-123", "notebook_id": "nb-456"}
        ]
        mock_repository.update.return_value = {
            "id": "path-123",
            "notebook_id": "nb-456",
            "title": "更新后的路径",
            "nodes": [],
            "status": "active",
            "schema_version": 1,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-02T00:00:00",
        }

        request = LearningPathUpdate(title="更新后的路径")

        result = await service.update_path("nb-456", request, owner_id="user-1")

        assert result.title == "更新后的路径"

    @pytest.mark.asyncio
    async def test_update_path_not_found(self, service, mock_repository):
        """测试更新学习路径不存在"""
        mock_repository.list.return_value = []

        request = LearningPathUpdate(title="更新后的路径")

        with pytest.raises(NotFoundError):
            await service.update_path("nb-456", request, owner_id="user-1")
