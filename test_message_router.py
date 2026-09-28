import pytest

from src.telegram.message import TelegramMessage
from src.telegram.message_router import TelegramMessageRouter


def test_register_and_route_message():
    router = TelegramMessageRouter()

    router.register("supervisor", "supervisor_queue")

    message = TelegramMessage.create(
        chat_id="123",
        text="Hola Odin",
        bot_name="supervisor",
    )

    assert router.route(message) == "supervisor_queue"


def test_unknown_bot_route_raises_error():
    router = TelegramMessageRouter()

    message = TelegramMessage.create(
        chat_id="123",
        text="Hola",
        bot_name="worker_1",
    )

    with pytest.raises(KeyError):
        router.route(message)


def test_empty_message_raises_error():
    router = TelegramMessageRouter()

    router.register("supervisor", "supervisor_queue")

    message = TelegramMessage.create(
        chat_id="123",
        text="   ",
        bot_name="supervisor",
    )

    with pytest.raises(ValueError):
        router.route(message)


def test_get_routes_returns_copy():
    router = TelegramMessageRouter()

    router.register("worker_1", "worker_1_queue")

    routes = router.get_routes()

    assert routes == {"worker_1": "worker_1_queue"}
