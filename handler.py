from abc import ABC, abstractmethod

from .command import TelegramCommand
from .message import TelegramMessage
from .response import TelegramResponse


class TelegramHandler(ABC):

    @abstractmethod
    def handle_message(
        self,
        message: TelegramMessage,
    ) -> TelegramResponse:
        """Procesa un mensaje recibido de Telegram."""
        raise NotImplementedError

    @abstractmethod
    def handle_command(
        self,
        command: TelegramCommand,
    ) -> TelegramResponse:
        """Procesa un comando recibido de Telegram."""
        raise NotImplementedError
