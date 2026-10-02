from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class ServiceStatus:
    name: str
    active: bool = False
    enabled: bool = False
    message: str = ""


class OdinServiceManager:
    def __init__(
        self,
        service_name: str = "odin",
        command_runner: Callable[[list[str]], int] | None = None,
    ) -> None:
        self.service_name = service_name
        self.command_runner = command_runner
        self._active = False
        self._enabled = False

    def _run(self, action: str) -> int:
        if self.command_runner is None:
            return 0

        return self.command_runner(
            ["systemctl", action, self.service_name]
        )

    def start(self) -> bool:
        result = self._run("start")

        if result == 0:
            self._active = True
            return True

        return False

    def stop(self) -> bool:
        result = self._run("stop")

        if result == 0:
            self._active = False
            return True

        return False

    def restart(self) -> bool:
        result = self._run("restart")

        if result == 0:
            self._active = True
            return True

        return False

    def enable(self) -> bool:
        result = self._run("enable")

        if result == 0:
            self._enabled = True
            return True

        return False

    def disable(self) -> bool:
        result = self._run("disable")

        if result == 0:
            self._enabled = False
            return True

        return False

    def status(self) -> ServiceStatus:
        return ServiceStatus(
            name=self.service_name,
            active=self._active,
            enabled=self._enabled,
            message=(
                "Service is active"
                if self._active
                else "Service is inactive"
            ),
      )
