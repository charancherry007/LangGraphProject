import pytest
from src.sop_orchestrator.artifacts.base import ArtifactMetadata, BaseArtifact

class DummyArtifact(BaseArtifact):
    content: str = ""

def test_metadata_defaults():
    metadata = ArtifactMetadata(
        artifact_id="123",
        artifact_name="test",
        artifact_type="DummyArtifact",
        execution_id="run-1",
        agent_name="agent-a"
    )
    assert metadata.version == "1.0.0"
    assert metadata.schema_version == "1.0.0"
    assert metadata.confidence == 1.0
    assert metadata.status == "CREATED"
    assert metadata.dependencies == []

def test_calculate_checksum():
    metadata = ArtifactMetadata(
        artifact_id="123",
        artifact_name="test",
        artifact_type="DummyArtifact",
        execution_id="run-1",
        agent_name="agent-a"
    )
    artifact = DummyArtifact(metadata=metadata, content="hello world")
    
    # Calculate checksum
    checksum = artifact.calculate_checksum()
    assert checksum is not None
    assert len(checksum) == 64  # SHA256 length
    
    # Update should set the metadata field
    artifact.update_checksum()
    assert artifact.metadata.checksum == checksum
    
    # Changing content should change checksum
    artifact.content = "new content"
    new_checksum = artifact.calculate_checksum()
    assert new_checksum != checksum
