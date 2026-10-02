from datetime import datetime, time

import pytest

from src.runtime.odin_daily_log import OdinDailyLog
from src.runtime.odin_log_service import OdinLogService
from src.runtime.odin_runtime_manager import OdinRuntimeManager
from src.runtime.odin_schedule import OdinSchedule, ScheduleWindow
from src.scheduler.odin_scheduler import OdinScheduler, ScheduledTask


def build_schedule(bot_id: str) -> OdinSchedule:
    schedule = OdinSchedule(
        bot_id=bot_id
    )

    schedule.set_windows(
        weekday=0,
        windows=[
            ScheduleWindow(
                start=time(4, 0),
                end=time(13, 0),
            ),
            ScheduleWindow(
                start=time(14, 0),
                end=time(22, 10),
            ),
        ],
    )

    return schedule


def test_runtime_starts_stopped():
    runtime = OdinRuntimeManager()

    assert runtime.is_stopped()
    assert not runtime.is_running()


def test_runtime_can_start():
    runtime = OdinRuntimeManager()

    runtime.start()

    assert runtime.is_running()
    assert not runtime.is_paused()


def test_runtime_can_pause():
    runtime = OdinRuntimeManager()

    runtime.start()
    runtime.pause()

    assert runtime.is_paused()
    assert not runtime.is_running()


def test_runtime_can_resume():
    runtime = OdinRuntimeManager()

    runtime.start()
    runtime.pause()
    runtime.resume()

    assert runtime.is_running()


def test_runtime_can_stop():
    runtime = OdinRuntimeManager()

    runtime.start()
    runtime.stop()

    assert runtime.is_stopped()


def test_pause_from_stopped_runtime_is_rejected():
    runtime = OdinRuntimeManager()

    with pytest.raises(RuntimeError):
        runtime.pause()


def test_resume_from_stopped_runtime_is_rejected():
    runtime = OdinRuntimeManager()

    with pytest.raises(RuntimeError):
        runtime.resume()


def test_registered_bot_respects_schedule():
    runtime = OdinRuntimeManager()

    schedule = build_schedule("worker_1")
    runtime.register_bot(schedule)
    runtime.start()

    working_time = datetime(
        2026,
        9,
        28,
        10,
        0,
    )

    pause_time = datetime(
        2026,
        9,
        28,
        13,
        30,
    )

    assert runtime.bot_should_work(
        "worker_1",
        working_time,
    )

    assert not runtime.bot_should_work(
        "worker_1",
        pause_time,
    )


def test_stopped_runtime_does_not_allow_work():
    runtime = OdinRuntimeManager()

    schedule = build_schedule("worker_1")
    runtime.register_bot(schedule)

    current = datetime(
        2026,
        9,
        28,
        10,
        0,
    )

    assert not runtime.bot_should_work(
        "worker_1",
        current,
    )


def test_paused_runtime_does_not_allow_work():
    runtime = OdinRuntimeManager()

    schedule = build_schedule("worker_1")
    runtime.register_bot(schedule)

    runtime.start()
    runtime.pause()

    current = datetime(
        2026,
        9,
        28,
        10,
        0,
    )

    assert not runtime.bot_should_work(
        "worker_1",
        current,
    )


def test_unknown_bot_cannot_work():
    runtime = OdinRuntimeManager()

    runtime.start()

    current = datetime(
        2026,
        9,
        28,
        10,
        0,
    )

    assert not runtime.bot_should_work(
        "unknown",
        current,
    )


def test_runtime_executes_ready_scheduled_task():
    scheduler = OdinScheduler()
    logs = OdinLogService()

    runtime = OdinRuntimeManager(
        scheduler=scheduler,
        log_service=logs,
    )

    schedule = build_schedule("worker_1")
    runtime.register_bot(schedule)

    executed = []

    scheduler.register_task(
        ScheduledTask(
            task_id="task_001",
            bot_id="worker_1",
            callback=lambda: executed.append(
                "done"
            ),
        )
    )

    runtime.start()

    current = datetime(
        2026,
        9,
        28,
        10,
        0,
    )

    result = runtime.run_once(current)

    assert executed == ["done"]
    assert result["status"] == "running"
    assert "task_001" in result["executed"]


def test_runtime_does_not_execute_task_during_pause():
    scheduler = OdinScheduler()
    logs = OdinLogService()

    runtime = OdinRuntimeManager(
        scheduler=scheduler,
        log_service=logs,
    )

    schedule = build_schedule("worker_1")
    runtime.register_bot(schedule)

    executed = []

    scheduler.register_task(
        ScheduledTask(
            task_id="task_002",
            bot_id="worker_1",
            callback=lambda: executed.append(
                "done"
            ),
        )
    )

    runtime.start()

    current = datetime(
        2026,
        9,
        28,
        13,
        30,
    )

    result = runtime.run_once(current)

    assert executed == []
    assert result["executed"] == {}


def test_runtime_updates_daily_log():
    logs = OdinLogService()
    runtime = OdinRuntimeManager(
        log_service=logs
    )

    schedule = build_schedule("worker_1")
    runtime.register_bot(schedule)

    runtime.start()

    current = datetime(
        2026,
        9,
        28,
        10,
        0,
    )

    runtime.run_once(current)

    log = logs.get_today(
        "worker_1"
    )

    assert isinstance(
        log,
        OdinDailyLog,
    )

    assert log.status == "working"


def test_runtime_status_contains_registered_bot():
    runtime = OdinRuntimeManager()

    schedule = build_schedule("worker_1")
    runtime.register_bot(schedule)
    runtime.start()

    current = datetime(
        2026,
        9,
        28,
        10,
        0,
    )

    status = runtime.status(current)

    assert status["runtime_state"] == "running"
    assert "worker_1" in status["bots"]
    assert status["bots"]["worker_1"][
        "should_work"
    ] is True


def test_runtime_can_remove_bot():
    runtime = OdinRuntimeManager()

    schedule = build_schedule("worker_1")
    runtime.register_bot(schedule)

    assert "worker_1" in runtime.list_bots()

    runtime.remove_bot("worker_1")

    assert "worker_1" not in runtime.list_bots()


def test_scheduler_task_can_be_disabled():
    scheduler = OdinScheduler()

    executed = []

    scheduler.set_default_schedule(
        "worker_1"
    )

    scheduler.register_task(
        ScheduledTask(
            task_id="task_003",
            bot_id="worker_1",
            callback=lambda: executed.append(
                "done"
            ),
        )
    )

    scheduler.disable_task(
        "task_003"
    )

    current = datetime(
        2026,
        9,
        28,
        10,
        0,
    )

    scheduler.run_ready_tasks(current)

    assert executed == []
