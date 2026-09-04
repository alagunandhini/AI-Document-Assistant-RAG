from src.rag_pipeline import answer_question


question = "What are the three stages of ETL?"

answer = answer_question(question)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(answer)