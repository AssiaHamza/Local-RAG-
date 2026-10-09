from uuid import uuid4

import ollama

MODEL = "nomic-embed-text"

def embed_text(chunks, document_id, filename):
    embeddings = []
    for chunk_index, chunk in enumerate(chunks):
        response = ollama.embed(model = MODEL, input = chunk)
        embeddings.append({"text": chunk, "embedding": response["embeddings"][0], "document_id": document_id, "filename": filename, "chunk_index": chunk_index, "id": str(uuid4())})
    return embeddings
