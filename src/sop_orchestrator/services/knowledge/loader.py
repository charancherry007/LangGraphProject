import uuid
from pathlib import Path
from typing import List, Optional
from src.sop_orchestrator.models.knowledge import ParsedDocument
from src.sop_orchestrator.services.knowledge.parsers.base import BaseParser
from src.sop_orchestrator.services.knowledge.parsers.pdf_parser import PDFParser
from src.sop_orchestrator.services.knowledge.parsers.docx_parser import DOCXParser
from src.sop_orchestrator.services.knowledge.parsers.markdown_parser import MarkdownParser
from src.sop_orchestrator.services.knowledge.parsers.xml_parser import XMLParser
from src.sop_orchestrator.services.knowledge.exceptions import DocumentParsingException

class KnowledgeLoader:
    def __init__(self):
        self.parsers: List[BaseParser] = [
            PDFParser(),
            DOCXParser(),
            MarkdownParser(),
            XMLParser()
        ]

    def _get_parser(self, file_path: Path) -> Optional[BaseParser]:
        for parser in self.parsers:
            if parser.can_parse(file_path):
                return parser
        return None

    def load_document(self, file_path: Path, knowledge_dir: Path) -> ParsedDocument:
        parser = self._get_parser(file_path)
        if not parser:
            raise DocumentParsingException(f"No parser found for file: {file_path}")
        
        document_id = str(uuid.uuid4())
        try:
            relative_path = str(file_path.relative_to(knowledge_dir))
        except ValueError:
            relative_path = file_path.name

        return parser.parse(file_path, document_id, relative_path)
