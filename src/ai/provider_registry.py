from __future__ import annotations

from typing import Any

from .model_provider import AIProvider


class AIProviderRegistry:
    """Registro central de proveedores de IA de ODIN."""

    def __init__(self) -> None:
        self._providers: dict[str, AIProvider] = {}

    def register(self, provider: AIProvider) -> None:
        if not isinstance(provider, AIProvider):
            raise TypeError("provider must implement AIProvider")

        name = provider.provider_name

        if name in self._providers:
            raise ValueError(f"Provider already registered: {name}")

        self._providers[name] = provider

    def replace(self, provider: AIProvider) -> None:
        if not isinstance(provider, AIProvider):
            raise TypeError("provider must implement AIProvider")

        self._providers[provider.provider_name] = provider

    def get(self, provider_name: str) -> AIProvider | None:
        if not provider_name or not provider_name.strip():
            return None

        return self._providers.get(provider_name.strip().lower())

    def require(self, provider_name: str) -> AIProvider:
        provider = self.get(provider_name)

        if provider is None:
            raise KeyError(
                f"AI provider not registered: {provider_name}"
            )

        return provider

    def exists(self, provider_name: str) -> bool:
        return self.get(provider_name) is not None

    def remove(self, provider_name: str) -> bool:
        name = provider_name.strip().lower()

        if name not in self._providers:
            return False

        del self._providers[name]
        return True

    def list_providers(self) -> list[str]:
        return sorted(self._providers.keys())

    def get_all(self) -> dict[str, AIProvider]:
        return dict(self._providers)

    def count(self) -> int:
        return len(self._providers)

    def supports_model(self, model: str) -> list[str]:
        if not model or not model.strip():
            return []

        return [
            name
            for name, provider in self._providers.items()
            if provider.supports_model(model)
        ]

    def find_provider_for_model(self, model: str) -> AIProvider | None:
        providers = self.supports_model(model)

        if not providers:
            return None

        return self._providers[providers[0]]

    def status(self) -> dict[str, Any]:
        return {
            "provider_count": self.count(),
            "providers": {
                name: provider.safe_status()
                for name, provider in self._providers.items()
            },
        }

    def clear(self) -> None:
        self._providers.clear()

    def __len__(self) -> int:
        return self.count()
