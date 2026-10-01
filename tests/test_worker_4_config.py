import pytest

from src.worker_4.config import Worker4Config


def test_config_has_default_values():
    config = Worker4Config()

    assert config.worker_id == "worker_4"
    assert config.enabled is False
    assert config.skills == []


def test_add_skill():
    config = Worker4Config()

    config.add_skill("data_analysis")

    assert config.skills == ["data_analysis"]
    assert config.has_skill("data_analysis") is True


def test_add_skill_does_not_duplicate():
    config = Worker4Config()

    config.add_skill("data_analysis")
    config.add_skill("data_analysis")

    assert config.skills == ["data_analysis"]


def test_add_empty_skill_fails():
    config = Worker4Config()

    with pytest.raises(ValueError):
        config.add_skill("   ")


def test_has_skill_returns_false_when_missing():
    config = Worker4Config()

    assert config.has_skill("cybersecurity") is False


def test_enable_worker():
    config = Worker4Config()

    config.enable()

    assert config.enabled is True


def test_disable_worker():
    config = Worker4Config(enabled=True)

    config.disable()

    assert config.enabled is False
