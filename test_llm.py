from src.llm import generate_answer


prompt = "Explain ETL in simple terms for a beginner."

answer = generate_answer(prompt)

print("\nLLM Answer:\n")
print(answer)