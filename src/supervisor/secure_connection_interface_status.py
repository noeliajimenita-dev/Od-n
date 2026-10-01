from typing import Any

from .secure_connection_interface_service import (
    SecureConnectionInterfaceService,
)
from .secure_connection_interface_session_service import (
    SecureConnectionInterfaceSessionService,
)


class SecureConnectionInterfaceStatus:
    """Provides consolidated status for secure connection interfaces."""

    def __init__(
        self,
        interface_service: SecureConnectionInterfaceService | None = None,
        session_service: SecureConnectionInterfaceSessionService | None = None,
    ) -> None:
        self.interface_service = (
            interface_service or SecureConnectionInterfaceService()
        )
        self.session_service = (
            session_service
            or SecureConnectionInterfaceSessionService()
        )

    def get_request_status(self, request_id: str) -> dict[str, Any]:
        request = self.interface_service.get_request(request_id)

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

    def get_session_status(self, session_id: str) -> dict[str, Any]:
        session = self.session_service.get_session(session_id)

        if session is None:
            return {
                "session_id": session_id,
                "exists": False,
                "status": "not_found",
            }

        return {
            "session_id": session.session_id,
            "request_id": session.request_id,
            "status": session.status,
            "active": session.is_active,
            "completed": session.is_completed,
            "cancelled": session.is_cancelled,
            "expired": session.is_expired,
            "exists": True,
        }

    def get_summary(self) -> dict[str, Any]:
        active_sessions = self.session_service.get_active_sessions()

        return {
            "active_sessions": len(active_sessions),
            "active_session_ids": [
                session.session_id
                for session in active_sessions
            ],
            "total_sessions": self.session_service.repository.count(),
        }
