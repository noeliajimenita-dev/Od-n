from typing import Any

from .authorization_request import AuthorizationRequest


class AuthorizationRepository:
    """Stores and manages authorization requests."""

    def __init__(self) -> None:
        self._requests: dict[str, AuthorizationRequest] = {}

    def save(self, request: AuthorizationRequest) -> None:
        if not isinstance(request, AuthorizationRequest):
            raise TypeError("request must be an AuthorizationRequest")

        self._requests[request.request_id] = request

    def get(self, request_id: str) -> AuthorizationRequest | None:
        return self._requests.get(request_id)

    def exists(self, request_id: str) -> bool:
        return request_id in self._requests

    def update(self, request: AuthorizationRequest) -> None:
        if not self.exists(request.request_id):
            raise KeyError(f"Authorization request not found: {request.request_id}")

        self._requests[request.request_id] = request

    def delete(self, request_id: str) -> None:
        self._requests.pop(request_id, None)

    def list_all(self) -> list[AuthorizationRequest]:
        return list(self._requests.values())

    def list_pending(self) -> list[AuthorizationRequest]:
        return [
            request
            for request in self._requests.values()
            if request.is_pending
        ]

    def count(self) -> int:
        return len(self._requests)

    def count_pending(self) -> int:
        return len(self.list_pending())

    def clear(self) -> None:
        self._requests.clear()
