import pytest

from src.audit.event import AuditEvent
from src.audit.logger import AuditLogger


def create_event(
    event_id: str = "EVENT-001",
) -> AuditEvent:
    return AuditEvent(
        event_id=event_id,
        actor="supervisor",
        action="TASK_CREATED",
        reason="Nueva tarea recibida",
        result="SUCCESS",
    )


def test_logger_starts_empty():
    logger = AuditLogger()

    assert logger.count() == 0
    assert logger.get_all_events() == []


def test_record_event():
    logger = AuditLogger()
    event = create_event()

    recorded = logger.record(event)

    assert recorded is event
    assert logger.count() == 1


def test_get_event():
    logger = AuditLogger()
    event = create_event()

    logger.record(event)

    result = logger.get_event("EVENT-001")

    assert result is event


def test_get_missing_event_returns_none():
    logger = AuditLogger()

    assert logger.get_event("UNKNOWN") is None


def test_get_all_events():
    logger = AuditLogger()

    first = create_event("EVENT-001")
    second = create_event("EVENT-002")

    logger.record(first)
    logger.record(second)

    events = logger.get_all_events()

    assert len(events) == 2
    assert events[0] is first
    assert events[1] is second


def test_get_all_events_returns_copy():
    logger = AuditLogger()
    logger.record(create_event())

    events = logger.get_all_events()
    events.clear()

    assert logger.count() == 1


def test_duplicate_event_id_is_rejected():
    logger = AuditLogger()

    logger.record(create_event("EVENT-001"))

    with pytest.raises(ValueError):
        logger.record(create_event("EVENT-001"))

    assert logger.count() == 1


def test_invalid_event_is_rejected():
    logger = AuditLogger()

    event = create_event()
    event.actor = ""

    with pytest.raises(ValueError):
        logger.record(event)

    assert logger.count() == 0


def test_clear_removes_events():
    logger = AuditLogger()

    logger.record(create_event("EVENT-001"))
    logger.record(create_event("EVENT-002"))

    assert logger.count() == 2

    logger.clear()

    assert logger.count() == 0
    assert logger.get_all_events() == []
