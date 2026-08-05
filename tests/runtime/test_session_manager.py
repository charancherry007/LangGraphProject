import pytest
from unittest.mock import Mock
from src.sop_orchestrator.runtime.session_manager import SessionManager
from src.sop_orchestrator.services.project_service import ProjectService
from src.sop_orchestrator.models.project import ProjectConfig

@pytest.fixture
def mock_project_service():
    return Mock(spec=ProjectService)

@pytest.fixture
def session_manager(mock_project_service):
    return SessionManager(mock_project_service)

def test_load_project(session_manager, mock_project_service):
    expected_config = Mock(spec=ProjectConfig)
    mock_project_service.load_project.return_value = expected_config
    
    result = session_manager.load_project("test_proj")
    
    assert result == expected_config
    mock_project_service.load_project.assert_called_once_with("test_proj")

def test_create_project(session_manager, mock_project_service):
    expected_config = Mock(spec=ProjectConfig)
    mock_project_service.create_project.return_value = expected_config
    
    result = session_manager.create_project("new_proj")
    
    assert result == expected_config
    mock_project_service.create_project.assert_called_once_with("new_proj")

def test_validate_project(session_manager, mock_project_service):
    mock_project_service.validate_structure.return_value = True
    
    assert session_manager.validate_project("valid_proj") is True
    mock_project_service.validate_structure.assert_called_once_with("valid_proj")
