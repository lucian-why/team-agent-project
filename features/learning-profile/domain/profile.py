"""
学习画像领域模型

定义学习画像的数据结构。
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ProfileBase(BaseModel):
    """学习画像基础模型"""

    name: str = Field(..., description="画像名称")
    description: Optional[str] = Field(None, description="画像描述")
    learning_style: Optional[str] = Field(None, description="学习风格")
    interests: List[str] = Field(default_factory=list, description="兴趣领域")
    goals: List[str] = Field(default_factory=list, description="学习目标")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class ProfileCreate(ProfileBase):
    """创建学习画像请求模型"""
    pass


class ProfileUpdate(BaseModel):
    """更新学习画像请求模型"""

    name: Optional[str] = Field(None, description="画像名称")
    description: Optional[str] = Field(None, description="画像描述")
    learning_style: Optional[str] = Field(None, description="学习风格")
    interests: Optional[List[str]] = Field(None, description="兴趣领域")
    goals: Optional[List[str]] = Field(None, description="学习目标")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")


class Profile(ProfileBase):
    """学习画像完整模型"""

    id: str = Field(..., description="画像 ID")
    user_id: str = Field(..., description="用户 ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class ProfileSummary(BaseModel):
    """学习画像摘要"""

    id: str
    name: str
    learning_style: Optional[str]
    interests: List[str]
    created_at: datetime
