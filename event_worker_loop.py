from .event_worker_runner import TelegramEventWorkerRunner


class TelegramEventWorkerLoop:
    def __init__(self, runner: TelegramEventWorkerRunner):
        self.runner = runner
        self.running = False

    def start(self) -> None:
        self.running = True

    def stop(self) -> None:
        self.running = False

    def run_cycle(self) -> int:
        if not self.running:
            return 0

        return self.runner.run_once()

    def is_running(self) -> bool:
        return self.running
