from __future__ import annotations

import json
from typing import Any

from .credential_vault import Credential, CredentialVault


class OCICredentialVault:
    """
    Production adapter for OCI Vault.

    The OCI client is injected from outside so this class does not
    contain authentication credentials or hardcoded OCI secrets.

    The client is expected to provide the operations required to
    create, retrieve, and delete secrets.
    """

    def __init__(
        self,
        client: Any,
        vault_id: str,
        secret_prefix: str = "odin-credential-",
    ) -> None:
        if client is None:
            raise ValueError("client cannot be None")

        if not vault_id or not vault_id.strip():
            raise ValueError("vault_id cannot be empty")

        if not secret_prefix or not secret_prefix.strip():
            raise ValueError("secret_prefix cannot be empty")

        self.client = client
        self.vault_id = vault_id
        self.secret_prefix = secret_prefix

    def _secret_name(self, credential_ref: str) -> str:
        if not credential_ref.startswith(CredentialVault.PREFIX):
            raise ValueError(
                "credential_ref must start with "
                "'credential_'"
            )

        account_id = credential_ref[
            len(CredentialVault.PREFIX):
        ]

        if not account_id:
            raise ValueError(
                "credential_ref contains no account identifier"
            )

        return f"{self.secret_prefix}{account_id}"

    def store(
        self,
        credential_ref: str,
        username: str,
        password: str,
    ) -> None:
        secret_name = self._secret_name(credential_ref)

        payload = json.dumps(
            {
                "username": username,
                "password": password,
            }
        )

        self.client.create_or_update_secret(
            vault_id=self.vault_id,
            secret_name=secret_name,
            secret_content=payload,
        )

    def get(
        self,
        credential_ref: str,
    ) -> Credential | None:
        secret_name = self._secret_name(credential_ref)

        secret = self.client.get_secret(
            vault_id=self.vault_id,
            secret_name=secret_name,
        )

        if secret is None:
            return None

        data = self._decode_secret(secret)

        return Credential(
            credential_ref=credential_ref,
            username=data["username"],
            password=data["password"],
        )

    def exists(
        self,
        credential_ref: str,
    ) -> bool:
        secret_name = self._secret_name(credential_ref)

        return self.client.secret_exists(
            vault_id=self.vault_id,
            secret_name=secret_name,
        )

    def delete(
        self,
        credential_ref: str,
    ) -> bool:
        secret_name = self._secret_name(credential_ref)

        return self.client.delete_secret(
            vault_id=self.vault_id,
            secret_name=secret_name,
        )

    def count(self) -> int:
        return self.client.count_secrets(
            vault_id=self.vault_id,
            secret_prefix=self.secret_prefix,
        )

    @staticmethod
    def _decode_secret(secret: Any) -> dict[str, str]:
        if isinstance(secret, dict):
            data = secret
        else:
            data = json.loads(secret)

        if "username" not in data:
            raise ValueError(
                "Vault secret does not contain username"
            )

        if "password" not in data:
            raise ValueError(
                "Vault secret does not contain password"
            )

        return {
            "username": str(data["username"]),
            "password": str(data["password"]),
  }
