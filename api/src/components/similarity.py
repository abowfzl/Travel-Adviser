from typing import Any

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder

from components.base_component import BaseComponent
from llm.basellm import BaseLLM
from embedding.base_embedding import BaseEmbedding
from wrapper.neo4j_wrapper import Neo4jDatabase
from Utils.data_formatter import format_entries

from .classifier import is_travel_related_query


def validate_user_trip_information(city_name: str, mentioned_city_in_question: str, stay_duration: str) -> (int, str):

    if mentioned_city_in_question is not None and mentioned_city_in_question.isalpha() and " " not in mentioned_city_in_question and mentioned_city_in_question != "نمیدانم":
        city_name = mentioned_city_in_question

    if city_name is None or not city_name.isalpha() or " " in city_name or city_name == "نمیدانم":
        return 0, None

    if stay_duration is None or not stay_duration.isdigit() or stay_duration == "نمیدانم":
        return 0, city_name

    # Convert stay_duration to an integer
    stay_duration = int(stay_duration)

    return stay_duration, city_name


def create_prompt(use_history: bool):
    if use_history:
        messages = [
            MessagesPlaceholder(variable_name="chat_history"),
            ("system", "{question}")

        ]
    else:
        messages = [
            ("system", "{question}")
        ]

    prompt = ChatPromptTemplate.from_messages(messages)

    return prompt


class Neo4jSimilarity(BaseComponent):
    def __init__(self, database: Neo4jDatabase, embedder: BaseEmbedding, llm: BaseLLM) -> None:
        self.database = database
        self.embedder = embedder
        self.llm = llm

    async def get_user_trip_information(self, question: str, session_id: str, ) -> (int, str):
        use_history = True
        # Questions that need chat history
        city_name_question = "بر اساس آخرین مکالمه، آخرین مقصد مورد نظر کاربر کجاست؟ فقط نام آخرین شهر را بنویس. اگر مطمئن نیستی یا نمی‌دانی، فقط 'نمیدانم' بنویس."
        stay_duration_question = "بر اساس آخرین مکالمه، کاربر چند روز قصد دارد سفر کند؟ در جواب فقط و فقط آخرین عدد اعلام شده ریاضی را به عدد بده، مثل 2 یا 3. اگر مطمئن نیستی یا نمی‌دانی، فقط 'نمیدانم' بنویس."

        # Question that does not need chat history
        mentioned_city_name_question = f"در متن زیر که متن کاربر است، اگر تنها نام یک شهر ذکر شده باشد، فقط نام آن شهر را بنویس. اگر بیش از یک شهر ذکر شده یا هیچ شهری ذکر نشده، یا اگر مطمئن نیستی، کلمه 'نمیدانم' را بنویس.متن: {question}"

        prompt = create_prompt(use_history)
        # Generate responses with history
        city_name = await self.llm.generate_streaming(city_name_question, session_id, None, prompt, False,
                                                      use_history=use_history, save_conversation=False)
        stay_duration = await self.llm.generate_streaming(stay_duration_question, session_id, None, prompt, False,
                                                          use_history=use_history, save_conversation=False)

        use_history = False
        prompt = create_prompt(use_history)
        # Generate response without history
        mentioned_city_in_question = await self.llm.generate_streaming(mentioned_city_name_question, session_id, None,
                                                                       prompt, use_history, use_history=False)

        stay_duration, city_name = validate_user_trip_information(city_name, mentioned_city_in_question, stay_duration)

        return stay_duration, city_name

    async def run_async(self, question: str, session_id: str, similars=None) -> Any:

        # if is_attraction_query(question) is False:
        #     return []

        stay_duration, city_name = await self.get_user_trip_information(question, session_id)

        if city_name is None:
            return []

        if stay_duration == 0:
            stay_duration = 2

        await self.llm.websocket.send_json({"type": "debug", "detail": f"recognized city: {city_name}, stay_duration: {stay_duration}"})

        nearest_cities = self.database.find_nearest_cities(city_name)

        if not nearest_cities:
            await self.llm.websocket.send_json(
                {"type": "debug", "detail": f"city {city_name} not found in db"})
            return []

        city_names = [city['n']['Name'] for city in nearest_cities]

        # question_embedding = await self.embedder.embed_query(question)

        retrieved_items = self.database.get_attractions(city_names=city_names)

        contents = format_entries(retrieved_items)

        return contents[:stay_duration * 2]

    def run(self, question: str, session_id: str, similars=None) -> Any:
        pass
