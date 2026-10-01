from collections.abc import Callable
from typing import Any


class ExternalAccountExecutorRepository:
    """Repository for external account operation handlers."""

    def __init__(self) -> None:
        self._handlers: dict[
            str,
            Callable[[Any, Any], Any],
        ] = {}

    def register(
        self,
        action: str,
        handler: Callable[[Any, Any], Any],
    ) -> None:
        if not action.strip():
            raise ValueError("action cannot be empty")

        if not callable(handler):
            raise ValueError("handler must be callable")

        self._handlers[action] = handler

    def get(
        self,
        action: str,
    ) -> Callable[[Any, Any], Any] | None:
        return self._handlers.get(action)

    def exists(self, action: str) -> bool:
        return action in self._handlers

    def delete(self, action: str) -> bool:
        if action not in self._handlers:
            return False

        del self._handlers[action]
        return True

    def list_actions(self) -> list[str]:
        return list(self._handlers.keys())

    def count(self) -> int:
        return len(self._handlers)

    def clear(self) -> None:
        self._handlers.clear()
