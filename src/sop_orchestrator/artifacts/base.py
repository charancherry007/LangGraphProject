import hashlib
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ArtifactMetadata(BaseModel):
    artifact_id: str
    artifact_name: str
    artifact_type: str
    execution_id: str
    agent_name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = "1.0.0"
    schema_version: str = "1.0.0"
    checksum: Optional[str] = None
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    dependencies: List[str] = Field(default_factory=list)
    source_documents: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)
    status: str = "CREATED"

    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)

class BaseArtifact(BaseModel):
    metadata: ArtifactMetadata
    
    def calculate_checksum(self) -> str:
        """Calculate the SHA256 checksum of the serialized artifact, excluding the checksum field itself."""
        # Create a copy of the dictionary without the checksum to calculate
        data_to_hash = self.model_dump(mode='json')
        if "metadata" in data_to_hash and "checksum" in data_to_hash["metadata"]:
            data_to_hash["metadata"]["checksum"] = None
            
        json_str = json.dumps(data_to_hash, sort_keys=True)
        return hashlib.sha256(json_str.encode('utf-8')).hexdigest()
        
    def update_checksum(self) -> None:
        """Calculate and update the checksum in metadata."""
        self.metadata.checksum = self.calculate_checksum()
