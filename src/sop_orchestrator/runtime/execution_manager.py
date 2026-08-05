import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from src.sop_orchestrator.models.project import ProjectConfig

from src.sop_orchestrator.services.artifact_service import ArtifactService

class ExecutionManager:
    def __init__(self, project_config: ProjectConfig):
        self.project_config = project_config
        self.artifact_service = ArtifactService(
            artifacts_dir=project_config.artifacts_dir,
            registry_file=project_config.artifacts_dir / "metadata" / "registry.json"
        )

    def create_execution_id(self) -> str:
        """Create a unique execution ID."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        short_uuid = str(uuid.uuid4())[:8]
        return f"RUN-{timestamp}-{short_uuid}"

    def create_runtime_session(self) -> str:
        """Initialize runtime session folders, metadata, and artifact manifest."""
        execution_id = self.create_execution_id()
        
        self.create_logs_folder(execution_id)
        self.create_checkpoint_folder(execution_id)
        self.persist_execution_metadata(execution_id)
        
        # Initialize the execution manifest in the artifact registry
        self.artifact_service.start_execution(execution_id, self.project_config.project_id)
        
        return execution_id

    def create_logs_folder(self, execution_id: str) -> None:
        """Create logs folder for the execution."""
        logs_dir = self.project_config.logs_dir / execution_id
        logs_dir.mkdir(parents=True, exist_ok=True)

    def create_checkpoint_folder(self, execution_id: str) -> None:
        """Create checkpoint folder for the execution."""
        checkpoints_dir = self.project_config.checkpoints_dir / execution_id
        checkpoints_dir.mkdir(parents=True, exist_ok=True)

    def persist_execution_metadata(self, execution_id: str) -> None:
        """Persist metadata about this execution."""
        metadata = {
            "execution_id": execution_id,
            "project_id": self.project_config.project_id,
            "start_time": datetime.now(timezone.utc).isoformat(),
            "status": "INITIALIZED"
        }
        
        metadata_path = self.project_config.reports_dir / f"{execution_id}_metadata.json"
        
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
