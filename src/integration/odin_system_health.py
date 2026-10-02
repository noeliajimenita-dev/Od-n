from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class HealthCheck:
    name: str
    healthy: bool
    details: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "healthy": self.healthy,
            "details": self.details,
        }


@dataclass
class OdinHealthReport:
    healthy: bool
    ready: bool
    timestamp: str
    checks: list[HealthCheck] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "healthy": self.healthy,
            "ready": self.ready,
            "timestamp": self.timestamp,
            "checks": [check.to_dict() for check in self.checks],
        }


class OdinSystemHealth:
    """
    Realiza comprobaciones de salud y preparación de ODIN.

    No modifica componentes ni ejecuta trabajos reales.
    """

    def check(self, system: Any) -> OdinHealthReport:
        checks: list[HealthCheck] = []

        if system is None:
            checks.append(
                HealthCheck(
                    name="system",
                    healthy=False,
                    details="ODIN system is not configured",
                )
            )

            return OdinHealthReport(
                healthy=False,
                ready=False,
                timestamp=datetime.now().isoformat(),
                checks=checks,
            )

        checks.append(self._check_component(system, "runtime"))
        checks.append(self._check_component(system, "logs"))
        checks.append(self._check_component(system, "backups"))
        checks.append(self._check_component(system, "recovery"))

        checks.append(
            self._check_optional_component(
                system,
                "execution_service",
            )
        )

        checks.append(
            self._check_optional_component(
                system,
                "ai_service",
            )
        )

        checks.append(
            self._check_optional_component(
                system,
                "platform_manager",
            )
        )

        required_checks = [
            check
            for check in checks
            if check.name in {
                "runtime",
                "logs",
                "backups",
                "recovery",
            }
        ]

        healthy = all(check.healthy for check in required_checks)

        execution_configured = (
            getattr(system, "execution_service", None) is not None
        )

        ready = healthy and execution_configured

        return OdinHealthReport(
            healthy=healthy,
            ready=ready,
            timestamp=datetime.now().isoformat(),
            checks=checks,
        )

    def is_healthy(self, system: Any) -> bool:
        return self.check(system).healthy

    def is_ready(self, system: Any) -> bool:
        return self.check(system).ready

    @staticmethod
    def _check_component(
        system: Any,
        component_name: str,
    ) -> HealthCheck:
        component = getattr(system, component_name, None)

        if component is None:
            return HealthCheck(
                name=component_name,
                healthy=False,
                details="Required component is missing",
            )

        status_method = getattr(component, "status", None)

        if not callable(status_method):
            return HealthCheck(
                name=component_name,
                healthy=False,
                details="Component does not provide status()",
            )

        try:
            status = status_method()

            return HealthCheck(
                name=component_name,
                healthy=True,
                details=f"Status available: {type(status).__name__}",
            )

        except Exception as exc:
            return HealthCheck(
                name=component_name,
                healthy=False,
                details=f"Status check failed: {exc}",
            )

    @staticmethod
    def _check_optional_component(
        system: Any,
        component_name: str,
    ) -> HealthCheck:
        component = getattr(system, component_name, None)

        if component is None:
            return HealthCheck(
                name=component_name,
                healthy=False,
                details="Optional component is not configured",
            )

        return HealthCheck(
            name=component_name,
            healthy=True,
            details="Component is configured",
)
