from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os

from src.rag_pipeline import answer_question
from src.document_loader import extract_text_from_pdf
from src.text_cleaner import clean_text
from src.chunker import create_chunks
from src.embeddings import create_embeddings
from src.vector_store import store_chunks



app = FastAPI(
    title="AI Document Intelligence & RAG Assistant"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI Document Intelligence & RAG Assistant API is running"
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # Check that the uploaded file is a PDF
    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported."
        }

    # Save uploaded PDF
    os.makedirs("data", exist_ok=True)

    file_path = os.path.join(
        "data",
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = extract_text_from_pdf(file_path)

    # Clean text
    cleaned_text = clean_text(text)

    # Create chunks
    chunks = create_chunks(cleaned_text)

    # Create embeddings
    embeddings = create_embeddings(chunks)

    # Store in ChromaDB
    store_chunks(chunks, embeddings)

    return {
        "message": "Document uploaded and processed successfully",
        "filename": file.filename,
        "chunks_created": len(chunks)
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer = answer_question(request.question)

    return {
        "question": request.question,
        "answer": answer
    }