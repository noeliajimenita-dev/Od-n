from src.telegram.event_queue import TelegramEventQueue
from src.telegram.event_worker_status import get_event_worker_status


def test_event_worker_status_empty_queue():
    queue = TelegramEventQueue()

    status = get_event_worker_status(queue)

    assert status["pending_events"] == 0
    assert status["queue_empty"] is True


def test_event_worker_status_with_pending_events():
    queue = TelegramEventQueue()

    queue.enqueue("event-1")
    queue.enqueue("event-2")

    status = get_event_worker_status(queue)

    assert status["pending_events"] == 2
    assert status["queue_empty"] is False
