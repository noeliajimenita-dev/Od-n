from __future__ import annotations

from datetime import datetime
from typing import Any

from src.integration.odin_system import OdinSystem
from src.integration.odin_system_health import OdinSystemHealth
from src.integration.odin_system_validator import OdinSystemValidator


class OdinSystemReport:
    """
    Genera reportes operativos seguros del sistema ODIN.

    El reporte está pensado para Telegram, logs, diagnóstico
    y supervisión interna. Nunca incluye credenciales.
    """

    def __init__(
        self,
        health: OdinSystemHealth | None = None,
        validator: OdinSystemValidator | None = None,
    ) -> None:
        self.health = health or OdinSystemHealth()
        self.validator = validator or OdinSystemValidator()

    def generate(
        self,
        system: OdinSystem,
        current_datetime: datetime | None = None,
    ) -> dict[str, Any]:
        current = current_datetime or datetime.now()

        validation = self.validator.validate(system)
        health = self.health.check(system)
        status = system.status(current)

        return {
            "system": "ODIN",
            "timestamp": current.isoformat(),
            "healthy": health.healthy,
            "ready": health.ready,
            "validation": validation.to_dict(),
            "health": health.to_dict(),
            "runtime": self._safe_section(
                status.get("runtime")
            ),
            "backups": self._safe_section(
                status.get("backups")
            ),
            "recovery": self._safe_section(
                status.get("recovery")
            ),
            "platforms": list(
                status.get("platforms", [])
            ),
            "components": {
                "supervisor": bool(
                    status.get("supervisor_configured")
                ),
                "execution": bool(
                    status.get("execution_configured")
                ),
                "ai": bool(
                    status.get("ai_configured")
                ),
            },
        }

    def summary(
        self,
        system: OdinSystem,
        current_datetime: datetime | None = None,
    ) -> str:
        report = self.generate(
            system,
            current_datetime,
        )

        validation = report["validation"]
        health = report["health"]

        lines = [
            "ODIN SYSTEM REPORT",
            f"Healthy: {report['healthy']}",
            f"Ready: {report['ready']}",
            f"Validation: {validation['valid']}",
            f"Health: {health['healthy']}",
        ]

        errors = validation.get("errors", [])
        warnings = validation.get("warnings", [])

        if errors:
            lines.append(
                f"Errors: {len(errors)}"
            )

        if warnings:
            lines.append(
                f"Warnings: {len(warnings)}"
            )

        components = report["components"]

        lines.extend(
            [
                f"Supervisor: {components['supervisor']}",
                f"Execution: {components['execution']}",
                f"AI: {components['ai']}",
                f"Platforms: {len(report['platforms'])}",
            ]
        )

        return "\n".join(lines)

    @staticmethod
    def _safe_section(
        value: Any,
    ) -> dict[str, Any] | list[Any] | str | None:
        """
        Filtra estructuras de estado para impedir que secretos
        sean incluidos accidentalmente en reportes.
        """

        if value is None:
            return None

        if isinstance(value, dict):
            safe: dict[str, Any] = {}

            blocked = {
                "password",
                "token",
                "api_key",
                "apikey",
                "secret",
                "credential",
                "credentials",
                "private_key",
                "authorization",
            }

            for key, item in value.items():
                key_lower = str(key).lower()

                if any(
                    blocked_word in key_lower
                    for blocked_word in blocked
                ):
                    safe[key] = "[REDACTED]"
                    continue

                safe[key] = OdinSystemReport._safe_value(item)

            return safe

        if isinstance(value, list):
            return [
                OdinSystemReport._safe_value(item)
                for item in value
            ]

        return value

    @staticmethod
    def _safe_value(value: Any) -> Any:
        if isinstance(value, dict):
            return OdinSystemReport._safe_section(value)

        if isinstance(value, list):
            return [
                OdinSystemReport._safe_value(item)
                for item in value
            ]

        return value
