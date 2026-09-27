from src.audit.event import AuditEvent
from src.audit.logger import AuditLogger
from src.audit.status import get_audit_status


def create_event(
    event_id: str,
    actor: str,
    action: str,
    result: str,
    task_id: str | None = None,
    error: str | None = None,
) -> AuditEvent:
    return AuditEvent(
        event_id=event_id,
        actor=actor,
        action=action,
        reason="Prueba de auditoría",
        result=result,
        task_id=task_id,
        error=error,
    )


def test_empty_audit_status():
    logger = AuditLogger()

    status = get_audit_status(logger)

    assert status["total_events"] == 0
    assert status["events_with_errors"] == 0
    assert status["events_with_tasks"] == 0
    assert status["actors"] == {}
    assert status["actions"] == {}
    assert status["results"] == {}


def test_audit_status_counts_events():
    logger = AuditLogger()

    logger.record(
        create_event(
            "EVENT-001",
            "supervisor",
            "TASK_CREATED",
            "SUCCESS",
        )
    )

    logger.record(
        create_event(
            "EVENT-002",
            "worker_1",
            "TASK_COMPLETED",
            "SUCCESS",
        )
    )

    status = get_audit_status(logger)

    assert status["total_events"] == 2


def test_audit_status_counts_actors():
    logger = AuditLogger()

    logger.record(
        create_event(
            "EVENT-003",
            "supervisor",
            "TASK_CREATED",
            "SUCCESS",
        )
    )

    logger.record(
        create_event(
            "EVENT-004",
            "supervisor",
            "TASK_ASSIGNED",
            "SUCCESS",
        )
    )

    logger.record(
        create_event(
            "EVENT-005",
            "worker_1",
            "TASK_COMPLETED",
            "SUCCESS",
        )
    )

    status = get_audit_status(logger)

    assert status["actors"]["supervisor"] == 2
    assert status["actors"]["worker_1"] == 1


def test_audit_status_counts_actions():
    logger = AuditLogger()

    logger.record(
        create_event(
            "EVENT-006",
            "supervisor",
            "TASK_CREATED",
            "SUCCESS",
        )
    )

    logger.record(
        create_event(
            "EVENT-007",
            "worker_1",
            "TASK_CREATED",
            "SUCCESS",
        )
    )

    status = get_audit_status(logger)

    assert status["actions"]["TASK_CREATED"] == 2


def test_audit_status_counts_results():
    logger = AuditLogger()

    logger.record(
        create_event(
            "EVENT-008",
            "supervisor",
            "TASK_CREATED",
            "SUCCESS",
        )
    )

    logger.record(
        create_event(
            "EVENT-009",
            "worker_1",
            "TASK_FAILED",
            "ERROR",
        )
    )

    status = get_audit_status(logger)

    assert status["results"]["SUCCESS"] == 1
    assert status["results"]["ERROR"] == 1


def test_audit_status_counts_task_events():
    logger = AuditLogger()

    logger.record(
        create_event(
            "EVENT-010",
            "supervisor",
            "TASK_CREATED",
            "SUCCESS",
            task_id="TASK-001",
        )
    )

    logger.record(
        create_event(
            "EVENT-011",
            "worker_1",
            "SYSTEM_CHECK",
            "SUCCESS",
        )
    )

    status = get_audit_status(logger)

    assert status["events_with_tasks"] == 1


def test_audit_status_counts_errors():
    logger = AuditLogger()

    logger.record(
        create_event(
            "EVENT-012",
            "worker_1",
            "TASK_FAILED",
            "ERROR",
            error="Error de prueba",
        )
    )

    logger.record(
        create_event(
            "EVENT-013",
            "supervisor",
            "TASK_CREATED",
            "SUCCESS",
        )
    )

    status = get_audit_status(logger)

    assert status["events_with_errors"] == 1
