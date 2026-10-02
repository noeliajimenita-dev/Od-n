from __future__ import annotations

from datetime import datetime
from typing import Any

from src.runtime.odin_runtime_manager import OdinRuntimeManager
from src.runtime.odin_backup import OdinBackupManager
from src.runtime.odin_recovery import OdinRecoveryManager
from src.runtime.odin_log_service import OdinLogService


class OdinSystem:
    """
    Punto central de integración de ODIN.

    Esta clase no reemplaza los módulos existentes.
    Los coordina para que el sistema completo pueda
    iniciarse, ejecutarse, pausarse, respaldarse
    y consultar su estado desde una única interfaz.
    """

    def __init__(
        self,
        runtime: OdinRuntimeManager | None = None,
        logs: OdinLogService | None = None,
        backups: OdinBackupManager | None = None,
        recovery: OdinRecoveryManager | None = None,
        supervisor: Any | None = None,
        execution_service: Any | None = None,
        ai_service: Any | None = None,
        platform_manager: Any | None = None,
    ) -> None:
        self.logs = logs or OdinLogService()

        self.runtime = runtime or OdinRuntimeManager(
            log_service=self.logs
        )

        self.backups = (
            backups or OdinBackupManager()
        )

        self.recovery = recovery or OdinRecoveryManager(
            backup_manager=self.backups
        )

        self.supervisor = supervisor
        self.execution_service = execution_service
        self.ai_service = ai_service
        self.platform_manager = platform_manager

        self._started = False

    def start(self) -> None:
        self.runtime.start()
        self._started = True

    def pause(self) -> None:
        self.runtime.pause()

    def resume(self) -> None:
        self.runtime.resume()

    def stop(self) -> None:
        self.runtime.stop()
        self._started = False

    def register_bot(
        self,
        schedule: Any,
    ) -> None:
        self.runtime.register_bot(schedule)

    def run_once(
        self,
        current_datetime: datetime | None = None,
    ) -> dict[str, Any]:
        return self.runtime.run_once(
            current_datetime
        )

    def create_backup(
        self,
        backup_id: str,
        version: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        backup = self.backups.create_backup(
            backup_id=backup_id,
            version=version,
            data=data or {},
        )

        return backup.to_dict()

    def restore(
        self,
        backup_id: str,
    ) -> dict[str, Any]:
        result = self.recovery.restore(
            backup_id
        )

        return result.to_dict()

    def execute_task(
        self,
        task: Any,
    ) -> Any:
        if self.execution_service is None:
            raise RuntimeError(
                "Execution service is not configured"
            )

        execute = getattr(
            self.execution_service,
            "execute",
            None,
        )

        if execute is None:
            raise RuntimeError(
                "Execution service has no execute method"
            )

        return execute(task)

    def execute_task_with_ai(
        self,
        task: Any,
    ) -> Any:
        if self.execution_service is None:
            raise RuntimeError(
                "Execution service is not configured"
            )

        execute = getattr(
            self.execution_service,
            "execute_with_ai",
            None,
        )

        if execute is None:
            raise RuntimeError(
                "AI execution is not configured"
            )

        if self.ai_service is None:
            raise RuntimeError(
                "AI service is not configured"
            )

        return execute(
            task,
            self.ai_service,
        )

    def get_platforms(self) -> list[str]:
        if self.platform_manager is None:
            return []

        list_platforms = getattr(
            self.platform_manager,
            "list_platforms",
            None,
        )

        if list_platforms is None:
            return []

        return list_platforms()

    def status(
        self,
        current_datetime: datetime | None = None,
    ) -> dict[str, Any]:
        current = (
            current_datetime
            or datetime.now()
        )

        return {
            "started": self._started,
            "timestamp": current.isoformat(),
            "runtime": self.runtime.status(
                current
            ),
            "backups": self.backups.status(),
            "recovery": self.recovery.status(),
            "platforms": self.get_platforms(),
            "supervisor_configured": (
                self.supervisor is not None
            ),
            "execution_configured": (
                self.execution_service is not None
            ),
            "ai_configured": (
                self.ai_service is not None
            ),
        }
