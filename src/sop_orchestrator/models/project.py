from pydantic import BaseModel
from pathlib import Path

class ProjectConfig(BaseModel):
    project_id: str
    project_name: str
    base_path: Path
    knowledge_dir: Path
    skills_dir: Path
    inputs_dir: Path
    outputs_dir: Path
    artifacts_dir: Path
    reports_dir: Path
    checkpoints_dir: Path
    logs_dir: Path

    @classmethod
    def from_directory(cls, base_path: Path) -> "ProjectConfig":
        return cls(
            project_id=base_path.name,
            project_name=base_path.name,
            base_path=base_path,
            knowledge_dir=base_path / "knowledge",
            skills_dir=base_path / "skills",
            inputs_dir=base_path / "inputs",
            outputs_dir=base_path / "outputs",
            artifacts_dir=base_path / "artifacts",
            reports_dir=base_path / "reports",
            checkpoints_dir=base_path / "checkpoints",
            logs_dir=base_path / "logs"
        )
