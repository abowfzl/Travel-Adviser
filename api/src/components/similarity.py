from typing import Any
import ast

from components.base_component import BaseComponent
from embedding.base_embedding import BaseEmbedding
from wrapper.neo4j_wrapper import Neo4jDatabase

from .classifier import is_attraction_query


class Neo4jSimilarity(BaseComponent):
    def __init__(self, database: Neo4jDatabase, embedder: BaseEmbedding) -> None:
        self.database = database
        self.embedder = embedder

    async def run_async(self, question: str, session_id: str, similars=None) -> Any:

        if is_attraction_query(question) is False:
            return []

        question_embedding = await self.embedder.embed_query(question)
        retrieved_items = self.database.semantic_search(question_embedding=question_embedding)

        contents = []
        for item in retrieved_items.items:
            data = ast.literal_eval(item.content)

            contents.append({
                'city_name': data['city_name'],
                'name': data['name'],
                'title': data['title'],
                'text': data['text'] if 'text' in data else "",
                'location': data['location'],
                'url': data['url']
            })

        return contents

    def run(self, question: str, session_id: str, similars=None) -> Any:
        pass
