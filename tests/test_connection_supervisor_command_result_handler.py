from unittest.mock import Mock

from src.telegram.connection_supervisor_command_result import (
    ConnectionCommandResult,
)
from src.telegram.connection_supervisor_command_result_handler import (
    ConnectionSupervisorCommandResultHandler,
)


def test_handle_returns_blocked_status_for_none_result():
    handler = ConnectionSupervisorCommandResultHandler()

    result = handler.handle(None)

    assert result == "COMMAND_BLOCKED"


def test_handle_converts_result_to_string():
    handler = ConnectionSupervisorCommandResultHandler()
    result = Mock(spec=ConnectionCommandResult)

    result.__str__ = Mock(return_value="COMMAND_OK")

    output = handler.handle(result)

    assert output == "COMMAND_OK"
    result.__str__.assert_called_once()
