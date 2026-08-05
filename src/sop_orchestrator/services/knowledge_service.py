import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from src.sop_orchestrator.models.project import ProjectConfig
from src.sop_orchestrator.models.knowledge import KnowledgeManifest, KnowledgeStatistics, DocumentRegistryEntry, Citation

from src.sop_orchestrator.services.knowledge.scanner import KnowledgeScanner
from src.sop_orchestrator.services.knowledge.registry import DocumentRegistry
from src.sop_orchestrator.services.knowledge.loader import KnowledgeLoader
from src.sop_orchestrator.services.knowledge.chunker import KnowledgeChunker
from src.sop_orchestrator.services.knowledge.embeddings import EmbeddingService
from src.sop_orchestrator.services.knowledge.vector_store import VectorStoreManager
from src.sop_orchestrator.services.knowledge.retriever import Retriever
from src.sop_orchestrator.services.knowledge.citation import CitationManager
from src.sop_orchestrator.services.knowledge.cache import KnowledgeCache
from src.sop_orchestrator.services.knowledge.exceptions import KnowledgeRepositoryException

logger = logging.getLogger(__name__)

class KnowledgeRepositoryService:
    def __init__(self, project_config: ProjectConfig, api_key: str = ""):
        self.knowledge_dir = project_config.knowledge_dir
        self.project_config = project_config
        
        self.scanner = KnowledgeScanner(project_config)
        self.registry = DocumentRegistry(project_config)
        self.loader = KnowledgeLoader()
        self.chunker = KnowledgeChunker()
        self.embedding_service = EmbeddingService(api_key=api_key)
        self.vector_store = VectorStoreManager(project_config, self.embedding_service)
        self.retriever = Retriever(self.vector_store)
        self.citation_manager = CitationManager()
        self.cache = KnowledgeCache(project_config)
        
        self.manifest_file = self.knowledge_dir / "manifest.json"
        
        self.expected_folders = [
            "CHC",
            "System",
            "Policies",
            "Templates",
            "vector_store"
        ]

    def validate_repository(self) -> bool:
        """Validate the existence of the knowledge repository structure."""
        if not self.knowledge_dir.exists():
            return False
            
        return all((self.knowledge_dir / folder).exists() for folder in self.expected_folders)

    def detect_index(self) -> bool:
        """Check if the vector store index exists."""
        vector_store_dir = self.knowledge_dir / "vector_store"
        if not vector_store_dir.exists():
            return False
            
        # Simplified check: looking for files in the directory
        try:
            return any(vector_store_dir.iterdir())
        except Exception:
            return False

    def index_repository(self) -> KnowledgeManifest:
        """Scan and index all new or modified documents in the repository."""
        logger.info("Scanning knowledge repository...")
        existing_hashes = self.registry.get_all_hashes()
        scan_results = self.scanner.scan(existing_hashes)
        
        new_files = scan_results.get("new", [])
        modified_files = scan_results.get("modified", [])
        deleted_files = scan_results.get("deleted", [])
        
        files_to_process = new_files + modified_files
        
        for file_path in deleted_files:
            rel_path = str(file_path.relative_to(self.knowledge_dir))
            entry = self.registry.get_entry(rel_path)
            if entry:
                self.vector_store.delete_document_vectors(entry.document_id)
                self.registry.remove_entry(rel_path)
                logger.info(f"Deleted vectors and registry entry for {rel_path}")

        total_processed = 0
        
        for file_path in files_to_process:
            try:
                rel_path = str(file_path.relative_to(self.knowledge_dir))
                
                # If modified, remove old vectors first
                if file_path in modified_files:
                    old_entry = self.registry.get_entry(rel_path)
                    if old_entry:
                        self.vector_store.delete_document_vectors(old_entry.document_id)
                
                logger.info(f"Indexing document: {rel_path}")
                parsed_doc = self.loader.load_document(file_path, self.knowledge_dir)
                chunks = self.chunker.chunk_document(parsed_doc)
                self.vector_store.index_chunks(chunks)
                
                entry = DocumentRegistryEntry(
                    document_id=parsed_doc.document_id,
                    version=1, # Add_or_update will bump this if modified
                    hash_value=parsed_doc.hash_value,
                    last_indexed=datetime.utcnow(),
                    status="INDEXED",
                    knowledge_source=str(Path(rel_path).parent),
                    embedding_version=self.embedding_service.model,
                    chunk_count=len(chunks)
                )
                self.registry.add_or_update_entry(rel_path, entry)
                total_processed += 1
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {e}")
                
        # Invalidate cache if anything changed
        if files_to_process or deleted_files:
            self.cache.clear_namespace("retrieval")
            self.cache.clear_namespace("manifest")
            
        manifest = self.generate_manifest()
        return manifest

    def search(self, query: str, top_k: int = 5, score_threshold: float = 0.7, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search the knowledge repository for relevant chunks."""
        logger.info(f"Searching for: {query}")
        cache_key = f"{query}_{top_k}_{score_threshold}_{str(filters)}"
        cached_results = self.cache.get(cache_key, "retrieval")
        if cached_results:
            return cached_results
            
        results = self.retriever.retrieve(query, top_k=top_k, score_threshold=score_threshold, filters=filters)
        self.cache.set(cache_key, results, "retrieval")
        return results

    def retrieve(self, query: str, top_k: int = 5, score_threshold: float = 0.7, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Search and attach citations to the results."""
        results = self.search(query, top_k, score_threshold, filters)
        citations = self.citation_manager.generate_citations(results)
        
        return {
            "results": results,
            "citations": [c.model_dump() for c in citations]
        }

    def statistics(self) -> KnowledgeStatistics:
        """Generate repository statistics."""
        entries = self.registry.entries.values()
        num_docs = len(entries)
        total_chunks = sum(e.chunk_count for e in entries)
        sources = len(set(e.knowledge_source for e in entries if e.knowledge_source))
        
        # Simple storage size estimation
        storage_size = sum(f.stat().st_size for f in self.knowledge_dir.rglob("*") if f.is_file())
        
        return KnowledgeStatistics(
            number_of_documents=num_docs,
            chunks=total_chunks,
            embeddings=total_chunks, # 1 embedding per chunk
            average_chunk_size=self.chunker.chunk_size, # Approximate
            knowledge_sources=sources,
            coverage=100.0, # Approximate
            storage_size_bytes=storage_size
        )

    def generate_manifest(self) -> KnowledgeManifest:
        """Generate and save the knowledge manifest."""
        manifest = KnowledgeManifest(
            indexed_documents=list(self.registry.entries.keys()),
            embedding_version=self.embedding_service.model,
            chunk_strategy=self.chunker.strategy,
            statistics=self.statistics(),
            last_updated=datetime.utcnow(),
            index_version="v1"
        )
        
        with open(self.manifest_file, "w") as f:
            f.write(manifest.model_dump_json(indent=2))
            
        return manifest
