from .event_queue import TelegramEventQueue
from .event_processor import TelegramEventProcessor


class TelegramEventWorker:
    def __init__(
        self,
        queue: TelegramEventQueue,
        processor: TelegramEventProcessor,
    ):
        self.queue = queue
        self.processor = processor

    def process_next(self):
        event = self.queue.dequeue()

        if event is None:
            return None

        return self.processor.process(event)

    def process_all(self) -> list:
        results = []

        while not self.queue.is_empty():
            result = self.process_next()
            results.append(result)

        return results
