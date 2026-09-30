from unittest.mock import Mock

from src.telegram.connection_supervisor_command_result import (
    ConnectionCommandResult,
)
from src.telegram.connection_supervisor_command_result_handler import (
    ConnectionSupervisorCommandResultHandler,
)
from src.telegram.connection_supervisor_command_response import (
    ConnectionSupervisorCommandResponse,
)


def test_build_returns_handler_response():
    result_handler = Mock(
        spec=ConnectionSupervisorCommandResultHandler
    )
    result = Mock(spec=ConnectionCommandResult)

    result_handler.handle.return_value = "COMMAND_OK"

    response = ConnectionSupervisorCommandResponse(
        result_handler
    )

    output = response.build(result)

    result_handler.handle.assert_called_once_with(result)
    assert output == "COMMAND_OK"


def test_build_handles_blocked_command():
    result_handler = Mock(
        spec=ConnectionSupervisorCommandResultHandler
    )

    result_handler.handle.return_value = "COMMAND_BLOCKED"

    response = ConnectionSupervisorCommandResponse(
        result_handler
    )

    output = response.build(None)

    result_handler.handle.assert_called_once_with(None)
    assert output == "COMMAND_BLOCKED"
