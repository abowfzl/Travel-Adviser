from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage


class Neo4jChatHistoryDatabase:
    def __init__(
            self,
            host: str = "neo4j+s://6fc52ca0.databases.neo4j.io",
            user: str = "abofazlmoslemian1234@gmail.com",
            password: str = "@BOLFazl 1380",
            session_id: str = ""
    ) -> None:
        self._driver = Neo4jChatMessageHistory(
            url=host,
            username=user,
            password=password,
            session_id=session_id)

    async def add_messages(self, messages: [(str, str)]):
        new_messages = []

        for message in messages:
            text = message[1]
            keyword = message[0]

            if keyword == 'ai':
                new_messages.append(AIMessage(content=text))
            else:
                new_messages.append(HumanMessage(content=text))

        await self._driver.aadd_messages(new_messages)

    async def get_messages(self):
        await self._driver.aget_messages()
