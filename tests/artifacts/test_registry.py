import pytest
from src.sop_orchestrator.artifacts.registry import ArtifactRegistry, ArtifactIndexEntry
from src.sop_orchestrator.artifacts.exceptions import ArtifactRegistryException

@pytest.fixture
def registry(tmp_path):
    registry_file = tmp_path / "registry.json"
    return ArtifactRegistry(registry_file)

def test_register_artifact(registry):
    entry = ArtifactIndexEntry(
        artifact_id="art-1",
        artifact_type="Dummy",
        execution_id="run-1",
        agent_name="agent-a",
        version="1.0.0",
        path="/tmp/path"
    )
    registry.register_artifact(entry)
    
    # Check it can be retrieved
    assert registry.get_artifact_location("art-1") == "/tmp/path"
    
    # Check persistence
    registry2 = ArtifactRegistry(registry.registry_file)
    assert registry2.get_artifact_location("art-1") == "/tmp/path"

def test_execution_manifests(registry):
    registry.start_execution("run-1", "proj-1")
    manifest = registry.get_execution_manifest("run-1")
    assert manifest.execution_id == "run-1"
    assert manifest.status == "RUNNING"
    
    # Adding artifact during execution
    entry = ArtifactIndexEntry(
        artifact_id="art-1",
        artifact_type="Dummy",
        execution_id="run-1",
        agent_name="agent-a",
        version="1.0.0",
        path="/tmp/path"
    )
    registry.register_artifact(entry)
    assert "art-1" in manifest.artifacts
    
    registry.finish_execution("run-1")
    assert manifest.status == "COMPLETED"
    assert manifest.duration_seconds > 0
