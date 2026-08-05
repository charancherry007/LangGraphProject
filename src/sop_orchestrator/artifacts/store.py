import json
from pathlib import Path
from typing import List, Type, TypeVar, Optional, Dict, Any
from src.sop_orchestrator.artifacts.base import BaseArtifact
from src.sop_orchestrator.artifacts.serializer import ArtifactSerializer
from src.sop_orchestrator.artifacts.exceptions import ArtifactNotFoundException

T = TypeVar('T', bound=BaseArtifact)

class ArtifactStore:
    def __init__(self, artifacts_dir: Path):
        self.artifacts_dir = artifacts_dir
        
        # Ensure directories exist
        self._ensure_directories()
        
    def _ensure_directories(self) -> None:
        folders = ["knowledge", "process", "gap", "sme", "sop", "metadata"]
        for folder in folders:
            (self.artifacts_dir / folder).mkdir(parents=True, exist_ok=True)

    def _get_path_for_type(self, artifact_type: str) -> Path:
        """Map an artifact type to its corresponding subdirectory."""
        mapping = {
            "KnowledgePackage": "knowledge",
            "EvidenceGraph": "knowledge",
            "ArtifactCatalog": "knowledge",
            "BusinessRules": "knowledge",
            "Glossary": "knowledge",
            "ActorCatalog": "knowledge",
            "SystemCatalog": "knowledge",
            "ProcessGraph": "process",
            "DecisionInventory": "process",
            "StateModel": "process",
            "ProcessVariants": "process",
            "GapRegister": "gap",
            "ClarificationPack": "gap",
            "ConfidenceDashboard": "gap",
            "Assumptions": "gap",
            "RiskRegister": "gap",
            "QuestionBank": "sme",
            "ValidatedAnswers": "sme",
            "DecisionLog": "sme",
            "EnterpriseSOP": "sop",
            "TraceabilityMatrix": "sop",
            "ExecutionReport": "sop",
        }
        folder = mapping.get(artifact_type, "metadata")
        return self.artifacts_dir / folder

    def get_artifact_path(self, artifact: BaseArtifact) -> Path:
        """Get the expected file path for an artifact, including versioning."""
        base_dir = self._get_path_for_type(artifact.metadata.artifact_type)
        # We append the version to the filename so previous versions aren't overwritten
        filename = f"{artifact.metadata.artifact_name}_v{artifact.metadata.version}.json"
        return base_dir / filename

    def save_artifact(self, artifact: BaseArtifact) -> Path:
        """Save an artifact to disk and return its path."""
        path = self.get_artifact_path(artifact)
        ArtifactSerializer.save_to_file(artifact, path)
        return path

    def load_artifact(self, path: Path, model_class: Type[T]) -> T:
        """Load an artifact from disk."""
        if not path.exists():
            raise ArtifactNotFoundException(str(path))
        return ArtifactSerializer.load_from_file(path, model_class)

    def delete_artifact(self, path: Path) -> None:
        """Delete an artifact from disk."""
        if path.exists():
            path.unlink()

    def list_artifacts_in_dir(self, directory: Path) -> List[Path]:
        """List all artifact files in a specific directory."""
        if not directory.exists():
            return []
        return [f for f in directory.iterdir() if f.is_file() and f.suffix == ".json"]
