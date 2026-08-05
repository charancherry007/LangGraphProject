from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path


class KnowledgeStatistics(BaseModel):
    number_of_documents: int = 0
    chunks: int = 0
    embeddings: int = 0
    average_chunk_size: float = 0.0
    knowledge_sources: int = 0
    coverage: float = 0.0
    storage_size_bytes: int = 0


class KnowledgeManifest(BaseModel):
    indexed_documents: List[str] = Field(default_factory=list)
    embedding_version: str = "text-embedding-ada-002"
    chunk_strategy: str = "recursive_character"
    statistics: KnowledgeStatistics = Field(default_factory=KnowledgeStatistics)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    index_version: str = "v1"


class Citation(BaseModel):
    citation_id: str
    document_name: str
    section: Optional[str] = None
    page: Optional[int] = None
    chunk: str
    confidence: float
    source_type: str


class DocumentChunk(BaseModel):
    text: str
    document_id: str
    document_name: str
    section: Optional[str] = None
    page: Optional[int] = None
    chunk_number: int
    parent_heading: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DocumentRegistryEntry(BaseModel):
    document_id: str
    version: int
    hash_value: str
    last_indexed: datetime
    status: str
    knowledge_source: str
    embedding_version: str
    chunk_count: int


class ParsedDocument(BaseModel):
    document_id: str
    document_name: str
    document_type: str
    relative_path: str
    created_at: datetime
    modified_at: datetime
    language: str = "en"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    sections: List[str] = Field(default_factory=list)
    paragraphs: List[str] = Field(default_factory=list)
    tables: List[Dict[str, Any]] = Field(default_factory=list)
    images: List[Dict[str, Any]] = Field(default_factory=list)
    page_count: Optional[int] = None
    raw_text: str
    normalized_text: str
    hash_value: str
