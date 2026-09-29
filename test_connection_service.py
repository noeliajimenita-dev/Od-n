import os

import pytest

from src.telegram.client import TelegramClient
from src.telegram.connection_guard import TelegramConnectionGuard
from src.telegram.connection_policy import TelegramConnectionPolicy
from src.telegram.connection_session import TelegramConnectionSession
from src.telegram.connection_controller import TelegramConnectionController
from src.telegram.connection_registry import TelegramConnectionRegistry
from src.telegram.connection_service import TelegramConnectionService


def create_service():
    os.environ["TEST_TELEGRAM_TOKEN"] = "test-token"

    registry = TelegramConnectionRegistry()
    controllers = {}

    for bot_name in ("supervisor", "worker_1"):
        registry.register(bot_name)

        client = TelegramClient(
            bot_name=bot_name,
            token_env_variable="TEST_TELEGRAM_TOKEN",
        )

        guard = TelegramConnectionGuard(client)
        policy = TelegramConnectionPolicy()
        session = registry.get(bot_name)

        controllers[bot_name] = TelegramConnectionController(
            guard=guard,
            policy=policy,
            session=session,
        )

    return TelegramConnectionService(
        registry=registry,
        controllers=controllers,
    )


def cleanup_token():
    os.environ.pop("TEST_TELEGRAM_TOKEN", None)


def test_connect_bot():
    service = create_service()

    service.connect_bot("worker_1")

    assert service.is_connected("worker_1") is True

    cleanup_token()


def test_disconnect_bot():
    service = create_service()

    service.connect_bot("worker_1")
    service.disconnect_bot("worker_1")

    assert service.is_connected("worker_1") is False

    cleanup_token()


def test_get_bot_status():
    service = create_service()

    status = service.get_status("supervisor")

    assert status["bot_name"] == "supervisor"
    assert status["connected"] is False

    cleanup_token()


def test_get_all_status():
    service = create_service()

    status = service.get_all_status()

    assert set(status.keys()) == {
        "supervisor",
        "worker_1",
    }

    assert status["supervisor"]["connected"] is False
    assert status["worker_1"]["connected"] is False

    cleanup_token()


def test_unknown_bot_is_rejected():
    service = create_service()

    with pytest.raises(KeyError):
        service.connect_bot("worker_99")

    cleanup_token()
