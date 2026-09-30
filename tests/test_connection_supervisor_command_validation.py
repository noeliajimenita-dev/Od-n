from unittest.mock import Mock

from src.telegram.connection_supervisor_command_validation import (
    ConnectionSupervisorCommandValidation,
)
from src.telegram.connection_supervisor_commands import (
    ConnectionCommandRequest,
)


def test_validate_accepts_complete_request():
    request = Mock(spec=ConnectionCommandRequest)
    request.command = "CONNECT"
    request.bot_name = "bot_1"

    validator = ConnectionSupervisorCommandValidation()

    assert validator.validate(request) is True


def test_validate_rejects_none_request():
    validator = ConnectionSupervisorCommandValidation()

    assert validator.validate(None) is False


def test_validate_rejects_missing_command():
    request = Mock(spec=ConnectionCommandRequest)
    request.command = None
    request.bot_name = "bot_1"

    validator = ConnectionSupervisorCommandValidation()

    assert validator.validate(request) is False


def test_validate_rejects_missing_bot_name():
    request = Mock(spec=ConnectionCommandRequest)
    request.command = "CONNECT"
    request.bot_name = None

    validator = ConnectionSupervisorCommandValidation()

    assert validator.validate(request) is False
