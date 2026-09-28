import os

import pytest

from src.telegram.client import TelegramClient
from src.telegram.connection_guard import TelegramConnectionGuard
from src.telegram.connection_policy import TelegramConnectionPolicy
from src.telegram.connection_session import TelegramConnectionSession
from src.telegram.connection_controller import TelegramConnectionController


def create_controller():
    os.environ["TEST_TELEGRAM_TOKEN"] = "test-token"

    client = TelegramClient(
        bot_name="test_bot",
        token_env_variable="TEST_TELEGRAM_TOKEN",
    )

    guard = TelegramConnectionGuard(client)
    policy = TelegramConnectionPolicy()
    session = TelegramConnectionSession(bot_name="test_bot")

    controller = TelegramConnectionController(
        guard=guard,
        policy=policy,
        session=session,
    )

    return controller


def test_controller_connects_valid_bot():
    controller = create_controller()

    controller.connect()

    assert controller.is_connected() is True

    del os.environ["TEST_TELEGRAM_TOKEN"]


def test_controller_disconnects():
    controller = create_controller()

    controller.connect()
    controller.disconnect()

    assert controller.is_connected() is False

    del os.environ["TEST_TELEGRAM_TOKEN"]


def test_controller_blocks_disabled_bot():
    controller = create_controller()

    with pytest.raises(RuntimeError):
        controller.connect(enabled=False)

    assert controller.is_connected() is False

    del os.environ["TEST_TELEGRAM_TOKEN"]


def test_controller_status():
    controller = create_controller()

    status = controller.status()

    assert status["bot_name"] == "test_bot"
    assert status["connected"] is False

    controller.connect()

    status = controller.status()

    assert status["connected"] is True

    del os.environ["TEST_TELEGRAM_TOKEN"]
