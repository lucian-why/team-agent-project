"""
播客服务层

提供播客的业务逻辑。
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from shared.database.repository import Repository
from ..domain.episode import (
    PodcastEpisode,
    PodcastEpisodeCreate,
    PodcastGenerationRequest,
    PodcastGenerationResponse,
    PodcastJobStatus,
)


def _now_iso() -> str:
    """获取当前时间的 ISO 格式字符串"""
    return datetime.now(timezone.utc).isoformat()


def _normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """标准化记录格式"""
    normalized = dict(record)
    if "created_at" in normalized and "created" not in normalized:
        normalized["created"] = normalized.pop("created_at")
    if "updated_at" in normalized and "updated" not in normalized:
        normalized["updated"] = normalized.pop("updated_at")
    if normalized.get("created") is not None:
        normalized["created"] = str(normalized["created"])
    if normalized.get("updated") is not None:
        normalized["updated"] = str(normalized["updated"])
    return normalized


class PodcastService:
    """播客服务"""

    def __init__(self):
        self.repository = Repository("podcast_episode")

    async def get_episodes(
        self,
        owner_id: str = "",
        limit: int = 50,
        offset: int = 0,
    ) -> List[PodcastEpisode]:
        """
        获取播客剧集列表

        Args:
            owner_id: 所有者 ID
            limit: 返回数量限制
            offset: 偏移量

        Returns:
            剧集列表
        """
        rows = await self.repository.list(
            filters={"owner_id": owner_id},
            limit=limit,
            offset=offset,
        )
        return [PodcastEpisode.model_validate(_normalize_record(row)) for row in rows]

    async def get_episode(
        self,
        episode_id: str,
        owner_id: str = "",
    ) -> PodcastEpisode:
        """
        获取播客剧集详情

        Args:
            episode_id: 剧集 ID
            owner_id: 所有者 ID

        Returns:
            剧集详情

        Raises:
            NotFoundError: 剧集不存在
        """
        row = await self.repository.get(episode_id)
        if not row:
            raise NotFoundError(f"Podcast episode {episode_id} not found")
        return PodcastEpisode.model_validate(_normalize_record(row))

    async def delete_episode(
        self,
        episode_id: str,
        owner_id: str = "",
    ) -> bool:
        """
        删除播客剧集

        Args:
            episode_id: 剧集 ID
            owner_id: 所有者 ID

        Returns:
            是否删除成功

        Raises:
            NotFoundError: 剧集不存在
        """
        # 验证剧集存在
        await self.get_episode(episode_id, owner_id)
        return await self.repository.delete(episode_id)

    async def submit_generation_job(
        self,
        request: PodcastGenerationRequest,
        owner_id: str = "",
    ) -> PodcastGenerationResponse:
        """
        提交播客生成任务

        Args:
            request: 生成请求
            owner_id: 所有者 ID

        Returns:
            生成响应
        """
        # TODO: 实现任务提交逻辑
        job_id = f"job_{_now_iso()}"
        return PodcastGenerationResponse(
            job_id=job_id,
            status="submitted",
            message=f"Podcast generation started for episode '{request.episode_name}'",
            episode_profile=request.episode_profile,
            episode_name=request.episode_name,
        )

    async def get_job_status(
        self,
        job_id: str,
    ) -> PodcastJobStatus:
        """
        获取任务状态

        Args:
            job_id: 任务 ID

        Returns:
            任务状态
        """
        # TODO: 实现获取任务状态逻辑
        return PodcastJobStatus(
            job_id=job_id,
            status="unknown",
            message="Job status not available",
        )

    async def retry_episode(
        self,
        episode_id: str,
        owner_id: str = "",
    ) -> PodcastGenerationResponse:
        """
        重试播客剧集

        Args:
            episode_id: 剧集 ID
            owner_id: 所有者 ID

        Returns:
            生成响应

        Raises:
            NotFoundError: 剧集不存在
        """
        episode = await self.get_episode(episode_id, owner_id)

        # TODO: 实现重试逻辑
        job_id = f"job_{_now_iso()}"
        return PodcastGenerationResponse(
            job_id=job_id,
            status="submitted",
            message=f"Retry submitted for episode '{episode.name}'",
            episode_profile=episode.episode_profile.get("name", ""),
            episode_name=episode.name,
        )


class NotFoundError(Exception):
    """资源不存在异常"""
    pass
