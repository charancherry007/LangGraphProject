import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from src.sop_orchestrator.artifacts.exceptions import ArtifactRegistryException

class ExecutionArtifactManifest(BaseModel):
    execution_id: str
    project_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    workflow_phase: str = "INITIALIZATION"
    artifacts: List[str] = Field(default_factory=list)
    status: str = "RUNNING"
    duration_seconds: float = 0.0

class ArtifactIndexEntry(BaseModel):
    artifact_id: str
    artifact_type: str
    execution_id: str
    agent_name: str
    version: str
    path: str
    dependencies: List[str] = Field(default_factory=list)

class ArtifactIndex(BaseModel):
    entries: Dict[str, ArtifactIndexEntry] = Field(default_factory=dict)
    
    def add_entry(self, entry: ArtifactIndexEntry) -> None:
        self.entries[entry.artifact_id] = entry
        
    def get_entry(self, artifact_id: str) -> Optional[ArtifactIndexEntry]:
        return self.entries.get(artifact_id)
        
    def remove_entry(self, artifact_id: str) -> None:
        if artifact_id in self.entries:
            del self.entries[artifact_id]

class ArtifactRegistry:
    def __init__(self, registry_file: Path):
        self.registry_file = registry_file
        self.index = self._load_index()
        self.manifests: Dict[str, ExecutionArtifactManifest] = {}

    def _load_index(self) -> ArtifactIndex:
        if not self.registry_file.exists():
            return ArtifactIndex()
            
        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return ArtifactIndex.model_validate(data)
        except Exception as e:
            raise ArtifactRegistryException(f"Failed to load artifact registry: {str(e)}")

    def _save_index(self) -> None:
        try:
            self.registry_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                f.write(self.index.model_dump_json(indent=2))
        except Exception as e:
            raise ArtifactRegistryException(f"Failed to save artifact registry: {str(e)}")

    def register_artifact(self, entry: ArtifactIndexEntry) -> None:
        """Register an artifact in the index."""
        self.index.add_entry(entry)
        self._save_index()
        
        # Update manifest if active
        if entry.execution_id in self.manifests:
            manifest = self.manifests[entry.execution_id]
            if entry.artifact_id not in manifest.artifacts:
                manifest.artifacts.append(entry.artifact_id)

    def get_artifact_location(self, artifact_id: str) -> Optional[str]:
        """Get the file path for an artifact."""
        entry = self.index.get_entry(artifact_id)
        return entry.path if entry else None

    def start_execution(self, execution_id: str, project_id: str) -> None:
        """Initialize a new execution manifest."""
        self.manifests[execution_id] = ExecutionArtifactManifest(
            execution_id=execution_id,
            project_id=project_id
        )

    def finish_execution(self, execution_id: str, status: str = "COMPLETED") -> None:
        """Mark an execution as finished and update its duration."""
        if execution_id in self.manifests:
            manifest = self.manifests[execution_id]
            manifest.status = status
            manifest.duration_seconds = (datetime.now(timezone.utc) - manifest.created_at).total_seconds()

    def get_execution_manifest(self, execution_id: str) -> Optional[ExecutionArtifactManifest]:
        """Retrieve an execution manifest."""
        return self.manifests.get(execution_id)

    def get_all_artifacts(self) -> List[ArtifactIndexEntry]:
        """Get a list of all registered artifacts."""
        return list(self.index.entries.values())
