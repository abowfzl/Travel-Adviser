import os

from langchain.schema import StrOutputParser

from langchain_community.chat_models import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain_community.graphs import Neo4jGraph

from .basellm import BaseLLM

graph = Neo4jGraph(
    url=os.getenv('NEO4J_URL'),
    username=os.getenv('NEO4J_USER'),
    password=os.getenv('NEO4J_PASS'),
    database=os.getenv('NEO4J_DATABASE'),
)


def get_session_history(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)


class ChatOpenAIChat(BaseLLM):
    def __init__(
            self,
            websocket,
            model_name: str = "gpt-3.5-turbo",
    ) -> None:
        self.websocket = websocket
        self.model = ChatOpenAI(openai_api_key=os.getenv('OPENAPI_APIKEY'),
                                #openai_api_base=os.getenv('OPENAPI_BASEURL'),
                                streaming=True)
        self.model_name = model_name

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

        tokens = []

        async for chunk in chat_with_message_history.astream(
            {
                "question": question,
                "similars": similars,
            },
            config={
                "configurable": {
                    "session_id": session_id
                },
            }
        ):
            response = {"type": "stream", "output": chunk}
            await self.websocket.send_json(response)

            tokens.append(chunk)

        return tokens
