from src.telegram.connection_supervisor_command_message_controller import (
    ConnectionSupervisorCommandMessageController,
)


class FakeService:
    def __init__(self, message):
        self.message = message

    def process(self, raw_text: str):
        return self.message

    def is_valid(self, raw_text: str) -> bool:
        return self.message.is_valid


class FakeMessage:
    def __init__(self, valid: bool):
        self.is_valid = valid


def test_controller_handles_message():
    message = FakeMessage(valid=True)
    service = FakeService(message)

    controller = ConnectionSupervisorCommandMessageController(service)

    result = controller.handle("Approved")

    assert result is message


def test_controller_accepts_valid_message():
    message = FakeMessage(valid=True)
    service = FakeService(message)

    controller = ConnectionSupervisorCommandMessageController(service)

    assert controller.is_valid("Approved") is True


def test_controller_rejects_invalid_message():
    message = FakeMessage(valid=False)
    service = FakeService(message)

    controller = ConnectionSupervisorCommandMessageController(service)

    assert controller.is_valid("unknown command") is False
