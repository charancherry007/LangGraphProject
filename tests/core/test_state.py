from src.sop_orchestrator.core.state import WorkflowState, ArtifactRegistry

def test_workflow_state_initialization():
    state = WorkflowState()
    
    assert state.project is None
    assert state.execution_id is None
    assert state.l4_map_path is None
    assert state.reference_sop_path is None
    assert state.supporting_documents_paths == []
    assert isinstance(state.artifact_registry, ArtifactRegistry)
    assert state.artifact_registry.artifacts == {}
    assert state.current_phase is None
    assert state.messages == []
    assert state.status == "INITIALIZED"

def test_workflow_state_update():
    state = WorkflowState()
    state.project = {"id": "test_proj"}
    state.execution_id = "RUN-123"
    state.l4_map_path = "path/to/l4"
    state.status = "RUNNING"
    
    assert state.project["id"] == "test_proj"
    assert state.execution_id == "RUN-123"
    assert state.l4_map_path == "path/to/l4"
    assert state.status == "RUNNING"
