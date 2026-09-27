from dataclasses import dataclass

from .actions import PermissionAction, PermissionLevel
from .roles import get_role_permissions


@dataclass(frozen=True)
class PermissionDecision:
    """Resultado de una comprobación de permisos."""

    role: str
    action: PermissionAction
    level: PermissionLevel
    allowed: bool
    requires_approval: bool


def check_permission(
    role: str,
    action: PermissionAction,
) -> PermissionDecision:
    """
    Comprueba los permisos de un rol para una acción determinada.

    Una acción con REQUIRES_APPROVAL no se considera permitida
    automáticamente: necesita autorización posterior.
    """

    permissions = get_role_permissions(role)

    level = permissions.get(
        action,
        PermissionLevel.DENIED,
    )

    return PermissionDecision(
        role=role,
        action=action,
        level=level,
        allowed=level == PermissionLevel.ALLOWED,
        requires_approval=level == PermissionLevel.REQUIRES_APPROVAL,
    )
