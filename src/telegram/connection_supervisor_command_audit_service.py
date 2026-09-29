from .connection_supervisor_command_audit import (
    ConnectionCommandAudit,
)
from .connection_supervisor_command_audit_logger import (
    ConnectionCommandAuditLogger,
)
from .connection_supervisor_command_audit_status import (
    ConnectionCommandAuditStatus,
    get_connection_command_audit_status,
)
from .connection_supervisor_command_audit_report import (
    build_connection_command_audit_report,
)


class ConnectionCommandAuditService:
    def __init__(
        self,
        logger: ConnectionCommandAuditLogger | None = None,
    ):
        self.logger = logger or ConnectionCommandAuditLogger()

    def record(self, audit: ConnectionCommandAudit) -> None:
        self.logger.record(audit)

    def get(self, audit_id: str) -> ConnectionCommandAudit:
        return self.logger.get(audit_id)

    def get_all(self) -> list[ConnectionCommandAudit]:
        return self.logger.get_all()

    def count(self) -> int:
        return self.logger.count()

    def get_status(self) -> ConnectionCommandAuditStatus:
        return get_connection_command_audit_status(self.logger)

    def build_report(self) -> str:
        return build_connection_command_audit_report(self.logger)
