from dataclasses import dataclass, field


@dataclass
class Worker4Config:
    worker_id: str = "worker_4"
    enabled: bool = False
    skills: list[str] = field(default_factory=list)

    def add_skill(self, skill: str) -> None:
        skill = skill.strip()

        if not skill:
            raise ValueError("Skill cannot be empty")

        if skill not in self.skills:
            self.skills.append(skill)

    def has_skill(self, skill: str) -> bool:
        return skill.strip() in self.skills

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False
