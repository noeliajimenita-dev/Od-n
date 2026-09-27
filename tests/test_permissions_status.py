from src.permissions.actions import DEFAULT_PERMISSIONS, PermissionLevel
from src.permissions.status import get_permissions_status


def test_permissions_status_contains_expected_fields():
    status = get_permissions_status()

    assert "total_actions" in status
    assert "allowed" in status
    assert "requires_approval" in status
    assert "denied" in status


def test_total_actions_matches_permissions():
    status = get_permissions_status()

    assert status["total_actions"] == len(DEFAULT_PERMISSIONS)


def test_permission_counts_are_correct():
    status = get_permissions_status()

    expected_allowed = sum(
        1
        for level in DEFAULT_PERMISSIONS.values()
        if level == PermissionLevel.ALLOWED
    )

    expected_requires_approval = sum(
        1
        for level in DEFAULT_PERMISSIONS.values()
        if level == PermissionLevel.REQUIRES_APPROVAL
    )

    expected_denied = sum(
        1
        for level in DEFAULT_PERMISSIONS.values()
        if level == PermissionLevel.DENIED
    )

    assert status["allowed"] == expected_allowed
    assert status["requires_approval"] == expected_requires_approval
    assert status["denied"] == expected_denied


def test_permission_counts_add_up_to_total():
    status = get_permissions_status()

    assert (
        status["allowed"]
        + status["requires_approval"]
        + status["denied"]
        == status["total_actions"]
    )
