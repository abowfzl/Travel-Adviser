from abc import ABC, abstractmethod

from neo4j_genai.embedder import Embedder


class BaseEmbedding(Embedder):
    """"""

    @abstractmethod
    async def embed_query(
            self, text: str
    ) -> list[float]:
        """Comment"""
