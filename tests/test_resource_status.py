from src.resource_manager.limits import ResourceLimits
from src.resource_manager.manager import ResourceManager
from src.resource_manager.status import get_resource_status
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


def test_resource_status_returns_dictionary():
    manager = create_manager()

    status = get_resource_status(manager)

    assert isinstance(status, dict)


def test_resource_status_contains_daily_information():
    manager = create_manager()

    status = get_resource_status(manager)

    assert "daily" in status
    assert "used" in status["daily"]
    assert "limit" in status["daily"]
    assert "available" in status["daily"]
    assert "alert_level" in status["daily"]


def test_resource_status_contains_monthly_information():
    manager = create_manager()

    status = get_resource_status(manager)

    assert "monthly" in status
    assert "used" in status["monthly"]
    assert "limit" in status["monthly"]
    assert "available" in status["monthly"]
    assert "alert_level" in status["monthly"]


def test_initial_resource_status():
    manager = create_manager()

    status = get_resource_status(manager)

    assert status["daily"]["used"] == 0
    assert status["monthly"]["used"] == 0
    assert status["limit_reached"] is False


def test_resource_status_after_consumption():
    manager = create_manager()

    manager.consume(500)

    status = get_resource_status(manager)

    assert status["daily"]["used"] == 500
    assert status["monthly"]["used"] == 500
    assert status["daily"]["alert_level"] == 50
