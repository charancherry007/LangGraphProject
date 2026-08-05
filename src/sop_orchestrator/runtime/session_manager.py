from src.sop_orchestrator.services.project_service import ProjectService
from src.sop_orchestrator.models.project import ProjectConfig

class SessionManager:
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service

    def load_project(self, project_name: str) -> ProjectConfig:
        """Load an existing project and return its context."""
        return self.project_service.load_project(project_name)

    def create_project(self, project_name: str) -> ProjectConfig:
        """Create a new project and return its context."""
        return self.project_service.create_project(project_name)

    def validate_project(self, project_name: str) -> bool:
        """Validate an existing project."""
        return self.project_service.validate_structure(project_name)
