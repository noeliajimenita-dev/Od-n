"""
Estado general del Audit Log de THE ODIN PROJECT.
"""

from collections import Counter

from .logger import AuditLogger


def get_audit_status(logger: AuditLogger) -> dict:
    """Devuelve un resumen seguro del registro de auditoría."""

    events = logger.get_all_events()

    actors = Counter(
        event.actor
        for event in events
    )

    actions = Counter(
        event.action
        for event in events
    )

    results = Counter(
        event.result
        for event in events
    )

    events_with_errors = sum(
        1
        for event in events
        if event.error
    )

    events_with_tasks = sum(
        1
        for event in events
        if event.task_id
    )

    return {
        "total_events": len(events),
        "events_with_errors": events_with_errors,
        "events_with_tasks": events_with_tasks,
        "actors": dict(actors),
        "actions": dict(actions),
        "results": dict(results),
    }
