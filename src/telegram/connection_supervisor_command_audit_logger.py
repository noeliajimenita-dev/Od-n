from .connection_supervisor_command_audit import ConnectionCommandAudit


class ConnectionCommandAuditLogger:
    def __init__(self):
        self._entries: dict[str, ConnectionCommandAudit] = {}

    def record(self, audit: ConnectionCommandAudit) -> None:
        if audit.audit_id in self._entries:
            raise ValueError(
                f"El registro de auditoría ya existe: {audit.audit_id}"
            )

        self._entries[audit.audit_id] = audit

    def get(self, audit_id: str) -> ConnectionCommandAudit:
        if audit_id not in self._entries:
            raise KeyError(
                f"Registro de auditoría no encontrado: {audit_id}"
            )

        return self._entries[audit_id]

    def get_all(self) -> list[ConnectionCommandAudit]:
        return list(self._entries.values())

    def count(self) -> int:
        return len(self._entries)
