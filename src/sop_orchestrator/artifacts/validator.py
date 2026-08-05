from typing import List, Dict, Any
from src.sop_orchestrator.artifacts.base import BaseArtifact
from src.sop_orchestrator.artifacts.exceptions import ArtifactValidationException

class ArtifactValidator:
    @staticmethod
    def validate(artifact: BaseArtifact, available_artifacts: List[str] = None) -> None:
        """Run all validations on the artifact."""
        ArtifactValidator.validate_metadata(artifact)
        ArtifactValidator.validate_checksum(artifact)
        if available_artifacts is not None:
            ArtifactValidator.validate_dependencies(artifact, available_artifacts)

    @staticmethod
    def validate_metadata(artifact: BaseArtifact) -> None:
        """Validate that all required metadata fields are present and valid."""
        if not artifact.metadata.artifact_id:
            raise ArtifactValidationException("Missing artifact_id in metadata.")
        if not artifact.metadata.artifact_type:
            raise ArtifactValidationException("Missing artifact_type in metadata.")
        if not artifact.metadata.execution_id:
            raise ArtifactValidationException("Missing execution_id in metadata.")
        if not artifact.metadata.agent_name:
            raise ArtifactValidationException("Missing agent_name in metadata.")

    @staticmethod
    def validate_checksum(artifact: BaseArtifact) -> None:
        """Validate the artifact's checksum matches its contents."""
        stored_checksum = artifact.metadata.checksum
        if not stored_checksum:
            raise ArtifactValidationException("Missing checksum in metadata.")
            
        calculated = artifact.calculate_checksum()
        if stored_checksum != calculated:
            raise ArtifactValidationException(f"Checksum mismatch. Stored: {stored_checksum}, Calculated: {calculated}")

    @staticmethod
    def validate_dependencies(artifact: BaseArtifact, available_artifacts: List[str]) -> None:
        """Validate that all dependencies exist in the available artifacts."""
        missing = [dep for dep in artifact.metadata.dependencies if dep not in available_artifacts]
        if missing:
            raise ArtifactValidationException(f"Missing dependencies: {', '.join(missing)}")
