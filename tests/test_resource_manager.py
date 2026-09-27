from src.resource_manager.alerts import (
    create_alert,
    get_alert_level,
    get_usage_percentage,
)
from src.resource_manager.budget import ResourceBudget
from src.resource_manager.limits import ResourceLimits
from src.resource_manager.manager import ResourceManager
from src.resource_manager.usage import ResourceUsage


def create_manager():
    limits = ResourceLimits(
        daily_token_limit=1000,
        monthly_token_limit=10000,
        safety_reserve_percent=10,
    )

    usage = ResourceUsage()

    return ResourceManager(
        limits=limits,
        usage=usage,
    )


def test_usage_percentage():
    assert get_usage_percentage(500, 1000) == 50.0


def test_alert_level():
    assert get_alert_level(500, 1000) == 50
    assert get_alert_level(750, 1000) == 75
    assert get_alert_level(900, 1000) == 90
    assert get_alert_level(1000, 1000) == 100


def test_alert_creation():
    alert = create_alert(900, 1000)

    assert alert is not None
    assert alert.level == 90


def test_usage_tracking():
    usage = ResourceUsage()

    usage.add_tokens(250)

    assert usage.daily_tokens == 250
    assert usage.monthly_tokens == 250


def test_budget_allows_safe_consumption():
    manager = create_manager()

    assert manager.can_execute(500) is True


def test_budget_protects_safety_reserve():
    manager = create_manager()

    assert manager.can_execute(901) is False


def test_resource_consumption():
    manager = create_manager()

    result = manager.consume(500)

    assert result is True
    assert manager.usage.daily_tokens == 500
    assert manager.usage.monthly_tokens == 500


def test_consumption_beyond_budget_is_rejected():
    manager = create_manager()

    result = manager.consume(901)

    assert result is False
    assert manager.usage.daily_tokens == 0


def test_resource_limit_detection():
    manager = create_manager()

    manager.usage.add_tokens(1000)

    assert manager.is_resource_limit_reached() is True


def test_daily_reset():
    manager = create_manager()

    manager.usage.add_tokens(500)
    manager.reset_daily()

    assert manager.usage.daily_tokens == 0
    assert manager.usage.monthly_tokens == 500


def test_monthly_reset():
    manager = create_manager()

    manager.usage.add_tokens(500)
    manager.reset_monthly()

    assert manager.usage.monthly_tokens == 0
    assert manager.usage.daily_tokens == 500
