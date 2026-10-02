from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ResourceLimit:
    """Límites configurables para un proveedor de IA."""

    requests_limit: int | None = None
    tokens_limit: int | None = None

    def __post_init__(self) -> None:
        if self.requests_limit is not None and self.requests_limit < 0:
            raise ValueError("requests_limit cannot be negative")

        if self.tokens_limit is not None and self.tokens_limit < 0:
            raise ValueError("tokens_limit cannot be negative")


@dataclass
class ResourceUsage:
    """Uso acumulado de un proveedor."""

    requests: int = 0
    tokens: int = 0

    def register(
        self,
        requests: int = 1,
        tokens: int = 0,
    ) -> None:
        if requests < 0:
            raise ValueError("requests cannot be negative")

        if tokens < 0:
            raise ValueError("tokens cannot be negative")

        self.requests += requests
        self.tokens += tokens

    def reset(self) -> None:
        self.requests = 0
        self.tokens = 0


class ResourceManager:
    """
    Gestor de consumo de recursos de IA.

    Los límites definidos aquí son límites internos de seguridad
    de ODIN y no representan necesariamente los límites oficiales
    del proveedor.
    """

    def __init__(self) -> None:
        self._limits: dict[str, ResourceLimit] = {}
        self._usage: dict[str, ResourceUsage] = {}
        self._paused: set[str] = set()

    def configure(
        self,
        provider: str,
        requests_limit: int | None = None,
        tokens_limit: int | None = None,
    ) -> None:
        name = self._normalize_provider(provider)

        self._limits[name] = ResourceLimit(
            requests_limit=requests_limit,
            tokens_limit=tokens_limit,
        )

        self._usage.setdefault(name, ResourceUsage())

    def get_limit(
        self,
        provider: str,
    ) -> ResourceLimit | None:
        return self._limits.get(
            self._normalize_provider(provider)
        )

    def get_usage(
        self,
        provider: str,
    ) -> ResourceUsage:
        name = self._normalize_provider(provider)
        return self._usage.setdefault(
            name,
            ResourceUsage(),
        )

    def can_execute(
        self,
        provider: str,
        estimated_tokens: int = 0,
    ) -> bool:
        name = self._normalize_provider(provider)

        if estimated_tokens < 0:
            raise ValueError(
                "estimated_tokens cannot be negative"
            )

        if name in self._paused:
            return False

        limit = self._limits.get(name)

        if limit is None:
            return True

        usage = self.get_usage(name)

        if (
            limit.requests_limit is not None
            and usage.requests + 1 > limit.requests_limit
        ):
            return False

        if (
            limit.tokens_limit is not None
            and usage.tokens + estimated_tokens
            > limit.tokens_limit
        ):
            return False

        return True

    def register_usage(
        self,
        provider: str,
        requests: int = 1,
        tokens: int = 0,
    ) -> bool:
        name = self._normalize_provider(provider)

        if not self.can_execute(
            name,
            estimated_tokens=tokens,
        ):
            return False

        usage = self.get_usage(name)

        usage.register(
            requests=requests,
            tokens=tokens,
        )

        if self._limit_reached(name):
            self._paused.add(name)

        return True

    def pause(self, provider: str) -> None:
        self._paused.add(
            self._normalize_provider(provider)
        )

    def resume(self, provider: str) -> None:
        self._paused.discard(
            self._normalize_provider(provider)
        )

    def reset_usage(
        self,
        provider: str,
        resume: bool = True,
    ) -> None:
        name = self._normalize_provider(provider)

        self.get_usage(name).reset()

        if resume:
            self._paused.discard(name)

    def is_paused(self, provider: str) -> bool:
        return (
            self._normalize_provider(provider)
            in self._paused
        )

    def is_limit_reached(self, provider: str) -> bool:
        return self._limit_reached(
            self._normalize_provider(provider)
        )

    def _limit_reached(self, provider: str) -> bool:
        limit = self._limits.get(provider)

        if limit is None:
            return False

        usage = self.get_usage(provider)

        requests_reached = (
            limit.requests_limit is not None
            and usage.requests >= limit.requests_limit
        )

        tokens_reached = (
            limit.tokens_limit is not None
            and usage.tokens >= limit.tokens_limit
        )

        return requests_reached or tokens_reached

    def status(
        self,
        provider: str | None = None,
    ) -> dict[str, Any]:
        if provider is not None:
            return self._provider_status(
                self._normalize_provider(provider)
            )

        return {
            name: self._provider_status(name)
            for name in sorted(self._usage.keys())
        }

    def _provider_status(
        self,
        provider: str,
    ) -> dict[str, Any]:
        usage = self.get_usage(provider)
        limit = self._limits.get(provider)

        return {
            "provider": provider,
            "requests": usage.requests,
            "tokens": usage.tokens,
            "requests_limit": (
                limit.requests_limit
                if limit
                else None
            ),
            "tokens_limit": (
                limit.tokens_limit
                if limit
                else None
            ),
            "paused": provider in self._paused,
            "limit_reached": self._limit_reached(provider),
        }

    def providers(self) -> list[str]:
        return sorted(
            set(self._limits) | set(self._usage)
        )

    @staticmethod
    def _normalize_provider(provider: str) -> str:
        if not provider or not provider.strip():
            raise ValueError(
                "provider cannot be empty"
            )

        return provider.strip().lower()

    def __repr__(self) -> str:
        return (
            f"ResourceManager("
            f"providers={len(self.providers())}"
            ")"
      )
