from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

converter = DocumentConverter()
chunker = HybridChunker()

def chunk_pdf(pdf_path: str):
    result = converter.convert(pdf_path)
    chunks = []

    for chunk in chunker.chunk(result.document):
        if chunk.text.strip():
            chunks.append(chunk.text)

    return chunks
