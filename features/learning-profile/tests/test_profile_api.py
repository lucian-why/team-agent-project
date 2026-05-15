"""
学习画像 API 测试
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient

from ..api.router import router
from ..domain.profile import (
    StudentProfile,
    LearningPath,
)


@pytest.fixture
def client():
    """创建测试客户端"""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


@pytest.fixture
def mock_auth():
    """模拟认证"""
    with patch("..api.router.AuthMiddleware") as mock:
        mock.get_current_user = AsyncMock(return_value={"sub": "user-1", "email": "test@example.com"})
        yield mock


@pytest.fixture
def mock_profile_service():
    """模拟画像服务"""
    with patch("..api.router.profile_service") as mock:
        yield mock


@pytest.fixture
def mock_learning_path_service():
    """模拟学习路径服务"""
    with patch("..api.router.learning_path_service") as mock:
        yield mock


class TestStudentProfileAPI:
    """学生画像 API 测试"""

    def test_get_profile_success(self, client, mock_auth, mock_profile_service):
        """测试成功获取画像"""
        mock_profile_service.get_profile = AsyncMock(return_value=StudentProfile(
            id="profile-123",
            notebook_id="nb-456",
            major="计算机科学",
            schema_version=1,
        ))

        response = client.get(
            "/learning/notebooks/nb-456/profile",
            headers={"Authorization": "Bearer test-token"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "profile-123"
        assert data["notebook_id"] == "nb-456"
        assert data["major"] == "计算机科学"

    def test_get_profile_not_found(self, client, mock_auth, mock_profile_service):
        """测试获取画像不存在"""
        from ..service.profile_service import NotFoundError
        mock_profile_service.get_profile = AsyncMock(side_effect=NotFoundError("Profile not found"))

        response = client.get(
            "/learning/notebooks/nb-456/profile",
            headers={"Authorization": "Bearer test-token"},
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_upsert_profile_success(self, client, mock_auth, mock_profile_service):
        """测试成功创建或更新画像"""
        mock_profile_service.upsert_profile = AsyncMock(return_value=StudentProfile(
            id="profile-123",
            notebook_id="nb-456",
            major="计算机科学",
            schema_version=1,
        ))

        response = client.put(
            "/learning/notebooks/nb-456/profile",
            json={
                "notebook_id": "nb-456",
                "major": "计算机科学",
            },
            headers={"Authorization": "Bearer test-token"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "profile-123"
        assert data["major"] == "计算机科学"

    def test_update_profile_success(self, client, mock_auth, mock_profile_service):
        """测试成功更新画像"""
        mock_profile_service.update_profile = AsyncMock(return_value=StudentProfile(
            id="profile-123",
            notebook_id="nb-456",
            major="数据科学",
            schema_version=1,
        ))

        response = client.patch(
            "/learning/notebooks/nb-456/profile",
            json={
                "major": "数据科学",
            },
            headers={"Authorization": "Bearer test-token"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["major"] == "数据科学"

    def test_update_profile_not_found(self, client, mock_auth, mock_profile_service):
        """测试更新画像不存在"""
        from ..service.profile_service import NotFoundError
        mock_profile_service.update_profile = AsyncMock(side_effect=NotFoundError("Profile not found"))

        response = client.patch(
            "/learning/notebooks/nb-456/profile",
            json={"major": "数据科学"},
            headers={"Authorization": "Bearer test-token"},
        )

        assert response.status_code == 404

    def test_delete_profile_success(self, client, mock_auth, mock_profile_service):
        """测试成功删除画像"""
        mock_profile_service.delete_profile = AsyncMock(return_value=True)

        response = client.delete(
            "/learning/notebooks/nb-456/profile",
            headers={"Authorization": "Bearer test-token"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Profile deleted successfully"

    def test_delete_profile_not_found(self, client, mock_auth, mock_profile_service):
        """测试删除画像不存在"""
        from ..service.profile_service import NotFoundError
        mock_profile_service.delete_profile = AsyncMock(side_effect=NotFoundError("Profile not found"))

        response = client.delete(
            "/learning/notebooks/nb-456/profile",
            headers={"Authorization": "Bearer test-token"},
        )

        assert response.status_code == 404


class TestLearningPathAPI:
    """学习路径 API 测试"""

    def test_get_learning_path_success(self, client, mock_auth, mock_learning_path_service):
        """测试成功获取学习路径"""
        mock_learning_path_service.get_path = AsyncMock(return_value=LearningPath(
            id="path-123",
            notebook_id="nb-456",
            title="Python 学习路径",
            nodes=[],
            status="draft",
            schema_version=1,
        ))

        response = client.get(
            "/learning/notebooks/nb-456/learning-path",
            headers={"Authorization": "Bearer test-token"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "path-123"
        assert data["title"] == "Python 学习路径"

    def test_get_learning_path_not_found(self, client, mock_auth, mock_learning_path_service):
        """测试获取学习路径不存在"""
        from ..service.profile_service import NotFoundError
        mock_learning_path_service.get_path = AsyncMock(side_effect=NotFoundError("Path not found"))

        response = client.get(
            "/learning/notebooks/nb-456/learning-path",
            headers={"Authorization": "Bearer test-token"},
        )

        assert response.status_code == 404

    def test_upsert_learning_path_success(self, client, mock_auth, mock_learning_path_service):
        """测试成功创建或更新学习路径"""
        mock_learning_path_service.upsert_path = AsyncMock(return_value=LearningPath(
            id="path-123",
            notebook_id="nb-456",
            title="Python 学习路径",
            nodes=[],
            status="draft",
            schema_version=1,
        ))

        response = client.put(
            "/learning/notebooks/nb-456/learning-path",
            json={
                "notebook_id": "nb-456",
                "title": "Python 学习路径",
            },
            headers={"Authorization": "Bearer test-token"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "path-123"
        assert data["title"] == "Python 学习路径"

    def test_update_learning_path_success(self, client, mock_auth, mock_learning_path_service):
        """测试成功更新学习路径"""
        mock_learning_path_service.update_path = AsyncMock(return_value=LearningPath(
            id="path-123",
            notebook_id="nb-456",
            title="更新后的路径",
            nodes=[],
            status="active",
            schema_version=1,
        ))

        response = client.patch(
            "/learning/notebooks/nb-456/learning-path",
            json={
                "title": "更新后的路径",
                "status": "active",
            },
            headers={"Authorization": "Bearer test-token"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "更新后的路径"
        assert data["status"] == "active"

    def test_update_learning_path_not_found(self, client, mock_auth, mock_learning_path_service):
        """测试更新学习路径不存在"""
        from ..service.profile_service import NotFoundError
        mock_learning_path_service.update_path = AsyncMock(side_effect=NotFoundError("Path not found"))

        response = client.patch(
            "/learning/notebooks/nb-456/learning-path",
            json={"title": "更新后的路径"},
            headers={"Authorization": "Bearer test-token"},
        )

        assert response.status_code == 404
