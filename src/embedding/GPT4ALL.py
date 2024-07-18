from nomic import embed
from .base_embedding import BaseEmbedding


class Gpt4AllEmbedding(BaseEmbedding):
    """Wrapper around GPT4All embedding models."""

    async def embed_query(self, text: str) -> list[float]:
        embeddings = embed.text([text], model="nomic-embed-text-v1.5", inference_mode="local")
        return embeddings['embeddings'][0]
