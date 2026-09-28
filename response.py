from dataclasses import dataclass


@dataclass(frozen=True)
class TelegramResponse:
    text: str
    bot_name: str
    success: bool = True

    def is_empty(self) -> bool:
        return not self.text.strip()

    @classmethod
    def success_response(
        cls,
        bot_name: str,
        text: str,
    ) -> "TelegramResponse":
        return cls(
            text=text,
            bot_name=bot_name,
            success=True,
        )

    @classmethod
    def error_response(
        cls,
        bot_name: str,
        text: str,
    ) -> "TelegramResponse":
        return cls(
            text=text,
            bot_name=bot_name,
            success=False,
    )
