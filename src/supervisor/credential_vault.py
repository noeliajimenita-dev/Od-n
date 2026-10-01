from typing import Any


class CredentialVault:
    """Secure abstraction for storing and retrieving account credentials."""

    def __init__(self) -> None:
        self._credentials: dict[str, dict[str, Any]] = {}

    def store(
        self,
        credential_ref: str,
        username: str,
        password: str,
    ) -> None:
        if not credential_ref or not credential_ref.strip():
            raise ValueError("Credential reference cannot be empty")

        if not username or not username.strip():
            raise ValueError("Username cannot be empty")

        if not password:
            raise ValueError("Password cannot be empty")

        self._credentials[credential_ref] = {
            "username": username,
            "password": password,
        }

    def get(self, credential_ref: str) -> dict[str, Any] | None:
        return self._credentials.get(credential_ref)

    def exists(self, credential_ref: str) -> bool:
        return credential_ref in self._credentials

    def delete(self, credential_ref: str) -> None:
        self._credentials.pop(credential_ref, None)

    def clear(self) -> None:
        self._credentials.clear()

    def count(self) -> int:
        return len(self._credentials)
