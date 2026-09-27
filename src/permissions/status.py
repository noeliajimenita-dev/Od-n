from .actions import DEFAULT_PERMISSIONS, PermissionLevel


def get_permissions_status() -> dict:
    """Devuelve un resumen del estado del sistema de permisos."""

    total = len(DEFAULT_PERMISSIONS)

    allowed = sum(
        1
        for level in DEFAULT_PERMISSIONS.values()
        if level == PermissionLevel.ALLOWED
    )

    requires_approval = sum(
        1
        for level in DEFAULT_PERMISSIONS.values()
        if level == PermissionLevel.REQUIRES_APPROVAL
    )

    denied = sum(
        1
        for level in DEFAULT_PERMISSIONS.values()
        if level == PermissionLevel.DENIED
    )

    return {
        "total_actions": total,
        "allowed": allowed,
        "requires_approval": requires_approval,
        "denied": denied,
    }
