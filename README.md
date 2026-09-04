# AI Document Intelligence & RAG Assistant

A simple PDF question-answering application built using Python and RAG.

Users can upload a PDF and ask questions about the document. The application finds relevant content from the PDF and uses Google Gemini to generate the answer.

## Features

- Upload PDF
- Extract text from PDF
- Clean and split text into chunks
- Generate embeddings
- Store embeddings in ChromaDB
- Search relevant content
- Generate answers using Gemini
- FastAPI backend
- Simple web interface

## Technologies

- Python
- FastAPI
- PyMuPDF
- Sentence Transformers
- ChromaDB
- Google Gemini
- HTML, CSS, JavaScript
- Git & GitHub

## How It Works

```text
PDF
 ↓
Extract Text
 ↓
Clean & Chunk
 ↓
Create Embeddings
 ↓
Store in ChromaDB
 ↓
Ask Question
 ↓
Find Relevant Chunks
 ↓
Send Context to Gemini
 ↓
Get Answer

How RAG Works

When a document is uploaded, its text is extracted and divided into
smaller chunks. Each chunk is converted into an embedding and stored in
ChromaDB.

When a user asks a question:

The question is converted into an embedding.
ChromaDB searches for similar document chunks.
Relevant chunks are retrieved.
The retrieved content is added to the prompt.
Google Gemini generates an answer using the retrieved context.

This allows the application to answer questions based on the uploaded
document.

Tech Stack
Python — Application development
FastAPI — REST API backend
PyMuPDF — PDF text extraction
Sentence Transformers — Text embeddings
all-MiniLM-L6-v2 — Embedding model
ChromaDB — Vector database
Google Gemini — Large Language Model
HTML/CSS/JavaScript — Web UI
Git/GitHub — Version control

Run the application: uvicorn api.main:app --reload

Open the frontend: frontend/index.html
