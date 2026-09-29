from dataclasses import dataclass


@dataclass(frozen=True)
class ConnectionCommandResult:
    success: bool
    message: str
    bot_name: str | None = None

    @classmethod
    def ok(
        cls,
        message: str,
        bot_name: str | None = None,
    ) -> "ConnectionCommandResult":
        return cls(
            success=True,
            message=message,
            bot_name=bot_name,
        )

    @classmethod
    def error(
        cls,
        message: str,
        bot_name: str | None = None,
    ) -> "ConnectionCommandResult":
        return cls(
            success=False,
            message=message,
            bot_name=bot_name,
        )
