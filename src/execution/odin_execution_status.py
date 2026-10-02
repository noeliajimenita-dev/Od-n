from __future__ import annotations

from typing import Any

from .supervisor_execution_orchestrator import (
    SupervisorExecutionOrchestrator,
)


class OdinExecutionStatus:
    """Proporciona el estado consolidado del sistema de ejecución."""

    def __init__(
        self,
        orchestrator: SupervisorExecutionOrchestrator,
    ) -> None:
        if orchestrator is None:
            raise ValueError("orchestrator cannot be None")

        self.orchestrator = orchestrator

    def get_status(self) -> dict[str, Any]:
        status = self.orchestrator.status()

        return {
            "execution": status.get("execution", {}),
            "results": status.get("results", {}),
            "ready": self.is_ready(),
        }

    def worker_status(self) -> dict[str, Any]:
        execution = self.orchestrator.status().get(
            "execution",
            {},
        )

        coordinator = execution.get(
            "worker_coordinator",
            {},
        )

        return coordinator

    def result_status(self) -> dict[str, Any]:
        return self.orchestrator.summary()

    def successful_count(self) -> int:
        return self.orchestrator.result_service.count_successful()

    def failed_count(self) -> int:
        return self.orchestrator.result_service.count_failed()

    def total_count(self) -> int:
        return self.orchestrator.result_service.count()

    def is_ready(self) -> bool:
        try:
            status = self.orchestrator.status()

            execution = status.get(
                "execution",
                {},
            )

            return bool(execution)

        except Exception:
            return False

    def has_failures(self) -> bool:
        return self.failed_count() > 0

    def summary(self) -> dict[str, Any]:
        return {
            "ready": self.is_ready(),
            "total_executions": self.total_count(),
            "successful": self.successful_count(),
            "failed": self.failed_count(),
            "has_failures": self.has_failures(),
            "workers": self.worker_status(),
        }

    def __repr__(self) -> str:
        return (
            "OdinExecutionStatus("
            f"ready={self.is_ready()}, "
            f"executions={self.total_count()}"
            ")"
      )
