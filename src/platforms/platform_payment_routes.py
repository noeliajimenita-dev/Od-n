
"""Payment route registry for ODIN's job platforms.

These are default payment-route classifications, not a guarantee
of each platform's current rules or a verification of a specific job.
Unknown platforms require review.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class PaymentRoute(str, Enum):
    PLATFORM_WALLET = "platform_wallet"
    EXTERNAL_EMPLOYER = "external_employer"
    REVIEW_REQUIRED = "review_required"


@dataclass(frozen=True)
class PlatformPaymentRoute:
    platform: str
    route: PaymentRoute
    description: str
    requires_user_approval: bool = True


class PlatformPaymentRoutes:
    """Provides default payment routes for supported job platforms."""

    DEFAULT_ROUTES: Dict[str, PlatformPaymentRoute] = {
        "upwork": PlatformPaymentRoute(
            platform="Upwork",
            route=PaymentRoute.PLATFORM_WALLET,
            description=(
                "Use Upwork's permitted contract, payment, "
                "and withdrawal processes."
            ),
        ),
        "workana": PlatformPaymentRoute(
            platform="Workana",
            route=PaymentRoute.PLATFORM_WALLET,
            description=(
                "Use Workana's permitted payment and withdrawal "
                "processes for the contract."
            ),
        ),
        "fiverr": PlatformPaymentRoute(
            platform="Fiverr",
            route=PaymentRoute.PLATFORM_WALLET,
            description=(
                "Use Fiverr's permitted order, payment, "
                "and withdrawal processes."
            ),
        ),
        "computrabajo": PlatformPaymentRoute(
            platform="Computrabajo",
            route=PaymentRoute.EXTERNAL_EMPLOYER,
            description=(
                "For a legitimate employment relationship, "
                "confirm payroll and payment details directly "
                "with the verified employer."
            ),
        ),
        "linkedin": PlatformPaymentRoute(
            platform="LinkedIn",
            route=PaymentRoute.EXTERNAL_EMPLOYER,
            description=(
                "Confirm the employment contract and payroll "
                "process with the verified employer."
            ),
        ),
        "bumeran": PlatformPaymentRoute(
            platform="Bumeran",
            route=PaymentRoute.EXTERNAL_EMPLOYER,
            description=(
                "Confirm the employment contract and payment "
                "process with the verified employer."
            ),
        ),
    }

    def get_route(
        self,
        platform: str,
    ) -> PlatformPaymentRoute:
        """Return the default route; unknown platforms require review."""

        key = (platform or "").strip().lower()
        route = self.DEFAULT_ROUTES.get(key)

        if route is not None:
            return route

        return PlatformPaymentRoute(
            platform=platform.strip() if platform else "Unknown",
            route=PaymentRoute.REVIEW_REQUIRED,
            description=(
                "Payment route is unknown. Verify the platform's "
                "current rules and the client's identity before proceeding."
            ),
        )

    def all_routes(self) -> Dict[str, PlatformPaymentRoute]:
        """Return a copy of the configured default routes."""

        return dict(self.DEFAULT_ROUTES)

    def requires_external_payment_review(
        self,
        platform: str,
        employer_verified: bool,
        payment_terms_confirmed: bool,
    ) -> bool:
        """External payroll requires a verified employer and confirmed terms."""

        route = self.get_route(platform)

        if route.route == PaymentRoute.REVIEW_REQUIRED:
            return True

        if route.route == PaymentRoute.EXTERNAL_EMPLOYER:
            return not (employer_verified and payment_terms_confirmed)

        return False

    def can_prepare_payment_instructions(
        self,
        platform: str,
        direct_client: bool = False,
        employer_verified: bool = False,
        payment_terms_confirmed: bool = False,
    ) -> bool:
        """Decide whether payment instructions may be prepared for review.

        This does not send instructions or override platform rules.
        """

        route = self.get_route(platform)

        if route.route == PaymentRoute.REVIEW_REQUIRED:
            return False

        if route.route == PaymentRoute.PLATFORM_WALLET:
            # Payment must remain within the platform's permitted flow.
            return False

        return (
            direct_client
            and employer_verified
            and payment_terms_confirmed
        )
