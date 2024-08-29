from langchain_community.chat_message_histories import Neo4jChatMessageHistory


class NoSaveNeo4jChatMessageHistory(Neo4jChatMessageHistory):
    def add_message(self, message):
        # Override the save method to do nothing, preventing persistence
        pass
