"""
Límites de recursos de THE ODIN PROJECT.

Este módulo proporciona una base para controlar
el consumo de tokens y otros recursos.
"""

from dataclasses import dataclass


@dataclass
class ResourceLimits:
    """Límites configurables de recursos."""

    daily_token_limit: int = 0
    monthly_token_limit: int = 0
    safety_reserve_percent: int = 10

    def validate(self) -> list[str]:
        """Valida los límites configurados."""

        errors = []

        if self.daily_token_limit < 0:
            errors.append(
                "daily_token_limit no puede ser negativo."
            )

        if self.monthly_token_limit < 0:
            errors.append(
                "monthly_token_limit no puede ser negativo."
            )

        if not 0 <= self.safety_reserve_percent <= 100:
            errors.append(
                "safety_reserve_percent debe estar entre 0 y 100."
            )

        return errors

    def is_valid(self) -> bool:
        """Indica si los límites son válidos."""
        return len(self.validate()) == 0

    def safety_reserve_tokens(
        self,
        limit: int,
    ) -> int:
        """
        Calcula la reserva de seguridad para un límite.
        """

        if limit < 0:
            raise ValueError(
                "El límite no puede ser negativo."
            )

        return int(
            limit * self.safety_reserve_percent / 100
        )

    def usable_tokens(self, limit: int) -> int:
        """
        Calcula cuántos tokens quedan disponibles
        después de reservar la cantidad de seguridad.
        """

        reserve = self.safety_reserve_tokens(limit)

        return max(0, limit - reserve)
