from __future__ import annotations

from typing import Any

from .ai_router import AIRouter
from .model_provider import AIRequest, AIResponse
from .resource_manager import ResourceManager


class AIService:
    """Punto de entrada unificado para las solicitudes de IA de ODIN."""

    def __init__(
        self,
        router: AIRouter,
        resource_manager: ResourceManager,
    ) -> None:
        if router is None:
            raise ValueError("router cannot be None")

        if resource_manager is None:
            raise ValueError("resource_manager cannot be None")

        self.router = router
        self.resource_manager = resource_manager

    def generate(
        self,
        request: AIRequest,
        preferred_provider: str | None = None,
    ) -> AIResponse:
        provider = self.router.select_provider(
            model=request.model,
            preferred_provider=preferred_provider,
        )

        estimated_tokens = request.max_tokens or 0

        if not self.resource_manager.can_execute(
            provider.provider_name,
            estimated_tokens=estimated_tokens,
        ):
            raise RuntimeError(
                f"AI resource limit reached for provider: "
                f"{provider.provider_name}"
            )

        response = self.router.generate(
            request=request,
            preferred_provider=provider.provider_name,
        )

        registered = self.resource_manager.register_usage(
            provider=response.provider,
            requests=1,
            tokens=response.total_tokens,
        )

        if not registered:
            raise RuntimeError(
                f"AI usage limit reached after execution: "
                f"{response.provider}"
            )

        return response

    def can_generate(
        self,
        request: AIRequest,
        preferred_provider: str | None = None,
    ) -> bool:
        provider = self.router.select_provider(
            model=request.model,
            preferred_provider=preferred_provider,
        )

        estimated_tokens = request.max_tokens or 0

        return self.resource_manager.can_execute(
            provider.provider_name,
            estimated_tokens=estimated_tokens,
        )

    def get_provider_for_model(
        self,
        model: str,
        preferred_provider: str | None = None,
    ) -> str:
        provider = self.router.select_provider(
            model=model,
            preferred_provider=preferred_provider,
        )

        return provider.provider_name

    def provider_usage(
        self,
        provider: str,
    ) -> dict[str, Any]:
        return self.resource_manager.status(provider)

    def status(self) -> dict[str, Any]:
        return {
            "router": self.router.status(),
            "resources": self.resource_manager.status(),
        }

    def pause_provider(self, provider: str) -> None:
        self.resource_manager.pause(provider)

    def resume_provider(self, provider: str) -> None:
        self.resource_manager.resume(provider)

    def reset_provider(
        self,
        provider: str,
        resume: bool = True,
    ) -> None:
        self.resource_manager.reset_usage(
            provider,
            resume=resume,
        )

    def __repr__(self) -> str:
        return (
            f"AIService("
            f"providers={self.router.registry.count()}"
            ")"
          )
