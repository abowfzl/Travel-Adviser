import os

from langchain.schema import StrOutputParser

from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain_community.graphs import Neo4jGraph
from langchain_community.llms import GPT4All

from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory

from .basellm import BaseLLM


graph = Neo4jGraph(
    url=os.getenv('NEO4J_URL'),
    username=os.getenv('NEO4J_USER'),
    password=os.getenv('NEO4J_PASS'),
    database=os.getenv('NEO4J_DATABASE'),
)


def get_session_history(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)


class CustomAsyncCallbackHandler(AsyncCallbackHandler):
    def __init__(self, websocket):
        self.websocket = websocket
        self.tokens = []

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        response = {"type": "stream", "output": token}
        self.tokens.append(token)
        await self.websocket.send_json(response)

    def copy_token(self):
        return self.tokens.copy()

    def clear_tokens(self):
        self.tokens.clear()


class Gpt4AllChat(BaseLLM):
    def __init__(
            self,
            websocket,
            model_name: str = "Meta-Llama-3-8B-Instruct.Q4_0.gguf",
            max_tokens: int = 1000,
            temperature: float = 0.0,
    ) -> None:
        self.handler = CustomAsyncCallbackHandler(websocket)
        self.websocket = websocket
        self.model = GPT4All(model="Meta-Llama-3-8B-Instruct.Q4_0.gguf",
                             callbacks=[self.handler],
                             streaming=True)
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature

    async def generate_streaming(
            self,
            question: str,
            session_id: str,
            similars,
            prompt: ChatPromptTemplate
    ) -> [str]:

        await self.websocket.send_json({"type": "debug", "detail": f"created prompt: {prompt}"})
        await self.websocket.send_json({"type": "debug", "detail": f"fetched similars: {similars}"})

        chain = prompt | self.model | StrOutputParser()

        await self.websocket.send_json({"type": "debug", "detail": "chain created and model is going to generate"})

        chat_with_message_history = RunnableWithMessageHistory(
            chain,
            get_session_history=get_session_history,
            input_messages_key="question",
            history_messages_key="chat_history",
        )

        await chat_with_message_history.ainvoke(
            {
                "question": question,
                "similars": similars,
            },
            config={
                "configurable": {
                    "session_id": session_id
                    },
            }
        )

        # await chain.ainvoke({"question": question, "similars": similars})

        results = self.handler.copy_token()
        self.handler.clear_tokens()
        return results
