from src.document_loader import extract_text_from_pdf
from src.text_cleaner import clean_text
from src.chunker import create_chunks
from src.embeddings import create_embeddings
from src.vector_store import store_chunks


pdf_path = "data/sample.pdf"

text = extract_text_from_pdf(pdf_path)

cleaned_text = clean_text(text)

chunks = create_chunks(cleaned_text)

embeddings = create_embeddings(chunks)

store_chunks(
    chunks,
    embeddings,
    source=pdf_path
)

print("Document successfully stored in ChromaDB!")
print("Number of chunks:", len(chunks))