import chromadb
import uuid


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def store_chunks(chunks, embeddings, source="unknown"):
    ids = [
        str(uuid.uuid4())
        for _ in chunks
    ]

    metadatas = [
        {
            "source": source,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )


def search_chunks(query_embedding, n_results=3):
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results
    )

    return results