from enum import Enum


class TelegramEventType(str, Enum):
    MESSAGE = "message"
    COMMAND = "command"
    CALLBACK = "callback"
    ERROR = "error"
    STATUS = "status"
    CONNECTION = "connection"


def is_valid_event_type(event_type: str) -> bool:
    return event_type.strip().lower() in {
        event.value for event in TelegramEventType
    }
