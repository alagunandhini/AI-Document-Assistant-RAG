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

from src.database import SessionLocal, Document, DocumentChunk



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

    # Create SQL database session
    db = SessionLocal()

    document = None

    try:
        # Save document metadata in SQL
        document = Document(
            filename=file.filename,
            file_size=os.path.getsize(file_path),
            total_chunks=len(chunks),
            status="processing"
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        # Save chunks in SQL
        for index, chunk in enumerate(chunks):

            chunk_record = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                chunk_text=chunk
            )

            db.add(chunk_record)

        db.commit()

        # Create embeddings
        embeddings = create_embeddings(chunks)

        # Store embeddings in ChromaDB
        store_chunks(
            chunks,
            embeddings,
            source=file.filename
        )

        # Mark document as processed
        document.status = "processed"

        db.commit()

        return {
            "message": "Document uploaded and processed successfully",
            "filename": file.filename,
            "chunks_created": len(chunks),
            "document_id": document.id,
            "status": document.status
        }

    except Exception as e:

        if document:
            document.status = "failed"
            db.commit()

        return {
            "error": str(e),
            "filename": file.filename,
            "status": "failed"
        }

    finally:
        db.close()

@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer = answer_question(request.question)

    return {
        "question": request.question,
        "answer": answer
    }

@app.get("/documents")
def get_documents():
    db = SessionLocal()

    try:
        documents = db.query(Document).all()

        return [
            {
                "id": document.id,
                "filename": document.filename,
                "file_size": document.file_size,
                "total_chunks": document.total_chunks,
                "status": document.status,
                "uploaded_at": document.uploaded_at
            }
            for document in documents
        ]

    finally:
        db.close()