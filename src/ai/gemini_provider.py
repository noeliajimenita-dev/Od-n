from __future__ import annotations

import json
import os
from typing import Any
from urllib import error, request

from .model_provider import AIProvider, AIRequest, AIResponse


class GeminiProvider(AIProvider):
    """Proveedor Gemini basado en la API HTTP de Google."""

    DEFAULT_MODELS = {
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    }

    API_URL = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/{model}:generateContent"
    )

    def __init__(
        self,
        api_key: str | None = None,
        supported_models: set[str] | None = None,
        timeout: int = 60,
    ) -> None:
        super().__init__("gemini")

        self.api_key = (
            api_key
            or os.getenv("ODIN_GEMINI_API_KEY")
            or os.getenv("GEMINI_API_KEY")
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
        return bool(model and model.strip()) and model.strip() in self.supported_models

    def generate(self, request_data: AIRequest) -> AIResponse:
        self.validate_request(request_data)

        if not self.api_key:
            raise RuntimeError("Gemini API key is not configured")

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": request_data.prompt,
                        }
                    ]
                }
            ]
        }

        generation_config: dict[str, Any] = {}

        if request_data.max_tokens is not None:
            generation_config["maxOutputTokens"] = request_data.max_tokens

        if request_data.temperature is not None:
            generation_config["temperature"] = request_data.temperature

        if generation_config:
            payload["generationConfig"] = generation_config

        endpoint = self.API_URL.format(model=request_data.model)

        url = f"{endpoint}?key={self.api_key}"

        http_request = request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
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
                f"Gemini API error {exc.code}: {body}"
            ) from exc

        except error.URLError as exc:
            raise RuntimeError(
                f"Gemini connection error: {exc.reason}"
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
                "provider": "gemini",
            },
        )

    @staticmethod
    def _extract_text(data: dict[str, Any]) -> str:
        candidates = data.get("candidates") or []

        if not candidates:
            raise RuntimeError("Gemini returned no candidates")

        parts = (
            candidates[0]
            .get("content", {})
            .get("parts", [])
        )

        texts = [
            part.get("text", "")
            for part in parts
            if part.get("text")
        ]

        text = "".join(texts).strip()

        if not text:
            raise RuntimeError("Gemini returned an empty response")

        return text

    @staticmethod
    def _extract_usage(data: dict[str, Any]) -> dict[str, int]:
        usage_metadata = data.get("usageMetadata") or {}

        prompt_tokens = int(
            usage_metadata.get("promptTokenCount", 0)
        )

        output_tokens = int(
            usage_metadata.get("candidatesTokenCount", 0)
        )

        total_tokens = int(
            usage_metadata.get("totalTokenCount", 0)
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
            "GeminiProvider("
            f"configured={bool(self.api_key)}, "
            f"models={len(self.supported_models)}"
            ")"
      )
