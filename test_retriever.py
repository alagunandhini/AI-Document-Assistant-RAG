from src.retriever import retrieve_relevant_chunks


question = "What is ETL?"

chunks = retrieve_relevant_chunks(question)

print("\nRelevant chunks:\n")

for i, chunk in enumerate(chunks, start=1):
    print(f"--- Chunk {i} ---")
    print(chunk)
    print()