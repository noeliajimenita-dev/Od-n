import os

import pytest

from src.telegram.client import TelegramClient
from src.telegram.connection_guard import TelegramConnectionGuard
from src.telegram.connection_policy import TelegramConnectionPolicy
from src.telegram.connection_session import TelegramConnectionSession
from src.telegram.connection_controller import TelegramConnectionController
from src.telegram.connection_recovery import TelegramConnectionRecovery


def create_recovery():
    os.environ["TEST_TELEGRAM_TOKEN"] = "test-token"

    client = TelegramClient(
        bot_name="worker_1",
        token_env_variable="TEST_TELEGRAM_TOKEN",
    )

    guard = TelegramConnectionGuard(client)
    policy = TelegramConnectionPolicy()
    session = TelegramConnectionSession(bot_name="worker_1")

    controller = TelegramConnectionController(
        guard=guard,
        policy=policy,
        session=session,
    )

    return TelegramConnectionRecovery(controller)


def test_recovery_connects_disconnected_bot():
    recovery = create_recovery()

    assert recovery.is_recovered() is False

    result = recovery.recover()

    assert result is True
    assert recovery.is_recovered() is True

    del os.environ["TEST_TELEGRAM_TOKEN"]


def test_recovery_keeps_existing_connection():
    recovery = create_recovery()

    recovery.recover()
    result = recovery.recover()

    assert result is True
    assert recovery.is_recovered() is True

    del os.environ["TEST_TELEGRAM_TOKEN"]


def test_recovery_blocks_disabled_bot():
    recovery = create_recovery()

    with pytest.raises(RuntimeError):
        recovery.recover(enabled=False)

    assert recovery.is_recovered() is False

    del os.environ["TEST_TELEGRAM_TOKEN"]
