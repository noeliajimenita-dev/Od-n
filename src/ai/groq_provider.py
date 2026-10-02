from __future__ import annotations

import json
import os
from typing import Any
from urllib import error, request

from .model_provider import AIProvider, AIRequest, AIResponse


class GroqProvider(AIProvider):
    """Proveedor Groq basado en la API HTTP compatible con OpenAI."""

    DEFAULT_MODELS = {
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
    }

    API_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(
        self,
        api_key: str | None = None,
        supported_models: set[str] | None = None,
        timeout: int = 60,
    ) -> None:
        super().__init__("groq")

        self.api_key = (
            api_key
            or os.getenv("ODIN_GROQ_API_KEY")
            or os.getenv("GROQ_API_KEY")
        )

        self.supported_models = (
            set(supported_models)
            if supported_models is not None
            else set(self.DEFAULT_MODELS)
        )

        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        self.timeout = timeout

    def supports_model(self, model: str) -> bool:
        return (
            bool(model and model.strip())
            and model.strip() in self.supported_models
        )

    def generate(self, request_data: AIRequest) -> AIResponse:
        self.validate_request(request_data)

        if not self.api_key:
            raise RuntimeError("Groq API key is not configured")

        payload: dict[str, Any] = {
            "model": request_data.model,
            "messages": [
                {
                    "role": "user",
                    "content": request_data.prompt,
                }
            ],
        }

        if request_data.max_tokens is not None:
            payload["max_tokens"] = request_data.max_tokens

        if request_data.temperature is not None:
            payload["temperature"] = request_data.temperature

        http_request = request.Request(
            url=self.API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(
                http_request,
                timeout=self.timeout,
            ) as response:
                raw_body = response.read().decode("utf-8")

        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")

            raise RuntimeError(
                f"Groq API error {exc.code}: {body}"
            ) from exc

        except error.URLError as exc:
            raise RuntimeError(
                f"Groq connection error: {exc.reason}"
            ) from exc

        data = json.loads(raw_body)

        text = self._extract_text(data)
        usage = self._extract_usage(data)

        return AIResponse(
            request_id=request_data.request_id,
            provider=self.provider_name,
            model=request_data.model,
            text=text,
            usage=usage,
            metadata={
                "provider": "groq",
            },
        )

    @staticmethod
    def _extract_text(data: dict[str, Any]) -> str:
        choices = data.get("choices") or []

        if not choices:
            raise RuntimeError("Groq returned no choices")

        message = choices[0].get("message") or {}
        text = str(message.get("content") or "").strip()

        if not text:
            raise RuntimeError("Groq returned an empty response")

        return text

    @staticmethod
    def _extract_usage(data: dict[str, Any]) -> dict[str, int]:
        usage = data.get("usage") or {}

        prompt_tokens = int(
            usage.get("prompt_tokens", 0)
        )

        output_tokens = int(
            usage.get("completion_tokens", 0)
        )

        total_tokens = int(
            usage.get("total_tokens", 0)
        )

        return {
            "prompt_tokens": prompt_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        }

    def safe_status(self) -> dict[str, Any]:
        return {
            "provider": self.provider_name,
            "configured": bool(self.api_key),
            "models": sorted(self.supported_models),
            "timeout": self.timeout,
        }

    def __repr__(self) -> str:
        return (
            "GroqProvider("
            f"configured={bool(self.api_key)}, "
            f"models={len(self.supported_models)}"
            ")"
        )
