"""
资料源服务层

提供资料源的业务逻辑。
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from shared.database.repository import Repository
from ..domain.source import (
    Source,
    SourceCreate,
    SourceUpdate,
    SourceList,
    SourceInsight,
    CreateInsightRequest,
    InsightCreationResponse,
    SourceStatusResponse,
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


class SourceService:
    """资料源服务"""

    def __init__(self):
        self.repository = Repository("source")

    async def get_sources(
        self,
        owner_id: str = "",
        notebook_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        sort_by: str = "updated",
        sort_order: str = "desc",
    ) -> List[SourceList]:
        """
        获取资料源列表

        Args:
            owner_id: 所有者 ID
            notebook_id: 笔记本 ID（可选）
            limit: 返回数量限制
            offset: 偏移量
            sort_by: 排序字段
            sort_order: 排序顺序

        Returns:
            资料源列表
        """
        filters = {"owner_id": owner_id}
        if notebook_id:
            filters["notebook_id"] = notebook_id

        rows = await self.repository.list(
            filters=filters,
            limit=limit,
            offset=offset,
        )
        return [SourceList.model_validate(_normalize_record(row)) for row in rows]

    async def get_source(
        self,
        source_id: str,
        owner_id: str = "",
    ) -> Source:
        """
        获取资料源详情

        Args:
            source_id: 资料源 ID
            owner_id: 所有者 ID

        Returns:
            资料源详情

        Raises:
            NotFoundError: 资料源不存在
        """
        row = await self.repository.get(source_id)
        if not row:
            raise NotFoundError(f"Source {source_id} not found")
        return Source.model_validate(_normalize_record(row))

    async def create_source(
        self,
        request: SourceCreate,
        owner_id: str = "",
    ) -> Source:
        """
        创建资料源

        Args:
            request: 创建请求
            owner_id: 所有者 ID

        Returns:
            创建的资料源
        """
        data = {
            "title": request.title or "Processing...",
            "topics": [],
            "owner_id": owner_id,
        }
        record = await self.repository.create(data)
        return Source.model_validate(_normalize_record(record))

    async def update_source(
        self,
        source_id: str,
        request: SourceUpdate,
        owner_id: str = "",
    ) -> Source:
        """
        更新资料源

        Args:
            source_id: 资料源 ID
            request: 更新请求
            owner_id: 所有者 ID

        Returns:
            更新后的资料源

        Raises:
            NotFoundError: 资料源不存在
        """
        # 验证资料源存在且属于当前用户
        await self.get_source(source_id, owner_id)

        update_data = request.model_dump(exclude_unset=True)
        update_data["updated"] = _now_iso()

        result = await self.repository.update(source_id, update_data)
        record = result[0] if isinstance(result, list) else result
        return Source.model_validate(_normalize_record(record))

    async def delete_source(
        self,
        source_id: str,
        owner_id: str = "",
    ) -> bool:
        """
        删除资料源

        Args:
            source_id: 资料源 ID
            owner_id: 所有者 ID

        Returns:
            是否删除成功

        Raises:
            NotFoundError: 资料源不存在
        """
        # 验证资料源存在且属于当前用户
        await self.get_source(source_id, owner_id)
        return await self.repository.delete(source_id)

    async def get_source_status(
        self,
        source_id: str,
        owner_id: str = "",
    ) -> SourceStatusResponse:
        """
        获取资料源处理状态

        Args:
            source_id: 资料源 ID
            owner_id: 所有者 ID

        Returns:
            处理状态
        """
        source = await self.get_source(source_id, owner_id)
        return SourceStatusResponse(
            status=source.status,
            message=f"Source processing status: {source.status}",
            processing_info=source.processing_info,
            command_id=source.command_id,
        )

    async def retry_source(
        self,
        source_id: str,
        owner_id: str = "",
    ) -> Source:
        """
        重试资料源处理

        Args:
            source_id: 资料源 ID
            owner_id: 所有者 ID

        Returns:
            更新后的资料源
        """
        # TODO: 实现重试逻辑
        raise NotImplementedError("Retry not implemented yet")

    async def get_insights(
        self,
        source_id: str,
        owner_id: str = "",
    ) -> List[SourceInsight]:
        """
        获取资料源洞察列表

        Args:
            source_id: 资料源 ID
            owner_id: 所有者 ID

        Returns:
            洞察列表
        """
        # TODO: 实现获取洞察逻辑
        return []

    async def create_insight(
        self,
        source_id: str,
        request: CreateInsightRequest,
        owner_id: str = "",
    ) -> InsightCreationResponse:
        """
        创建资料源洞察

        Args:
            source_id: 资料源 ID
            request: 创建请求
            owner_id: 所有者 ID

        Returns:
            创建响应
        """
        # TODO: 实现创建洞察逻辑
        return InsightCreationResponse(
            status="pending",
            message="Insight generation started",
            source_id=source_id,
            transformation_id=request.transformation_id,
            command_id=None,
        )


class NotFoundError(Exception):
    """资源不存在异常"""
    pass
