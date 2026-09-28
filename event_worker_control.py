from .event_worker_loop import TelegramEventWorkerLoop


class TelegramEventWorkerControl:
    def __init__(self, worker_loop: TelegramEventWorkerLoop):
        self.worker_loop = worker_loop

    def start(self) -> None:
        self.worker_loop.start()

    def stop(self) -> None:
        self.worker_loop.stop()

    def run_cycle(self) -> int:
        return self.worker_loop.run_cycle()

    def is_running(self) -> bool:
        return self.worker_loop.is_running()

    def status(self) -> dict:
        return {
            "running": self.is_running(),
        }
