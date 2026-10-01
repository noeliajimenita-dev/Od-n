from .account_connection_request import AccountConnectionRequest


class AccountConnectionRepository:
    """Stores and manages account connection requests."""

    def __init__(self) -> None:
        self._requests: dict[str, AccountConnectionRequest] = {}

    def save(self, request: AccountConnectionRequest) -> None:
        if not isinstance(request, AccountConnectionRequest):
            raise TypeError(
                "request must be an AccountConnectionRequest"
            )

        self._requests[request.request_id] = request

    def get(self, request_id: str) -> AccountConnectionRequest | None:
        return self._requests.get(request_id)

    def exists(self, request_id: str) -> bool:
        return request_id in self._requests

    def update(self, request: AccountConnectionRequest) -> None:
        if not self.exists(request.request_id):
            raise KeyError(
                f"Connection request not found: {request.request_id}"
            )

        self._requests[request.request_id] = request

    def delete(self, request_id: str) -> None:
        self._requests.pop(request_id, None)

    def list_all(self) -> list[AccountConnectionRequest]:
        return list(self._requests.values())

    def list_pending(self) -> list[AccountConnectionRequest]:
        return [
            request
            for request in self._requests.values()
            if request.is_pending
        ]

    def list_waiting_for_user(self) -> list[AccountConnectionRequest]:
        return [
            request
            for request in self._requests.values()
            if request.needs_user_action
        ]

    def count(self) -> int:
        return len(self._requests)

    def clear(self) -> None:
        self._requests.clear()
