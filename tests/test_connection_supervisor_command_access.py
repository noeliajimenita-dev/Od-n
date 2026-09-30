from unittest.mock import Mock

from src.telegram.connection_supervisor_command_access import (
    ConnectionSupervisorCommandAccess,
)
from src.telegram.connection_supervisor_command_guard import (
    ConnectionSupervisorCommandGuard,
)
from src.telegram.connection_supervisor_commands import (
    ConnectionCommandRequest,
)


def test_can_execute_returns_true_when_guard_allows():
    guard = Mock(spec=ConnectionSupervisorCommandGuard)
    request = Mock(spec=ConnectionCommandRequest)

    guard.allow.return_value = True

    access = ConnectionSupervisorCommandAccess(guard)

    assert access.can_execute(request) is True
    guard.allow.assert_called_once_with(request)


def test_can_execute_returns_false_when_guard_blocks():
    guard = Mock(spec=ConnectionSupervisorCommandGuard)
    request = Mock(spec=ConnectionCommandRequest)

    guard.allow.return_value = False

    access = ConnectionSupervisorCommandAccess(guard)

    assert access.can_execute(request) is False
    guard.allow.assert_called_once_with(request)
