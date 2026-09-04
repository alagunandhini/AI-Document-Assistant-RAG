from fastapi import FastAPI
from pydantic import BaseModel

from src.rag_pipeline import answer_question


app = FastAPI(
    title="AI Document Intelligence & RAG Assistant"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI Document Intelligence & RAG Assistant API is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    answer = answer_question(request.question)

    return {
        "question": request.question,
        "answer": answer
    }