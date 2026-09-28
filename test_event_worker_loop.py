from src.telegram.event_queue import TelegramEventQueue
from src.telegram.event_processor import TelegramEventProcessor
from src.telegram.event_worker_runner import TelegramEventWorkerRunner
from src.telegram.event_worker_loop import TelegramEventWorkerLoop


def create_loop():
    queue = TelegramEventQueue()
    processor = TelegramEventProcessor()
    runner = TelegramEventWorkerRunner(queue, processor)
    return queue, TelegramEventWorkerLoop(runner)


def test_loop_starts_and_stops():
    _, loop = create_loop()

    assert loop.is_running() is False

    loop.start()
    assert loop.is_running() is True

    loop.stop()
    assert loop.is_running() is False


def test_cycle_does_nothing_when_stopped():
    queue, loop = create_loop()

    queue.enqueue("event-1")

    processed = loop.run_cycle()

    assert processed == 0
    assert queue.is_empty() is False


def test_cycle_processes_events_when_running():
    queue, loop = create_loop()

    queue.enqueue("event-1")
    queue.enqueue("event-2")

    loop.start()

    processed = loop.run_cycle()

    assert processed == 2
    assert queue.is_empty() is True
