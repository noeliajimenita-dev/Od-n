from __future__ import annotations

from .credential_vault import Credential


class CredentialVaultBackend:
    """
    Development backend for the credential vault.

    This backend exists for local testing only.
    Production deployments must use a real secret-management
    service such as OCI Vault.

    Credentials are intentionally kept behind this interface so
    the rest of ODIN never depends on the storage implementation.
    """

    def __init__(self) -> None:
        self._credentials: dict[str, Credential] = {}

    def store(
        self,
        credential_ref: str,
        username: str,
        password: str,
    ) -> None:
        self._validate_reference(credential_ref)
        self._validate_username(username)
        self._validate_password(password)

        self._credentials[credential_ref] = Credential(
            credential_ref=credential_ref,
            username=username,
            password=password,
        )

    def get(
        self,
        credential_ref: str,
    ) -> Credential | None:
        self._validate_reference(credential_ref)
        return self._credentials.get(credential_ref)

    def exists(
        self,
        credential_ref: str,
    ) -> bool:
        self._validate_reference(credential_ref)
        return credential_ref in self._credentials

    def delete(
        self,
        credential_ref: str,
    ) -> bool:
        self._validate_reference(credential_ref)

        if credential_ref not in self._credentials:
            return False

        del self._credentials[credential_ref]
        return True

    def count(self) -> int:
        return len(self._credentials)

    def clear(self) -> None:
        self._credentials.clear()

    def list_references(self) -> list[str]:
        return list(self._credentials.keys())

    @staticmethod
    def _validate_reference(
        credential_ref: str,
    ) -> None:
        if not credential_ref or not credential_ref.strip():
            raise ValueError("credential_ref cannot be empty")

        if not credential_ref.startswith("credential_"):
            raise ValueError(
                "credential_ref must start with 'credential_'"
            )

    @staticmethod
    def _validate_username(username: str) -> None:
        if not username or not username.strip():
            raise ValueError("username cannot be empty")

    @staticmethod
    def _validate_password(password: str) -> None:
        if not password:
            raise ValueError("password cannot be empty")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(credentials={self.count()})"
          )
