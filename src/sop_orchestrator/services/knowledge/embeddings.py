import time
from typing import List
from langchain_openai import OpenAIEmbeddings
from src.sop_orchestrator.services.knowledge.exceptions import EmbeddingException

class EmbeddingService:
    def __init__(self, api_key: str, model: str = "text-embedding-ada-002", max_retries: int = 3):
        self.model = model
        self.max_retries = max_retries
        # In a real environment, you'd pass api_key to OpenAIEmbeddings
        # Here we mock it if key is missing or invalid for testing
        self.embeddings = OpenAIEmbeddings(model=self.model, api_key=api_key or "mock_key")

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        retries = 0
        while retries < self.max_retries:
            try:
                # We can handle batching here if the input list is too large
                return self.embeddings.embed_documents(texts)
            except Exception as e:
                retries += 1
                if retries >= self.max_retries:
                    raise EmbeddingException(f"Failed to generate embeddings after {self.max_retries} retries: {e}")
                time.sleep(1 * retries)
        return []

    def generate_embedding(self, text: str) -> List[float]:
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            raise EmbeddingException(f"Failed to generate embedding: {e}")
