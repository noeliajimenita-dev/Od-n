from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AIRequest:
    """Solicitud normalizada de inferencia para ODIN."""

    request_id: str
    prompt: str
    model: str
    max_tokens: int | None = None
    temperature: float | None = None
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id cannot be empty")

        if not self.prompt.strip():
            raise ValueError("prompt cannot be empty")

        if not self.model.strip():
            raise ValueError("model cannot be empty")

        if self.max_tokens is not None and self.max_tokens <= 0:
            raise ValueError("max_tokens must be greater than zero")

        if self.temperature is not None:
            if self.temperature < 0:
                raise ValueError("temperature cannot be negative")

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "prompt": self.prompt,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "metadata": dict(self.metadata or {}),
        }


@dataclass(frozen=True)
class AIResponse:
    """Respuesta normalizada de cualquier proveedor de IA."""

    request_id: str
    provider: str
    model: str
    text: str
    usage: dict[str, int]
    metadata: dict[str, Any] | None = None

    @property
    def total_tokens(self) -> int:
        return int(self.usage.get("total_tokens", 0))

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "provider": self.provider,
            "model": self.model,
            "text": self.text,
            "usage": dict(self.usage),
            "metadata": dict(self.metadata or {}),
        }


class AIProvider(ABC):
    """
    Interfaz común de proveedores de IA.

    Gemini y Groq implementarán este contrato posteriormente.
    """

    def __init__(self, provider_name: str) -> None:
        if not provider_name or not provider_name.strip():
            raise ValueError("provider_name cannot be empty")

        self.provider_name = provider_name.strip().lower()

    @abstractmethod
    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """Ejecuta una solicitud de IA."""
        raise NotImplementedError

    @abstractmethod
    def supports_model(
        self,
        model: str,
    ) -> bool:
        """Indica si el proveedor admite el modelo solicitado."""
        raise NotImplementedError

    def validate_request(
        self,
        request: AIRequest,
    ) -> None:
        """Validación común antes de ejecutar."""
        if request is None:
            raise ValueError("request cannot be None")

        if not self.supports_model(request.model):
            raise ValueError(
                f"Model not supported by {self.provider_name}: "
                f"{request.model}"
            )

    def safe_status(self) -> dict[str, Any]:
        """
        Estado seguro del proveedor.

        Nunca incluye API keys.
        """
        return {
            "provider": self.provider_name,
            "configured": True,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(provider={self.provider_name!r})"
          )
