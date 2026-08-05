import fitz
import hashlib
from pathlib import Path
from datetime import datetime
from src.sop_orchestrator.models.knowledge import ParsedDocument
from src.sop_orchestrator.services.knowledge.parsers.base import BaseParser
from src.sop_orchestrator.services.knowledge.exceptions import DocumentParsingException

class PDFParser(BaseParser):
    def can_parse(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == ".pdf"

    def parse(self, file_path: Path, document_id: str, relative_path: str) -> ParsedDocument:
        try:
            doc = fitz.open(file_path)
            raw_text = ""
            paragraphs = []
            
            for page in doc:
                text = page.get_text()
                raw_text += text + "\n"
                # Simple paragraph splitting
                page_paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
                paragraphs.extend(page_paragraphs)
                
            doc.close()
            
            normalized_text = " ".join(raw_text.split())
            hash_value = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
            
            stat = file_path.stat()
            
            return ParsedDocument(
                document_id=document_id,
                document_name=file_path.name,
                document_type="PDF",
                relative_path=relative_path,
                created_at=datetime.fromtimestamp(stat.st_ctime),
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                page_count=len(doc),
                raw_text=raw_text,
                normalized_text=normalized_text,
                hash_value=hash_value,
                paragraphs=paragraphs
            )
        except Exception as e:
            raise DocumentParsingException(f"Failed to parse PDF {file_path}: {e}")
