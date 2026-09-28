from src.telegram.event_queue import TelegramEventQueue
from src.telegram.event_processor import TelegramEventProcessor
from src.telegram.event_worker_runner import TelegramEventWorkerRunner
from src.telegram.event_worker_loop import TelegramEventWorkerLoop
from src.telegram.event_worker_control import TelegramEventWorkerControl


def create_control():
    queue = TelegramEventQueue()
    processor = TelegramEventProcessor()
    runner = TelegramEventWorkerRunner(queue, processor)
    loop = TelegramEventWorkerLoop(runner)
    control = TelegramEventWorkerControl(loop)

    return queue, control


def test_control_starts_and_stops_worker():
    _, control = create_control()

    assert control.is_running() is False

    control.start()
    assert control.is_running() is True

    control.stop()
    assert control.is_running() is False


def test_control_runs_cycle():
    queue, control = create_control()

    queue.enqueue("event-1")
    queue.enqueue("event-2")

    control.start()

    processed = control.run_cycle()

    assert processed == 2
    assert queue.is_empty() is True


def test_control_status():
    _, control = create_control()

    status = control.status()

    assert status["running"] is False

    control.start()

    status = control.status()

    assert status["running"] is True
