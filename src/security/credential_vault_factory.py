from __future__ import annotations

import os

from .credential_vault import CredentialVault
from .credential_vault_backend import CredentialVaultBackend


class CredentialVaultFactory:
    """Creates the credential vault used by ODIN."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"

    @classmethod
    def create(
        cls,
        environment: str | None = None,
    ) -> CredentialVault:
        selected_environment = (
            environment
            or os.getenv("ODIN_ENVIRONMENT")
            or cls.DEVELOPMENT
        ).strip().lower()

        if selected_environment == cls.DEVELOPMENT:
            backend = CredentialVaultBackend()
            return CredentialVault(backend)

        if selected_environment == cls.PRODUCTION:
            raise RuntimeError(
                "Production credential backend is not configured yet"
            )

        raise ValueError(
            f"Unsupported ODIN environment: {selected_environment}"
        )

    @classmethod
    def is_production(cls, environment: str | None = None) -> bool:
        selected_environment = (
            environment
            or os.getenv("ODIN_ENVIRONMENT")
            or cls.DEVELOPMENT
        ).strip().lower()

        return selected_environment == cls.PRODUCTION
