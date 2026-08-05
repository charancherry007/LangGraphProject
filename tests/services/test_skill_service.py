import pytest
from pathlib import Path
from src.sop_orchestrator.services.skill_service import SkillService
from src.sop_orchestrator.models.project import ProjectConfig

@pytest.fixture
def skill_service(tmp_path):
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
    # Ensure skills dir exists
    project_config.skills_dir.mkdir(parents=True, exist_ok=True)
    return SkillService(project_config)

def test_discover_skills(skill_service, tmp_path):
    assert skill_service.discover_skills() == []
    
    # Create mock skills
    (tmp_path / "skills" / "01_KnowledgeHarvesting.agent.md").touch()
    (tmp_path / "skills" / "other.md").touch() # Should be ignored
    
    skills = skill_service.discover_skills()
    assert skills == ["01_KnowledgeHarvesting.agent.md"]

def test_validate_skills(skill_service, tmp_path):
    # Missing all
    validation = skill_service.validate_skills()
    assert all(not v for v in validation.values())
    
    # Create some
    (tmp_path / "skills" / "01_KnowledgeHarvesting.agent.md").touch()
    (tmp_path / "skills" / "05_L4toSOP.agent.md").touch()
    
    validation = skill_service.validate_skills()
    assert validation["01_KnowledgeHarvesting.agent.md"] is True
    assert validation["05_L4toSOP.agent.md"] is True
    assert validation["02_ProcessReconstruction.agent.md"] is False

def test_get_execution_list(skill_service, tmp_path):
    # Only some exist
    (tmp_path / "skills" / "05_L4toSOP.agent.md").touch()
    (tmp_path / "skills" / "02_ProcessReconstruction.agent.md").touch()
    
    execution_list = skill_service.get_execution_list()
    # Order should be maintained from expected_skills
    assert execution_list == [
        "02_ProcessReconstruction.agent.md",
        "05_L4toSOP.agent.md"
    ]
