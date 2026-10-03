from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class JobOpportunity:
    job_id: str
    title: str
    description: str = ""
    budget: float = 0.0
    currency: str = "USD"
    estimated_hours: float | None = None
    required_skills: tuple[str, ...] = ()
    client_verified: bool = False
    payment_verified: bool = False
    client_hires: int = 0
    client_spend: float = 0.0
    platform: str = ""
    external_communication_requested: bool = False
    upfront_payment_requested: bool = False
    free_work_requested: bool = False
    suspicious_link: bool = False
    personal_information_requested: bool = False
    unusually_high_pay: bool = False


@dataclass(frozen=True)
class OpportunityAnalysis:
    job_id: str
    title: str
    value_score: float
    skill_match_score: float
    risk_score: float
    expected_value: float
    risk_level: str
    recommendation: str
    reasons: tuple[str, ...] = field(default_factory=tuple)


class JobOpportunityAnalyzer:
    """
    Analiza oportunidades freelance para ODIN.

    IMPORTANTE:
    Este analizador no determina que una oferta sea realmente una estafa.
    Solamente identifica señales de riesgo y datos verificables disponibles.
    """

    RISK_WEIGHTS = {
        "external_communication": 30.0,
        "upfront_payment": 35.0,
        "free_work": 30.0,
        "suspicious_link": 25.0,
        "personal_information": 25.0,
        "unusually_high_pay": 15.0,
        "unverified_payment": 10.0,
        "unverified_client": 5.0,
    }

    def __init__(
        self,
        bot_skills: Iterable[str] = (),
        minimum_expected_value: float = 20.0,
        maximum_risk_for_recommendation: float = 35.0,
    ) -> None:
        self.bot_skills = {
            self._normalize(skill)
            for skill in bot_skills
            if skill
        }

        self.minimum_expected_value = minimum_expected_value
        self.maximum_risk_for_recommendation = (
            maximum_risk_for_recommendation
        )

    def analyze(self, job: JobOpportunity) -> OpportunityAnalysis:
        skill_match = self._calculate_skill_match(job.required_skills)
        risk_score, risk_reasons = self._calculate_risk(job)

        value_score = self._calculate_value_score(
            job,
            skill_match,
            risk_score,
        )

        expected_value = self._calculate_expected_value(
            job,
            skill_match,
            risk_score,
        )

        risk_level = self._risk_level(risk_score)

        recommendation = self._recommendation(
            job,
            expected_value,
            risk_score,
            skill_match,
        )

        reasons = list(risk_reasons)

        if skill_match >= 80:
            reasons.append("Alta coincidencia con las habilidades del bot.")
        elif skill_match >= 50:
            reasons.append("Coincidencia parcial con las habilidades del bot.")
        else:
            reasons.append("Baja coincidencia con las habilidades del bot.")

        if job.payment_verified:
            reasons.append("Método de pago verificado según los datos disponibles.")
        else:
            reasons.append("Método de pago no verificado según los datos disponibles.")

        return OpportunityAnalysis(
            job_id=job.job_id,
            title=job.title,
            value_score=round(value_score, 2),
            skill_match_score=round(skill_match, 2),
            risk_score=round(risk_score, 2),
            expected_value=round(expected_value, 2),
            risk_level=risk_level,
            recommendation=recommendation,
            reasons=tuple(reasons),
        )

    def analyze_many(
        self,
        jobs: Iterable[JobOpportunity],
    ) -> list[OpportunityAnalysis]:
        results = [self.analyze(job) for job in jobs]

        return sorted(
            results,
            key=lambda result: (
                result.recommendation == "REVISAR",
                result.recommendation == "DESCARTAR",
                -result.expected_value,
            ),
        )

    def _calculate_skill_match(
        self,
        required_skills: Iterable[str],
    ) -> float:
        required = {
            self._normalize(skill)
            for skill in required_skills
            if skill
        }

        if not required:
            return 50.0

        if not self.bot_skills:
            return 0.0

        matches = required.intersection(self.bot_skills)

        return (len(matches) / len(required)) * 100.0

    def _calculate_risk(
        self,
        job: JobOpportunity,
    ) -> tuple[float, list[str]]:
        score = 0.0
        reasons: list[str] = []

        checks = (
            (
                job.external_communication_requested,
                "El cliente solicita comunicación fuera de la plataforma.",
                "external_communication",
            ),
            (
                job.upfront_payment_requested,
                "Se solicita un pago por adelantado al freelancer.",
                "upfront_payment",
            ),
            (
                job.free_work_requested,
                "Se solicita trabajo gratuito o una prueba no asegurada.",
                "free_work",
            ),
            (
                job.suspicious_link,
                "La oferta contiene un enlace marcado como sospechoso.",
                "suspicious_link",
            ),
            (
                job.personal_information_requested,
                "Se solicita información personal sensible antes de tiempo.",
                "personal_information",
            ),
            (
                job.unusually_high_pay,
                "La remuneración parece inusualmente alta para el trabajo descrito.",
                "unusually_high_pay",
            ),
            (
                not job.payment_verified,
                "El método de pago no aparece como verificado.",
                "unverified_payment",
            ),
            (
                not job.client_verified,
                "El cliente no aparece como verificado.",
                "unverified_client",
            ),
        )

        for triggered, reason, weight_key in checks:
            if triggered:
                score += self.RISK_WEIGHTS[weight_key]
                reasons.append(reason)

        return min(score, 100.0), reasons

    def _calculate_value_score(
        self,
        job: JobOpportunity,
        skill_match: float,
        risk_score: float,
    ) -> float:
        if job.budget <= 0:
            budget_score = 0.0
        elif job.budget >= 500:
            budget_score = 100.0
        else:
            budget_score = min(job.budget / 500.0 * 100.0, 100.0)

        score = (
            budget_score * 0.45
            + skill_match * 0.40
            + (100.0 - risk_score) * 0.15
        )

        return min(max(score, 0.0), 100.0)

    def _calculate_expected_value(
        self,
        job: JobOpportunity,
        skill_match: float,
        risk_score: float,
    ) -> float:
        if job.budget <= 0:
            return 0.0

        skill_probability = max(skill_match / 100.0, 0.05)
        risk_factor = max(1.0 - risk_score / 100.0, 0.05)

        return job.budget * skill_probability * risk_factor

    def _recommendation(
        self,
        job: JobOpportunity,
        expected_value: float,
        risk_score: float,
        skill_match: float,
    ) -> str:
        if risk_score >= 70:
            return "DESCARTAR"

        if (
            risk_score > self.maximum_risk_for_recommendation
            or skill_match < 50
        ):
            return "REVISAR"

        if expected_value < self.minimum_expected_value:
            return "REVISAR"

        return "PRIORIZAR"

    @staticmethod
    def _risk_level(risk_score: float) -> str:
        if risk_score >= 70:
            return "ALTO"

        if risk_score >= 35:
            return "MEDIO"

        return "BAJO"

    @staticmethod
    def _normalize(value: str) -> str:
        return " ".join(
            value.lower().strip().replace("-", " ").replace("_", " ").split()
        )


__all__ = [
    "JobOpportunity",
    "OpportunityAnalysis",
    "JobOpportunityAnalyzer",
  ]
