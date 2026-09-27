"""
Registro básico del consumo de recursos.
"""

from dataclasses import dataclass


@dataclass
class ResourceUsage:
    """Representa el consumo acumulado de un recurso."""

    daily_tokens: int = 0
    monthly_tokens: int = 0

    def add_tokens(self, amount: int) -> None:
        """Agrega tokens al consumo diario y mensual."""

        if amount < 0:
            raise ValueError(
                "La cantidad de tokens no puede ser negativa."
            )

        self.daily_tokens += amount
        self.monthly_tokens += amount

    def reset_daily(self) -> None:
        """Reinicia únicamente el contador diario."""

        self.daily_tokens = 0

    def reset_monthly(self) -> None:
        """Reinicia el contador mensual."""

        self.monthly_tokens = 0

    def remaining_daily(self, limit: int) -> int:
        """Devuelve los tokens diarios restantes."""

        if limit < 0:
            raise ValueError(
                "El límite no puede ser negativo."
            )

        return max(0, limit - self.daily_tokens)

    def remaining_monthly(self, limit: int) -> int:
        """Devuelve los tokens mensuales restantes."""

        if limit < 0:
            raise ValueError(
                "El límite no puede ser negativo."
            )

        return max(0, limit - self.monthly_tokens)

    def is_daily_limit_reached(self, limit: int) -> bool:
        """Indica si se alcanzó el límite diario."""

        return self.daily_tokens >= limit

    def is_monthly_limit_reached(self, limit: int) -> bool:
        """Indica si se alcanzó el límite mensual."""

        return self.monthly_tokens >= limit
