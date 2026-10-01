from typing import Any

from .secure_connection_interface import (
    SecureConnectionInterface,
    SecureConnectionRequest,
)


class SecureConnectionInterfaceService:
    """
    Service layer for secure external-account connection requests.

    Credentials must be entered through the secure interface itself,
    never through Telegram messages or this service.
    """

    def __init__(
        self,
        interface: SecureConnectionInterface | None = None,
    ) -> None:
        self.interface = interface or SecureConnectionInterface()

    def create_connection_request(
        self,
        request_id: str,
        service: str,
        username: str,
        interface_token: str,
    ) -> SecureConnectionRequest:
        return self.interface.create_request(
            request_id=request_id,
            service=service,
            username=username,
            interface_token=interface_token,
        )

    def get_request(
        self,
        request_id: str,
    ) -> SecureConnectionRequest | None:
        return self.interface.get_request(request_id)

    def complete_request(
        self,
        request_id: str,
    ) -> SecureConnectionRequest:
        return self.interface.complete_request(request_id)

    def cancel_request(
        self,
        request_id: str,
    ) -> SecureConnectionRequest:
        return self.interface.cancel_request(request_id)

    def has_request(self, request_id: str) -> bool:
        return self.interface.has_request(request_id)

    def get_status(self, request_id: str) -> dict[str, Any]:
        request = self.get_request(request_id)

        if request is None:
            return {
                "request_id": request_id,
                "exists": False,
                "status": "not_found",
            }

        return {
            "request_id": request.request_id,
            "service": request.service,
            "username": request.username,
            "status": request.status,
            "exists": True,
  }
