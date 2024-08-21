import os
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Utils.session_id_generator import Session
from components.result_generator import ResultGenerator
from components.similarity import Neo4jSimilarity
from embedding.GPT4ALL import Gpt4AllEmbedding
from embedding.OpenAI import OpenAIEmbedding
from llm.OpenAI import ChatOpenAIChat
from llm.GPT4ALL import Gpt4AllChat
from wrapper.neo4j_wrapper import Neo4jDatabase
from wrapper.neo4j_chathistory_wrapper import Neo4jChatHistoryDatabase

neo4j_connection = Neo4jDatabase(
    host=os.getenv('NEO4J_URL'),
    user=os.getenv('NEO4J_USER'),
    password=os.getenv('NEO4J_PASS'),
    database=os.getenv('NEO4J_DATABASE'),
)

# Initialize LLM modules
openai_api_key = os.environ.get("OPENAI_API_KEY", None)


def create_neo4j_chat_history_connection(session_id: str):
    return Neo4jChatHistoryDatabase(
        host=os.getenv('NEO4J_URL'),
        user=os.getenv('NEO4J_USER'),
        password=os.getenv('NEO4J_PASS'),
        session_id=session_id)


def create_embedder(model_name):
    model = None

    if model_name == 'openai':
        model = OpenAIEmbedding()

    elif model_name == 'gpt4all':
        model = Gpt4AllEmbedding()

    return model


def create_model(model_name, websocket):
    model = None
    if model_name == 'openai':
        model = ChatOpenAIChat(websocket)

    elif model_name == 'gpt4all':
        model = Gpt4AllChat(websocket)

    return model


class Payload(BaseModel):
    question: str
    session_id: str
    model_name: Optional[str]


# Define FastAPI endpoint
app = FastAPI()

origins = [
    "*",
]

# Maximum number of records used in the context
HARD_LIMIT_CONTEXT_RECORDS = 10

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/text2text")
async def websocket_endpoint(websocket: WebSocket):
    async def send_debug_message(message):
        await websocket.send_json({"type": "debug", "detail": message})

    async def send_error_message(message):
        await websocket.send_json({"type": "error", "detail": message})

    await websocket.accept()
    await send_debug_message("connected")
    try:
        while True:
            data = await websocket.receive_json()

            if "type" not in data:
                await websocket.send_json({"error": "missing type"})
                continue

            if "session_id" not in data:
                await websocket.send_json({"error": "missing session id"})
                continue

            if "model" not in data:
                await websocket.send_json({"error": "missing model"})
                continue

            session_id = data['session_id']

            model_name = data['model']

            model = create_model(model_name, websocket)

            if model is None:
                await websocket.send_json({"error": "model undefined"})
                continue

            result_generator = ResultGenerator(
                llm=model
            )

            embedder = create_embedder(model_name)

            similarity = Neo4jSimilarity(
                database=neo4j_connection,
                embedder=embedder,
                llm=model
            )

            if data["type"] == "question":
                try:
                    question = data["question"]

                    await send_debug_message("received question: " + question)
                    try:
                        similars = await similarity.run_async(question=question, session_id=session_id)
                    except Exception as e:
                        await send_error_message(str(e))
                        continue

                    await websocket.send_json(
                        {
                            "type": "start",
                            "similars": similars
                        }
                    )
                    output = await result_generator.run_async(
                        question=question,
                        session_id=session_id,
                        similars=similars
                    )

                    await websocket.send_json(
                        {
                            "type": "end",
                            "output": output,
                            "similars": similars,
                        }
                    )
                except Exception as e:
                    await send_error_message(str(e))
                await send_debug_message("output done")
    except WebSocketDisconnect:
        print("disconnected")


@app.get("/")
async def read_root():
    return {"message": "Hello from Travel Adviser project!"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/ready")
async def readiness_check():
    return {"status": "ok"}


@app.post("/generate_session_id")
async def generate_session_id():
    session = Session()
    return {'session_id': session.generate_session_id()}


@app.post("/similars")
async def get_similars(payload: Payload):
    embedder = create_embedder(payload.model_name)

    similarity = Neo4jSimilarity(
        database=neo4j_connection,
        embedder=embedder
    )
    similars = await similarity.run_async(question=payload.question, session_id=payload.session_id)

    return {'similars': similars}


@app.get("/chat_history")
async def get_chat_history(session_id: str):
    if session_id is None:
        raise HTTPException(status_code=401, detail="not authorized!")

    chat_history_db = create_neo4j_chat_history_connection(session_id)

    messages = chat_history_db.get_messages()

    return {"messages": messages}


@app.get("/hasapikey")
async def has_api_key():
    return JSONResponse(content={"output": openai_api_key is not None})


@app.delete("/chat_history")
async def clear_chat_history(session_id: str):
    if session_id is None:
        raise HTTPException(status_code=401, detail="not authorized!")

    chat_history_db = create_neo4j_chat_history_connection(session_id)

    chat_history_db.clear_messages()

    return {"success": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=int(os.environ.get("PORT", 8000)), host="127.0.0.1")
