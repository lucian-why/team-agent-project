"""
AI 提供商接口 - 统一的 AI 模型访问层

所有 feature 模块通过此接口访问 AI 模型，接口锁死，所有人依赖。
"""

from typing import AsyncGenerator, Any, Dict, Optional


class AIProvider:
    """AI 提供商基类"""

    def __init__(self, provider_name: str, api_key: Optional[str] = None):
        self.provider_name = provider_name
        self.api_key = api_key

    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        生成文本

        Args:
            prompt: 输入提示
            model: 模型名称（可选，使用默认模型）
            **kwargs: 其他参数

        Returns:
            生成的文本
        """
        # TODO: 实现 AI 生成逻辑
        raise NotImplementedError

    async def stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        流式生成文本

        Args:
            prompt: 输入提示
            model: 模型名称（可选，使用默认模型）
            **kwargs: 其他参数

        Yields:
            生成的文本片段
        """
        # TODO: 实现 AI 流式生成逻辑
        raise NotImplementedError

    async def embeddings(
        self,
        text: str,
        model: Optional[str] = None
    ) -> list[float]:
        """
        生成文本嵌入

        Args:
            text: 输入文本
            model: 模型名称（可选，使用默认模型）

        Returns:
            嵌入向量
        """
        # TODO: 实现嵌入生成逻辑
        raise NotImplementedError


class AIProviderFactory:
    """AI 提供商工厂"""

    @staticmethod
    def create(provider_name: str, **kwargs) -> AIProvider:
        """
        创建 AI 提供商实例

        Args:
            provider_name: 提供商名称（openai, anthropic, deepseek 等）
            **kwargs: 提供商特定参数

        Returns:
            AI 提供商实例
        """
        # TODO: 实现提供商工厂逻辑
        raise NotImplementedError
