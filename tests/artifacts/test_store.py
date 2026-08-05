import pytest
from src.sop_orchestrator.artifacts.store import ArtifactStore
from src.sop_orchestrator.artifacts.base import ArtifactMetadata
from src.sop_orchestrator.artifacts.types import KnowledgePackage

@pytest.fixture
def store(tmp_path):
    return ArtifactStore(tmp_path)

def test_store_initializes_directories(tmp_path):
    store = ArtifactStore(tmp_path)
    assert (tmp_path / "knowledge").exists()
    assert (tmp_path / "process").exists()
    assert (tmp_path / "gap").exists()
    assert (tmp_path / "sme").exists()
    assert (tmp_path / "sop").exists()
    assert (tmp_path / "metadata").exists()

def test_store_save_and_load(store, tmp_path):
    metadata = ArtifactMetadata(
        artifact_id="k-1",
        artifact_name="my_knowledge",
        artifact_type="KnowledgePackage",
        execution_id="run-1",
        agent_name="agent-a"
    )
    artifact = KnowledgePackage(metadata=metadata, domain_knowledge="test data")
    
    path = store.save_artifact(artifact)
    assert path.parent.name == "knowledge"
    assert path.name == "my_knowledge_v1.0.0.json"
    
    loaded = store.load_artifact(path, KnowledgePackage)
    assert loaded.domain_knowledge == "test data"
    
    store.delete_artifact(path)
    assert not path.exists()

def test_list_artifacts_in_dir(store, tmp_path):
    metadata = ArtifactMetadata(
        artifact_id="k-1",
        artifact_name="test",
        artifact_type="KnowledgePackage",
        execution_id="run-1",
        agent_name="agent-a"
    )
    artifact = KnowledgePackage(metadata=metadata)
    store.save_artifact(artifact)
    
    files = store.list_artifacts_in_dir(tmp_path / "knowledge")
    assert len(files) == 1
    assert files[0].name == "test_v1.0.0.json"
