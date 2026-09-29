from dataclasses import dataclass
from enum import Enum


class ConnectionCommand(str, Enum):
    CONNECT = "CONNECT"
    DISCONNECT = "DISCONNECT"
    RECOVER = "RECOVER"
    STATUS = "STATUS"


@dataclass(frozen=True)
class ConnectionCommandRequest:
    command: ConnectionCommand
    bot_name: str | None = None

    def requires_bot(self) -> bool:
        return self.command in {
            ConnectionCommand.CONNECT,
            ConnectionCommand.DISCONNECT,
            ConnectionCommand.RECOVER,
        }
