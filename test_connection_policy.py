import os

import pytest

from src.telegram.client import TelegramClient
from src.telegram.connection_guard import TelegramConnectionGuard
from src.telegram.connection_policy import TelegramConnectionPolicy


def create_guard():
    os.environ["TEST_TELEGRAM_TOKEN"] = "test-token"

    client = TelegramClient(
        bot_name="test_bot",
        token_env_variable="TEST_TELEGRAM_TOKEN",
    )

    return TelegramConnectionGuard(client)


def test_policy_allows_valid_connection():
    guard = create_guard()
    policy = TelegramConnectionPolicy()

    assert policy.can_connect(guard, enabled=True) is True

    policy.validate(guard, enabled=True)

    del os.environ["TEST_TELEGRAM_TOKEN"]


def test_policy_blocks_disabled_bot():
    guard = create_guard()
    policy = TelegramConnectionPolicy()

    assert policy.can_connect(guard, enabled=False) is False

    with pytest.raises(RuntimeError):
        policy.validate(guard, enabled=False)

    del os.environ["TEST_TELEGRAM_TOKEN"]


def test_policy_blocks_missing_token():
    variable_name = "TEST_TELEGRAM_TOKEN_MISSING"
    os.environ.pop(variable_name, None)

    client = TelegramClient(
        bot_name="test_bot",
        token_env_variable=variable_name,
    )

    guard = TelegramConnectionGuard(client)
    policy = TelegramConnectionPolicy()

    assert policy.can_connect(guard, enabled=True) is False

    with pytest.raises(RuntimeError):
        policy.validate(guard, enabled=True)
