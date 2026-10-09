from retrieval.keyword_search import keyword_search
from retrieval.vector_search import vector_search
from retrieval.rerank import rerank

def hybrid_search(question, limit: int = 5):
    vector_results = vector_search(question, limit * 4)

    keyword_results = keyword_search(question, limit * 4)

    merged = {}

    for chunk in vector_results + keyword_results:
        key = (chunk["document_id"], chunk["chunk_index"])

        if key not in merged:
            merged[key] = chunk

    results = list(merged.values())
    results = rerank(question, results)

    return results[:limit]
