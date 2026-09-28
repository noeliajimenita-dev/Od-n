import pytest

from src.telegram.telegram_event import TelegramEvent
from src.telegram.telegram_event_router import TelegramEventRouter


def test_register_and_dispatch_event():
    router = TelegramEventRouter()

    def handler(event):
        return event.event_type

    router.register("message", handler)

    event = TelegramEvent.create(
        bot_name="supervisor",
        chat_id="123",
        event_type="message",
    )

    assert router.dispatch(event) == "message"


def test_unknown_event_raises_error():
    router = TelegramEventRouter()

    event = TelegramEvent.create(
        bot_name="worker_1",
        chat_id="123",
        event_type="unknown",
    )

    with pytest.raises(KeyError):
        router.dispatch(event)


def test_invalid_event_raises_error():
    router = TelegramEventRouter()

    event = TelegramEvent(
        event_id="",
        bot_name="worker_1",
        chat_id="123",
        event_type="message",
        created_at=TelegramEvent.create(
            bot_name="worker_1",
            chat_id="123",
            event_type="message",
        ).created_at,
    )

    with pytest.raises(ValueError):
        router.dispatch(event)


def test_has_handler():
    router = TelegramEventRouter()

    router.register("message", lambda event: "ok")

    assert router.has_handler("message")
    assert not router.has_handler("command")
