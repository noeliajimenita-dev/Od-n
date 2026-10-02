from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TelegramResponse:
    """Respuesta preparada para ser enviada a Telegram."""

    chat_id: str
    text: str
    success: bool = True
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "chat_id": self.chat_id,
            "text": self.text,
            "success": self.success,
            "metadata": self.metadata or {},
        }


class TelegramResponseBuilder:
    """Generador central de respuestas de ODIN."""

    def success(
        self,
        chat_id: str,
        message: str,
        **metadata: Any,
    ) -> TelegramResponse:
        return self._build(
            chat_id=chat_id,
            message=message,
            success=True,
            metadata=metadata,
        )

    def error(
        self,
        chat_id: str,
        message: str,
        **metadata: Any,
    ) -> TelegramResponse:
        return self._build(
            chat_id=chat_id,
            message=message,
            success=False,
            metadata=metadata,
        )

    def command_accepted(
        self,
        chat_id: str,
        command: str,
        message: str = "Command accepted.",
    ) -> TelegramResponse:
        return self.success(
            chat_id=chat_id,
            message=message,
            command=command,
        )

    def command_rejected(
        self,
        chat_id: str,
        command: str,
        reason: str,
    ) -> TelegramResponse:
        return self.error(
            chat_id=chat_id,
            message=f"Command rejected: {reason}",
            command=command,
        )

    def authorization_required(
        self,
        chat_id: str,
        action: str,
        reason: str,
        deadline_minutes: int | None = None,
    ) -> TelegramResponse:
        metadata: dict[str, Any] = {
            "action": action,
            "authorization_required": True,
        }

        if deadline_minutes is not None:
            metadata["deadline_minutes"] = deadline_minutes

        message = (
            "Authorization required.\n"
            f"Action: {action}\n"
            f"Reason: {reason}"
        )

        if deadline_minutes is not None:
            message += (
                f"\nTime limit: {deadline_minutes} minutes"
            )

        return self.success(
            chat_id=chat_id,
            message=message,
            **metadata,
        )

    def task_status(
        self,
        chat_id: str,
        task_id: str,
        status: str,
        detail: str | None = None,
    ) -> TelegramResponse:
        message = (
            f"Task: {task_id}\n"
            f"Status: {status}"
        )

        if detail:
            message += f"\n{detail}"

        return self.success(
            chat_id=chat_id,
            message=message,
            task_id=task_id,
            status=status,
        )

    def task_completed(
        self,
        chat_id: str,
        task_id: str,
        result: Any = None,
    ) -> TelegramResponse:
        message = (
            f"Task completed.\n"
            f"Task: {task_id}"
        )

        if result is not None:
            message += f"\nResult: {result}"

        return self.success(
            chat_id=chat_id,
            message=message,
            task_id=task_id,
            status="completed",
        )

    def task_failed(
        self,
        chat_id: str,
        task_id: str,
        error: str,
    ) -> TelegramResponse:
        return self.error(
            chat_id=chat_id,
            message=(
                f"Task failed.\n"
                f"Task: {task_id}\n"
                f"Error: {error}"
            ),
            task_id=task_id,
            status="failed",
        )

    def paused(
        self,
        chat_id: str,
        reason: str = "Pause requested by user.",
    ) -> TelegramResponse:
        return self.success(
            chat_id=chat_id,
            message=f"ODIN paused.\n{reason}",
            status="paused",
        )

    def resumed(
        self,
        chat_id: str,
    ) -> TelegramResponse:
        return self.success(
            chat_id=chat_id,
            message="ODIN resumed.",
            status="running",
        )

    def _build(
        self,
        chat_id: str,
        message: str,
        success: bool,
        metadata: dict[str, Any],
    ) -> TelegramResponse:
        if not chat_id or not str(chat_id).strip():
            raise ValueError("chat_id cannot be empty")

        if not message or not message.strip():
            raise ValueError("message cannot be empty")

        return TelegramResponse(
            chat_id=str(chat_id),
            text=message.strip(),
            success=success,
            metadata=metadata,
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
