from .event_queue import TelegramEventQueue


def get_event_worker_status(queue: TelegramEventQueue) -> dict:
    pending_events = queue.size()

    return {
        "pending_events": pending_events,
        "queue_empty": queue.is_empty(),
    }
