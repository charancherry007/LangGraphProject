import pytest
import json
from datetime import datetime, timezone
from pathlib import Path
from src.sop_orchestrator.runtime.execution_manager import ExecutionManager
from src.sop_orchestrator.models.project import ProjectConfig

@pytest.fixture
def execution_manager(tmp_path):
    project_config = ProjectConfig(
        project_id="test_proj",
        project_name="test_proj",
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
    # Ensure reports dir exists
    project_config.reports_dir.mkdir()
    project_config.artifacts_dir.mkdir()
    return ExecutionManager(project_config)

def test_create_execution_id(execution_manager):
    exec_id = execution_manager.create_execution_id()
    
    assert exec_id.startswith("RUN-")
    # Format: RUN-YYYYMMDDHHMMSS-uuid8
    parts = exec_id.split("-")
    assert len(parts) == 3
    assert len(parts[1]) == 14 # Timestamp len
    assert len(parts[2]) == 8 # Short UUID len

def test_create_logs_folder(execution_manager):
    execution_manager.create_logs_folder("RUN-TEST")
    
    logs_dir = execution_manager.project_config.logs_dir / "RUN-TEST"
    assert logs_dir.exists()
    assert logs_dir.is_dir()

def test_create_checkpoint_folder(execution_manager):
    execution_manager.create_checkpoint_folder("RUN-TEST")
    
    cp_dir = execution_manager.project_config.checkpoints_dir / "RUN-TEST"
    assert cp_dir.exists()
    assert cp_dir.is_dir()

def test_persist_execution_metadata(execution_manager):
    exec_id = "RUN-TEST"
    execution_manager.persist_execution_metadata(exec_id)
    
    metadata_file = execution_manager.project_config.reports_dir / f"{exec_id}_metadata.json"
    assert metadata_file.exists()
    
    with open(metadata_file, "r") as f:
        data = json.load(f)
        
    assert data["execution_id"] == exec_id
    assert data["project_id"] == "test_proj"
    assert "start_time" in data
    assert data["status"] == "INITIALIZED"

def test_create_runtime_session(execution_manager):
    exec_id = execution_manager.create_runtime_session()
    
    assert exec_id.startswith("RUN-")
    
    assert (execution_manager.project_config.logs_dir / exec_id).exists()
    assert (execution_manager.project_config.checkpoints_dir / exec_id).exists()
    assert (execution_manager.project_config.reports_dir / f"{exec_id}_metadata.json").exists()
