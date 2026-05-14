"""学习画像模块"""

from .domain.profile import Profile, ProfileCreate, ProfileUpdate
from .service.profile_service import ProfileService
from .api.router import router

__all__ = ["Profile", "ProfileCreate", "ProfileUpdate", "ProfileService", "router"]
