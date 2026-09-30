from enum import Enum


class Worker2Status(str, Enum):
    IDLE = "idle"
    WORKING = "working"
    PAUSED = "paused"
    STOPPED = "stopped"


class Worker2StatusManager:
    def __init__(self):
        self._status = Worker2Status.IDLE

    @property
    def status(self) -> Worker2Status:
        return self._status

    def set_status(self, status: Worker2Status) -> None:
        if not isinstance(status, Worker2Status):
            raise ValueError("Invalid worker status")

        self._status = status

    def is_available(self) -> bool:
        return self._status == Worker2Status.IDLE

    def is_working(self) -> bool:
        return self._status == Worker2Status.WORKING

    def is_paused(self) -> bool:
        return self._status == Worker2Status.PAUSED

    def is_stopped(self) -> bool:
        return self._status == Worker2Status.STOPPED
