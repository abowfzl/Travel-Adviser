from uuid import uuid4

from langchain.schema import StrOutputParser
from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain_community.graphs import Neo4jGraph
from langchain_community.llms import GPT4All
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

local_path = (
    "./models/Meta-Llama-3-8B-Instruct.Q4_0.gguf"  # replace with your local file path
)
chat_llm = GPT4All(model=local_path, streaming=True)

graph = Neo4jGraph(
    url="bolt://54.161.194.89:7687",
    username="neo4j",
    password="allowances-tunnels-selectors"
)

SESSION_ID = str(uuid4())
print(f"Session ID: {SESSION_ID}")


def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a travel advisor, having a conversation about the attractions of cities. Respond using adviser slang.",
        ),
        # ("system", "{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

chat_chain = prompt | chat_llm | StrOutputParser()

# current_weather = """
#     {
#         "surf": [
#             {"beach": "Fistral", "conditions": "6ft waves and offshore winds"},
#             {"beach": "Polzeath", "conditions": "Flat and calm"},
#             {"beach": "Watergate Bay", "conditions": "3ft waves and onshore winds"}
#         ]
#     }"""

chat_with_message_history = RunnableWithMessageHistory(
    chat_chain,
    get_memory,
    input_messages_key="question",
    history_messages_key="chat_history",
)

while True:
    question = input("> ")

    response = chat_with_message_history.invoke(
        {
            # "context": current_weather,
            "question": question,

        },
        config={
            "configurable": {"session_id": SESSION_ID}
        }
    )

    print(response)
