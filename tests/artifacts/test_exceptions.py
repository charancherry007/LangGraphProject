import pytest
from src.sop_orchestrator.artifacts.exceptions import (
    ArtifactNotFoundException,
    ArtifactValidationException
)

def test_artifact_not_found_exception():
    exc = ArtifactNotFoundException("test-id")
    assert exc.artifact_id == "test-id"
    assert str(exc) == "Artifact not found: test-id"

def test_artifact_validation_exception():
    exc = ArtifactValidationException("test message")
    assert str(exc) == "test message"
