"""
Estado seguro del Resource Manager.
"""

from .manager import ResourceManager


def get_resource_status(
    manager: ResourceManager,
) -> dict:
    """
    Devuelve un resumen del estado actual
    de los recursos.
    """

    daily_limit = manager.limits.daily_token_limit
    monthly_limit = manager.limits.monthly_token_limit

    daily_used = manager.usage.daily_tokens
    monthly_used = manager.usage.monthly_tokens

    daily_alert = manager.get_daily_alert()
    monthly_alert = manager.get_monthly_alert()

    return {
        "daily": {
            "used": daily_used,
            "limit": daily_limit,
            "available": manager.budget.daily_available(),
            "alert_level": (
                daily_alert.level
                if daily_alert
                else None
            ),
        },
        "monthly": {
            "used": monthly_used,
            "limit": monthly_limit,
            "available": manager.budget.monthly_available(),
            "alert_level": (
                monthly_alert.level
                if monthly_alert
                else None
            ),
        },
        "limit_reached": (
            manager.is_resource_limit_reached()
        ),
    }
