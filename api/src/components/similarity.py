from typing import Any

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder

from components.base_component import BaseComponent
from llm.basellm import BaseLLM
from embedding.base_embedding import BaseEmbedding
from wrapper.neo4j_wrapper import Neo4jDatabase
from Utils.data_formatter import format_entries

from .classifier import is_attraction_query


def validate_user_trip_information(city_name: str, stay_duration: str) -> (int, str):
    if city_name is None or not city_name.isalpha() or " " in city_name or city_name == "نمیدانم":
        return 0, None

    if stay_duration is None or not stay_duration.isdigit() or stay_duration == "نمیدانم":
        return 0, city_name

    # Convert stay_duration to an integer
    stay_duration = int(stay_duration)

    return stay_duration, city_name


def create_prompt():
    messages = [
        MessagesPlaceholder(variable_name="chat_history"),
        ("system", "{question}")

    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    return prompt


class Neo4jSimilarity(BaseComponent):
    def __init__(self, database: Neo4jDatabase, embedder: BaseEmbedding, llm: BaseLLM) -> None:
        self.database = database
        self.embedder = embedder
        self.llm = llm

    async def get_user_trip_information(self, session_id: str,) -> (int, str):
        prompt = create_prompt()
        city_name_question = "بر اساس آخرین مکالمه، آخرین مقصد مورد نظر کاربر کجاست؟ فقط نام آخرین شهر را بنویس. اگر مطمئن نیستی یا نمی‌دانی، فقط 'نمیدانم' بنویس."
        stay_duration_question = "بر اساس آخرین مکالمه، کاربر چند روز قصد دارد سفر کند؟ در جواب فقط و فقط آخرین عدد اعلام شده ریاضی را به عدد بده، مثل 2 یا 3. اگر مطمئن نیستی یا نمی‌دانی، فقط 'نمیدانم' بنویس."

        city_name = await self.llm.generate_streaming(city_name_question, session_id, None, prompt, False)
        stay_duration = await self.llm.generate_streaming(stay_duration_question, session_id, None, prompt, False)

        stay_duration, city_name = validate_user_trip_information(city_name, stay_duration)

        return stay_duration, city_name

    async def run_async(self, question: str, session_id: str, similars=None) -> Any:

        # if is_attraction_query(question) is False:
        #     return []

        stay_duration, city_name = await self.get_user_trip_information(session_id)

        if city_name is None:
            return []

        if stay_duration == 0:
            stay_duration = 2

        nearest_cities = self.database.find_nearest_cities(city_name)
        city_names = [city['n']['Name'] for city in nearest_cities]

        # question_embedding = await self.embedder.embed_query(question)

        retrieved_items = self.database.get_attractions(city_names=city_names)

        contents = format_entries(retrieved_items)

        return contents[:stay_duration * 2]

    def run(self, question: str, session_id: str, similars=None) -> Any:
        pass
