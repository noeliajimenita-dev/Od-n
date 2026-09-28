from src.telegram.event_queue import TelegramEventQueue
from src.telegram.telegram_event import TelegramEvent


def create_event(event_type: str) -> TelegramEvent:
    return TelegramEvent.create(
        bot_name="worker_1",
        chat_id="123",
        event_type=event_type,
    )


def test_enqueue_and_dequeue():
    queue = TelegramEventQueue()

    event = create_event("message")

    queue.enqueue(event)

    assert queue.size() == 1
    assert queue.dequeue() == event
    assert queue.is_empty()


def test_dequeue_empty_queue():
    queue = TelegramEventQueue()

    assert queue.dequeue() is None


def test_queue_preserves_order():
    queue = TelegramEventQueue()

    first = create_event("message")
    second = create_event("command")

    queue.enqueue(first)
    queue.enqueue(second)

    assert queue.dequeue() == first
    assert queue.dequeue() == second


def test_clear_queue():
    queue = TelegramEventQueue()

    queue.enqueue(create_event("message"))
    queue.enqueue(create_event("status"))

    queue.clear()

    assert queue.is_empty()
    assert queue.size() == 0
