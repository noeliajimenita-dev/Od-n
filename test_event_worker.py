from src.telegram.event_processor import TelegramEventProcessor
from src.telegram.event_queue import TelegramEventQueue
from src.telegram.event_worker import TelegramEventWorker
from src.telegram.telegram_event import TelegramEvent
from src.telegram.telegram_event_router import TelegramEventRouter


def create_event(event_type: str) -> TelegramEvent:
    return TelegramEvent.create(
        bot_name="worker_1",
        chat_id="123",
        event_type=event_type,
    )


def create_worker() -> TelegramEventWorker:
    router = TelegramEventRouter()

    router.register(
        "message",
        lambda event: f"Procesado: {event.event_type}",
    )

    router.register(
        "command",
        lambda event: f"Procesado: {event.event_type}",
    )

    processor = TelegramEventProcessor(router)
    queue = TelegramEventQueue()

    return TelegramEventWorker(queue, processor)


def test_process_next():
    worker = create_worker()

    event = create_event("message")
    worker.queue.enqueue(event)

    result = worker.process_next()

    assert result == "Procesado: message"
    assert worker.queue.is_empty()


def test_process_all():
    worker = create_worker()

    worker.queue.enqueue(create_event("message"))
    worker.queue.enqueue(create_event("command"))

    results = worker.process_all()

    assert results == [
        "Procesado: message",
        "Procesado: command",
    ]


def test_process_empty_queue():
    worker = create_worker()

    assert worker.process_next() is None
