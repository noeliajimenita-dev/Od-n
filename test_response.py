from src.telegram.response import TelegramResponse


def test_success_response():
    response = TelegramResponse.success_response(
        bot_name="supervisor",
        text="Tarea completada.",
    )

    assert response.bot_name == "supervisor"
    assert response.text == "Tarea completada."
    assert response.success
    assert not response.is_empty()


def test_error_response():
    response = TelegramResponse.error_response(
        bot_name="worker_1",
        text="Ocurrió un error.",
    )

    assert response.bot_name == "worker_1"
    assert not response.success
    assert not response.is_empty()


def test_empty_response():
    response = TelegramResponse(
        bot_name="worker_2",
        text="   ",
    )

    assert response.is_empty()
