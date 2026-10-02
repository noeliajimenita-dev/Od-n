from __future__ import annotations

import json
from typing import Any
from urllib import error, parse, request


class TelegramHTTPTransport:
    """
    Transporte HTTP mínimo para Telegram Bot API.

    No almacena tokens. El token se recibe únicamente cuando se
    ejecuta una operación.
    """

    API_BASE = "https://api.telegram.org"

    def __init__(
        self,
        timeout: float = 30.0,
        api_base: str | None = None,
    ) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        self.timeout = timeout
        self.api_base = (
            api_base.rstrip("/")
            if api_base
            else self.API_BASE
        )

    def send_message(
        self,
        token: str,
        chat_id: str,
        text: str,
    ) -> dict[str, Any]:
        """Envía un mensaje mediante sendMessage."""
        self._validate_token(token)

        if not chat_id or not str(chat_id).strip():
            raise ValueError("chat_id cannot be empty")

        if not text or not text.strip():
            raise ValueError("text cannot be empty")

        return self._request(
            token=token,
            method="sendMessage",
            payload={
                "chat_id": str(chat_id),
                "text": text,
            },
        )

    def get_updates(
        self,
        token: str,
        offset: int | None = None,
        timeout: int = 0,
    ) -> list[dict[str, Any]]:
        """
        Obtiene actualizaciones pendientes de Telegram.

        El timeout aquí corresponde al parámetro de Telegram y no
        sustituye al timeout HTTP del transporte.
        """
        self._validate_token(token)

        if timeout < 0:
            raise ValueError("timeout cannot be negative")

        payload: dict[str, Any] = {
            "timeout": timeout,
        }

        if offset is not None:
            payload["offset"] = offset

        response = self._request(
            token=token,
            method="getUpdates",
            payload=payload,
        )

        result = response.get("result", [])

        if not isinstance(result, list):
            raise RuntimeError(
                "Telegram returned an invalid updates payload"
            )

        return result

    def get_me(
        self,
        token: str,
    ) -> dict[str, Any]:
        """Verifica el token consultando getMe."""
        self._validate_token(token)

        return self._request(
            token=token,
            method="getMe",
            payload={},
        )

    def _request(
        self,
        token: str,
        method: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Ejecuta una petición POST contra Telegram.

        Los errores HTTP y respuestas inválidas se convierten en
        excepciones controladas.
        """
        url = (
            f"{self.api_base}/bot"
            f"{parse.quote(token, safe='')}/"
            f"{method}"
        )

        body = json.dumps(payload).encode("utf-8")

        http_request = request.Request(
            url=url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(
                http_request,
                timeout=self.timeout,
            ) as response:
                raw_response = response.read().decode("utf-8")

        except error.HTTPError as exc:
            raise RuntimeError(
                f"Telegram HTTP error: {exc.code}"
            ) from exc

        except error.URLError as exc:
            raise RuntimeError(
                f"Telegram connection error: {exc.reason}"
            ) from exc

        except TimeoutError as exc:
            raise RuntimeError(
                "Telegram request timed out"
            ) from exc

        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Telegram returned invalid JSON"
            ) from exc

        if not isinstance(data, dict):
            raise RuntimeError(
                "Telegram returned an invalid response"
            )

        if data.get("ok") is not True:
            description = data.get(
                "description",
                "Telegram request failed",
            )

            error_code = data.get("error_code")

            if error_code is not None:
                raise RuntimeError(
                    f"Telegram API error {error_code}: "
                    f"{description}"
                )

            raise RuntimeError(
                f"Telegram API error: {description}"
            )

        return data

    @staticmethod
    def _validate_token(token: str) -> None:
        """
        Valida únicamente presencia.

        Nunca registra ni transforma el token en mensajes de error.
        """
        if not token or not token.strip():
            raise ValueError("Telegram token cannot be empty")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(api_base={self.api_base!r}, "
            f"timeout={self.timeout})"
          )
