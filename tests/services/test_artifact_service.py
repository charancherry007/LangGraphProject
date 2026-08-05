import pytest
from src.sop_orchestrator.services.artifact_service import ArtifactService
from src.sop_orchestrator.artifacts.base import ArtifactMetadata
from src.sop_orchestrator.artifacts.types import KnowledgePackage

@pytest.fixture
def artifact_service(tmp_path):
    registry_file = tmp_path / "metadata" / "registry.json"
    return ArtifactService(tmp_path, registry_file)

def test_save_and_get_artifact(artifact_service):
    metadata = ArtifactMetadata(
        artifact_id="art-1",
        artifact_name="my_test",
        artifact_type="KnowledgePackage",
        execution_id="run-1",
        agent_name="agent-a"
    )
    artifact = KnowledgePackage(metadata=metadata, domain_knowledge="test")
    
    # Save
    artifact_service.save_artifact(artifact)
    
    # Ensure it's in the registry
    assert artifact_service.registry.get_artifact_location("art-1") is not None
    
    # Get
    loaded = artifact_service.get_artifact("art-1", KnowledgePackage)
    assert loaded.domain_knowledge == "test"
    assert loaded.metadata.checksum is not None

def test_create_new_version(artifact_service):
    metadata = ArtifactMetadata(
        artifact_id="art-1",
        artifact_name="my_test",
        artifact_type="KnowledgePackage",
        execution_id="run-1",
        agent_name="agent-a",
        version="1.0.0"
    )
    artifact = KnowledgePackage(metadata=metadata)
    
    artifact = artifact_service.create_new_version(artifact, bump_type="patch")
    assert artifact.metadata.version == "1.0.1"
    
    artifact = artifact_service.create_new_version(artifact, bump_type="minor")
    assert artifact.metadata.version == "1.1.0"

    artifact = artifact_service.create_new_version(artifact, bump_type="major")
    assert artifact.metadata.version == "2.0.0"
