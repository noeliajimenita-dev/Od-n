from enum import Enum


class Worker5Status(str, Enum):
    IDLE = "idle"
    WORKING = "working"
    PAUSED = "paused"
    STOPPED = "stopped"


class Worker5StatusManager:
    def __init__(self):
        self._status = Worker5Status.IDLE

    @property
    def status(self) -> Worker5Status:
        return self._status

    def set_status(self, status: Worker5Status) -> None:
        if not isinstance(status, Worker5Status):
            raise ValueError("Invalid worker status")

        self._status = status

    def is_available(self) -> bool:
        return self._status == Worker5Status.IDLE

    def is_working(self) -> bool:
        return self._status == Worker5Status.WORKING

    def is_paused(self) -> bool:
        return self._status == Worker5Status.PAUSED

    def is_stopped(self) -> bool:
        return self._status == Worker5Status.STOPPED
