import logging
from pathlib import Path
from typing import List, Type, TypeVar, Optional, Dict, Any
from src.sop_orchestrator.artifacts.base import BaseArtifact
from src.sop_orchestrator.artifacts.store import ArtifactStore
from src.sop_orchestrator.artifacts.registry import ArtifactRegistry, ArtifactIndexEntry
from src.sop_orchestrator.artifacts.validator import ArtifactValidator
from src.sop_orchestrator.artifacts.exceptions import ArtifactNotFoundException

T = TypeVar('T', bound=BaseArtifact)
logger = logging.getLogger(__name__)

class ArtifactService:
    """High-level interface for managing artifacts. This is the only service agents should use."""
    
    def __init__(self, artifacts_dir: Path, registry_file: Path):
        self.store = ArtifactStore(artifacts_dir)
        self.registry = ArtifactRegistry(registry_file)

    def save_artifact(self, artifact: BaseArtifact) -> None:
        """Validate, version, update checksum, and persist an artifact."""
        # 1. Update checksum
        artifact.update_checksum()
        
        # 2. Validate
        # In a full system, we might want to check available_artifacts from registry
        ArtifactValidator.validate(artifact)
        
        # 3. Save to store
        path = self.store.save_artifact(artifact)
        
        # 4. Update registry
        entry = ArtifactIndexEntry(
            artifact_id=artifact.metadata.artifact_id,
            artifact_type=artifact.metadata.artifact_type,
            execution_id=artifact.metadata.execution_id,
            agent_name=artifact.metadata.agent_name,
            version=artifact.metadata.version,
            path=str(path),
            dependencies=artifact.metadata.dependencies
        )
        self.registry.register_artifact(entry)
        
        logger.info(f"Artifact Saved: {artifact.metadata.artifact_id} (Version: {artifact.metadata.version})")

    def get_artifact(self, artifact_id: str, model_class: Type[T]) -> T:
        """Retrieve an artifact by ID."""
        path_str = self.registry.get_artifact_location(artifact_id)
        if not path_str:
            raise ArtifactNotFoundException(artifact_id)
            
        path = Path(path_str)
        artifact = self.store.load_artifact(path, model_class)
        
        # Verify checksum
        ArtifactValidator.validate_checksum(artifact)
        
        logger.info(f"Artifact Loaded: {artifact_id}")
        return artifact

    def create_new_version(self, artifact: BaseArtifact, bump_type: str = "patch") -> BaseArtifact:
        """Create a new version of an artifact (minor or patch)."""
        # Parse current version
        parts = artifact.metadata.version.split('.')
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        if bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        else:
            patch += 1
            
        new_version = f"{major}.{minor}.{patch}"
        artifact.metadata.version = new_version
        artifact.metadata.update_timestamp()
        
        logger.info(f"Artifact Versioned: {artifact.metadata.artifact_id} -> {new_version}")
        return artifact
        
    def start_execution(self, execution_id: str, project_id: str) -> None:
        self.registry.start_execution(execution_id, project_id)
        
    def finish_execution(self, execution_id: str, status: str = "COMPLETED") -> None:
        self.registry.finish_execution(execution_id, status)
