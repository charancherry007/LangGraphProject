import hashlib
from pathlib import Path
from datetime import datetime
from src.sop_orchestrator.models.knowledge import ParsedDocument
from src.sop_orchestrator.services.knowledge.parsers.base import BaseParser
from src.sop_orchestrator.services.knowledge.exceptions import DocumentParsingException

class MarkdownParser(BaseParser):
    def can_parse(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in [".md", ".txt", ".markdown"]

    def parse(self, file_path: Path, document_id: str, relative_path: str) -> ParsedDocument:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            
            paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]
            normalized_text = " ".join(raw_text.split())
            hash_value = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
            
            stat = file_path.stat()
            doc_type = "Markdown" if file_path.suffix.lower() != ".txt" else "TXT"
            
            return ParsedDocument(
                document_id=document_id,
                document_name=file_path.name,
                document_type=doc_type,
                relative_path=relative_path,
                created_at=datetime.fromtimestamp(stat.st_ctime),
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                page_count=None,
                raw_text=raw_text,
                normalized_text=normalized_text,
                hash_value=hash_value,
                paragraphs=paragraphs
            )
        except Exception as e:
            raise DocumentParsingException(f"Failed to parse {file_path.suffix} file {file_path}: {e}")
