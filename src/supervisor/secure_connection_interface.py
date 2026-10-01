from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SecureConnectionRequest:
    request_id: str
    service: str
    username: str
    interface_token: str
    status: str = "pending"

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "service": self.service,
            "username": self.username,
            "interface_token": self.interface_token,
            "status": self.status,
        }


class SecureConnectionInterface:
    """
    Backend contract for a secure external-account connection interface.

    This class does not collect passwords through Telegram and does not
    implement the web UI itself. It creates the data required by a secure
    credential-entry interface.
    """

    def __init__(self) -> None:
        self._requests: dict[str, SecureConnectionRequest] = {}

    def create_request(
        self,
        request_id: str,
        service: str,
        username: str,
        interface_token: str,
    ) -> SecureConnectionRequest:
        if not request_id:
            raise ValueError("request_id cannot be empty")
        if not service:
            raise ValueError("service cannot be empty")
        if not username:
            raise ValueError("username cannot be empty")
        if not interface_token:
            raise ValueError("interface_token cannot be empty")

        request = SecureConnectionRequest(
            request_id=request_id,
            service=service,
            username=username,
            interface_token=interface_token,
        )

        self._requests[request_id] = request
        return request

    def get_request(self, request_id: str) -> SecureConnectionRequest | None:
        return self._requests.get(request_id)

    def complete_request(self, request_id: str) -> SecureConnectionRequest:
        request = self._requests.get(request_id)

        if request is None:
            raise ValueError(f"Connection request not found: {request_id}")

        completed = SecureConnectionRequest(
            request_id=request.request_id,
            service=request.service,
            username=request.username,
            interface_token=request.interface_token,
            status="completed",
        )

        self._requests[request_id] = completed
        return completed

    def cancel_request(self, request_id: str) -> SecureConnectionRequest:
        request = self._requests.get(request_id)

        if request is None:
            raise ValueError(f"Connection request not found: {request_id}")

        cancelled = SecureConnectionRequest(
            request_id=request.request_id,
            service=request.service,
            username=request.username,
            interface_token=request.interface_token,
            status="cancelled",
        )

        self._requests[request_id] = cancelled
        return cancelled

    def has_request(self, request_id: str) -> bool:
        return request_id in self._requests
