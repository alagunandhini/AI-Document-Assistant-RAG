from src.retriever import retrieve_relevant_chunks
from src.llm import generate_answer


def answer_question(question):
    # 1. Retrieve relevant chunks from ChromaDB
    chunks = retrieve_relevant_chunks(
        question,
        n_results=3
    )

    # 2. Combine the retrieved chunks into one context
    context = "\n\n".join(chunks)

    # 3. Create the RAG prompt
    prompt = f"""
You are a document question-answering assistant.

Answer the question using only the information provided
in the context below.

If the answer is not present in the context,
say "I don't know based on the provided document."

Context:
{context}

Question:
{question}

Answer:
"""

    # 4. Send the context and question to Gemini
    answer = generate_answer(prompt)

    return answer