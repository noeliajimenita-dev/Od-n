from dataclasses import dataclass


@dataclass(frozen=True)
class TelegramCommand:
    name: str
    arguments: tuple[str, ...] = ()

    @classmethod
    def parse(cls, text: str) -> "TelegramCommand | None":
        text = text.strip()

        if not text.startswith("/"):
            return None

        parts = text.split()
        name = parts[0][1:].lower()

        if not name:
            return None

        return cls(
            name=name,
            arguments=tuple(parts[1:]),
        )

    def has_arguments(self) -> bool:
        return bool(self.arguments)
