from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


class OdinSystemValidator:
    """
    Valida la configuración de los componentes principales de ODIN.

    No ejecuta tareas ni modifica el sistema.
    Su función es detectar dependencias faltantes antes de iniciar
    operaciones reales.
    """

    REQUIRED_COMPONENTS = (
        "runtime",
        "logs",
        "backups",
        "recovery",
    )

    OPTIONAL_COMPONENTS = (
        "supervisor",
        "execution_service",
        "ai_service",
        "platform_manager",
    )

    def validate(self, system: Any) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        if system is None:
            return ValidationResult(
                valid=False,
                errors=["ODIN system is not configured"],
            )

        for component in self.REQUIRED_COMPONENTS:
            value = getattr(system, component, None)

            if value is None:
                errors.append(
                    f"Required component is missing: {component}"
                )

        for component in self.OPTIONAL_COMPONENTS:
            value = getattr(system, component, None)

            if value is None:
                warnings.append(
                    f"Optional component is not configured: {component}"
                )

        self._validate_runtime(system, errors)
        self._validate_logs(system, errors)
        self._validate_backups(system, errors)
        self._validate_recovery(system, errors)

        return ValidationResult(
            valid=not errors,
            errors=errors,
            warnings=warnings,
        )

    def _validate_runtime(
        self,
        system: Any,
        errors: list[str],
    ) -> None:
        runtime = getattr(system, "runtime", None)

        if runtime is None:
            return

        required_methods = (
            "start",
            "pause",
            "resume",
            "stop",
            "run_once",
            "status",
        )

        self._validate_methods(
            runtime,
            "runtime",
            required_methods,
            errors,
        )

    def _validate_logs(
        self,
        system: Any,
        errors: list[str],
    ) -> None:
        logs = getattr(system, "logs", None)

        if logs is None:
            return

        required_methods = (
            "summary",
            "export",
        )

        self._validate_methods(
            logs,
            "logs",
            required_methods,
            errors,
        )

    def _validate_backups(
        self,
        system: Any,
        errors: list[str],
    ) -> None:
        backups = getattr(system, "backups", None)

        if backups is None:
            return

        required_methods = (
            "create_backup",
            "status",
        )

        self._validate_methods(
            backups,
            "backups",
            required_methods,
            errors,
        )

    def _validate_recovery(
        self,
        system: Any,
        errors: list[str],
    ) -> None:
        recovery = getattr(system, "recovery", None)

        if recovery is None:
            return

        required_methods = (
            "restore",
            "status",
        )

        self._validate_methods(
            recovery,
            "recovery",
            required_methods,
            errors,
        )

    @staticmethod
    def _validate_methods(
        component: Any,
        component_name: str,
        required_methods: tuple[str, ...],
        errors: list[str],
    ) -> None:
        for method_name in required_methods:
            method = getattr(component, method_name, None)

            if not callable(method):
                errors.append(
                    f"Component '{component_name}' "
                    f"does not provide required method: {method_name}"
                )

    def is_valid(self, system: Any) -> bool:
        return self.validate(system).valid

    def assert_valid(self, system: Any) -> None:
        result = self.validate(system)

        if result.valid:
            return

        message = "; ".join(result.errors)

        raise RuntimeError(
            f"ODIN system validation failed: {message}"
  )
