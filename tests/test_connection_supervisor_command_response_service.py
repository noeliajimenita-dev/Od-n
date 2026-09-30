from unittest.mock import Mock

from src.telegram.connection_supervisor_command_response import (
    ConnectionSupervisorCommandResponse,
)
from src.telegram.connection_supervisor_command_response_sender import (
    ConnectionSupervisorCommandResponseSender,
)
from src.telegram.connection_supervisor_command_response_service import (
    ConnectionSupervisorCommandResponseService,
)
from src.telegram.connection_supervisor_command_result import (
    ConnectionCommandResult,
)


def test_handle_builds_sends_and_returns_response():
    response = Mock(spec=ConnectionSupervisorCommandResponse)
    sender = Mock(spec=ConnectionSupervisorCommandResponseSender)
    result = Mock(spec=ConnectionCommandResult)

    response.build.return_value = "COMMAND_OK"

    service = ConnectionSupervisorCommandResponseService(
        response,
        sender,
    )

    output = service.handle(result)

    response.build.assert_called_once_with(result)
    sender.send.assert_called_once_with("COMMAND_OK")
    assert output == "COMMAND_OK"


def test_handle_supports_blocked_result():
    response = Mock(spec=ConnectionSupervisorCommandResponse)
    sender = Mock(spec=ConnectionSupervisorCommandResponseSender)

    response.build.return_value = "COMMAND_BLOCKED"

    service = ConnectionSupervisorCommandResponseService(
        response,
        sender,
    )

    output = service.handle(None)

    response.build.assert_called_once_with(None)
    sender.send.assert_called_once_with("COMMAND_BLOCKED")
    assert output == "COMMAND_BLOCKED"
