from src.telegram.connection_supervisor_command_service import (
    TelegramConnectionSupervisorCommandService,
)
from src.telegram.connection_supervisor_command_service_status import (
    get_connection_command_service_status,
)


class FakeRouter:
    pass


class FakeExecutor:
    pass


def test_command_service_is_available():
    service = TelegramConnectionSupervisorCommandService(
        router=FakeRouter(),
        executor=FakeExecutor(),
    )

    status = get_connection_command_service_status(service)

    assert status.available is True


def test_command_service_is_unavailable_without_router():
    service = TelegramConnectionSupervisorCommandService(
        router=None,
        executor=FakeExecutor(),
    )

    status = get_connection_command_service_status(service)

    assert status.available is False


def test_command_service_is_unavailable_without_executor():
    service = TelegramConnectionSupervisorCommandService(
        router=FakeRouter(),
        executor=None,
    )

    status = get_connection_command_service_status(service)

    assert status.available is False
