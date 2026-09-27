from src.telegram.registry import (
    create_bot_registry,
    get_bot,
    get_enabled_bots,
)


def test_registry_contains_six_bots():
    registry = create_bot_registry()

    assert len(registry) == 6


def test_registry_contains_supervisor_and_workers():
    registry = create_bot_registry()

    expected_bots = {
        "supervisor",
        "worker_1",
        "worker_2",
        "worker_3",
        "worker_4",
        "worker_5",
    }

    assert set(registry.keys()) == expected_bots


def test_get_bot():
    registry = create_bot_registry()

    bot = get_bot("worker_1", registry)

    assert bot is not None
    assert bot.name == "worker_1"


def test_get_unknown_bot():
    registry = create_bot_registry()

    bot = get_bot("unknown_bot", registry)

    assert bot is None


def test_all_bots_are_enabled_by_default():
    registry = create_bot_registry()

    enabled_bots = get_enabled_bots(registry)

    assert len(enabled_bots) == 6


def test_disabled_bot_is_not_returned():
    registry = create_bot_registry()

    registry["worker_3"].__class__

    registry["worker_3"] = type(registry["worker_3"])(
        name="worker_3",
        token_env_variable="TELEGRAM_WORKER_3_BOT_TOKEN",
        enabled=False,
    )

    enabled_bots = get_enabled_bots(registry)

    assert len(enabled_bots) == 5
    assert all(bot.name != "worker_3" for bot in enabled_bots)
