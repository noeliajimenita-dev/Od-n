DEFAULT_SKILLS = [
    "machine_learning",
    "data_science",
    "cybersecurity",
    "devops_cloud",
    "app_development",
    "ai_engineering",
    "automation_agents",
    "full_stack_web",
    "ai_video",
    "graphic_design",
    "digital_marketing",
    "ecommerce_shopify",
    "project_management",
    "virtual_assistant",
    "data_analysis",
]


class Worker2Skills:
    def __init__(self, skills: list[str] | None = None):
        self.skills = list(skills or DEFAULT_SKILLS)

    def has_skill(self, skill: str) -> bool:
        return skill.strip().lower() in self.skills

    def add_skill(self, skill: str) -> None:
        normalized = skill.strip().lower()

        if not normalized:
            raise ValueError("Skill cannot be empty")

        if normalized not in self.skills:
            self.skills.append(normalized)

    def remove_skill(self, skill: str) -> None:
        normalized = skill.strip().lower()

        if normalized in self.skills:
            self.skills.remove(normalized)

    def all_skills(self) -> list[str]:
        return list(self.skills)
