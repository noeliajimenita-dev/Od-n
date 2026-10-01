from .secure_connection_interface import SecureConnectionRequest


class SecureConnectionInterfaceValidator:
    """Validates secure connection interface requests."""

    def validate(self, request: SecureConnectionRequest) -> bool:
        if not isinstance(request, SecureConnectionRequest):
            raise TypeError("request must be a SecureConnectionRequest")

        if not request.request_id.strip():
            raise ValueError("request_id cannot be empty")

        if not request.service.strip():
            raise ValueError("service cannot be empty")

        if not request.username.strip():
            raise ValueError("username cannot be empty")

        if not request.interface_token.strip():
            raise ValueError("interface_token cannot be empty")

        return True

    def validate_status(self, request: SecureConnectionRequest) -> bool:
        if request.status not in {
            "pending",
            "completed",
            "cancelled",
        }:
            raise ValueError(f"Invalid connection status: {request.status}")

        return True

    def is_ready_for_interface(
        self,
        request: SecureConnectionRequest,
    ) -> bool:
        self.validate(request)
        self.validate_status(request)

        return request.status == "pending"
