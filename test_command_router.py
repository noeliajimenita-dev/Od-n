import pytest

from src.telegram.command import TelegramCommand
from src.telegram.command_router import TelegramCommandRouter


def test_register_and_dispatch_command():
    router = TelegramCommandRouter()

    def handler(command):
        return f"Ejecutado: {command.name}"

    router.register("status", handler)

    command = TelegramCommand.parse("/status")

    assert command is not None
    assert router.dispatch(command) == "Ejecutado: status"


def test_unknown_command_raises_error():
    router = TelegramCommandRouter()

    command = TelegramCommand.parse("/unknown")

    assert command is not None

    with pytest.raises(KeyError):
        router.dispatch(command)


def test_has_handler():
    router = TelegramCommandRouter()

    router.register("start", lambda command: "ok")

    assert router.has_handler("start")
    assert not router.has_handler("stop")


def test_get_commands():
    router = TelegramCommandRouter()

    router.register("status", lambda command: "status")
    router.register("start", lambda command: "start")

    assert router.get_commands() == ("start", "status")
