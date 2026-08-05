import hashlib
from pathlib import Path
from typing import List, Dict, Set
from src.sop_orchestrator.models.project import ProjectConfig

class KnowledgeScanner:
    def __init__(self, project_config: ProjectConfig):
        self.knowledge_dir = project_config.knowledge_dir
        self.expected_folders = [
            "CHC",
            "System",
            "Policies",
            "Templates",
            "Supporting Documents",
            "Reference SOP"
        ]

    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def scan(self, existing_registry_entries: Dict[str, str]) -> Dict[str, List[Path]]:
        """
        Scan the knowledge repository.
        existing_registry_entries is a dict of {relative_path: hash_value}
        Returns:
            Dict containing lists of 'new', 'modified', and 'deleted' file paths.
        """
        current_files: Dict[str, Path] = {}
        
        for folder in self.expected_folders:
            folder_path = self.knowledge_dir / folder
            if folder_path.exists() and folder_path.is_dir():
                for file_path in folder_path.rglob("*"):
                    if file_path.is_file() and not file_path.name.startswith("."):
                        rel_path = str(file_path.relative_to(self.knowledge_dir))
                        current_files[rel_path] = file_path

        new_files = []
        modified_files = []
        
        for rel_path, file_path in current_files.items():
            if rel_path not in existing_registry_entries:
                new_files.append(file_path)
            else:
                current_hash = self._get_file_hash(file_path)
                if current_hash != existing_registry_entries[rel_path]:
                    modified_files.append(file_path)

        current_paths_set = set(current_files.keys())
        deleted_paths = [Path(self.knowledge_dir / p) for p in existing_registry_entries.keys() if p not in current_paths_set]

        return {
            "new": new_files,
            "modified": modified_files,
            "deleted": deleted_paths
        }
