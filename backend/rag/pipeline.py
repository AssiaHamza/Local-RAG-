from llm.chat import chat
from memory.history import add_message, get_history
from retrieval.retriever import retrieve


def ask(question: str, session_id: str):

    chunks=retrieve(question)
    context = "\n\n".join([chunk["text"] 
                           for chunk in chunks])

    history = get_history(session_id)

    answer = chat(question=question, context=context, history=history)

    add_message(session_id, "user", question)
    add_message(session_id, "assistant", answer)

    sources = [{"text": chunk["text"], "filename": chunk.get("filename") or "Source"}
        for chunk in chunks]

    return {"answer": answer, "sources": sources}