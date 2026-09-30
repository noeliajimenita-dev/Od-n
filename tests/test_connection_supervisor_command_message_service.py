from src.telegram.connection_supervisor_command_message_service import (
    ConnectionSupervisorCommandMessageService,
)


class FakeFactory:
    def __init__(self, message):
        self.message = message

    def create(self, raw_text: str):
        return self.message


class FakeMessage:
    def __init__(self, valid: bool):
        self.is_valid = valid


def test_service_processes_message():
    message = FakeMessage(valid=True)
    factory = FakeFactory(message)

    service = ConnectionSupervisorCommandMessageService(factory)

    result = service.process("Approved")

    assert result is message


def test_service_accepts_valid_command():
    message = FakeMessage(valid=True)
    factory = FakeFactory(message)

    service = ConnectionSupervisorCommandMessageService(factory)

    assert service.is_valid("Approved") is True


def test_service_rejects_invalid_command():
    message = FakeMessage(valid=False)
    factory = FakeFactory(message)

    service = ConnectionSupervisorCommandMessageService(factory)

    assert service.is_valid("unknown command") is False
