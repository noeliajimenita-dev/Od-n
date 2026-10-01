from typing import Any

from .credential_vault import CredentialVault


class SecureCredentialVaultAdapter:
    """
    Adapter between secure credential submissions and CredentialVault.

    The adapter works with credential references instead of exposing
    credentials to the rest of the connection flow.
    """

    def __init__(
        self,
        vault: CredentialVault | None = None,
    ) -> None:
        self.vault = vault or CredentialVault()

    def store(
        self,
        credential_ref: str,
        username: str,
        password: str,
    ) -> str:
        if not credential_ref.strip():
            raise ValueError("credential_ref cannot be empty")

        if not username.strip():
            raise ValueError("username cannot be empty")

        if not password:
            raise ValueError("password cannot be empty")

        self.vault.store(
            credential_ref=credential_ref,
            username=username,
            password=password,
        )

        return credential_ref

    def exists(self, credential_ref: str) -> bool:
        return self.vault.exists(credential_ref)

    def get(
        self,
        credential_ref: str,
    ) -> dict[str, Any] | None:
        if not self.vault.exists(credential_ref):
            return None

        return self.vault.get(credential_ref)

    def delete(self, credential_ref: str) -> bool:
        if not self.vault.exists(credential_ref):
            return False

        self.vault.delete(credential_ref)
        return True

    def count(self) -> int:
        return self.vault.count()
