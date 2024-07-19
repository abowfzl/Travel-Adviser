from typing import Any

from components.base_component import BaseComponent
from embedding.base_embedding import BaseEmbedding
from wrapper.neo4j_wrapper import Neo4jDatabase


class Neo4jSimilarity(BaseComponent):
    def __init__(self, database: Neo4jDatabase, embedder: BaseEmbedding) -> None:
        self.database = database
        self.embedder = embedder

    async def run_async(self, question: str, session_id: str, similars=None) -> Any:
        question_embedding = await self.embedder.embed_query(question)
        retrieved_items = self.database.semantic_search(question_embedding=question_embedding)
        contents = [item.content for item in retrieved_items.items]

        return contents

    def run(self, question: str, session_id: str, similars=None) -> Any:
        pass
