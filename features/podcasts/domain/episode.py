"""
播客领域模型

定义播客相关的数据结构。
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PodcastEpisodeBase(BaseModel):
    """播客剧集基础模型"""
    name: str = Field(..., description="剧集名称")
    episode_profile: Dict[str, Any] = Field(default_factory=dict, description="剧集配置")
    speaker_profile: Dict[str, Any] = Field(default_factory=dict, description=" speaker 配置")
    briefing: str = Field("", description="简介")
    content: Optional[str] = Field(None, description="内容")


class PodcastEpisodeCreate(PodcastEpisodeBase):
    """创建播客剧集请求模型"""
    notebook_id: Optional[str] = Field(None, description="笔记本 ID")
    episode_profile_name: Optional[str] = Field(None, description="剧集配置名称")
    speaker_profile_name: Optional[str] = Field(None, description="speaker 配置名称")
    briefing_suffix: Optional[str] = Field(None, description="简介后缀")


class PodcastEpisode(PodcastEpisodeBase):
    """播客剧集完整模型"""
    id: str = Field(..., description="剧集 ID")
    audio_file: Optional[str] = Field(None, description="音频文件路径")
    audio_url: Optional[str] = Field(None, description="音频 URL")
    transcript: Optional[Dict[str, Any]] = Field(None, description="转录文本")
    outline: Optional[Dict[str, Any]] = Field(None, description="大纲")
    created: Optional[str] = Field(None, description="创建时间")
    job_status: Optional[str] = Field(None, description="任务状态")
    error_message: Optional[str] = Field(None, description="错误消息")
    command_id: Optional[str] = Field(None, description="命令 ID")

    class Config:
        from_attributes = True


class PodcastGenerationRequest(BaseModel):
    """播客生成请求模型"""
    episode_profile: str = Field(..., description="剧集配置名称")
    speaker_profile: str = Field(..., description="speaker 配置名称")
    episode_name: str = Field(..., description="剧集名称")
    notebook_id: Optional[str] = Field(None, description="笔记本 ID")
    content: Optional[str] = Field(None, description="内容")
    briefing_suffix: Optional[str] = Field(None, description="简介后缀")


class PodcastGenerationResponse(BaseModel):
    """播客生成响应模型"""
    job_id: str = Field(..., description="任务 ID")
    status: str = Field("submitted", description="状态")
    message: str = Field(..., description="消息")
    episode_profile: str = Field(..., description="剧集配置")
    episode_name: str = Field(..., description="剧集名称")


class PodcastJobStatus(BaseModel):
    """播客任务状态模型"""
    job_id: str = Field(..., description="任务 ID")
    status: str = Field(..., description="状态")
    message: Optional[str] = Field(None, description="消息")
    error_message: Optional[str] = Field(None, description="错误消息")
    started_at: Optional[str] = Field(None, description="开始时间")
    completed_at: Optional[str] = Field(None, description="完成时间")
