from src.telegram.connection_supervisor_command_service import (
    TelegramConnectionSupervisorCommandService,
)
from src.telegram.connection_supervisor_command_service_report import (
    build_connection_command_service_report,
)


class FakeRouter:
    pass


class FakeExecutor:
    pass


def test_report_when_service_is_available():
    service = TelegramConnectionSupervisorCommandService(
        router=FakeRouter(),
        executor=FakeExecutor(),
    )

    report = build_connection_command_service_report(service)

    assert "TELEGRAM COMMAND SERVICE" in report
    assert "Status: AVAILABLE" in report


def test_report_when_service_is_unavailable():
    service = TelegramConnectionSupervisorCommandService(
        router=None,
        executor=FakeExecutor(),
    )

    report = build_connection_command_service_report(service)

    assert "TELEGRAM COMMAND SERVICE" in report
    assert "Status: UNAVAILABLE" in report
