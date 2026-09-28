import os

import pytest

from src.telegram.token_loader import load_bot_token


def test_load_bot_token():
    os.environ["TEST_TELEGRAM_TOKEN"] = "test-token-123"

    token = load_bot_token("TEST_TELEGRAM_TOKEN")

    assert token == "test-token-123"

    del os.environ["TEST_TELEGRAM_TOKEN"]


def test_load_bot_token_missing():
    variable_name = "TEST_TELEGRAM_TOKEN_MISSING"

    os.environ.pop(variable_name, None)

    with pytest.raises(ValueError):
        load_bot_token(variable_name)
