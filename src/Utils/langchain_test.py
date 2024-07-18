from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

template = PromptTemplate(template="""
You are a cockney fruit and vegetable seller.
Your role is to assist your customer with their fruit and vegetable needs.
Respond using cockney rhyming slang.

Output JSON as {{"description": "your response here"}}

Tell me about the following fruit: {fruit}
""", input_variables=["fruit"])


local_path = (
    "./models/Meta-Llama-3-8B-Instruct.Q4_0.gguf"  # replace with your local file path
)
chat_llm = GPT4All(model=local_path, streaming=True)

llm_chain = template | chat_llm | StrOutputParser()

response = llm_chain.invoke({"fruit": "apple"})

print(response)
