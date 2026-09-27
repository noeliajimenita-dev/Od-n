"""
Acciones y niveles de permiso de THE ODIN PROJECT.
"""

from enum import Enum


class PermissionLevel(str, Enum):
    """Nivel de autorización necesario para una acción."""

    ALLOWED = "ALLOWED"
    REQUIRES_APPROVAL = "REQUIRES_APPROVAL"
    DENIED = "DENIED"


class PermissionAction(str, Enum):
    """Acciones controladas por el sistema de permisos."""

    READ_CODE = "READ_CODE"
    READ_DOCUMENTATION = "READ_DOCUMENTATION"
    ANALYZE_TASK = "ANALYZE_TASK"
    CREATE_TASK = "CREATE_TASK"
    ASSIGN_TASK = "ASSIGN_TASK"

    CREATE_BRANCH = "CREATE_BRANCH"
    MODIFY_CODE = "MODIFY_CODE"
    RUN_TESTS = "RUN_TESTS"
    CREATE_BACKUP = "CREATE_BACKUP"

    USE_AI_PROVIDER = "USE_AI_PROVIDER"
    USE_RESOURCE = "USE_RESOURCE"

    MERGE_MAIN = "MERGE_MAIN"
    DELETE_CODE = "DELETE_CODE"
    DELETE_BACKUP = "DELETE_BACKUP"

    PUBLISH = "PUBLISH"
    DELIVER_TO_CLIENT = "DELIVER_TO_CLIENT"

    SPEND_MONEY = "SPEND_MONEY"
    ADD_CREDENTIAL = "ADD_CREDENTIAL"
    CHANGE_CREDENTIAL = "CHANGE_CREDENTIAL"

    DEPLOY_PRODUCTION = "DEPLOY_PRODUCTION"
    EXECUTE_EXTERNAL_ACTION = "EXECUTE_EXTERNAL_ACTION"


DEFAULT_PERMISSIONS: dict[PermissionAction, PermissionLevel] = {
    PermissionAction.READ_CODE: PermissionLevel.ALLOWED,
    PermissionAction.READ_DOCUMENTATION: PermissionLevel.ALLOWED,
    PermissionAction.ANALYZE_TASK: PermissionLevel.ALLOWED,
    PermissionAction.CREATE_TASK: PermissionLevel.ALLOWED,
    PermissionAction.ASSIGN_TASK: PermissionLevel.ALLOWED,

    PermissionAction.CREATE_BRANCH: PermissionLevel.ALLOWED,
    PermissionAction.MODIFY_CODE: PermissionLevel.ALLOWED,
    PermissionAction.RUN_TESTS: PermissionLevel.ALLOWED,
    PermissionAction.CREATE_BACKUP: PermissionLevel.ALLOWED,

    PermissionAction.USE_AI_PROVIDER: PermissionLevel.ALLOWED,
    PermissionAction.USE_RESOURCE: PermissionLevel.ALLOWED,

    PermissionAction.MERGE_MAIN: PermissionLevel.REQUIRES_APPROVAL,
    PermissionAction.DELETE_CODE: PermissionLevel.REQUIRES_APPROVAL,
    PermissionAction.DELETE_BACKUP: PermissionLevel.REQUIRES_APPROVAL,

    PermissionAction.PUBLISH: PermissionLevel.REQUIRES_APPROVAL,
    PermissionAction.DELIVER_TO_CLIENT: PermissionLevel.REQUIRES_APPROVAL,

    PermissionAction.SPEND_MONEY: PermissionLevel.REQUIRES_APPROVAL,
    PermissionAction.ADD_CREDENTIAL: PermissionLevel.REQUIRES_APPROVAL,
    PermissionAction.CHANGE_CREDENTIAL: PermissionLevel.REQUIRES_APPROVAL,

    PermissionAction.DEPLOY_PRODUCTION: PermissionLevel.REQUIRES_APPROVAL,
    PermissionAction.EXECUTE_EXTERNAL_ACTION: PermissionLevel.REQUIRES_APPROVAL,
}


def get_permission_level(
    action: PermissionAction,
) -> PermissionLevel:
    """Devuelve el nivel de permiso de una acción."""

    return DEFAULT_PERMISSIONS.get(
        action,
        PermissionLevel.DENIED,
)
