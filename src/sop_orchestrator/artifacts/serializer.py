import json
import yaml
from pathlib import Path
from typing import Dict, Any, Type, TypeVar
from src.sop_orchestrator.artifacts.base import BaseArtifact
from src.sop_orchestrator.artifacts.exceptions import ArtifactSerializationException

T = TypeVar('T', bound=BaseArtifact)

class ArtifactSerializer:
    @staticmethod
    def to_json(artifact: BaseArtifact, pretty: bool = False) -> str:
        """Serialize artifact to JSON string."""
        try:
            return artifact.model_dump_json(indent=2 if pretty else None)
        except Exception as e:
            raise ArtifactSerializationException(f"Failed to serialize to JSON: {str(e)}")

    @staticmethod
    def from_json(json_str: str, model_class: Type[T]) -> T:
        """Deserialize JSON string to artifact model."""
        try:
            return model_class.model_validate_json(json_str)
        except Exception as e:
            raise ArtifactSerializationException(f"Failed to deserialize from JSON: {str(e)}")

    @staticmethod
    def to_yaml(artifact: BaseArtifact) -> str:
        """Serialize artifact to YAML string."""
        try:
            data = artifact.model_dump(mode='json')
            return yaml.dump(data, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise ArtifactSerializationException(f"Failed to serialize to YAML: {str(e)}")

    @staticmethod
    def from_yaml(yaml_str: str, model_class: Type[T]) -> T:
        """Deserialize YAML string to artifact model."""
        try:
            data = yaml.safe_load(yaml_str)
            return model_class.model_validate(data)
        except Exception as e:
            raise ArtifactSerializationException(f"Failed to deserialize from YAML: {str(e)}")

    @classmethod
    def save_to_file(cls, artifact: BaseArtifact, filepath: Path, format: str = 'json', pretty: bool = True) -> None:
        """Save artifact to a file."""
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            if format.lower() == 'json':
                content = cls.to_json(artifact, pretty=pretty)
            elif format.lower() in ('yaml', 'yml'):
                content = cls.to_yaml(artifact)
            else:
                raise ArtifactSerializationException(f"Unsupported format: {format}")
                
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise ArtifactSerializationException(f"Failed to save artifact to file: {str(e)}")

    @classmethod
    def load_from_file(cls, filepath: Path, model_class: Type[T]) -> T:
        """Load artifact from a file."""
        if not filepath.exists():
            raise ArtifactSerializationException(f"File not found: {filepath}")
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if filepath.suffix.lower() == '.json':
                return cls.from_json(content, model_class)
            elif filepath.suffix.lower() in ('.yaml', '.yml'):
                return cls.from_yaml(content, model_class)
            else:
                raise ArtifactSerializationException(f"Unsupported file extension: {filepath.suffix}")
        except Exception as e:
            raise ArtifactSerializationException(f"Failed to load artifact from file: {str(e)}")
