from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class TelegramEvent:
    event_id: str
    bot_name: str
    chat_id: str
    event_type: str
    created_at: datetime

    @classmethod
    def create(
        cls,
        bot_name: str,
        chat_id: str,
        event_type: str,
    ) -> "TelegramEvent":
        return cls(
            event_id=str(uuid4()),
            bot_name=bot_name,
            chat_id=chat_id,
            event_type=event_type,
            created_at=datetime.now(timezone.utc),
        )

    def is_valid(self) -> bool:
        return bool(
            self.event_id.strip()
            and self.bot_name.strip()
            and self.chat_id.strip()
            and self.event_type.strip()
        )
