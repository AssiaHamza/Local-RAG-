from fastapi import APIRouter, Depends
from db.qdrant import list_documents, delete_document

router = APIRouter(prefix="/document", tags=["document"])

@router.get("/")

async def get_document():
    return list_documents()

@router.delete("/{document_id}")
async def remove_document(document_id: str):
    delete_document(document_id)
    return {"message": f"Document {document_id} deleted successfully."}