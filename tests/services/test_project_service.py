import pytest
from pathlib import Path
from src.sop_orchestrator.services.project_service import ProjectService
from src.sop_orchestrator.models.project import ProjectConfig

@pytest.fixture
def project_service(tmp_path):
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()
    return ProjectService(projects_dir)

def test_discover_projects(project_service, tmp_path):
    assert project_service.discover_projects() == []
    
    # Create mock projects
    (tmp_path / "projects" / "proj1").mkdir()
    (tmp_path / "projects" / "proj2").mkdir()
    
    projects = project_service.discover_projects()
    assert set(projects) == {"proj1", "proj2"}

def test_create_project(project_service, tmp_path):
    config = project_service.create_project("test_proj")
    
    assert isinstance(config, ProjectConfig)
    assert config.project_name == "test_proj"
    
    project_path = tmp_path / "projects" / "test_proj"
    assert project_path.exists()
    
    expected_dirs = [
        "knowledge/CHC", "knowledge/System", "knowledge/Policies",
        "knowledge/Templates", "knowledge/vector_store",
        "skills/Shared", "inputs", "outputs", "reports", "checkpoints", "logs",
        "artifacts/knowledge", "artifacts/process", "artifacts/gap", "artifacts/sme", "artifacts/sop", "artifacts/metadata"
    ]
    
    for d in expected_dirs:
        assert (project_path / d).exists()

def test_validate_structure(project_service, tmp_path):
    # Should fail for non-existent project
    assert not project_service.validate_structure("invalid_proj")
    
    # Create valid project
    project_service.create_project("valid_proj")
    assert project_service.validate_structure("valid_proj")
    
    # Create invalid project
    invalid_path = tmp_path / "projects" / "broken_proj"
    invalid_path.mkdir()
    (invalid_path / "knowledge").mkdir()
    # Missing other folders
    assert not project_service.validate_structure("broken_proj")
