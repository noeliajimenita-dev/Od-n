from src.telegram.event_types import (
    TelegramEventType,
    is_valid_event_type,
)


def test_valid_event_types():
    assert is_valid_event_type("message")
    assert is_valid_event_type("command")
    assert is_valid_event_type("callback")
    assert is_valid_event_type("error")
    assert is_valid_event_type("status")
    assert is_valid_event_type("connection")


def test_invalid_event_type():
    assert not is_valid_event_type("unknown")
    assert not is_valid_event_type("")


def test_event_type_values():
    assert TelegramEventType.MESSAGE.value == "message"
    assert TelegramEventType.COMMAND.value == "command"
    assert TelegramEventType.STATUS.value == "status"
