from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Credential:
    """Credential data kept inside the secure vault."""

    credential_ref: str
    username: str
    password: str


class CredentialVaultBackend(Protocol):
    """Contract for a secure credential storage backend."""

    def store(
        self,
        credential_ref: str,
        username: str,
        password: str,
    ) -> None:
        ...

    def get(
        self,
        credential_ref: str,
    ) -> Credential | None:
        ...

    def delete(
        self,
        credential_ref: str,
    ) -> bool:
        ...

    def exists(
        self,
        credential_ref: str,
    ) -> bool:
        ...

    def count(self) -> int:
        ...


class CredentialVault:
    """
    Secure credential-vault facade.

    ODIN interacts with this class instead of accessing credentials
    directly from Telegram handlers, platform connectors, or workers.

    A production backend such as OCI Vault can be attached later
    without changing the rest of the application.
    """

    PREFIX = "credential_"

    def __init__(self, backend: CredentialVaultBackend) -> None:
        if backend is None:
            raise ValueError("backend cannot be None")

        self.backend = backend

    def store(
        self,
        credential_ref: str,
        username: str,
        password: str,
    ) -> Credential:
        self._validate_reference(credential_ref)
        self._validate_username(username)
        self._validate_password(password)

        credential = Credential(
            credential_ref=credential_ref,
            username=username,
            password=password,
        )

        self.backend.store(
            credential_ref=credential.credential_ref,
            username=credential.username,
            password=credential.password,
        )

        return credential

    def get(
        self,
        credential_ref: str,
    ) -> Credential | None:
        self._validate_reference(credential_ref)
        return self.backend.get(credential_ref)

    def delete(
        self,
        credential_ref: str,
    ) -> bool:
        self._validate_reference(credential_ref)
        return self.backend.delete(credential_ref)

    def exists(
        self,
        credential_ref: str,
    ) -> bool:
        self._validate_reference(credential_ref)
        return self.backend.exists(credential_ref)

    def count(self) -> int:
        return self.backend.count()

    @classmethod
    def build_reference(cls, account_id: str) -> str:
        if not account_id or not account_id.strip():
            raise ValueError("account_id cannot be empty")

        normalized = account_id.strip()

        return f"{cls.PREFIX}{normalized}"

    @classmethod
    def _validate_reference(
        cls,
        credential_ref: str,
    ) -> None:
        if not credential_ref or not credential_ref.strip():
            raise ValueError("credential_ref cannot be empty")

        if not credential_ref.startswith(cls.PREFIX):
            raise ValueError(
                f"credential_ref must start with '{cls.PREFIX}'"
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
