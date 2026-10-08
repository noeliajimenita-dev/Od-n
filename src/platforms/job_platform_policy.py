
"""Política de ofertas remotas y comunicación segura de ODIN."""

from dataclasses import dataclass
from enum import Enum
import re


class JobDecision(str, Enum):
    ACCEPT_FOR_REVIEW = "accept_for_review"
    REJECT = "reject"
    HUMAN_REVIEW = "human_review"


@dataclass(frozen=True)
class JobPolicyResult:
    decision: JobDecision
    reason: str


class JobPlatformPolicy:
    """Filtra ofertas; no postula ni envía mensajes por sí mismo."""

    OFF_PLATFORM_PATTERNS = (
        r"\b(whatsapp|telegram|discord|signal)\b",
        r"\b(contact me|message me|chat me)\b.{0,50}"
        r"\b(outside|off platform|privately)\b",
        r"\b(continue|move|take)\b.{0,40}"
        r"\b(conversation|chat|communication)\b.{0,40}"
        r"\b(outside|off platform|privately)\b",
        r"\b(write|contact|message)\b.{0,40}"
        r"\b(my personal number|my phone|my email)\b",
        r"\b(paga|pagame|pago)\b.{0,40}"
        r"\b(por fuera|fuera de la plataforma)\b",
        r"\b(hablemos|escribime|contactame)\b.{0,40}"
        r"\b(whatsapp|telegram|por privado)\b",
    )

    REMOTE_TERMS = (
        "remote", "remotely", "work from home",
        "fully remote", "trabajo remoto", "100% remoto",
        "desde casa", "teletrabajo",
    )

    NON_REMOTE_TERMS = (
        "on-site", "onsite", "in person",
        "presencial", "híbrido", "hybrid",
    )

    def evaluate(
        self,
        platform: str,
        description: str,
        remote: bool | None = None,
        requests_off_platform_contact: bool = False,
    ) -> JobPolicyResult:
        text = (description or "").lower()
        platform_name = (platform or "").strip().lower()

        if not platform_name:
            return JobPolicyResult(
                JobDecision.HUMAN_REVIEW,
                "No se identificó la plataforma de origen.",
            )

        # Rechazar explícitamente las solicitudes de salir de la plataforma.
        if requests_off_platform_contact or any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in self.OFF_PLATFORM_PATTERNS
        ):
            return JobPolicyResult(
                JobDecision.REJECT,
                "La oferta solicita contacto o conversación fuera "
                "de la plataforma de origen.",
            )

        # La modalidad presencial o híbrida no cumple el requisito.
        if any(term in text for term in self.NON_REMOTE_TERMS):
            return JobPolicyResult(
                JobDecision.REJECT,
                "La oferta no es completamente remota.",
            )

        explicitly_remote = remote is True or any(
            term in text for term in self.REMOTE_TERMS
        )

        if remote is False or not explicitly_remote:
            return JobPolicyResult(
                JobDecision.HUMAN_REVIEW,
                "No se pudo confirmar que el trabajo sea 100% remoto.",
            )

        return JobPolicyResult(
            JobDecision.ACCEPT_FOR_REVIEW,
            "Es remota y no se detectó una solicitud explícita "
            "de continuar fuera de la plataforma. Requiere revisar "
            "la oferta y aprobar la postulación.",
        )
