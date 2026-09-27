"""
Control del presupuesto de recursos de THE ODIN PROJECT.
"""

from dataclasses import dataclass

from .limits import ResourceLimits
from .usage import ResourceUsage


@dataclass
class ResourceBudget:
    """Combina límites y consumo para controlar recursos."""

    limits: ResourceLimits
    usage: ResourceUsage

    def daily_available(self) -> int:
        """Devuelve los tokens diarios disponibles."""

        usable = self.limits.usable_tokens(
            self.limits.daily_token_limit
        )

        return max(
            0,
            usable - self.usage.daily_tokens
        )

    def monthly_available(self) -> int:
        """Devuelve los tokens mensuales disponibles."""

        usable = self.limits.usable_tokens(
            self.limits.monthly_token_limit
        )

        return max(
            0,
            usable - self.usage.monthly_tokens
        )

    def can_use(self, estimated_tokens: int) -> bool:
        """
        Comprueba si una tarea puede ejecutarse
        sin consumir la reserva de seguridad.
        """

        if estimated_tokens < 0:
            raise ValueError(
                "La estimación de tokens no puede ser negativa."
            )

        return (
            estimated_tokens <= self.daily_available()
            and estimated_tokens <= self.monthly_available()
        )

    def consume(self, tokens: int) -> bool:
        """
        Registra consumo si existe presupuesto disponible.
        """

        if not self.can_use(tokens):
            return False

        self.usage.add_tokens(tokens)

        return True

    def safety_reserve_active(self) -> bool:
        """Indica si el consumo alcanzó la zona de reserva."""

        return (
            self.daily_available() <= 0
            or self.monthly_available() <= 0
  )
