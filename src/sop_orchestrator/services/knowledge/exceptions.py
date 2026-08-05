class KnowledgeRepositoryException(Exception):
    """Base exception for Knowledge Repository operations."""
    pass

class DocumentParsingException(KnowledgeRepositoryException):
    """Raised when document parsing fails."""
    pass

class EmbeddingException(KnowledgeRepositoryException):
    """Raised when embedding generation fails."""
    pass

class VectorStoreException(KnowledgeRepositoryException):
    """Raised when vector store operations fail."""
    pass

class ChunkingException(KnowledgeRepositoryException):
    """Raised when document chunking fails."""
    pass

class RetrievalException(KnowledgeRepositoryException):
    """Raised when retrieval operations fail."""
    pass

class CitationException(KnowledgeRepositoryException):
    """Raised when citation generation fails."""
    pass
