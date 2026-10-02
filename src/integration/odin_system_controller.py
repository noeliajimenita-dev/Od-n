from __future__ import annotations

from datetime import datetime
from typing import Any

from src.integration.odin_system import OdinSystem
from src.integration.odin_system_validator import OdinSystemValidator


class OdinSystemController:
    """
    Punto de control central para las operaciones de ODIN.

    El controller no implementa la lógica de cada componente.
    Coordina las operaciones a través de OdinSystem.
    """

    def __init__(
        self,
        system: OdinSystem,
        validator: OdinSystemValidator | None = None,
    ) -> None:
        self.system = system
        self.validator = validator or OdinSystemValidator()

    def validate(self) -> dict[str, Any]:
        result = self.validator.validate(self.system)
        return result.to_dict()

    def start(self) -> dict[str, Any]:
        self.validator.assert_valid(self.system)

        self.system.start()

        return {
            "success": True,
            "action": "start",
            "status": self.system.status(),
        }

    def pause(self) -> dict[str, Any]:
        self.system.pause()

        return {
            "success": True,
            "action": "pause",
            "status": self.system.status(),
        }

    def resume(self) -> dict[str, Any]:
        self.system.resume()

        return {
            "success": True,
            "action": "resume",
            "status": self.system.status(),
        }

    def stop(self) -> dict[str, Any]:
        self.system.stop()

        return {
            "success": True,
            "action": "stop",
            "status": self.system.status(),
        }

    def run_once(
        self,
        current_datetime: datetime | None = None,
    ) -> dict[str, Any]:
        return self.system.run_once(current_datetime)

    def execute_task(self, task: Any) -> Any:
        return self.system.execute_task(task)

    def execute_task_with_ai(self, task: Any) -> Any:
        return self.system.execute_task_with_ai(task)

    def create_backup(
        self,
        backup_id: str,
        version: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.system.create_backup(
            backup_id=backup_id,
            version=version,
            data=data,
        )

    def restore(self, backup_id: str) -> dict[str, Any]:
        return self.system.restore(backup_id)

    def status(
        self,
        current_datetime: datetime | None = None,
    ) -> dict[str, Any]:
        return self.system.status(current_datetime)

    def register_bot(self, schedule: Any) -> dict[str, Any]:
        self.system.register_bot(schedule)

        return {
            "success": True,
            "action": "register_bot",
            "status": self.system.status(),
      }
