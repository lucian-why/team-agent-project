"""
学习画像单元测试
"""

import pytest
from datetime import datetime

from ..domain.profile import Profile, ProfileCreate, ProfileUpdate


class TestProfile:
    """学习画像模型测试"""

    def test_profile_create(self):
        """测试创建画像请求模型"""
        data = ProfileCreate(
            name="Test Profile",
            description="Test description",
            learning_style="visual",
            interests=["math", "science"],
            goals=["learn python"]
        )

        assert data.name == "Test Profile"
        assert data.description == "Test description"
        assert data.learning_style == "visual"
        assert "math" in data.interests
        assert "learn python" in data.goals

    def test_profile_update(self):
        """测试更新画像请求模型"""
        data = ProfileUpdate(
            name="Updated Profile",
            interests=["math", "programming"]
        )

        assert data.name == "Updated Profile"
        assert data.interests == ["math", "programming"]
        assert data.description is None  # 未更新的字段为 None

    def test_profile_model(self):
        """测试完整画像模型"""
        now = datetime.utcnow()
        profile = Profile(
            id="profile-123",
            user_id="user-456",
            name="Test Profile",
            description="Test description",
            learning_style="visual",
            interests=["math", "science"],
            goals=["learn python"],
            metadata={"key": "value"},
            created_at=now,
            updated_at=now
        )

        assert profile.id == "profile-123"
        assert profile.user_id == "user-456"
        assert profile.name == "Test Profile"
        assert profile.created_at == now

    def test_profile_from_attributes(self):
        """测试从字典创建画像"""
        data = {
            "id": "profile-123",
            "user_id": "user-456",
            "name": "Test Profile",
            "description": "Test description",
            "learning_style": "visual",
            "interests": ["math", "science"],
            "goals": ["learn python"],
            "metadata": {"key": "value"},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        profile = Profile(**data)

        assert profile.id == data["id"]
        assert profile.name == data["name"]
        assert profile.interests == data["interests"]
