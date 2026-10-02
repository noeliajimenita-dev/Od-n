from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class OdinBackup:
    backup_id: str
    version: str
    created_at: datetime
    data: dict[str, Any] = field(default_factory=dict)
    protected: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "backup_id": self.backup_id,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "data": dict(self.data),
            "protected": self.protected,
        }


class OdinBackupManager:
    """
    Gestor de backups de ODIN.

    Reglas principales:
    - Cada backup tiene un identificador y versión.
    - El backup más reciente queda protegido.
    - No se permite eliminar todos los backups.
    - Se puede recuperar un backup por ID o versión.
    """

    def __init__(self) -> None:
        self._backups: dict[str, OdinBackup] = {}

    def create_backup(
        self,
        backup_id: str,
        version: str,
        data: dict[str, Any] | None = None,
        protected: bool = False,
    ) -> OdinBackup:
        if not backup_id or not backup_id.strip():
            raise ValueError(
                "backup_id cannot be empty"
            )

        if not version or not version.strip():
            raise ValueError(
                "version cannot be empty"
            )

        if backup_id in self._backups:
            raise ValueError(
                f"Backup already exists: {backup_id}"
            )

        backup = OdinBackup(
            backup_id=backup_id,
            version=version,
            created_at=datetime.now(),
            data=dict(data or {}),
            protected=protected,
        )

        self._backups[backup_id] = backup
        self._protect_latest()

        return backup

    def get(
        self,
        backup_id: str,
    ) -> OdinBackup | None:
        return self._backups.get(backup_id)

    def get_by_version(
        self,
        version: str,
    ) -> OdinBackup | None:
        matches = [
            backup
            for backup in self._backups.values()
            if backup.version == version
        ]

        if not matches:
            return None

        return max(
            matches,
            key=lambda backup: backup.created_at,
        )

    def latest(self) -> OdinBackup | None:
        if not self._backups:
            return None

        return max(
            self._backups.values(),
            key=lambda backup: backup.created_at,
        )

    def list_backups(self) -> list[OdinBackup]:
        return sorted(
            self._backups.values(),
            key=lambda backup: backup.created_at,
            reverse=True,
        )

    def delete(
        self,
        backup_id: str,
    ) -> bool:
        backup = self._backups.get(backup_id)

        if backup is None:
            return False

        if backup.protected:
            raise PermissionError(
                "Protected backup cannot be deleted"
            )

        if len(self._backups) <= 1:
            raise PermissionError(
                "ODIN must keep at least one backup"
            )

        del self._backups[backup_id]
        self._protect_latest()

        return True

    def protect(
        self,
        backup_id: str,
    ) -> None:
        backup = self._require(backup_id)
        backup.protected = True

    def unprotect(
        self,
        backup_id: str,
    ) -> None:
        backup = self._require(backup_id)

        if backup == self.latest():
            raise PermissionError(
                "Latest backup must remain protected"
            )

        backup.protected = False

    def has_backup(
        self,
        backup_id: str,
    ) -> bool:
        return backup_id in self._backups

    def count(self) -> int:
        return len(self._backups)

    def can_restore(
        self,
        backup_id: str,
    ) -> bool:
        return backup_id in self._backups

    def restore_data(
        self,
        backup_id: str,
    ) -> dict[str, Any]:
        backup = self._require(backup_id)
        return dict(backup.data)

    def status(self) -> dict[str, Any]:
        latest = self.latest()

        return {
            "total_backups": len(self._backups),
            "latest_backup": (
                latest.backup_id
                if latest
                else None
            ),
            "latest_version": (
                latest.version
                if latest
                else None
            ),
            "protected_backups": [
                backup.backup_id
                for backup in self._backups.values()
                if backup.protected
            ],
        }

    def _protect_latest(self) -> None:
        latest = self.latest()

        if latest is None:
            return

        latest.protected = True

    def _require(
        self,
        backup_id: str,
    ) -> OdinBackup:
        backup = self.get(backup_id)

        if backup is None:
            raise KeyError(
                f"Backup not found: {backup_id}"
            )

        return backup
