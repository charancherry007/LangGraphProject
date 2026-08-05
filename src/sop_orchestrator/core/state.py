from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class ArtifactRegistry(BaseModel):
    artifacts: Dict[str, Any] = Field(default_factory=dict)

class WorkflowState(BaseModel):
    project: Optional[Dict[str, Any]] = None
    execution_id: Optional[str] = None
    l4_map_path: Optional[str] = None
    reference_sop_path: Optional[str] = None
    supporting_documents_paths: List[str] = Field(default_factory=list)
    artifact_registry: ArtifactRegistry = Field(default_factory=ArtifactRegistry)
    current_phase: Optional[str] = None
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    status: str = "INITIALIZED"
