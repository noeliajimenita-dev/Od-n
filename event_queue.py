from collections import deque

from .telegram_event import TelegramEvent


class TelegramEventQueue:
    def __init__(self):
        self._queue: deque[TelegramEvent] = deque()

    def enqueue(self, event: TelegramEvent) -> None:
        if not event.is_valid():
            raise ValueError("No se puede agregar un evento inválido.")

        self._queue.append(event)

    def dequeue(self) -> TelegramEvent | None:
        if not self._queue:
            return None

        return self._queue.popleft()

    def size(self) -> int:
        return len(self._queue)

    def is_empty(self) -> bool:
        return not self._queue

    def clear(self) -> None:
        self._queue.clear()
