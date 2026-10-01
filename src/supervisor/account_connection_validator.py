class AccountConnectionValidator:
    """Validates data required for an external account connection."""

    def validate_service(self, service: str) -> None:
        if not service or not service.strip():
            raise ValueError("Service cannot be empty")

    def validate_username(self, username: str) -> None:
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")

    def validate_credential_reference(
        self,
        credential_ref: str,
    ) -> None:
        if not credential_ref or not credential_ref.strip():
            raise ValueError(
                "Credential reference cannot be empty"
            )

    def validate_connection(
        self,
        service: str,
        username: str,
        credential_ref: str,
    ) -> bool:
        self.validate_service(service)
        self.validate_username(username)
        self.validate_credential_reference(credential_ref)

        return True
