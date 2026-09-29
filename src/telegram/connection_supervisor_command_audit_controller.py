from .connection_supervisor_command_audit import (
    ConnectionCommandAudit,
)
from .connection_supervisor_command_audit_service import (
    ConnectionCommandAuditService,
)


class ConnectionCommandAuditController:
    def __init__(
        self,
        service: ConnectionCommandAuditService,
    ):
        self.service = service

    def record(self, audit: ConnectionCommandAudit) -> None:
        self.service.record(audit)

    def get(self, audit_id: str) -> ConnectionCommandAudit:
        return self.service.get(audit_id)

    def get_all(self) -> list[ConnectionCommandAudit]:
        return self.service.get_all()

    def count(self) -> int:
        return self.service.count()

    def status(self):
        return self.service.get_status()

    def report(self) -> str:
        return self.service.build_report()
