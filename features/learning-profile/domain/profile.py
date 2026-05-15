"""
学习画像领域模型

定义学习画像的数据结构，从现有项目迁移并重构。
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class WrongQuestion(BaseModel):
    """错题模型"""
    id: str
    question: str
    user_answer: str
    correct_answer: str
    mistake_type: str
    source_label: str


class WrongQuestionGroup(BaseModel):
    """错题分组模型"""
    notebook_id: str
    notebook_name: str
    source_count: int
    wrong_questions: List[WrongQuestion] = Field(default_factory=list)
    frequent_mistakes: List[str] = Field(default_factory=list)
    quiz_href: str = ""


class StudentProfileBase(BaseModel):
    """学生画像基础模型"""
    major: Optional[str] = Field(None, description="专业")
    course: Optional[str] = Field(None, description="课程")
    learning_goal: Optional[str] = Field(None, description="学习目标")
    knowledge_level: Optional[str] = Field(None, description="知识水平")
    cognitive_style: Optional[str] = Field(None, description="认知风格")
    weak_points: List[str] = Field(default_factory=list, description="薄弱点")
    interest_tags: List[str] = Field(default_factory=list, description="兴趣标签")
    practice_preference: Optional[str] = Field(None, description="练习偏好")
    pace_preference: Optional[str] = Field(None, description="进度偏好")
    resource_preference: Optional[str] = Field(None, description="资源偏好")
    confidence: float = Field(0.0, description="置信度")
    evidence_summary: Optional[str] = Field(None, description="证据摘要")
    source_ids: List[str] = Field(default_factory=list, description="来源 ID 列表")
    created_by: str = Field("user", description="创建者")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class StudentProfileCreate(StudentProfileBase):
    """创建学生画像请求模型"""
    notebook_id: str = Field(..., description="笔记本 ID")


class StudentProfileUpdate(BaseModel):
    """更新学生画像请求模型"""
    major: Optional[str] = None
    course: Optional[str] = None
    learning_goal: Optional[str] = None
    knowledge_level: Optional[str] = None
    cognitive_style: Optional[str] = None
    weak_points: Optional[List[str]] = None
    interest_tags: Optional[List[str]] = None
    practice_preference: Optional[str] = None
    pace_preference: Optional[str] = None
    resource_preference: Optional[str] = None
    confidence: Optional[float] = None
    evidence_summary: Optional[str] = None
    source_ids: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class StudentProfile(StudentProfileBase):
    """学生画像完整模型"""
    id: str = Field(..., description="画像 ID")
    notebook_id: str = Field(..., description="笔记本 ID")
    schema_version: int = Field(1, description="模式版本")
    created: Optional[str] = Field(None, description="创建时间")
    updated: Optional[str] = Field(None, description="更新时间")

    class Config:
        from_attributes = True


class LearningPathNode(BaseModel):
    """学习路径节点"""
    id: str
    title: str
    description: str = ""
    learning_objectives: List[str] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)
    recommended_source_ids: List[str] = Field(default_factory=list)
    recommended_resource_types: List[str] = Field(default_factory=list)
    estimated_minutes: int = 30
    status: str = "todo"
    mastery_score: float = 0.0


class LearningPathBase(BaseModel):
    """学习路径基础模型"""
    profile_id: Optional[str] = Field(None, description="关联的画像 ID")
    title: str = Field("学习路径", description="路径标题")
    course: str = Field("", description="课程名称")
    nodes: List[LearningPathNode] = Field(default_factory=list, description="路径节点")
    current_node_id: Optional[str] = Field(None, description="当前节点 ID")
    status: str = Field("draft", description="状态")
    source_ids: List[str] = Field(default_factory=list, description="来源 ID 列表")
    created_by: str = Field("user", description="创建者")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class LearningPathCreate(LearningPathBase):
    """创建学习路径请求模型"""
    notebook_id: str = Field(..., description="笔记本 ID")


class LearningPathUpdate(BaseModel):
    """更新学习路径请求模型"""
    profile_id: Optional[str] = None
    title: Optional[str] = None
    course: Optional[str] = None
    nodes: Optional[List[LearningPathNode]] = None
    current_node_id: Optional[str] = None
    status: Optional[str] = None
    source_ids: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class LearningPath(LearningPathBase):
    """学习路径完整模型"""
    id: str = Field(..., description="路径 ID")
    notebook_id: str = Field(..., description="笔记本 ID")
    schema_version: int = Field(1, description="模式版本")
    created: Optional[str] = Field(None, description="创建时间")
    updated: Optional[str] = Field(None, description="更新时间")

    class Config:
        from_attributes = True
