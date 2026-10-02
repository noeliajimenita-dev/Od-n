from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .credential_vault import Credential, CredentialVault


@dataclass(frozen=True)
class CredentialStatus:
    """Estado seguro de una credencial sin exponer secretos."""

    credential_ref: str
    exists: bool
    username: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "credential_ref": self.credential_ref,
            "exists": self.exists,
            "username": self.username,
        }


class CredentialVaultService:
    """
    Servicio de alto nivel para gestionar credenciales de ODIN.

    Esta clase nunca devuelve contraseñas en estados, reportes o
    representaciones públicas. La contraseña solamente se obtiene
    mediante get_credential(), cuando un componente autorizado
    realmente necesita utilizarla.
    """

    def __init__(self, vault: CredentialVault) -> None:
        if vault is None:
            raise ValueError("vault cannot be None")

        self.vault = vault

    def store_credential(
        self,
        account_id: str,
        username: str,
        password: str,
    ) -> str:
        """
        Guarda una credencial y devuelve únicamente su referencia.

        La referencia puede almacenarse en configuraciones y objetos
        internos; la contraseña nunca forma parte del valor retornado.
        """
        credential_ref = CredentialVault.build_reference(account_id)

        self.vault.store(
            credential_ref=credential_ref,
            username=username,
            password=password,
        )

        return credential_ref

    def store_by_reference(
        self,
        credential_ref: str,
        username: str,
        password: str,
    ) -> str:
        """Guarda una credencial utilizando una referencia existente."""
        credential = self.vault.store(
            credential_ref=credential_ref,
            username=username,
            password=password,
        )

        return credential.credential_ref

    def get_credential(
        self,
        credential_ref: str,
    ) -> Credential | None:
        """
        Recupera una credencial para uso interno autorizado.

        Este método no debe utilizarse para generar logs, mensajes
        de Telegram, reportes o respuestas al usuario.
        """
        return self.vault.get(credential_ref)

    def get_username(
        self,
        credential_ref: str,
    ) -> str | None:
        """Obtiene solamente el usuario asociado a una credencial."""
        credential = self.vault.get(credential_ref)

        if credential is None:
            return None

        return credential.username

    def exists(
        self,
        credential_ref: str,
    ) -> bool:
        """Comprueba si existe una credencial sin recuperar el secreto."""
        return self.vault.exists(credential_ref)

    def status(
        self,
        credential_ref: str,
    ) -> CredentialStatus:
        """
        Devuelve información segura sobre una credencial.

        Nunca incluye la contraseña.
        """
        exists = self.vault.exists(credential_ref)

        if not exists:
            return CredentialStatus(
                credential_ref=credential_ref,
                exists=False,
            )

        return CredentialStatus(
            credential_ref=credential_ref,
            exists=True,
            username=self.get_username(credential_ref),
        )

    def delete(
        self,
        credential_ref: str,
    ) -> bool:
        """Elimina una credencial del backend configurado."""
        return self.vault.delete(credential_ref)

    def count(self) -> int:
        """Devuelve el número de credenciales almacenadas."""
        return self.vault.count()

    def validate_reference(
        self,
        credential_ref: str,
    ) -> bool:
        """
        Comprueba que una referencia tenga el formato esperado.

        No accede al secreto.
        """
        try:
            CredentialVault._validate_reference(credential_ref)
        except ValueError:
            return False

        return True

    def safe_summary(self) -> dict[str, Any]:
        """
        Genera un resumen seguro para Supervisor, logs o monitoreo.

        No expone usuarios ni contraseñas individuales.
        """
        return {
            "credential_count": self.count(),
            "vault_configured": True,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(credentials={self.count()})"
      )
