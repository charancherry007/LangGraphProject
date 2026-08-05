import pytest
from pathlib import Path
from src.sop_orchestrator.artifacts.base import ArtifactMetadata, BaseArtifact
from src.sop_orchestrator.artifacts.serializer import ArtifactSerializer

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
    return DummyArtifact(metadata=metadata, content="hello world")

def test_json_serialization(dummy_artifact):
    json_str = ArtifactSerializer.to_json(dummy_artifact)
    assert "hello world" in json_str
    
    loaded = ArtifactSerializer.from_json(json_str, DummyArtifact)
    assert loaded.metadata.artifact_id == "123"
    assert loaded.content == "hello world"

def test_yaml_serialization(dummy_artifact):
    yaml_str = ArtifactSerializer.to_yaml(dummy_artifact)
    assert "hello world" in yaml_str
    
    loaded = ArtifactSerializer.from_yaml(yaml_str, DummyArtifact)
    assert loaded.metadata.artifact_id == "123"
    assert loaded.content == "hello world"

def test_file_io(dummy_artifact, tmp_path):
    json_file = tmp_path / "test.json"
    ArtifactSerializer.save_to_file(dummy_artifact, json_file, format='json')
    assert json_file.exists()
    
    loaded_json = ArtifactSerializer.load_from_file(json_file, DummyArtifact)
    assert loaded_json.content == "hello world"
    
    yaml_file = tmp_path / "test.yaml"
    ArtifactSerializer.save_to_file(dummy_artifact, yaml_file, format='yaml')
    assert yaml_file.exists()
    
    loaded_yaml = ArtifactSerializer.load_from_file(yaml_file, DummyArtifact)
    assert loaded_yaml.content == "hello world"
