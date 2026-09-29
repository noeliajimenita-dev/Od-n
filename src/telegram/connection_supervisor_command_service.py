from .connection_supervisor_command_executor import (
    TelegramConnectionSupervisorCommandExecutor,
)
from .connection_supervisor_command_result import ConnectionCommandResult
from .connection_supervisor_command_router import (
    TelegramConnectionSupervisorCommandRouter,
)
from .connection_supervisor_commands import ConnectionCommandRequest


class TelegramConnectionSupervisorCommandService:
    def __init__(
        self,
        router: TelegramConnectionSupervisorCommandRouter,
        executor: TelegramConnectionSupervisorCommandExecutor,
    ):
        self.router = router
        self.executor = executor

    def execute(
        self,
        request: ConnectionCommandRequest,
    ) -> ConnectionCommandResult:
        self.router.handler = _ExecutorAdapter(self.executor)
        result = self.router.route(request)

        if isinstance(result, ConnectionCommandResult):
            return result

        return ConnectionCommandResult.ok(result)


class _ExecutorAdapter:
    def __init__(
        self,
        executor: TelegramConnectionSupervisorCommandExecutor,
    ):
        self.executor = executor

    def handle(self, request: ConnectionCommandRequest):
        return self.executor.execute(request)
