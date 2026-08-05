"""Custom exceptions for the artifact framework."""

class ArtifactFrameworkException(Exception):
    """Base exception for all artifact framework errors."""
    pass

class ArtifactNotFoundException(ArtifactFrameworkException):
    """Raised when an artifact cannot be found in the store or registry."""
    def __init__(self, artifact_id: str, message: str = None):
        self.artifact_id = artifact_id
        super().__init__(message or f"Artifact not found: {artifact_id}")

class ArtifactValidationException(ArtifactFrameworkException):
    """Raised when an artifact fails schema, metadata, or dependency validation."""
    pass

class ArtifactVersionException(ArtifactFrameworkException):
    """Raised when there is an issue with artifact versioning."""
    pass

class ArtifactSerializationException(ArtifactFrameworkException):
    """Raised when an artifact cannot be serialized or deserialized."""
    pass

class ArtifactRegistryException(ArtifactFrameworkException):
    """Raised when there is an issue with the artifact registry."""
    pass
