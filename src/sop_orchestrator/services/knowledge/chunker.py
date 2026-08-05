from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.sop_orchestrator.models.knowledge import ParsedDocument, DocumentChunk
from src.sop_orchestrator.services.knowledge.exceptions import ChunkingException

class KnowledgeChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, strategy: str = "recursive_character"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.strategy = strategy
        
        if self.strategy == "recursive_character":
            self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separators=["\n\n", "\n", " ", ""]
            )
        else:
            # Fallback to recursive character for others for now
            self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separators=["\n\n", "\n", " ", ""]
            )

    def chunk_document(self, document: ParsedDocument) -> List[DocumentChunk]:
        try:
            # If paragraphs are available, we can chunk based on them or just use raw_text
            text_to_chunk = document.raw_text
            chunks = self.splitter.split_text(text_to_chunk)
            
            document_chunks = []
            for i, chunk_text in enumerate(chunks):
                doc_chunk = DocumentChunk(
                    text=chunk_text,
                    document_id=document.document_id,
                    document_name=document.document_name,
                    chunk_number=i + 1,
                    # Section, Page, Parent Heading can be extrapolated if needed
                )
                document_chunks.append(doc_chunk)
                
            return document_chunks
        except Exception as e:
            raise ChunkingException(f"Failed to chunk document {document.document_id}: {e}")
