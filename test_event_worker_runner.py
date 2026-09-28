from src.telegram.event_queue import TelegramEventQueue
from src.telegram.event_processor import TelegramEventProcessor
from src.telegram.event_worker_runner import TelegramEventWorkerRunner


def test_worker_runner_processes_pending_events():
    queue = TelegramEventQueue()
    processor = TelegramEventProcessor()

    queue.enqueue("event-1")
    queue.enqueue("event-2")

    runner = TelegramEventWorkerRunner(queue, processor)

    processed = runner.run_once()

    assert processed == 2
    assert queue.is_empty() is True


def test_worker_runner_with_empty_queue():
    queue = TelegramEventQueue()
    processor = TelegramEventProcessor()

    runner = TelegramEventWorkerRunner(queue, processor)

    processed = runner.run_once()

    assert processed == 0
