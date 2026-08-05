from pathlib import Path
from typing import List, Dict, Any
from src.sop_orchestrator.models.project import ProjectConfig

class SkillService:
    def __init__(self, project_config: ProjectConfig):
        self.skills_dir = project_config.skills_dir
        self.expected_skills = [
            "01_KnowledgeHarvesting.agent.md",
            "02_ProcessReconstruction.agent.md",
            "03_GapDiscovery.agent.md",
            "04_SMEInterview.agent.md",
            "05_L4toSOP.agent.md"
        ]

    def discover_skills(self) -> List[str]:
        """Discover available skills."""
        if not self.skills_dir.exists():
            return []
        
        found_skills = [f.name for f in self.skills_dir.iterdir() if f.is_file() and f.name.endswith(".agent.md")]
        return sorted(found_skills)

    def validate_skills(self) -> Dict[str, bool]:
        """Validate existence and readability of required skills."""
        validation_results = {}
        for skill in self.expected_skills:
            skill_path = self.skills_dir / skill
            validation_results[skill] = skill_path.exists() and skill_path.is_file()
        return validation_results

    def get_execution_list(self) -> List[str]:
        """Return the ordered list of skills to execute."""
        validation = self.validate_skills()
        
        # Only return skills that exist, maintaining required order
        return [skill for skill in self.expected_skills if validation.get(skill, False)]
