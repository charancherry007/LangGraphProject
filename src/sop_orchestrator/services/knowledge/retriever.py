import uuid
from typing import List, Dict, Any, Optional
from src.sop_orchestrator.services.knowledge.vector_store import VectorStoreManager
from src.sop_orchestrator.services.knowledge.exceptions import RetrievalException

class Retriever:
    def __init__(self, vector_store: VectorStoreManager):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5, score_threshold: float = 0.7, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        try:
            results = self.vector_store.search(query, top_k=top_k, filter_metadata=filters)
            
            if not results or not results['documents'] or not results['documents'][0]:
                return []
                
            retrieved_chunks = []
            
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            distances = results['distances'][0]
            
            for doc, meta, dist in zip(documents, metadatas, distances):
                # Convert distance to confidence score (assuming cosine distance from chromadb)
                # Cosine distance is 1 - cosine_similarity. So confidence can be 1 - dist/2
                # Note: ChromaDB default is L2, but we configured cosine
                confidence = max(0.0, 1.0 - dist)
                
                if confidence >= score_threshold:
                    retrieved_chunks.append({
                        "text": doc,
                        "metadata": meta,
                        "confidence": confidence,
                        "distance": dist
                    })
                    
            return retrieved_chunks
        except Exception as e:
            raise RetrievalException(f"Failed to retrieve information: {e}")
