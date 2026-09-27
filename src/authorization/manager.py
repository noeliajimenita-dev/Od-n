from .request import AuthorizationRequest


class AuthorizationManager:
    """Gestiona solicitudes de autorización."""

    def __init__(self) -> None:
        self._requests: dict[str, AuthorizationRequest] = {}

    def create_request(
        self,
        action: str,
        requester: str,
        reason: str,
        task_id: str | None = None,
    ) -> AuthorizationRequest:
        """Crea y registra una nueva solicitud."""

        request = AuthorizationRequest(
            action=action,
            requester=requester,
            reason=reason,
            task_id=task_id,
        )

        self._requests[request.request_id] = request
        return request

    def get_request(
        self,
        request_id: str,
    ) -> AuthorizationRequest | None:
        """Obtiene una solicitud por su identificador."""

        return self._requests.get(request_id)

    def get_all(self) -> list[AuthorizationRequest]:
        """Devuelve todas las solicitudes."""

        return list(self._requests.values())

    def get_pending(self) -> list[AuthorizationRequest]:
        """Devuelve únicamente las solicitudes pendientes."""

        return [
            request
            for request in self._requests.values()
            if request.is_pending()
        ]

    def approve(self, request_id: str) -> bool:
        """Aprueba una solicitud pendiente."""

        request = self.get_request(request_id)

        if request is None or not request.is_pending():
            return False

        request.approve()
        return True

    def deny(self, request_id: str) -> bool:
        """Rechaza una solicitud pendiente."""

        request = self.get_request(request_id)

        if request is None or not request.is_pending():
            return False

        request.deny()
        return True

    def count(self) -> int:
        """Devuelve el número total de solicitudes."""

        return len(self._requests)

    def count_pending(self) -> int:
        """Devuelve el número de solicitudes pendientes."""

        return len(self.get_pending())
