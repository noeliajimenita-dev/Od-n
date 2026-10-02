from __future__ import annotations

import json

import pytest

from src.security.credential_vault import CredentialVault
from src.security.credential_vault_backend import CredentialVaultBackend
from src.security.credential_vault_factory import CredentialVaultFactory
from src.security.credential_vault_service import CredentialVaultService
from src.security.oci_credential_vault import OCICredentialVault


class FakeOCIClient:
    def __init__(self) -> None:
        self.secrets: dict[str, str] = {}

    def create_or_update_secret(
        self,
        vault_id: str,
        secret_name: str,
        secret_content: str,
    ) -> None:
        self.secrets[secret_name] = secret_content

    def get_secret(
        self,
        vault_id: str,
        secret_name: str,
    ) -> str | None:
        return self.secrets.get(secret_name)

    def secret_exists(
        self,
        vault_id: str,
        secret_name: str,
    ) -> bool:
        return secret_name in self.secrets

    def delete_secret(
        self,
        vault_id: str,
        secret_name: str,
    ) -> bool:
        if secret_name not in self.secrets:
            return False

        del self.secrets[secret_name]
        return True

    def count_secrets(
        self,
        vault_id: str,
        secret_prefix: str,
    ) -> int:
        return sum(
            1
            for name in self.secrets
            if name.startswith(secret_prefix)
        )


def build_service() -> CredentialVaultService:
    backend = CredentialVaultBackend()
    vault = CredentialVault(backend)
    return CredentialVaultService(vault)


def test_build_reference() -> None:
    reference = CredentialVault.build_reference("computrabajo")

    assert reference == "credential_computrabajo"


def test_build_reference_rejects_empty_account() -> None:
    with pytest.raises(ValueError):
        CredentialVault.build_reference("")


def test_backend_stores_and_reads_credentials() -> None:
    backend = CredentialVaultBackend()

    backend.store(
        credential_ref="credential_test",
        username="user@example.com",
        password="secret",
    )

    credential = backend.get("credential_test")

    assert credential is not None
    assert credential.username == "user@example.com"
    assert credential.password == "secret"


def test_vault_stores_credentials() -> None:
    backend = CredentialVaultBackend()
    vault = CredentialVault(backend)

    credential = vault.store(
        credential_ref="credential_test",
        username="user@example.com",
        password="secret",
    )

    assert credential.credential_ref == "credential_test"
    assert vault.exists("credential_test")
    assert vault.count() == 1


def test_vault_rejects_invalid_reference() -> None:
    backend = CredentialVaultBackend()
    vault = CredentialVault(backend)

    with pytest.raises(ValueError):
        vault.store(
            credential_ref="invalid",
            username="user@example.com",
            password="secret",
        )


def test_vault_rejects_empty_username() -> None:
    backend = CredentialVaultBackend()
    vault = CredentialVault(backend)

    with pytest.raises(ValueError):
        vault.store(
            credential_ref="credential_test",
            username="",
            password="secret",
        )


def test_vault_rejects_empty_password() -> None:
    backend = CredentialVaultBackend()
    vault = CredentialVault(backend)

    with pytest.raises(ValueError):
        vault.store(
            credential_ref="credential_test",
            username="user@example.com",
            password="",
        )


def test_service_stores_using_account_id() -> None:
    service = build_service()

    reference = service.store_credential(
        account_id="computrabajo",
        username="user@example.com",
        password="secret",
    )

    assert reference == "credential_computrabajo"
    assert service.exists(reference)


def test_service_returns_credential_when_authorized() -> None:
    service = build_service()

    reference = service.store_credential(
        account_id="linkedin",
        username="user@example.com",
        password="secret",
    )

    credential = service.get_credential(reference)

    assert credential is not None
    assert credential.username == "user@example.com"
    assert credential.password == "secret"


def test_service_can_get_username_without_password() -> None:
    service = build_service()

    reference = service.store_credential(
        account_id="upwork",
        username="user@example.com",
        password="secret",
    )

    assert service.get_username(reference) == "user@example.com"


def test_status_does_not_expose_password() -> None:
    service = build_service()

    reference = service.store_credential(
        account_id="workana",
        username="user@example.com",
        password="super-secret-password",
    )

    status = service.status(reference)
    data = status.to_dict()

    assert data["exists"] is True
    assert data["username"] == "user@example.com"
    assert "password" not in data
    assert "super-secret-password" not in json.dumps(data)


def test_safe_summary_does_not_expose_secrets() -> None:
    service = build_service()

    service.store_credential(
        account_id="fiverr",
        username="user@example.com",
        password="super-secret-password",
    )

    summary = service.safe_summary()
    serialized = json.dumps(summary)

    assert summary["credential_count"] == 1
    assert "password" not in serialized
    assert "user@example.com" not in serialized
    assert "super-secret-password" not in serialized


def test_service_deletes_credentials() -> None:
    service = build_service()

    reference = service.store_credential(
        account_id="test-account",
        username="user@example.com",
        password="secret",
    )

    assert service.delete(reference) is True
    assert service.exists(reference) is False
    assert service.count() == 0


def test_development_factory_creates_vault() -> None:
    vault = CredentialVaultFactory.create("development")

    assert isinstance(vault, CredentialVault)
    assert vault.count() == 0


def test_factory_rejects_unknown_environment() -> None:
    with pytest.raises(ValueError):
        CredentialVaultFactory.create("unknown")


def test_production_factory_is_not_enabled_yet() -> None:
    assert CredentialVaultFactory.is_production("production") is True

    with pytest.raises(RuntimeError):
        CredentialVaultFactory.create("production")


def test_oci_adapter_stores_and_reads_secret() -> None:
    client = FakeOCIClient()

    vault = OCICredentialVault(
        client=client,
        vault_id="ocid1.vault.test",
    )

    vault.store(
        credential_ref="credential_computrabajo",
        username="user@example.com",
        password="secret",
    )

    assert vault.exists("credential_computrabajo") is True

    credential = vault.get("credential_computrabajo")

    assert credential is not None
    assert credential.username == "user@example.com"
    assert credential.password == "secret"


def test_oci_adapter_uses_secret_prefix() -> None:
    client = FakeOCIClient()

    vault = OCICredentialVault(
        client=client,
        vault_id="ocid1.vault.test",
        secret_prefix="odin-",
    )

    vault.store(
        credential_ref="credential_upwork",
        username="user@example.com",
        password="secret",
    )

    assert "odin-upwork" in client.secrets


def test_oci_adapter_deletes_secret() -> None:
    client = FakeOCIClient()

    vault = OCICredentialVault(
        client=client,
        vault_id="ocid1.vault.test",
    )

    vault.store(
        credential_ref="credential_linkedin",
        username="user@example.com",
        password="secret",
    )

    assert vault.delete("credential_linkedin") is True
    assert vault.exists("credential_linkedin") is False


def test_oci_adapter_counts_secrets() -> None:
    client = FakeOCIClient()

    vault = OCICredentialVault(
        client=client,
        vault_id="ocid1.vault.test",
    )

    vault.store(
        credential_ref="credential_one",
        username="one@example.com",
        password="secret",
    )

    vault.store(
        credential_ref="credential_two",
        username="two@example.com",
        password="secret",
    )

    assert vault.count() == 2


def test_oci_adapter_rejects_invalid_reference() -> None:
    client = FakeOCIClient()

    vault = OCICredentialVault(
        client=client,
        vault_id="ocid1.vault.test",
    )

    with pytest.raises(ValueError):
        vault.store(
            credential_ref="invalid",
            username="user@example.com",
            password="secret",
        )


def test_backend_clear_removes_all_credentials() -> None:
    backend = CredentialVaultBackend()

    backend.store(
        credential_ref="credential_one",
        username="one@example.com",
        password="secret",
    )

    backend.store(
        credential_ref="credential_two",
        username="two@example.com",
        password="secret",
    )

    assert backend.count() == 2

    backend.clear()

    assert backend.count() == 0
    assert backend.list_references() == []


def test_service_reference_validation() -> None:
    service = build_service()

    assert service.validate_reference("credential_valid") is True
    assert service.validate_reference("invalid") is False


def test_missing_credential_status_is_safe() -> None:
    service = build_service()

    status = service.status("credential_missing")

    assert status.exists is False
    assert status.username is None
    assert status.to_dict() == {
        "credential_ref": "credential_missing",
        "exists": False,
        "username": None,
  }
