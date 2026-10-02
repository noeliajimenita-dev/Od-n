from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Job:
    """Oportunidad de trabajo externa."""

    job_id: str
    platform: str
    title: str
    description: str
    url: str = ""
    price: float = 0.0
    currency: str = "USD"
    posted_at: str | None = None
    deadline: str | None = None
    required_skills: set[str] = field(default_factory=set)
    status: str = "new"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.job_id.strip():
            raise ValueError("job_id cannot be empty")

        if not self.platform.strip():
            raise ValueError("platform cannot be empty")

        if not self.title.strip():
            raise ValueError("title cannot be empty")

        if not self.description.strip():
            raise ValueError(
                "description cannot be empty"
            )

        if self.price < 0:
            raise ValueError(
                "price cannot be negative"
            )

    def add_skill(self, skill: str) -> None:
        skill = skill.strip().lower()

        if not skill:
            raise ValueError(
                "skill cannot be empty"
            )

        self.required_skills.add(skill)

    def remove_skill(self, skill: str) -> bool:
        skill = skill.strip().lower()

        if skill not in self.required_skills:
            return False

        self.required_skills.remove(skill)
        return True

    def requires_skill(self, skill: str) -> bool:
        return (
            skill.strip().lower()
            in self.required_skills
        )

    def mark_reviewing(self) -> None:
        self.status = "reviewing"

    def mark_eligible(self) -> None:
        self.status = "eligible"

    def mark_discarded(self) -> None:
        self.status = "discarded"

    def mark_applied(self) -> None:
        self.status = "applied"

    def mark_completed(self) -> None:
        self.status = "completed"

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        if not key.strip():
            raise ValueError(
                "metadata key cannot be empty"
            )

        self.metadata[key] = value

    def is_active(self) -> bool:
        return self.status in {
            "new",
            "reviewing",
            "eligible",
        }

    def is_eligible(self) -> bool:
        return self.status == "eligible"

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "platform": self.platform,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "price": self.price,
            "currency": self.currency,
            "posted_at": self.posted_at,
            "deadline": self.deadline,
            "required_skills": sorted(
                self.required_skills
            ),
            "status": self.status,
            "metadata": dict(self.metadata),
        }

    def __repr__(self) -> str:
        return (
            "Job("
            f"job_id={self.job_id!r}, "
            f"platform={self.platform!r}, "
            f"status={self.status!r}"
            ")"
          )
