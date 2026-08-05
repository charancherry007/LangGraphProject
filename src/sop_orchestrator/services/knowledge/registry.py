import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel
from src.sop_orchestrator.models.project import ProjectConfig
from src.sop_orchestrator.models.knowledge import DocumentRegistryEntry

class DocumentRegistry:
    def __init__(self, project_config: ProjectConfig):
        self.registry_file = project_config.knowledge_dir / "registry.json"
        self.entries: Dict[str, DocumentRegistryEntry] = {}
        self.load()

    def load(self):
        """Load the registry from disk."""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, "r") as f:
                    data = json.load(f)
                    for key, val in data.items():
                        self.entries[key] = DocumentRegistryEntry(**val)
            except Exception:
                self.entries = {}

    def save(self):
        """Save the registry to disk."""
        with open(self.registry_file, "w") as f:
            json.dump({k: v.model_dump(mode='json') for k, v in self.entries.items()}, f, indent=2)

    def get_entry(self, relative_path: str) -> Optional[DocumentRegistryEntry]:
        return self.entries.get(relative_path)

    def add_or_update_entry(self, relative_path: str, entry: DocumentRegistryEntry):
        if relative_path in self.entries:
            entry.version = self.entries[relative_path].version + 1
        else:
            entry.version = 1
        self.entries[relative_path] = entry
        self.save()

    def remove_entry(self, relative_path: str):
        if relative_path in self.entries:
            del self.entries[relative_path]
            self.save()

    def get_all_hashes(self) -> Dict[str, str]:
        """Return a mapping of relative paths to their current hashes."""
        return {k: v.hash_value for k, v in self.entries.items()}
