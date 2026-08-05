import uuid
from typing import List, Dict, Any
from src.sop_orchestrator.models.knowledge import Citation
from src.sop_orchestrator.services.knowledge.exceptions import CitationException

class CitationManager:
    def __init__(self):
        pass

    def generate_citations(self, retrieval_results: List[Dict[str, Any]]) -> List[Citation]:
        citations = []
        try:
            for result in retrieval_results:
                meta = result.get('metadata', {})
                
                citation = Citation(
                    citation_id=str(uuid.uuid4())[:8],
                    document_name=meta.get('document_name', 'Unknown'),
                    section=meta.get('section'),
                    page=meta.get('page'),
                    chunk=result.get('text', ''),
                    confidence=result.get('confidence', 0.0),
                    source_type="vector_store"
                )
                citations.append(citation)
            return citations
        except Exception as e:
            raise CitationException(f"Failed to generate citations: {e}")
