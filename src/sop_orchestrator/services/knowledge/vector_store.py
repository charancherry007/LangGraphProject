import chromadb
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.sop_orchestrator.models.project import ProjectConfig
from src.sop_orchestrator.models.knowledge import DocumentChunk
from src.sop_orchestrator.services.knowledge.exceptions import VectorStoreException
from src.sop_orchestrator.services.knowledge.embeddings import EmbeddingService

class VectorStoreManager:
    def __init__(self, project_config: ProjectConfig, embedding_service: EmbeddingService):
        self.persist_directory = str(project_config.knowledge_dir / "vector_store")
        try:
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            self.collection = self.client.get_or_create_collection(
                name="knowledge_base",
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            raise VectorStoreException(f"Failed to initialize Vector Store: {e}")
            
        self.embedding_service = embedding_service

    def index_chunks(self, chunks: List[DocumentChunk]):
        if not chunks:
            return
            
        try:
            ids = []
            documents = []
            metadatas = []
            
            for chunk in chunks:
                chunk_id = f"{chunk.document_id}_{chunk.chunk_number}"
                ids.append(chunk_id)
                documents.append(chunk.text)
                
                metadata = {
                    "document_id": chunk.document_id,
                    "document_name": chunk.document_name,
                    "chunk_number": chunk.chunk_number,
                }
                if chunk.section:
                    metadata["section"] = chunk.section
                if chunk.page is not None:
                    metadata["page"] = chunk.page
                
                metadatas.append(metadata)
                
            embeddings = self.embedding_service.generate_embeddings(documents)
            
            self.collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
        except Exception as e:
            raise VectorStoreException(f"Failed to index chunks: {e}")

    def delete_document_vectors(self, document_id: str):
        try:
            self.collection.delete(
                where={"document_id": document_id}
            )
        except Exception as e:
            raise VectorStoreException(f"Failed to delete vectors for document {document_id}: {e}")

    def search(self, query: str, top_k: int = 5, filter_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            query_embedding = self.embedding_service.generate_embedding(query)
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter_metadata,
                include=["documents", "metadatas", "distances"]
            )
            return results
        except Exception as e:
            raise VectorStoreException(f"Failed to search vector store: {e}")
