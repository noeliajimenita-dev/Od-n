from unittest.mock import Mock

from src.telegram.connection_supervisor_command_guard import (
    ConnectionSupervisorCommandGuard,
)
from src.telegram.connection_supervisor_command_security import (
    ConnectionSupervisorCommandSecurity,
)
from src.telegram.connection_supervisor_command_validation import (
    ConnectionSupervisorCommandValidation,
)
from src.telegram.connection_supervisor_commands import (
    ConnectionCommandRequest,
)


def test_allow_returns_true_when_validation_and_security_pass():
    validation = Mock(spec=ConnectionSupervisorCommandValidation)
    security = Mock(spec=ConnectionSupervisorCommandSecurity)
    request = Mock(spec=ConnectionCommandRequest)

    validation.validate.return_value = True
    security.is_allowed.return_value = True

    guard = ConnectionSupervisorCommandGuard(validation, security)

    assert guard.allow(request) is True
    validation.validate.assert_called_once_with(request)
    security.is_allowed.assert_called_once_with(request)


def test_allow_returns_false_when_validation_fails():
    validation = Mock(spec=ConnectionSupervisorCommandValidation)
    security = Mock(spec=ConnectionSupervisorCommandSecurity)
    request = Mock(spec=ConnectionCommandRequest)

    validation.validate.return_value = False

    guard = ConnectionSupervisorCommandGuard(validation, security)

    assert guard.allow(request) is False
    validation.validate.assert_called_once_with(request)
    security.is_allowed.assert_not_called()


def test_allow_returns_false_when_security_rejects():
    validation = Mock(spec=ConnectionSupervisorCommandValidation)
    security = Mock(spec=ConnectionSupervisorCommandSecurity)
    request = Mock(spec=ConnectionCommandRequest)

    validation.validate.return_value = True
    security.is_allowed.return_value = False

    guard = ConnectionSupervisorCommandGuard(validation, security)

    assert guard.allow(request) is False
    validation.validate.assert_called_once_with(request)
    security.is_allowed.assert_called_once_with(request)
