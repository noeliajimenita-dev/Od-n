from enum import Enum


class Worker3Status(str, Enum):
    IDLE = "idle"
    WORKING = "working"
    PAUSED = "paused"
    STOPPED = "stopped"


class Worker3StatusManager:
    def __init__(self):
        self._status = Worker3Status.IDLE

    @property
    def status(self) -> Worker3Status:
        return self._status

    def set_status(self, status: Worker3Status) -> None:
        if not isinstance(status, Worker3Status):
            raise ValueError("Invalid worker status")

        self._status = status

    def is_available(self) -> bool:
        return self._status == Worker3Status.IDLE

    def is_working(self) -> bool:
        return self._status == Worker3Status.WORKING

    def is_paused(self) -> bool:
        return self._status == Worker3Status.PAUSED

    def is_stopped(self) -> bool:
        return self._status == Worker3Status.STOPPED
