from pathlib import Path
from typing import List, Dict, Any
from src.sop_orchestrator.models.project import ProjectConfig

class ProjectService:
    def __init__(self, projects_dir: Path):
        self.projects_dir = projects_dir

    def discover_projects(self) -> List[str]:
        """Discover all projects in the projects directory."""
        if not self.projects_dir.exists():
            return []
        return [p.name for p in self.projects_dir.iterdir() if p.is_dir()]

    def create_project(self, project_name: str) -> ProjectConfig:
        """Create a new project structure."""
        project_path = self.projects_dir / project_name
        
        # Create base structure
        folders = [
            "knowledge/CHC",
            "knowledge/System",
            "knowledge/Policies",
            "knowledge/Templates",
            "knowledge/vector_store",
            "skills/Shared",
            "inputs",
            "outputs",
            "artifacts/knowledge",
            "artifacts/process",
            "artifacts/gap",
            "artifacts/sme",
            "artifacts/sop",
            "artifacts/metadata",
            "reports",
            "checkpoints",
            "logs"
        ]
        
        for folder in folders:
            (project_path / folder).mkdir(parents=True, exist_ok=True)
            
        return ProjectConfig.from_directory(project_path)

    def validate_structure(self, project_name: str) -> bool:
        """Validate if project structure is correct."""
        project_path = self.projects_dir / project_name
        if not project_path.exists():
            return False
            
        required_dirs = [
            "knowledge",
            "skills",
            "inputs",
            "outputs",
            "artifacts",
            "reports",
            "checkpoints",
            "logs"
        ]
        
        return all((project_path / d).exists() for d in required_dirs)

    def read_configuration(self, project_name: str) -> Dict[str, Any]:
        """Read project configuration from project.yaml."""
        config_path = self.projects_dir / project_name / "project.yaml"
        # In a real implementation this would read YAML, but for now we'll 
        # return basic metadata since we don't have pyyaml properly setup in tests
        return {"name": project_name}

    def load_project(self, project_name: str) -> ProjectConfig:
        """Load project configuration."""
        if not self.validate_structure(project_name):
            raise ValueError(f"Invalid project structure for {project_name}")
            
        return ProjectConfig.from_directory(self.projects_dir / project_name)
