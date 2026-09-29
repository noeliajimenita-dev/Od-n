import os

from src.telegram.client import TelegramClient
from src.telegram.connection_guard import TelegramConnectionGuard
from src.telegram.connection_policy import TelegramConnectionPolicy
from src.telegram.connection_session import TelegramConnectionSession
from src.telegram.connection_controller import TelegramConnectionController
from src.telegram.connection_registry import TelegramConnectionRegistry
from src.telegram.connection_service import TelegramConnectionService
from src.telegram.connection_service_status import (
    get_connection_service_status,
)


def create_service():
    os.environ["TEST_TELEGRAM_TOKEN"] = "test-token"

    registry = TelegramConnectionRegistry()
    controllers = {}

    for bot_name in ("supervisor", "worker_1", "worker_2"):
        session = registry.register(bot_name)

        client = TelegramClient(
            bot_name=bot_name,
            token_env_variable="TEST_TELEGRAM_TOKEN",
        )

        guard = TelegramConnectionGuard(client)
        policy = TelegramConnectionPolicy()

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


def test_service_status_all_disconnected():
    service = create_service()

    status = get_connection_service_status(service)

    assert status["total_bots"] == 3
    assert status["connected_bots"] == 0
    assert status["disconnected_bots"] == 3
    assert status["connected_bot_names"] == []
    assert set(status["disconnected_bot_names"]) == {
        "supervisor",
        "worker_1",
        "worker_2",
    }

    cleanup_token()


def test_service_status_mixed_connections():
    service = create_service()

    service.connect_bot("supervisor")
    service.connect_bot("worker_2")

    status = get_connection_service_status(service)

    assert status["total_bots"] == 3
    assert status["connected_bots"] == 2
    assert status["disconnected_bots"] == 1

    assert set(status["connected_bot_names"]) == {
        "supervisor",
        "worker_2",
    }

    assert status["disconnected_bot_names"] == ["worker_1"]

    cleanup_token()


def test_service_status_all_connected():
    service = create_service()

    service.connect_bot("supervisor")
    service.connect_bot("worker_1")
    service.connect_bot("worker_2")

    status = get_connection_service_status(service)

    assert status["total_bots"] == 3
    assert status["connected_bots"] == 3
    assert status["disconnected_bots"] == 0
    assert set(status["connected_bot_names"]) == {
        "supervisor",
        "worker_1",
        "worker_2",
    }
    assert status["disconnected_bot_names"] == []

    cleanup_token()
