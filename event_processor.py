from .telegram_event import TelegramEvent
from .telegram_event_router import TelegramEventRouter


class TelegramEventProcessor:
    def __init__(self, router: TelegramEventRouter):
        self.router = router

    def process(self, event: TelegramEvent):
        if not event.is_valid():
            raise ValueError("El evento de Telegram no es válido.")

        return self.router.dispatch(event)
