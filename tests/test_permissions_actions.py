from src.permissions.actions import (
    DEFAULT_PERMISSIONS,
    PermissionAction,
    PermissionLevel,
    get_permission_level,
)


def test_all_actions_have_default_permissions():
    for action in PermissionAction:
        assert action in DEFAULT_PERMISSIONS


def test_safe_actions_are_allowed():
    allowed_actions = {
        PermissionAction.READ_CODE,
        PermissionAction.READ_DOCUMENTATION,
        PermissionAction.ANALYZE_TASK,
        PermissionAction.CREATE_TASK,
        PermissionAction.ASSIGN_TASK,
        PermissionAction.CREATE_BRANCH,
        PermissionAction.MODIFY_CODE,
        PermissionAction.RUN_TESTS,
        PermissionAction.CREATE_BACKUP,
        PermissionAction.USE_AI_PROVIDER,
        PermissionAction.USE_RESOURCE,
    }

    for action in allowed_actions:
        assert get_permission_level(action) == PermissionLevel.ALLOWED


def test_sensitive_actions_require_approval():
    approval_actions = {
        PermissionAction.MERGE_MAIN,
        PermissionAction.DELETE_CODE,
        PermissionAction.DELETE_BACKUP,
        PermissionAction.PUBLISH,
        PermissionAction.DELIVER_TO_CLIENT,
        PermissionAction.SPEND_MONEY,
        PermissionAction.ADD_CREDENTIAL,
        PermissionAction.CHANGE_CREDENTIAL,
        PermissionAction.DEPLOY_PRODUCTION,
        PermissionAction.EXECUTE_EXTERNAL_ACTION,
    }

    for action in approval_actions:
        assert (
            get_permission_level(action)
            == PermissionLevel.REQUIRES_APPROVAL
        )


def test_permission_levels_are_valid():
    for level in DEFAULT_PERMISSIONS.values():
        assert level in {
            PermissionLevel.ALLOWED,
            PermissionLevel.REQUIRES_APPROVAL,
            PermissionLevel.DENIED,
        }


def test_permission_action_values_are_strings():
    for action in PermissionAction:
        assert isinstance(action.value, str)


def test_permission_level_values_are_strings():
    for level in PermissionLevel:
        assert isinstance(level.value, str)
