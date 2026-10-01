from src.supervisor.task_assignment_log import TaskAssignmentLog


def test_log_starts_empty():
    log = TaskAssignmentLog()

    assert log.list_events() == []
    assert log.count() == 0


def test_log_records_assignment_event():
    log = TaskAssignmentLog()

    event = log.record(
        "task-001",
        "worker_1",
        "assigned",
    )

    assert event.task_id == "task-001"
    assert event.worker_id == "worker_1"
    assert event.event == "assigned"
    assert event.timestamp


def test_log_normalizes_event():
    log = TaskAssignmentLog()

    event = log.record(
        " task-001 ",
        " worker_1 ",
        " ASSIGNED ",
    )

    assert event.task_id == "task-001"
    assert event.worker_id == "worker_1"
    assert event.event == "assigned"


def test_log_lists_events():
    log = TaskAssignmentLog()

    log.record("task-001", "worker_1", "assigned")
    log.record("task-002", "worker_2", "started")

    events = log.list_events()

    assert len(events) == 2
    assert events[0].task_id == "task-001"
    assert events[1].task_id == "task-002"


def test_log_filters_events_by_task():
    log = TaskAssignmentLog()

    log.record("task-001", "worker_1", "assigned")
    log.record("task-002", "worker_2", "assigned")
    log.record("task-001", "worker_1", "completed")

    events = log.task_events("task-001")

    assert len(events) == 2
    assert all(event.task_id == "task-001" for event in events)


def test_log_filters_events_by_worker():
    log = TaskAssignmentLog()

    log.record("task-001", "worker_1", "assigned")
    log.record("task-002", "worker_2", "assigned")
    log.record("task-003", "worker_1", "completed")

    events = log.worker_events("worker_1")

    assert len(events) == 2
    assert all(event.worker_id == "worker_1" for event in events)


def test_log_count_increases():
    log = TaskAssignmentLog()

    log.record("task-001", "worker_1", "assigned")
    log.record("task-002", "worker_2", "assigned")

    assert log.count() == 2


def test_log_clear_removes_events():
    log = TaskAssignmentLog()

    log.record("task-001", "worker_1", "assigned")
    log.record("task-002", "worker_2", "completed")

    log.clear()

    assert log.count() == 0
    assert log.list_events() == []


def test_log_rejects_empty_task_id():
    log = TaskAssignmentLog()

    try:
        log.record("", "worker_1", "assigned")
        assert False
    except ValueError as exc:
        assert str(exc) == "Task ID cannot be empty"


def test_log_rejects_empty_worker_id():
    log = TaskAssignmentLog()

    try:
        log.record("task-001", "", "assigned")
        assert False
    except ValueError as exc:
        assert str(exc) == "Worker ID cannot be empty"


def test_log_rejects_empty_event():
    log = TaskAssignmentLog()

    try:
        log.record("task-001", "worker_1", "")
        assert False
    except ValueError as exc:
        assert str(exc) == "Event cannot be empty"
