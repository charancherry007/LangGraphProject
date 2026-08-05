import pytest
from src.sop_orchestrator.artifacts.base import ArtifactMetadata, BaseArtifact
from src.sop_orchestrator.artifacts.validator import ArtifactValidator
from src.sop_orchestrator.artifacts.exceptions import ArtifactValidationException

class DummyArtifact(BaseArtifact):
    content: str = ""

@pytest.fixture
def dummy_artifact():
    metadata = ArtifactMetadata(
        artifact_id="123",
        artifact_name="test",
        artifact_type="DummyArtifact",
        execution_id="run-1",
        agent_name="agent-a"
    )
    artifact = DummyArtifact(metadata=metadata, content="hello")
    artifact.update_checksum()
    return artifact

def test_validate_valid_artifact(dummy_artifact):
    # Should not raise
    ArtifactValidator.validate(dummy_artifact)

def test_validate_metadata_missing_fields(dummy_artifact):
    dummy_artifact.metadata.artifact_id = ""
    with pytest.raises(ArtifactValidationException, match="Missing artifact_id"):
        ArtifactValidator.validate(dummy_artifact)

def test_validate_checksum_mismatch(dummy_artifact):
    dummy_artifact.content = "changed"
    with pytest.raises(ArtifactValidationException, match="Checksum mismatch"):
        ArtifactValidator.validate(dummy_artifact)

def test_validate_dependencies(dummy_artifact):
    dummy_artifact.metadata.dependencies = ["missing_dep"]
    dummy_artifact.update_checksum()
    
    with pytest.raises(ArtifactValidationException, match="Missing dependencies"):
        ArtifactValidator.validate(dummy_artifact, available_artifacts=["other_dep"])
        
    # Should not raise if dependency is available
    ArtifactValidator.validate(dummy_artifact, available_artifacts=["missing_dep"])
