import os

import pytest

from src.telegram.client import TelegramClient
from src.telegram.connection_guard import TelegramConnectionGuard


def test_connection_guard_allows_configured_bot():
    os.environ["TEST_TELEGRAM_TOKEN"] = "test-token"

    client = TelegramClient(
        bot_name="test_bot",
        token_env_variable="TEST_TELEGRAM_TOKEN",
    )
    guard = TelegramConnectionGuard(client)

    assert guard.can_connect() is True

    guard.require_connection()

    del os.environ["TEST_TELEGRAM_TOKEN"]


def test_connection_guard_blocks_missing_token():
    variable_name = "TEST_TELEGRAM_TOKEN_MISSING"
    os.environ.pop(variable_name, None)

    client = TelegramClient(
        bot_name="test_bot",
        token_env_variable=variable_name,
    )
    guard = TelegramConnectionGuard(client)

    assert guard.can_connect() is False

    with pytest.raises(RuntimeError):
        guard.require_connection()
