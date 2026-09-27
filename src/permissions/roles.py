"""
Roles y permisos de THE ODIN PROJECT.
"""

from .actions import (
    DEFAULT_PERMISSIONS,
    PermissionAction,
    PermissionLevel,
)


ROLE_SUPERVISOR = "supervisor"
ROLE_WORKER_1 = "worker_1"
ROLE_WORKER_2 = "worker_2"
ROLE_WORKER_3 = "worker_3"
ROLE_WORKER_4 = "worker_4"
ROLE_WORKER_5 = "worker_5"
ROLE_SYSTEM = "system"
ROLE_USER = "user"


WORKER_ROLES = {
    ROLE_WORKER_1,
    ROLE_WORKER_2,
    ROLE_WORKER_3,
    ROLE_WORKER_4,
    ROLE_WORKER_5,
}


def get_role_permissions(role: str) -> dict[PermissionAction, PermissionLevel]:
    """Devuelve los permisos base correspondientes a un rol."""

    if role == ROLE_USER:
        return dict(DEFAULT_PERMISSIONS)

    if role == ROLE_SUPERVISOR:
        return dict(DEFAULT_PERMISSIONS)

    if role in WORKER_ROLES:
        permissions = dict(DEFAULT_PERMISSIONS)

        permissions[PermissionAction.MERGE_MAIN] = (
            PermissionLevel.REQUIRES_APPROVAL
        )
        permissions[PermissionAction.DELETE_CODE] = (
            PermissionLevel.REQUIRES_APPROVAL
        )
        permissions[PermissionAction.DELETE_BACKUP] = (
            PermissionLevel.REQUIRES_APPROVAL
        )
        permissions[PermissionAction.PUBLISH] = (
            PermissionLevel.REQUIRES_APPROVAL
        )
        permissions[PermissionAction.DELIVER_TO_CLIENT] = (
            PermissionLevel.REQUIRES_APPROVAL
        )
        permissions[PermissionAction.SPEND_MONEY] = (
            PermissionLevel.REQUIRES_APPROVAL
        )
        permissions[PermissionAction.ADD_CREDENTIAL] = (
            PermissionLevel.REQUIRES_APPROVAL
        )
        permissions[PermissionAction.CHANGE_CREDENTIAL] = (
            PermissionLevel.REQUIRES_APPROVAL
        )
        permissions[PermissionAction.DEPLOY_PRODUCTION] = (
            PermissionLevel.REQUIRES_APPROVAL
        )
        permissions[PermissionAction.EXECUTE_EXTERNAL_ACTION] = (
            PermissionLevel.REQUIRES_APPROVAL
        )

        return permissions

    if role == ROLE_SYSTEM:
        return {
            action: PermissionLevel.ALLOWED
            for action in (
                PermissionAction.READ_CODE,
                PermissionAction.READ_DOCUMENTATION,
                PermissionAction.RUN_TESTS,
                PermissionAction.CREATE_BACKUP,
                PermissionAction.USE_RESOURCE,
            )
        }

    return {}


def has_role(role: str) -> bool:
    """Indica si el rol pertenece al sistema."""

    return role in {
        ROLE_SUPERVISOR,
        ROLE_WORKER_1,
        ROLE_WORKER_2,
        ROLE_WORKER_3,
        ROLE_WORKER_4,
        ROLE_WORKER_5,
        ROLE_SYSTEM,
        ROLE_USER,
      }
