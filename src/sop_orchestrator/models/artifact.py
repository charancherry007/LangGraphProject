from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List, Dict, Any

class Artifact(BaseModel):
    artifact_id: str = Field(..., description="Unique identifier for the artifact")
    artifact_type: str = Field(..., description="Type of the artifact")
    version: str = Field(..., description="Version string")
    execution_id: str = Field(..., description="Execution identifier")
    agent_name: str = Field(..., description="Agent that created the artifact")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    checksum: str = Field(..., description="Checksum of the artifact content")
    dependencies: List[str] = Field(default_factory=list, description="List of dependency artifact IDs")
    schema_version: str = Field(..., description="Schema version")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    source_references: List[str] = Field(default_factory=list, description="Source references")
    content: Dict[str, Any] = Field(default_factory=dict, description="Artifact payload")
