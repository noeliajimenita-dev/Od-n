from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable

from src.deployment.odin_startup import OdinStartup


@dataclass
class ProcessStatus:
    running: bool
    iterations: int
    failures: int
    last_error: str | None
    started_at: str | None
    last_iteration_at: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "running": self.running,
            "iterations": self.iterations,
            "failures": self.failures,
            "last_error": self.last_error,
            "started_at": self.started_at,
            "last_iteration_at": self.last_iteration_at,
        }


class OdinProcessManager:
    """
    Gestiona el ciclo de vida del proceso principal de ODIN.

    No implementa un daemon del sistema operativo.
    Proporciona el ciclo que posteriormente puede ser ejecutado
    por systemd, Docker u otro supervisor de procesos.
    """

    def __init__(
        self,
        startup: OdinStartup,
        interval_seconds: int = 30,
        sleep_function: Callable[[float], None] = time.sleep,
    ) -> None:
        if interval_seconds <= 0:
            raise ValueError(
                "interval_seconds must be greater than zero"
            )

        self.startup = startup
        self.interval_seconds = interval_seconds
        self.sleep_function = sleep_function

        self._running = False
        self._iterations = 0
        self._failures = 0
        self._last_error: str | None = None
        self._started_at: str | None = None
        self._last_iteration_at: str | None = None

    def start(self) -> dict[str, Any]:
        self.startup.start()

        self._running = True
        self._started_at = datetime.now().isoformat()
        self._last_error = None

        return self.status()

    def stop(self) -> dict[str, Any]:
        self._running = False

        try:
            self.startup.stop()
        except Exception as exc:
            self._last_error = str(exc)
            self._failures += 1

        return self.status()

    def run_once(self) -> dict[str, Any]:
        if not self._running:
            raise RuntimeError(
                "ODIN process is not running"
            )

        try:
            result = self.startup.system.run_once()

            self._iterations += 1
            self._last_iteration_at = (
                datetime.now().isoformat()
            )
            self._last_error = None

            return {
                "success": True,
                "result": result,
            }

        except Exception as exc:
            self._failures += 1
            self._last_error = str(exc)
            self._last_iteration_at = (
                datetime.now().isoformat()
            )

            return {
                "success": False,
                "error": str(exc),
            }

    def run_forever(
        self,
        max_iterations: int | None = None,
    ) -> dict[str, Any]:
        """
        Ejecuta el ciclo continuo.

        max_iterations existe principalmente para tests,
        simulaciones y ejecución controlada.
        """

        if not self._running:
            self.start()

        while self._running:
            self.run_once()

            if (
                max_iterations is not None
                and self._iterations >= max_iterations
            ):
                break

            self.sleep_function(
                self.interval_seconds
            )

        return self.status()

    def restart(self) -> dict[str, Any]:
        self.stop()
        return self.start()

    def status(self) -> dict[str, Any]:
        process_status = ProcessStatus(
            running=self._running,
            iterations=self._iterations,
            failures=self._failures,
            last_error=self._last_error,
            started_at=self._started_at,
            last_iteration_at=self._last_iteration_at,
        )

        return {
            "process": process_status.to_dict(),
            "interval_seconds": self.interval_seconds,
            "restart_on_failure": (
                self.startup
                .deployment_config
                .restart_on_failure
            ),
            "run_24_7": (
                self.startup
                .deployment_config
                .run_24_7
            ),
      }
