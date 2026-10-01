from .account_connection_controller import AccountConnectionController
from .account_connection_security import AccountConnectionSecurity
from .account_connection_session_service import (
    AccountConnectionSessionService,
)


class AccountConnectionFlow:
    """Coordinates the complete external account connection flow."""

    def __init__(
        self,
        controller: AccountConnectionController | None = None,
        session_service: AccountConnectionSessionService | None = None,
        security: AccountConnectionSecurity | None = None,
    ) -> None:
        self.controller = (
            controller or AccountConnectionController()
        )
        self.session_service = (
            session_service or AccountConnectionSessionService()
        )
        self.security = (
            security or AccountConnectionSecurity(
                session_service=self.session_service
            )
        )

    def start(
        self,
        request_id: str,
        session_id: str,
        service_name: str,
        username: str,
    ):
        request = self.controller.start_connection(
            request_id=request_id,
            service_name=service_name,
            username=username,
        )

        session = self.session_service.create_session(
            session_id=session_id,
            request_id=request.request_id,
            service=service_name,
        )

        self.session_service.wait_for_user(session.session_id)

        return {
            "request": request,
            "session": session,
            "status": "waiting_for_user",
        }

    def validate(
        self,
        session_id: str,
        credential_ref: str,
    ) -> bool:
        return self.security.authorize_connection(
            session_id=session_id,
            credential_ref=credential_ref,
        )

    def complete(
        self,
        request_id: str,
        session_id: str,
    ) -> dict[str, str]:
        self.controller.complete_connection(request_id)
        self.session_service.complete(session_id)

        return {
            "request_id": request_id,
            "session_id": session_id,
            "status": "connected",
        }

    def cancel(
        self,
        request_id: str,
        session_id: str,
    ) -> dict[str, str]:
        self.controller.cancel_connection(request_id)
        self.session_service.cancel(session_id)

        return {
            "request_id": request_id,
            "session_id": session_id,
            "status": "cancelled",
  }
