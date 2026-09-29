from datetime import datetime, timezone

import pytest

from src.telegram.connection_supervisor_command_audit import (
    ConnectionCommandAudit,
)
from src.telegram.connection_supervisor_command_audit_logger import (
    ConnectionCommandAuditLogger,
)


def create_audit(
    audit_id: str = "audit-1",
) -> ConnectionCommandAudit:
    return ConnectionCommandAudit(
        audit_id=audit_id,
        command="CONNECT",
        bot_name="bot_1",
        success=True,
        message="Bot conectado correctamente.",
        timestamp=datetime.now(timezone.utc),
    )


def test_logger_records_audit():
    logger = ConnectionCommandAuditLogger()
    audit = create_audit()

    logger.record(audit)

    assert logger.count() == 1
    assert logger.get(audit.audit_id) is audit


def test_logger_returns_all_audits():
    logger = ConnectionCommandAuditLogger()

    first = create_audit("audit-1")
    second = create_audit("audit-2")

    logger.record(first)
    logger.record(second)

    audits = logger.get_all()

    assert len(audits) == 2
    assert audits[0] is first
    assert audits[1] is second


def test_logger_rejects_duplicate_audit_id():
    logger = ConnectionCommandAuditLogger()

    logger.record(create_audit("audit-1"))

    with pytest.raises(ValueError):
        logger.record(create_audit("audit-1"))


def test_logger_raises_for_unknown_audit():
    logger = ConnectionCommandAuditLogger()

    with pytest.raises(KeyError):
        logger.get("unknown-audit")
