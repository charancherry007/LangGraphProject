import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.sop_orchestrator.models.project import ProjectConfig
from src.sop_orchestrator.services.knowledge.scanner import KnowledgeScanner
from src.sop_orchestrator.services.knowledge.chunker import KnowledgeChunker
from src.sop_orchestrator.services.knowledge.embeddings import EmbeddingService
from src.sop_orchestrator.services.knowledge.registry import DocumentRegistry
from src.sop_orchestrator.services.knowledge.cache import KnowledgeCache
from src.sop_orchestrator.models.knowledge import ParsedDocument
from datetime import datetime

@pytest.fixture
def mock_project_config(tmp_path):
    config = MagicMock(spec=ProjectConfig)
    config.knowledge_dir = tmp_path / "knowledge"
    config.knowledge_dir.mkdir()
    
    # Create required folders
    for folder in ["CHC", "System", "Policies", "Templates"]:
        (config.knowledge_dir / folder).mkdir()
        
    return config

def test_knowledge_scanner(mock_project_config):
    # Create a fake file
    test_file = mock_project_config.knowledge_dir / "CHC" / "test.txt"
    test_file.write_text("Hello World")
    
    scanner = KnowledgeScanner(mock_project_config)
    results = scanner.scan({})
    
    assert len(results["new"]) == 1
    assert "test.txt" in results["new"][0].name
    assert len(results["modified"]) == 0
    assert len(results["deleted"]) == 0

def test_knowledge_chunker():
    chunker = KnowledgeChunker(chunk_size=10, chunk_overlap=0)
    
    doc = ParsedDocument(
        document_id="123",
        document_name="test.txt",
        document_type="TXT",
        relative_path="CHC/test.txt",
        created_at=datetime.utcnow(),
        modified_at=datetime.utcnow(),
        raw_text="This is a test document for chunking.",
        normalized_text="This is a test document for chunking.",
        hash_value="abc"
    )
    
    chunks = chunker.chunk_document(doc)
    assert len(chunks) > 1
    assert chunks[0].document_id == "123"

@patch('src.sop_orchestrator.services.knowledge.embeddings.OpenAIEmbeddings')
def test_embedding_service(mock_openai):
    # Setup mock
    mock_instance = mock_openai.return_value
    mock_instance.embed_documents.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    
    service = EmbeddingService(api_key="fake")
    results = service.generate_embeddings(["test1", "test2"])
    
    assert len(results) == 2
    assert results[0] == [0.1, 0.2, 0.3]

def test_document_registry(mock_project_config):
    registry = DocumentRegistry(mock_project_config)
    assert len(registry.entries) == 0
    
    from src.sop_orchestrator.models.knowledge import DocumentRegistryEntry
    entry = DocumentRegistryEntry(
        document_id="123",
        version=1,
        hash_value="abc",
        last_indexed=datetime.utcnow(),
        status="INDEXED",
        knowledge_source="CHC",
        embedding_version="v1",
        chunk_count=5
    )
    
    registry.add_or_update_entry("CHC/test.txt", entry)
    
    loaded_registry = DocumentRegistry(mock_project_config)
    assert "CHC/test.txt" in loaded_registry.entries
    assert loaded_registry.entries["CHC/test.txt"].document_id == "123"
