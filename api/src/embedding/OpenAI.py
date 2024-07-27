from openai import AsyncOpenAI
from .base_embedding import BaseEmbedding

client = AsyncOpenAI()


class OpenAIEmbedding(BaseEmbedding):
    """Wrapper around OpenAI embedding models."""

    def __init__(
        self, model_name: str = "text-embedding-ada-002"
    ) -> None:
        self.model = model_name

    async def embed_query(self, text: str) -> list[float]:

        embedding = await client.embeddings.create(input=[text], model=self.model)
        return embedding.data[0].embedding
