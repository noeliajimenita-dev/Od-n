from .account_connection_repository import AccountConnectionRepository
from .account_connection_request import AccountConnectionRequest


class AccountConnectionService:
    """Manages external account connection requests."""

    def __init__(
        self,
        repository: AccountConnectionRepository | None = None,
    ) -> None:
        self.repository = (
            repository or AccountConnectionRepository()
        )

    def create_request(
        self,
        request_id: str,
        service: str,
        username: str,
    ) -> AccountConnectionRequest:
        if self.repository.exists(request_id):
            raise ValueError(
                f"Connection request already exists: {request_id}"
            )

        request = AccountConnectionRequest(
            request_id=request_id,
            service=service,
            username=username,
        )

        self.repository.save(request)
        return request

    def request_user_action(
        self,
        request_id: str,
    ) -> AccountConnectionRequest:
        request = self._get_request(request_id)

        request.request_user_action()
        self.repository.update(request)

        return request

    def mark_ready(
        self,
        request_id: str,
    ) -> AccountConnectionRequest:
        request = self._get_request(request_id)

        request.mark_ready()
        self.repository.update(request)

        return request

    def mark_connected(
        self,
        request_id: str,
    ) -> AccountConnectionRequest:
        request = self._get_request(request_id)

        request.mark_connected()
        self.repository.update(request)

        return request

    def cancel(
        self,
        request_id: str,
    ) -> AccountConnectionRequest:
        request = self._get_request(request_id)

        request.mark_cancelled()
        self.repository.update(request)

        return request

    def get(
        self,
        request_id: str,
    ) -> AccountConnectionRequest | None:
        return self.repository.get(request_id)

    def get_waiting_for_user(
        self,
    ) -> list[AccountConnectionRequest]:
        return self.repository.list_waiting_for_user()

    def _get_request(
        self,
        request_id: str,
    ) -> AccountConnectionRequest:
        request = self.repository.get(request_id)

        if request is None:
            raise KeyError(
                f"Connection request not found: {request_id}"
            )

        return request
