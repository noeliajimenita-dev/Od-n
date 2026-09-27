"""
Administrador central de recursos de THE ODIN PROJECT.
"""

from dataclasses import dataclass

from .alerts import ResourceAlert, create_alert
from .budget import ResourceBudget
from .limits import ResourceLimits
from .usage import ResourceUsage


@dataclass
class ResourceManager:
    """Coordina el control de recursos."""

    limits: ResourceLimits
    usage: ResourceUsage

    @property
    def budget(self) -> ResourceBudget:
        """Devuelve el presupuesto actual."""

        return ResourceBudget(
            limits=self.limits,
            usage=self.usage,
        )

    def can_execute(self, estimated_tokens: int) -> bool:
        """Comprueba si una tarea puede utilizar recursos."""

        return self.budget.can_use(
            estimated_tokens
        )

    def consume(self, tokens: int) -> bool:
        """Registra consumo si existe presupuesto disponible."""

        return self.budget.consume(tokens)

    def get_daily_alert(self) -> ResourceAlert | None:
        """Obtiene la alerta correspondiente al consumo diario."""

        return create_alert(
            self.usage.daily_tokens,
            self.limits.daily_token_limit,
        )

    def get_monthly_alert(self) -> ResourceAlert | None:
        """Obtiene la alerta correspondiente al consumo mensual."""

        return create_alert(
            self.usage.monthly_tokens,
            self.limits.monthly_token_limit,
        )

    def is_resource_limit_reached(self) -> bool:
        """Indica si se alcanzó algún límite disponible."""

        return (
            self.usage.is_daily_limit_reached(
                self.limits.daily_token_limit
            )
            or self.usage.is_monthly_limit_reached(
                self.limits.monthly_token_limit
            )
        )

    def reset_daily(self) -> None:
        """Reinicia el consumo diario."""

        self.usage.reset_daily()

    def reset_monthly(self) -> None:
        """Reinicia el consumo mensual."""

        self.usage.reset_monthly()
