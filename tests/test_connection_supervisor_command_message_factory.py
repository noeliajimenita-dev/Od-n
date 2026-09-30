from src.telegram.connection_supervisor_command_message import (
    ConnectionSupervisorCommandMessage,
)
from src.telegram.connection_supervisor_command_message_factory import (
    ConnectionSupervisorCommandMessageFactory,
)


class FakeParser:
    def __init__(self, result):
        self.result = result

    def parse(self, message: str) -> str | None:
        return self.result


def test_factory_creates_valid_command_message():
    parser = FakeParser("APPROVE")
    factory = ConnectionSupervisorCommandMessageFactory(parser)

    message = factory.create("Approved")

    assert isinstance(message, ConnectionSupervisorCommandMessage)
    assert message.raw_text == "Approved"
    assert message.command == "APPROVE"
    assert message.is_valid is True


def test_factory_creates_invalid_command_message():
    parser = FakeParser(None)
    factory = ConnectionSupervisorCommandMessageFactory(parser)

    message = factory.create("unknown command")

    assert isinstance(message, ConnectionSupervisorCommandMessage)
    assert message.raw_text == "unknown command"
    assert message.command is None
    assert message.is_valid is False
