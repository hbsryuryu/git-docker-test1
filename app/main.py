from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend_func.call_llm import generate_response

from dotenv import load_dotenv
# 環境変数読み込み
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  
    allow_methods=["*"],     
    allow_headers=["*"]      
)

# リクエストボディのモデル定義
class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat_stream(req:Request):
    try:
        req_body = await req.json()
    except ValueError:
        return Response("Invalid JSON in request body.", status_code=400)

    question = req_body.get("question")
    if not question:
        return Response("Invalid JSON in request body.", status_code=400)
    return StreamingResponse(generate_response(question), media_type="text/event-stream")
