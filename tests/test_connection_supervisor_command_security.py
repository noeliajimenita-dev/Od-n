from unittest.mock import Mock

from src.telegram.connection_supervisor_command_security import (
    ConnectionSupervisorCommandSecurity,
)
from src.telegram.connection_supervisor_commands import (
    ConnectionCommandRequest,
)


def test_allows_connect_command():
    request = Mock(spec=ConnectionCommandRequest)
    request.command = "CONNECT"

    security = ConnectionSupervisorCommandSecurity()

    assert security.is_allowed(request) is True


def test_allows_status_command():
    request = Mock(spec=ConnectionCommandRequest)
    request.command = "STATUS"

    security = ConnectionSupervisorCommandSecurity()

    assert security.is_allowed(request) is True


def test_rejects_unknown_command():
    request = Mock(spec=ConnectionCommandRequest)
    request.command = "UNKNOWN"

    security = ConnectionSupervisorCommandSecurity()

    assert security.is_allowed(request) is False


def test_rejects_none_request():
    security = ConnectionSupervisorCommandSecurity()

    assert security.is_allowed(None) is False
