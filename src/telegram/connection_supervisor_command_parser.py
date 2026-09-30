from .connection_supervisor_command_language import (
    ConnectionSupervisorCommandLanguage,
)


class ConnectionSupervisorCommandParser:
    def __init__(
        self,
        language: ConnectionSupervisorCommandLanguage,
    ):
        self.language = language

    def parse(self, message: str) -> str | None:
        return self.language.normalize(message)
