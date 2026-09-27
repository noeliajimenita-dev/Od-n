from src.permissions.actions import (
    PermissionAction,
    PermissionLevel,
)
from src.permissions.roles import (
    ROLE_SUPERVISOR,
    ROLE_SYSTEM,
    ROLE_USER,
    ROLE_WORKER_1,
    ROLE_WORKER_2,
    ROLE_WORKER_3,
    ROLE_WORKER_4,
    ROLE_WORKER_5,
    WORKER_ROLES,
    get_role_permissions,
    has_role,
)


def test_all_worker_roles_exist():
    assert WORKER_ROLES == {
        ROLE_WORKER_1,
        ROLE_WORKER_2,
        ROLE_WORKER_3,
        ROLE_WORKER_4,
        ROLE_WORKER_5,
    }


def test_known_roles_are_recognized():
    roles = {
        ROLE_SUPERVISOR,
        ROLE_WORKER_1,
        ROLE_WORKER_2,
        ROLE_WORKER_3,
        ROLE_WORKER_4,
        ROLE_WORKER_5,
        ROLE_SYSTEM,
        ROLE_USER,
    }

    for role in roles:
        assert has_role(role) is True


def test_unknown_role_is_rejected():
    assert has_role("unknown_role") is False


def test_supervisor_has_permissions():
    permissions = get_role_permissions(ROLE_SUPERVISOR)

    assert permissions[PermissionAction.READ_CODE] == PermissionLevel.ALLOWED
    assert (
        permissions[PermissionAction.MERGE_MAIN]
        == PermissionLevel.REQUIRES_APPROVAL
    )


def test_workers_have_basic_permissions():
    for role in WORKER_ROLES:
        permissions = get_role_permissions(role)

        assert (
            permissions[PermissionAction.READ_CODE]
            == PermissionLevel.ALLOWED
        )

        assert (
            permissions[PermissionAction.MODIFY_CODE]
            == PermissionLevel.ALLOWED
        )

        assert (
            permissions[PermissionAction.RUN_TESTS]
            == PermissionLevel.ALLOWED
        )


def test_workers_cannot_merge_main_without_approval():
    for role in WORKER_ROLES:
        permissions = get_role_permissions(role)

        assert (
            permissions[PermissionAction.MERGE_MAIN]
            == PermissionLevel.REQUIRES_APPROVAL
        )


def test_workers_cannot_spend_without_approval():
    for role in WORKER_ROLES:
        permissions = get_role_permissions(role)

        assert (
            permissions[PermissionAction.SPEND_MONEY]
            == PermissionLevel.REQUIRES_APPROVAL
        )


def test_workers_cannot_manage_credentials_without_approval():
    for role in WORKER_ROLES:
        permissions = get_role_permissions(role)

        assert (
            permissions[PermissionAction.ADD_CREDENTIAL]
            == PermissionLevel.REQUIRES_APPROVAL
        )

        assert (
            permissions[PermissionAction.CHANGE_CREDENTIAL]
            == PermissionLevel.REQUIRES_APPROVAL
        )


def test_system_has_limited_permissions():
    permissions = get_role_permissions(ROLE_SYSTEM)

    assert (
        permissions[PermissionAction.READ_CODE]
        == PermissionLevel.ALLOWED
    )

    assert (
        permissions[PermissionAction.RUN_TESTS]
        == PermissionLevel.ALLOWED
    )

    assert (
        permissions[PermissionAction.USE_RESOURCE]
        == PermissionLevel.ALLOWED
    )

    assert PermissionAction.SPEND_MONEY not in permissions


def test_unknown_role_has_no_permissions():
    permissions = get_role_permissions("unknown_role")

    assert permissions == {}
