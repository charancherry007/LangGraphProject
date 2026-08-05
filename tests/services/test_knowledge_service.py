import pytest
from pathlib import Path
from src.sop_orchestrator.services.knowledge_service import KnowledgeRepositoryService
from src.sop_orchestrator.models.project import ProjectConfig

@pytest.fixture
def knowledge_service(tmp_path):
    project_config = ProjectConfig(
        project_id="test",
        project_name="test",
        base_path=tmp_path,
        knowledge_dir=tmp_path / "knowledge",
        skills_dir=tmp_path / "skills",
        inputs_dir=tmp_path / "inputs",
        outputs_dir=tmp_path / "outputs",
        artifacts_dir=tmp_path / "artifacts",
        reports_dir=tmp_path / "reports",
        checkpoints_dir=tmp_path / "checkpoints",
        logs_dir=tmp_path / "logs"
    )
    return KnowledgeRepositoryService(project_config)

def test_validate_repository(knowledge_service, tmp_path):
    assert not knowledge_service.validate_repository()
    
    # Create valid repo
    for d in ["CHC", "System", "Policies", "Templates", "vector_store"]:
        (tmp_path / "knowledge" / d).mkdir(parents=True)
        
    assert knowledge_service.validate_repository()

def test_discover_documents(knowledge_service, tmp_path):
    # Create valid repo
    for d in ["CHC", "System", "Policies", "Templates", "vector_store"]:
        (tmp_path / "knowledge" / d).mkdir(parents=True)
        
    (tmp_path / "knowledge" / "CHC" / "doc1.txt").touch()
    (tmp_path / "knowledge" / "System" / "doc2.pdf").touch()
    
    docs = knowledge_service.discover_documents()
    assert docs["CHC"] == ["doc1.txt"]
    assert docs["System"] == ["doc2.pdf"]
    assert docs["Policies"] == []

def test_detect_index(knowledge_service, tmp_path):
    assert not knowledge_service.detect_index()
    
    # Create empty vector_store
    vs_dir = tmp_path / "knowledge" / "vector_store"
    vs_dir.mkdir(parents=True)
    assert not knowledge_service.detect_index()
    
    # Add files
    (vs_dir / "index.faiss").touch()
    assert knowledge_service.detect_index()
