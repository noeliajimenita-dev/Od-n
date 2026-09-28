import pytest

from src.telegram.event_processor import TelegramEventProcessor
from src.telegram.telegram_event import TelegramEvent
from src.telegram.telegram_event_router import TelegramEventRouter


def test_process_event():
    router = TelegramEventRouter()

    router.register(
        "message",
        lambda event: f"Procesado: {event.event_type}",
    )

    processor = TelegramEventProcessor(router)

    event = TelegramEvent.create(
        bot_name="supervisor",
        chat_id="123",
        event_type="message",
    )

    result = processor.process(event)

    assert result == "Procesado: message"


def test_process_invalid_event():
    router = TelegramEventRouter()
    processor = TelegramEventProcessor(router)

    event = TelegramEvent.create(
        bot_name="worker_1",
        chat_id="123",
        event_type="message",
    )

    invalid_event = TelegramEvent(
        event_id="",
        bot_name=event.bot_name,
        chat_id=event.chat_id,
        event_type=event.event_type,
        created_at=event.created_at,
    )

    with pytest.raises(ValueError):
        processor.process(invalid_event)
