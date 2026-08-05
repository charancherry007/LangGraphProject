from abc import ABC, abstractmethod
from pathlib import Path
from src.sop_orchestrator.models.knowledge import ParsedDocument
from src.sop_orchestrator.services.knowledge.exceptions import DocumentParsingException

class BaseParser(ABC):
    """Abstract strategy interface for document parsing."""

    @abstractmethod
    def can_parse(self, file_path: Path) -> bool:
        """Return True if this parser can handle the given file."""
        pass

    @abstractmethod
    def parse(self, file_path: Path, document_id: str, relative_path: str) -> ParsedDocument:
        """
        Parse the document and return a ParsedDocument object.
        
        Args:
            file_path: The absolute path to the file.
            document_id: The unique ID for the document.
            relative_path: The path relative to the knowledge root.
            
        Returns:
            ParsedDocument: The normalized document.
            
        Raises:
            DocumentParsingException: If parsing fails.
        """
        pass
