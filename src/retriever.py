from src.embeddings import model
from src.vector_store import search_chunks


def retrieve_relevant_chunks(question, n_results=3):
    query_embedding = model.encode([question])[0]

    results = search_chunks(
        query_embedding,
        n_results=n_results
    )

    return results["documents"][0]