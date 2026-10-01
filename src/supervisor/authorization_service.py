from .authorization_repository import AuthorizationRepository
from .authorization_request import AuthorizationRequest


class AuthorizationService:
    """Handles authorization requests for sensitive Supervisor actions."""

    def __init__(self, repository: AuthorizationRepository | None = None) -> None:
        self.repository = repository or AuthorizationRepository()

    def create_request(
        self,
        request_id: str,
        action: str,
        reason: str,
        purpose: str,
        time_limit_minutes: int | None = None,
    ) -> AuthorizationRequest:
        if self.repository.exists(request_id):
            raise ValueError(f"Authorization request already exists: {request_id}")

        request = AuthorizationRequest(
            request_id=request_id,
            action=action,
            reason=reason,
            purpose=purpose,
            time_limit_minutes=time_limit_minutes,
        )

        self.repository.save(request)
        return request

    def approve(self, request_id: str) -> AuthorizationRequest:
        request = self._get_request(request_id)

        if not request.is_pending:
            raise ValueError("Only pending requests can be approved")

        request.approve()
        self.repository.update(request)
        return request

    def reject(self, request_id: str) -> AuthorizationRequest:
        request = self._get_request(request_id)

        if not request.is_pending:
            raise ValueError("Only pending requests can be rejected")

        request.reject()
        self.repository.update(request)
        return request

    def expire(self, request_id: str) -> AuthorizationRequest:
        request = self._get_request(request_id)

        if not request.is_pending:
            raise ValueError("Only pending requests can expire")

        request.expire()
        self.repository.update(request)
        return request

    def get(self, request_id: str) -> AuthorizationRequest | None:
        return self.repository.get(request_id)

    def get_pending(self) -> list[AuthorizationRequest]:
        return self.repository.list_pending()

    def is_approved(self, request_id: str) -> bool:
        request = self.repository.get(request_id)
        return request is not None and request.is_approved

    def _get_request(self, request_id: str) -> AuthorizationRequest:
        request = self.repository.get(request_id)

        if request is None:
            raise KeyError(f"Authorization request not found: {request_id}")

        return request
