from .account_connection_service import AccountConnectionService
from .account_connection_validator import AccountConnectionValidator


class AccountConnectionController:
    """Coordinates the external account connection workflow."""

    def __init__(
        self,
        service: AccountConnectionService | None = None,
        validator: AccountConnectionValidator | None = None,
    ) -> None:
        self.service = service or AccountConnectionService()
        self.validator = validator or AccountConnectionValidator()

    def start_connection(
        self,
        request_id: str,
        service_name: str,
        username: str,
    ):
        self.validator.validate_service(service_name)
        self.validator.validate_username(username)

        request = self.service.create_request(
            request_id=request_id,
            service=service_name,
            username=username,
        )

        request.request_user_action()

        self.service.repository.update(request)

        return request

    def mark_ready(self, request_id: str):
        return self.service.mark_ready(request_id)

    def complete_connection(self, request_id: str):
        return self.service.mark_connected(request_id)

    def cancel_connection(self, request_id: str):
        return self.service.cancel(request_id)

    def get_request(self, request_id: str):
        return self.service.get(request_id)
