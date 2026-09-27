from datetime import datetime

import pytest

from src.audit.event import AuditEvent


def create_event() -> AuditEvent:
    return AuditEvent(
        event_id="EVENT-001",
        actor="supervisor",
        action="TASK_CREATED",
        reason="Nueva tarea recibida",
        result="SUCCESS",
        task_id="TASK-001",
        version="0.1.0",
        authorization_id="AUTH-001",
        tokens_used=120,
        files_changed=["src/example.py"],
    )


def test_audit_event_creation():
    event = create_event()

    assert event.event_id == "EVENT-001"
    assert event.actor == "supervisor"
    assert event.action == "TASK_CREATED"
    assert event.reason == "Nueva tarea recibida"
    assert event.result == "SUCCESS"
    assert isinstance(event.timestamp, datetime)


def test_audit_event_optional_fields():
    event = create_event()

    assert event.task_id == "TASK-001"
    assert event.version == "0.1.0"
    assert event.authorization_id == "AUTH-001"
    assert event.tokens_used == 120
    assert event.files_changed == ["src/example.py"]


def test_audit_event_is_valid():
    event = create_event()

    assert event.is_valid() is True
    assert event.validate() == []


@pytest.mark.parametrize(
    "field",
    [
        "event_id",
        "actor",
        "action",
        "reason",
        "result",
    ],
)
def test_required_fields_cannot_be_empty(field):
    event = create_event()

    setattr(event, field, "")

    assert event.is_valid() is False
    assert event.validate()


def test_negative_tokens_are_invalid():
    event = create_event()

    event.tokens_used = -1

    assert event.is_valid() is False
    assert "tokens_used no puede ser negativo." in event.validate()


def test_to_dict():
    event = create_event()

    data = event.to_dict()

    assert data["event_id"] == "EVENT-001"
    assert data["actor"] == "supervisor"
    assert data["action"] == "TASK_CREATED"
    assert data["reason"] == "Nueva tarea recibida"
    assert data["result"] == "SUCCESS"
    assert data["task_id"] == "TASK-001"
    assert data["version"] == "0.1.0"
    assert data["authorization_id"] == "AUTH-001"
    assert data["tokens_used"] == 120
    assert data["files_changed"] == ["src/example.py"]
    assert isinstance(data["timestamp"], str)


def test_to_dict_copies_mutable_fields():
    event = create_event()

    data = event.to_dict()

    data["files_changed"].append("another.py")
    data["metadata"]["new_value"] = True

    assert event.files_changed == ["src/example.py"]
    assert "new_value" not in event.metadata


def test_error_can_be_recorded():
    event = create_event()

    event.error = "Prueba fallida"

    assert event.error == "Prueba fallida"
    assert event.is_valid() is True
