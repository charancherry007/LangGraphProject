import zipfile
import hashlib
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from src.sop_orchestrator.models.knowledge import ParsedDocument
from src.sop_orchestrator.services.knowledge.parsers.base import BaseParser
from src.sop_orchestrator.services.knowledge.exceptions import DocumentParsingException

class XMLParser(BaseParser):
    def can_parse(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in [".drawio", ".xml", ".vsdx"]

    def _extract_text_from_xml(self, xml_content: str) -> str:
        try:
            soup = BeautifulSoup(xml_content, "xml")
            return " ".join(soup.stripped_strings)
        except Exception:
            return ""

    def parse(self, file_path: Path, document_id: str, relative_path: str) -> ParsedDocument:
        try:
            raw_text = ""
            ext = file_path.suffix.lower()
            
            if ext == ".vsdx":
                with zipfile.ZipFile(file_path, 'r') as z:
                    for filename in z.namelist():
                        if filename.endswith(".xml"):
                            content = z.read(filename).decode('utf-8', errors='ignore')
                            raw_text += self._extract_text_from_xml(content) + "\n"
            else:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    raw_text = self._extract_text_from_xml(f.read())
            
            paragraphs = [p.strip() for p in raw_text.split("\n") if p.strip()]
            normalized_text = " ".join(raw_text.split())
            hash_value = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
            
            stat = file_path.stat()
            doc_type = ext[1:].upper()
            
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
            raise DocumentParsingException(f"Failed to parse XML/VSDX {file_path}: {e}")
