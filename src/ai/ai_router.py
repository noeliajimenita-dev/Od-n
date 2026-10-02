from __future__ import annotations

from typing import Any

from .model_provider import AIProvider, AIRequest, AIResponse
from .provider_registry import AIProviderRegistry


class AIRouter:
    """Enrutador central de solicitudes de IA de ODIN."""

    def __init__(
        self,
        registry: AIProviderRegistry,
        preferred_providers: list[str] | None = None,
    ) -> None:
        if registry is None:
            raise ValueError("registry cannot be None")

        self.registry = registry
        self.preferred_providers = [
            name.strip().lower()
            for name in (preferred_providers or [])
            if name and name.strip()
        ]

    def select_provider(
        self,
        model: str,
        preferred_provider: str | None = None,
    ) -> AIProvider:
        if not model or not model.strip():
            raise ValueError("model cannot be empty")

        candidates: list[str] = []

        if preferred_provider and preferred_provider.strip():
            candidates.append(preferred_provider.strip().lower())

        candidates.extend(self.preferred_providers)

        for provider_name in candidates:
            provider = self.registry.get(provider_name)

            if provider is not None and provider.supports_model(model):
                return provider

        provider = self.registry.find_provider_for_model(model)

        if provider is None:
            raise ValueError(
                f"No provider supports model: {model}"
            )

        return provider

    def generate(
        self,
        request: AIRequest,
        preferred_provider: str | None = None,
    ) -> AIResponse:
        provider = self.select_provider(
            model=request.model,
            preferred_provider=preferred_provider,
        )

        return provider.generate(request)

    def supports_model(self, model: str) -> bool:
        return bool(self.registry.supports_model(model))

    def providers_for_model(self, model: str) -> list[str]:
        return self.registry.supports_model(model)

    def status(self) -> dict[str, Any]:
        return {
            "preferred_providers": list(self.preferred_providers),
            "providers": self.registry.list_providers(),
            "provider_count": self.registry.count(),
        }

    def set_preferences(
        self,
        providers: list[str],
    ) -> None:
        if providers is None:
            raise ValueError("providers cannot be None")

        self.preferred_providers = [
            provider.strip().lower()
            for provider in providers
            if provider and provider.strip()
        ]

    def add_preference(
        self,
        provider_name: str,
    ) -> None:
        name = provider_name.strip().lower()

        if not name:
            raise ValueError("provider_name cannot be empty")

        if name not in self.preferred_providers:
            self.preferred_providers.append(name)

    def remove_preference(
        self,
        provider_name: str,
    ) -> bool:
        name = provider_name.strip().lower()

        if name not in self.preferred_providers:
            return False

        self.preferred_providers.remove(name)
        return True

    def __repr__(self) -> str:
        return (
            f"AIRouter("
            f"providers={self.registry.count()}, "
            f"preferred={self.preferred_providers!r}"
            ")"
      )
