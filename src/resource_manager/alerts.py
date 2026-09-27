"""
Sistema de alertas de consumo de recursos.
"""

from dataclasses import dataclass


@dataclass
class ResourceAlert:
    """Representa una alerta de consumo."""

    level: int
    message: str


ALERT_LEVELS = {
    50: "Consumo de recursos al 50%.",
    75: "Consumo de recursos al 75%.",
    90: "Consumo de recursos al 90%.",
    100: "Límite de recursos alcanzado.",
}


def get_usage_percentage(
    used: int,
    limit: int,
) -> float:
    """Calcula el porcentaje de consumo."""

    if used < 0:
        raise ValueError(
            "El consumo no puede ser negativo."
        )

    if limit <= 0:
        return 0.0

    return (used / limit) * 100


def get_alert_level(
    used: int,
    limit: int,
) -> int | None:
    """
    Devuelve el nivel de alerta alcanzado.

    Se devuelve el nivel más alto alcanzado.
    """

    percentage = get_usage_percentage(
        used,
        limit,
    )

    reached_levels = [
        level
        for level in ALERT_LEVELS
        if percentage >= level
    ]

    if not reached_levels:
        return None

    return max(reached_levels)


def create_alert(
    used: int,
    limit: int,
) -> ResourceAlert | None:
    """Crea una alerta si se alcanzó un nivel configurado."""

    level = get_alert_level(
        used,
        limit,
    )

    if level is None:
        return None

    return ResourceAlert(
        level=level,
        message=ALERT_LEVELS[level],
  )
