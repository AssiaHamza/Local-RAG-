import ollama

MODEL = "llama3.1:8b"

SYSTEM_PROMPT = """You are a helpful assistant.
Answer ONLY using the provided context.
If the context does not contain the answer, say you don't know."""

def chat(question: str, context: str, history: list):
    prompt =f"""
Context:
{context}
Question:
{question}
"""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, *history, {"role": "user", "content": prompt}]
    response = ollama.chat(model=MODEL, messages=messages)
    return response["message"]["content"]
