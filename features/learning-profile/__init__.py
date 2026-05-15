"""学习画像模块"""

from .domain.profile import (
    StudentProfile,
    StudentProfileCreate,
    StudentProfileUpdate,
    LearningPath,
    LearningPathCreate,
    LearningPathUpdate,
)
from .service.profile_service import ProfileService, LearningPathService
from .api.router import router

__all__ = [
    "StudentProfile",
    "StudentProfileCreate",
    "StudentProfileUpdate",
    "LearningPath",
    "LearningPathCreate",
    "LearningPathUpdate",
    "ProfileService",
    "LearningPathService",
    "router",
]
