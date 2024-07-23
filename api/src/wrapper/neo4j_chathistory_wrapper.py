from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage


class Neo4jChatHistoryDatabase:
    def __init__(
            self,
            host: str,
            user: str,
            password: str,
            session_id: str
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

        for message in new_messages:
            self._driver.add_message(message)

    def get_messages(self):
        return self._driver.messages

    def clear_messages(self):
        return self._driver.clear()
