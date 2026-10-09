from qdrant_client import QdrantClient
from qdrant_client.models import Distance, Filter, FilterSelector, MatchValue, VectorParams, PointStruct, FieldCondition

client = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "documents"

def collection_exists():
    collections = client.get_collections().collections
    return any(collection.name == COLLECTION_NAME for collection in collections)

def create_collection(vector_size: int):
    if not collection_exists():
        client.create_collection(collection_name=COLLECTION_NAME, vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE))

def store_embeddings(embeddings):
        points=[]
        for item in embeddings:
            points.append(PointStruct(id=item["id"], vector=item["embedding"], payload={"text": item["text"], "document_id": item["document_id"], "filename": item["filename"], "chunk_index": item["chunk_index"]}))

        client.upsert(collection_name=COLLECTION_NAME, points=points)

def list_documents():
     documents = {}
     if not collection_exists():
          return []
     offset = None
     while True:
          points, offset = client.scroll(collection_name=COLLECTION_NAME, limit=100, with_payload=True,
                                         with_vectors=False, offset=offset)
          for point in points:
               payload = point.payload

               document_id = payload["document_id"]
               if document_id not in documents:
                    documents[document_id] = {
                         "document_id": document_id,
                         "filename": payload.get("filename"),
                         "chunks": 0
                    }

               documents[document_id]["chunks"] += 1
          if offset is None:
               break
     return list(documents.values())

def delete_document(document_id: str):
     if not collection_exists():
          return
     client.delete(collection_name=COLLECTION_NAME, points_selector=FilterSelector(filter=Filter(must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))])))

def list_chunks():
     chunks = []
     if not collection_exists():
          return chunks
     offset = None
     while True:
          points, offset = client.scroll(collection_name=COLLECTION_NAME, limit=100, with_payload=True,
                                         with_vectors=False, offset=offset)
          for point in points:

               chunks.append({
                    "text": point.payload["text"],
                    "filename": point.payload.get("filename"),
                    "document_id": point.payload["document_id"],
                    "chunk_index": point.payload["chunk_index"]
               })
          if offset is None:
               break
     return chunks
