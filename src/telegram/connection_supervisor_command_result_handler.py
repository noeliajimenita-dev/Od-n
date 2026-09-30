from .connection_supervisor_command_result import ConnectionCommandResult


class ConnectionSupervisorCommandResultHandler:
    def handle(
        self,
        result: ConnectionCommandResult | None,
    ) -> str:
        if result is None:
            return "COMMAND_BLOCKED"

        return str(result)
