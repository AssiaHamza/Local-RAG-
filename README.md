# Local RAG

A chat application that answers questions about your own PDF documents. Everything runs on your machine: the language model, the embeddings and the vector database. No document or question is sent to an external service.

You upload a PDF, ask a question in the chat, and get an answer written only from the content of your documents, with the source passages shown underneath.

## How it works

**Indexing a document**

1. The PDF is parsed and split into chunks with [Docling](https://github.com/docling-project/docling).
2. Each chunk is turned into a vector with the `nomic-embed-text` model, served by [Ollama](https://ollama.com).
3. Chunks and vectors are stored in [Qdrant](https://qdrant.tech).

**Answering a question**

1. **Vector search** finds chunks whose meaning is close to the question.
2. **Keyword search** (BM25) finds chunks that share its exact words.
3. The two result lists are merged and **reranked** with a cross-encoder (`ms-marco-MiniLM-L-6-v2`), and the best five are kept.
4. Those chunks, the question and the conversation so far are sent to `llama3.1:8b` (through Ollama), which is instructed to answer only from that context.

## Tech stack

| Part | Technology |
|---|---|
| Frontend | Streamlit |
| API | FastAPI |
| PDF parsing and chunking | Docling |
| Embeddings | `nomic-embed-text` via Ollama |
| Vector database | Qdrant |
| Keyword search | BM25 (`rank-bm25`) |
| Reranking | `sentence-transformers` cross-encoder |
| Answer generation | `llama3.1:8b` via Ollama |

## Requirements

- Python 3.11 or later (developed on 3.14)
- [Ollama](https://ollama.com/download)
- [Docker](https://www.docker.com/products/docker-desktop/), to run Qdrant
- About 8 GB of free disk space for the models and dependencies

## Setup

**1. Get the models** (about 5 GB in total):

```bash
ollama pull nomic-embed-text
ollama pull llama3.1:8b
```

**2. Start Qdrant:**

```bash
docker run -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

**3. Start the backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API runs on http://localhost:8000, with interactive documentation at http://localhost:8000/docs. The first start downloads the reranking and PDF-parsing models, so it takes a few minutes.

**4. Start the frontend**, in a second terminal:

```bash
cd frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501.

## Using it

1. Choose a PDF in the sidebar and click **Upload**. Indexing a long document takes a minute or two.
2. Ask a question in the chat box.
3. Open the expanders under an answer to read the passages it was based on.
4. **New Chat** starts a fresh conversation. **Del** removes a document from the index.

## API

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/upload/` | Upload and index a PDF |
| `POST` | `/chat/` | Ask a question (`question`, `session_id`) |
| `GET` | `/document/` | List indexed documents |
| `DELETE` | `/document/{document_id}` | Remove a document from the index |

## Project structure

```
backend/
  main.py        FastAPI application
  api/           HTTP routes: upload, chat, document
  ingestion/     PDF chunking and embedding
  db/            Qdrant storage
  retrieval/     vector search, keyword search, merging, reranking
  rag/           question-answering pipeline
  llm/           call to the chat model
  memory/        conversation history
frontend/
  app.py         Streamlit interface
```

## Current limitations

- Only PDF files are supported.
- Conversation history is kept in memory and is lost when the backend restarts.
- There are no user accounts: everyone using the same backend shares the same documents.
- Keyword search reads every stored chunk on each question, which is fine for a handful of documents but slow for large collections.
- Answer speed depends on your hardware, since the model runs locally.
