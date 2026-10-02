from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable

from .odin_backup import OdinBackupManager


@dataclass(frozen=True)
class RecoveryResult:
    backup_id: str
    version: str
    status: str
    restored_at: datetime
    data: dict[str, Any]
    error: str | None = None

    @property
    def successful(self) -> bool:
        return self.status == "restored"

    def to_dict(self) -> dict[str, Any]:
        return {
            "backup_id": self.backup_id,
            "version": self.version,
            "status": self.status,
            "restored_at": self.restored_at.isoformat(),
            "data": dict(self.data),
            "error": self.error,
        }


class OdinRecoveryManager:
    """
    Gestiona la restauración de ODIN desde backups.

    El manager no modifica directamente el código del sistema.
    Recibe un callback de restauración para que la capa superior
    controle cómo se aplica realmente una versión.
    """

    def __init__(
        self,
        backup_manager: OdinBackupManager,
        restore_callback: Callable[
            [dict[str, Any]], Any
        ] | None = None,
    ) -> None:
        if backup_manager is None:
            raise ValueError(
                "backup_manager cannot be None"
            )

        self.backup_manager = backup_manager
        self.restore_callback = restore_callback
        self._history: list[RecoveryResult] = []

    def restore(
        self,
        backup_id: str,
    ) -> RecoveryResult:
        backup = self.backup_manager.get(backup_id)

        if backup is None:
            result = RecoveryResult(
                backup_id=backup_id,
                version="unknown",
                status="failed",
                restored_at=datetime.now(),
                data={},
                error="Backup not found",
            )
            self._history.append(result)
            return result

        if not self.backup_manager.can_restore(
            backup_id
        ):
            result = RecoveryResult(
                backup_id=backup_id,
                version=backup.version,
                status="failed",
                restored_at=datetime.now(),
                data={},
                error="Backup cannot be restored",
            )
            self._history.append(result)
            return result

        data = self.backup_manager.restore_data(
            backup_id
        )

        try:
            if self.restore_callback is not None:
                self.restore_callback(
                    dict(data)
                )

            result = RecoveryResult(
                backup_id=backup.backup_id,
                version=backup.version,
                status="restored",
                restored_at=datetime.now(),
                data=data,
            )

        except Exception as exc:
            result = RecoveryResult(
                backup_id=backup.backup_id,
                version=backup.version,
                status="failed",
                restored_at=datetime.now(),
                data={},
                error=str(exc),
            )

        self._history.append(result)
        return result

    def restore_version(
        self,
        version: str,
    ) -> RecoveryResult:
        backup = self.backup_manager.get_by_version(
            version
        )

        if backup is None:
            result = RecoveryResult(
                backup_id="unknown",
                version=version,
                status="failed",
                restored_at=datetime.now(),
                data={},
                error="Version not found",
            )
            self._history.append(result)
            return result

        return self.restore(
            backup.backup_id
        )

    def latest_backup_id(self) -> str | None:
        latest = self.backup_manager.latest()

        if latest is None:
            return None

        return latest.backup_id

    def can_restore(
        self,
        backup_id: str,
    ) -> bool:
        return self.backup_manager.can_restore(
            backup_id
        )

    def get_history(
        self,
    ) -> list[RecoveryResult]:
        return list(self._history)

    def last_recovery(
        self,
    ) -> RecoveryResult | None:
        if not self._history:
            return None

        return self._history[-1]

    def status(self) -> dict[str, Any]:
        last = self.last_recovery()

        return {
            "recoveries": len(self._history),
            "last_recovery": (
                last.to_dict()
                if last
                else None
            ),
            "latest_backup_id": (
                self.latest_backup_id()
            ),
        }
