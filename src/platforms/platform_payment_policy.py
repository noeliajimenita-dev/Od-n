
"""Payment policy by platform for ODIN.

This module does not send payments or messages.
Unknown platform rules default to using the platform's
official payment methods.
"""

from dataclasses import dataclass
from enum import Enum


class PaymentRoute(str, Enum):
    PLATFORM = "platform"
    DIRECT_TRANSFER = "direct_transfer"
    REVIEW_REQUIRED = "review_required"


@dataclass(frozen=True)
class PaymentPolicyResult:
    platform: str
    route: PaymentRoute
    allowed: bool
    requires_user_approval: bool
    reason: str


class PlatformPaymentPolicy:
    """Conservative payment routing rules."""

    def __init__(self, direct_transfer_platforms=None):
        # Only explicitly configured direct-client sources are eligible.
        self._direct_transfer_platforms = {
            name.strip().lower()
            for name in (direct_transfer_platforms or [])
            if isinstance(name, str) and name.strip()
        }

    def evaluate(
        self,
        platform: str,
        direct_client: bool = False,
        client_requested_payment_details: bool = False,
    ) -> PaymentPolicyResult:
        name = (platform or "").strip().lower()

        if not name:
            return PaymentPolicyResult(
                platform="unknown",
                route=PaymentRoute.REVIEW_REQUIRED,
                allowed=False,
                requires_user_approval=True,
                reason="Platform is unknown; review payment rules first.",
            )

        # Known freelance marketplaces should use their permitted
        # payment and withdrawal flows.
        if name in {"upwork", "fiverr"}:
            return PaymentPolicyResult(
                platform=name,
                route=PaymentRoute.PLATFORM,
                allowed=True,
                requires_user_approval=True,
                reason="Use the marketplace's permitted payment methods.",
            )

        if not direct_client:
            return PaymentPolicyResult(
                platform=name,
                route=PaymentRoute.REVIEW_REQUIRED,
                allowed=False,
                requires_user_approval=True,
                reason="Confirm the employment or contract payment process.",
            )

        if name not in self._direct_transfer_platforms:
            return PaymentPolicyResult(
                platform=name,
                route=PaymentRoute.REVIEW_REQUIRED,
                allowed=False,
                requires_user_approval=True,
                reason="Direct transfers are not enabled for this source.",
            )

        if not client_requested_payment_details:
            return PaymentPolicyResult(
                platform=name,
                route=PaymentRoute.DIRECT_TRANSFER,
                allowed=False,
                requires_user_approval=True,
                reason="Wait until the client requests payment instructions.",
            )

        return PaymentPolicyResult(
            platform=name,
            route=PaymentRoute.DIRECT_TRANSFER,
            allowed=True,
            requires_user_approval=True,
            reason="Direct transfer may be prepared for your approval.",
        )

