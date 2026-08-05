import json
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional
from src.sop_orchestrator.models.project import ProjectConfig

class KnowledgeCache:
    def __init__(self, project_config: ProjectConfig):
        self.cache_dir = project_config.knowledge_dir / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, key: str, namespace: str) -> Path:
        hashed_key = hashlib.md5(key.encode('utf-8')).hexdigest()
        return self.cache_dir / f"{namespace}_{hashed_key}.json"

    def get(self, key: str, namespace: str) -> Optional[Any]:
        cache_path = self._get_cache_path(key, namespace)
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def set(self, key: str, value: Any, namespace: str):
        cache_path = self._get_cache_path(key, namespace)
        try:
            with open(cache_path, 'w') as f:
                json.dump(value, f)
        except Exception:
            pass

    def invalidate(self, key: str, namespace: str):
        cache_path = self._get_cache_path(key, namespace)
        if cache_path.exists():
            try:
                cache_path.unlink()
            except Exception:
                pass

    def clear_namespace(self, namespace: str):
        for cache_path in self.cache_dir.glob(f"{namespace}_*.json"):
            try:
                cache_path.unlink()
            except Exception:
                pass
