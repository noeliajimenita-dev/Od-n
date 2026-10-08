
"""Secure payment instructions for direct clients.

Bank details must be supplied through private environment variables.
Never commit real payment details to source control.
"""

from dataclasses import dataclass
from enum import Enum
import os
import re
from typing import Optional


class PaymentMethod(str, Enum):
    CBU = "cbu"
    CVU = "cvu"
    ALIAS = "alias"


class PaymentStatus(str, Enum):
    NOT_CONFIGURED = "not_configured"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class PaymentInstructions:
    method: PaymentMethod
    holder: str
    destination: str
    currency: str = "ARS"


@dataclass(frozen=True)
class PaymentInstructionResult:
    status: PaymentStatus
    message: str
    instructions: Optional[PaymentInstructions] = None


class PaymentInstructionService:
    """Prepares payment details without sending them automatically."""

    def __init__(self, environ=None):
        self._env = os.environ if environ is None else environ

    def _load_instructions(self) -> Optional[PaymentInstructions]:
        method_value = self._env.get("PAYMENT_METHOD", "").strip().lower()
        holder = self._env.get("PAYMENT_HOLDER", "").strip()

        if not method_value or not holder:
            return None

        try:
            method = PaymentMethod(method_value)
        except ValueError:
            return None

        if method == PaymentMethod.CBU:
            destination = self._env.get("PAYMENT_CBU", "").strip()
            if not re.fullmatch(r"\d{22}", destination):
                return None

        elif method == PaymentMethod.CVU:
            destination = self._env.get("PAYMENT_CVU", "").strip()
            if not re.fullmatch(r"\d{22}", destination):
                return None

        else:
            destination = self._env.get("PAYMENT_ALIAS", "").strip()
            if not destination or len(destination) > 50:
                return None

        return PaymentInstructions(
            method=method,
            holder=holder,
            destination=destination,
        )

    def prepare_for_client(
        self,
        platform: str,
        direct_client: bool,
        client_requested_payment_details: bool,
    ) -> PaymentInstructionResult:
        """Prepare details only for eligible direct-client payments."""

        if not direct_client:
            return PaymentInstructionResult(
                PaymentStatus.BLOCKED,
                "Use the platform's permitted payment method.",
            )

        if not client_requested_payment_details:
            return PaymentInstructionResult(
                PaymentStatus.BLOCKED,
                "Wait until the client requests payment instructions.",
            )

        instructions = self._load_instructions()
        if instructions is None:
            return PaymentInstructionResult(
                PaymentStatus.NOT_CONFIGURED,
                "Payment details are missing or invalid. Configure them privately.",
            )

        approval_required = (
            self._env.get("PAYMENT_REQUIRE_APPROVAL", "true").lower()
            == "true"
        )

        if approval_required:
            return PaymentInstructionResult(
                PaymentStatus.AWAITING_APPROVAL,
                "Review and approve these details before sharing them.",
                instructions,
            )

        # Even if approval is disabled, this service only prepares data.
        # Sending must be handled by a separate authorized component.
        return PaymentInstructionResult(
            PaymentStatus.APPROVED,
            "Instructions prepared. No message has been sent.",
            instructions,
        )

    @staticmethod
    def render_message(
        instructions: PaymentInstructions,
    ) -> str:
        """Render a message for human review; does not send it."""

        return (
            "Hola, estos son los datos para realizar la transferencia:\n"
            f"Titular: {instructions.holder}\n"
            f"Método: {instructions.method.value.upper()}\n"
            f"Destino: {instructions.destination}\n"
            f"Moneda: {instructions.currency}\n"
            "Por favor, confirmame cuando hayas realizado el pago."
        )
