from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class TelegramMessage:
    chat_id: str
    text: str
    bot_name: str
    received_at: datetime

    @classmethod
    def create(
        cls,
        chat_id: str,
        text: str,
        bot_name: str,
    ) -> "TelegramMessage":
        return cls(
            chat_id=chat_id,
            text=text,
            bot_name=bot_name,
            received_at=datetime.now(timezone.utc),
        )

    def is_empty(self) -> bool:
        return not self.text.strip()
