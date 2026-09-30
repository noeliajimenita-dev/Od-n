from unittest.mock import Mock

from src.telegram.connection_supervisor_command_dispatcher import (
    ConnectionSupervisorCommandDispatcher,
)
from src.telegram.connection_supervisor_command_pipeline import (
    ConnectionSupervisorCommandPipeline,
)
from src.telegram.connection_supervisor_command_result import (
    ConnectionCommandResult,
)
from src.telegram.connection_supervisor_commands import (
    ConnectionCommandRequest,
)


def test_process_dispatches_request_and_returns_result():
    dispatcher = Mock(spec=ConnectionSupervisorCommandDispatcher)
    expected_result = Mock(spec=ConnectionCommandResult)
    request = Mock(spec=ConnectionCommandRequest)

    dispatcher.dispatch.return_value = expected_result

    pipeline = ConnectionSupervisorCommandPipeline(dispatcher)

    result = pipeline.process(request)

    dispatcher.dispatch.assert_called_once_with(request)
    assert result is expected_result
