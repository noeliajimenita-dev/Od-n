import os

from src.telegram.client import TelegramClient
from src.telegram.connection_guard import TelegramConnectionGuard
from src.telegram.connection_policy import TelegramConnectionPolicy
from src.telegram.connection_session import TelegramConnectionSession
from src.telegram.connection_controller import TelegramConnectionController
from src.telegram.connection_registry import TelegramConnectionRegistry
from src.telegram.connection_service import TelegramConnectionService
from src.telegram.connection_supervisor import TelegramConnectionSupervisor


def create_supervisor():
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

    service = TelegramConnectionService(
        registry=registry,
        controllers=controllers,
    )

    return TelegramConnectionSupervisor(service)


def cleanup_token():
    os.environ.pop("TEST_TELEGRAM_TOKEN", None)


def test_supervisor_inspects_connections():
    supervisor = create_supervisor()

    status = supervisor.inspect()

    assert status["total_bots"] == 3
    assert status["connected_bots"] == 0
    assert status["disconnected_bots"] == 3

    cleanup_token()


def test_supervisor_lists_connected_and_disconnected_bots():
    supervisor = create_supervisor()

    supervisor.service.connect_bot("supervisor")
    supervisor.service.connect_bot("worker_2")

    connected = supervisor.connected_bots()
    disconnected = supervisor.disconnected_bots()

    assert set(connected) == {
        "supervisor",
        "worker_2",
    }

    assert disconnected == ["worker_1"]

    cleanup_token()


def test_supervisor_detects_when_all_bots_are_connected():
    supervisor = create_supervisor()

    supervisor.service.connect_bot("supervisor")
    supervisor.service.connect_bot("worker_1")
    supervisor.service.connect_bot("worker_2")

    assert supervisor.all_connected() is True

    cleanup_token()


def test_supervisor_detects_when_not_all_bots_are_connected():
    supervisor = create_supervisor()

    supervisor.service.connect_bot("supervisor")

    assert supervisor.all_connected() is False

    cleanup_token()
