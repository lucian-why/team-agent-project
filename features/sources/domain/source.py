"""
资料源领域模型

定义资料源相关的数据结构。
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class Asset(BaseModel):
    """资源资产模型"""
    file_path: Optional[str] = Field(None, description="文件路径")
    url: Optional[str] = Field(None, description="URL 地址")


class SourceBase(BaseModel):
    """资料源基础模型"""
    title: str = Field(..., description="标题")
    topics: List[str] = Field(default_factory=list, description="主题标签")
    asset: Optional[Asset] = Field(None, description="资源资产")
    full_text: Optional[str] = Field(None, description="全文内容")


class SourceCreate(BaseModel):
    """创建资料源请求模型"""
    type: str = Field(..., description="类型 (link|upload|text)")
    notebook_id: Optional[str] = Field(None, description="笔记本 ID")
    notebooks: Optional[List[str]] = Field(None, description="笔记本 ID 列表")
    url: Optional[str] = Field(None, description="URL")
    content: Optional[str] = Field(None, description="文本内容")
    title: Optional[str] = Field(None, description="标题")
    file_path: Optional[str] = Field(None, description="文件路径")
    transformations: List[str] = Field(default_factory=list, description="转换 ID 列表")
    embed: bool = Field(False, description="是否嵌入")
    delete_source: bool = Field(False, description="是否删除源")
    async_processing: bool = Field(False, description="是否异步处理")


class SourceUpdate(BaseModel):
    """更新资料源请求模型"""
    title: Optional[str] = None
    topics: Optional[List[str]] = None


class Source(SourceBase):
    """资料源完整模型"""
    id: str = Field(..., description="资料源 ID")
    owner_id: str = Field(..., description="所有者 ID")
    embedded: bool = Field(False, description="是否已嵌入")
    embedded_chunks: int = Field(0, description="嵌入块数量")
    file_available: Optional[bool] = Field(None, description="文件是否可用")
    created: Optional[str] = Field(None, description="创建时间")
    updated: Optional[str] = Field(None, description="更新时间")
    command_id: Optional[str] = Field(None, description="处理命令 ID")
    status: Optional[str] = Field(None, description="处理状态")
    processing_info: Optional[Dict[str, Any]] = Field(None, description="处理信息")
    notebooks: List[str] = Field(default_factory=list, description="关联的笔记本 ID")
    insights_count: int = Field(0, description="洞察数量")

    class Config:
        from_attributes = True


class SourceList(BaseModel):
    """资料源列表项模型"""
    id: str = Field(..., description="资料源 ID")
    title: Optional[str] = Field(None, description="标题")
    topics: List[str] = Field(default_factory=list, description="主题标签")
    asset: Optional[Asset] = Field(None, description="资源资产")
    embedded: bool = Field(False, description="是否已嵌入")
    embedded_chunks: int = Field(0, description="嵌入块数量")
    insights_count: int = Field(0, description="洞察数量")
    created: Optional[str] = Field(None, description="创建时间")
    updated: Optional[str] = Field(None, description="更新时间")
    command_id: Optional[str] = Field(None, description="处理命令 ID")
    status: Optional[str] = Field(None, description="处理状态")
    processing_info: Optional[Dict[str, Any]] = Field(None, description="处理信息")

    class Config:
        from_attributes = True


class SourceInsight(BaseModel):
    """资料源洞察模型"""
    id: str = Field(..., description="洞察 ID")
    source_id: str = Field(..., description="资料源 ID")
    insight_type: str = Field(..., description="洞察类型")
    content: str = Field(..., description="内容")
    created: Optional[str] = Field(None, description="创建时间")
    updated: Optional[str] = Field(None, description="更新时间")


class CreateInsightRequest(BaseModel):
    """创建洞察请求模型"""
    transformation_id: str = Field(..., description="转换 ID")


class InsightCreationResponse(BaseModel):
    """洞察创建响应模型"""
    status: str = Field("pending", description="状态")
    message: str = Field(..., description="消息")
    source_id: str = Field(..., description="资料源 ID")
    transformation_id: str = Field(..., description="转换 ID")
    command_id: Optional[str] = Field(None, description="命令 ID")


class SourceStatusResponse(BaseModel):
    """资料源状态响应模型"""
    status: Optional[str] = Field(None, description="状态")
    message: Optional[str] = Field(None, description="消息")
    processing_info: Optional[Dict[str, Any]] = Field(None, description="处理信息")
    command_id: Optional[str] = Field(None, description="命令 ID")
