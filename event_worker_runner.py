from .event_queue import TelegramEventQueue
from .event_processor import TelegramEventProcessor


class TelegramEventWorkerRunner:
    def __init__(
        self,
        queue: TelegramEventQueue,
        processor: TelegramEventProcessor,
    ):
        self.queue = queue
        self.processor = processor

    def run_once(self) -> int:
        processed = 0

        while not self.queue.is_empty():
            event = self.queue.dequeue()

            if event is None:
                break

            self.processor.process(event)
            processed += 1

        return processed
