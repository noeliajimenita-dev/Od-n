from enum import Enum


class Worker4Status(str, Enum):
    IDLE = "idle"
    WORKING = "working"
    PAUSED = "paused"
    STOPPED = "stopped"


class Worker4StatusManager:
    def __init__(self):
        self._status = Worker4Status.IDLE

    @property
    def status(self) -> Worker4Status:
        return self._status

    def set_status(self, status: Worker4Status) -> None:
        if not isinstance(status, Worker4Status):
            raise ValueError("Invalid worker status")

        self._status = status

    def is_available(self) -> bool:
        return self._status == Worker4Status.IDLE

    def is_working(self) -> bool:
        return self._status == Worker4Status.WORKING

    def is_paused(self) -> bool:
        return self._status == Worker4Status.PAUSED

    def is_stopped(self) -> bool:
        return self._status == Worker4Status.STOPPED
