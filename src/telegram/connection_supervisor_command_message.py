from dataclasses import dataclass


@dataclass(frozen=True)
class ConnectionSupervisorCommandMessage:
    raw_text: str
    command: str | None

    @property
    def is_valid(self) -> bool:
        return bool(self.command)
