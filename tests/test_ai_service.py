from __future__ import annotations

import unittest

from src.ai.ai_router import AIRouter
from src.ai.ai_service import AIService
from src.ai.gemini_provider import GeminiProvider
from src.ai.groq_provider import GroqProvider
from src.ai.model_provider import AIProvider, AIRequest, AIResponse
from src.ai.provider_registry import AIProviderRegistry
from src.ai.resource_manager import ResourceManager


class FakeProvider(AIProvider):
    def __init__(
        self,
        name: str,
        models: set[str],
        response_text: str = "ok",
    ) -> None:
        super().__init__(name)
        self.models = models
        self.response_text = response_text

    def supports_model(self, model: str) -> bool:
        return model in self.models

    def generate(self, request: AIRequest) -> AIResponse:
        self.validate_request(request)

        return AIResponse(
            request_id=request.request_id,
            provider=self.provider_name,
            model=request.model,
            text=self.response_text,
            usage={
                "prompt_tokens": 5,
                "output_tokens": 7,
                "total_tokens": 12,
            },
        )


class TestAIRequest(unittest.TestCase):
    def test_valid_request(self) -> None:
        request = AIRequest(
            request_id="req-1",
            prompt="Hello",
            model="test-model",
            max_tokens=100,
            temperature=0.5,
        )

        self.assertEqual(request.request_id, "req-1")
        self.assertEqual(request.model, "test-model")
        self.assertEqual(request.max_tokens, 100)

    def test_empty_prompt_rejected(self) -> None:
        with self.assertRaises(ValueError):
            AIRequest(
                request_id="req-1",
                prompt="",
                model="test-model",
            )

    def test_invalid_max_tokens_rejected(self) -> None:
        with self.assertRaises(ValueError):
            AIRequest(
                request_id="req-1",
                prompt="Hello",
                model="test-model",
                max_tokens=0,
            )


class TestAIProviderRegistry(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = AIProviderRegistry()

    def test_register_and_get(self) -> None:
        provider = FakeProvider(
            "test",
            {"model-a"},
        )

        self.registry.register(provider)

        self.assertTrue(self.registry.exists("test"))
        self.assertIs(self.registry.get("test"), provider)

    def test_duplicate_registration_rejected(self) -> None:
        provider = FakeProvider(
            "test",
            {"model-a"},
        )

        self.registry.register(provider)

        with self.assertRaises(ValueError):
            self.registry.register(provider)

    def test_find_provider_for_model(self) -> None:
        provider = FakeProvider(
            "test",
            {"model-a"},
        )

        self.registry.register(provider)

        result = self.registry.find_provider_for_model(
            "model-a"
        )

        self.assertIs(result, provider)

    def test_remove_provider(self) -> None:
        provider = FakeProvider(
            "test",
            {"model-a"},
        )

        self.registry.register(provider)

        self.assertTrue(self.registry.remove("test"))
        self.assertFalse(self.registry.exists("test"))


class TestAIRouter(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = AIProviderRegistry()

        self.first = FakeProvider(
            "first",
            {"shared-model"},
            response_text="first",
        )

        self.second = FakeProvider(
            "second",
            {"shared-model"},
            response_text="second",
        )

        self.registry.register(self.first)
        self.registry.register(self.second)

    def test_preferred_provider_is_selected(self) -> None:
        router = AIRouter(
            self.registry,
            preferred_providers=["second"],
        )

        provider = router.select_provider(
            "shared-model"
        )

        self.assertEqual(
            provider.provider_name,
            "second",
        )

    def test_generate_uses_selected_provider(self) -> None:
        router = AIRouter(
            self.registry,
            preferred_providers=["second"],
        )

        request = AIRequest(
            request_id="req-1",
            prompt="Hello",
            model="shared-model",
        )

        response = router.generate(request)

        self.assertEqual(response.provider, "second")
        self.assertEqual(response.text, "second")

    def test_unsupported_model_rejected(self) -> None:
        router = AIRouter(self.registry)

        with self.assertRaises(ValueError):
            router.select_provider("unknown-model")


class TestResourceManager(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = ResourceManager()

    def test_configure_limits(self) -> None:
        self.manager.configure(
            "test",
            requests_limit=2,
            tokens_limit=100,
        )

        status = self.manager.status("test")

        self.assertEqual(
            status["requests_limit"],
            2,
        )
        self.assertEqual(
            status["tokens_limit"],
            100,
        )

    def test_usage_is_registered(self) -> None:
        self.manager.configure(
            "test",
            requests_limit=10,
            tokens_limit=100,
        )

        self.assertTrue(
            self.manager.register_usage(
                "test",
                requests=1,
                tokens=20,
            )
        )

        status = self.manager.status("test")

        self.assertEqual(status["requests"], 1)
        self.assertEqual(status["tokens"], 20)

    def test_request_limit_pauses_provider(self) -> None:
        self.manager.configure(
            "test",
            requests_limit=1,
        )

        self.assertTrue(
            self.manager.register_usage("test")
        )

        self.assertFalse(
            self.manager.can_execute("test")
        )

        self.assertTrue(
            self.manager.is_limit_reached("test")
        )

        def test_pause_and_resume(self) -> None:
        self.manager.pause("test")

        self.assertTrue(
            self.manager.is_paused("test")
        )

        self.manager.resume("test")

        self.assertFalse(
            self.manager.is_paused("test")
        )
