from enum import Enum


class Worker1Status(str, Enum):
    IDLE = "idle"
    WORKING = "working"
    PAUSED = "paused"
    STOPPED = "stopped"


class Worker1StatusManager:
    def __init__(self):
        self._status = Worker1Status.IDLE

    @property
    def status(self) -> Worker1Status:
        return self._status

    def set_status(self, status: Worker1Status) -> None:
        if not isinstance(status, Worker1Status):
            raise ValueError("Invalid worker status")

        self._status = status

    def is_available(self) -> bool:
        return self._status == Worker1Status.IDLE

    def is_working(self) -> bool:
        return self._status == Worker1Status.WORKING

    def is_paused(self) -> bool:
        return self._status == Worker1Status.PAUSED

    def is_stopped(self) -> bool:
        return self._status == Worker1Status.STOPPED
