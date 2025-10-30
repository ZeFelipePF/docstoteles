DocstoTeles

RAG (Retrieval-Augmented Generation) sample application built with Streamlit and LangChain to allow searching and chatting over collections of Markdown documents.

## Description

This project lets you import document collections (markdown .md files) as a vector index and ask questions using an LLM (via Groq). It's designed for local experimentation: scraping/importing documents, creating embeddings, and similarity search to answer questions with context.

Main components:
- Web UI: Streamlit (`docstoteles/app.py`).
- RAG service: `docstoteles/service/rag.py` (loads collections, creates embeddings, produces answers).
- Document loading: `langchain_community.document_loaders.DirectoryLoader` (markdown files).

## Features

- Load local Markdown collections (folder `data/collections/<name>`).
- Create embeddings with HuggingFace (`sentence-transformers`) and store them with FAISS.
- Ask questions (chat) with context retrieval (RetrievalQA).

## Technologies

- Streamlit — web UI and rapid prototyping.
- LangChain (`langchain-core`, `langchain-community`, `langchain-huggingface`) — RAG orchestration.
- HuggingFace / sentence-transformers — embedding generation (model `all-MiniLM-L6-v2`).
- FAISS — local vector indexing and search.
- Firecrawl — scraping/ingestion integration (optional API used by the scrapping service).
- Groq (`langchain-groq`) — LLM provider used for generation.
- Python 3.11+ — recommended runtime.

## Requirements

- Python 3.11+ (tested with 3.13 in a local venv).

Key dependencies (see also `requirements.txt`):
- streamlit
- langchain and related packages
- sentence-transformers
- faiss-cpu (or faiss-gpu if you have compatible CUDA)
- langchain-groq (to use Groq API)

## Installation (Windows PowerShell)

1. Clone the repo and cd into it:

```powershell
cd C:\path\to\chat_with_rag
```

2. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Upgrade pip and install requirements:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Additional packages sometimes required:

```powershell
python -m pip install sentence-transformers
python -m pip install faiss-cpu
python -m pip install langchain-huggingface
```

## Environment variables

Create a `.env` file in the repo root (or export variables). Minimal example:

```properties
FIRECRAWL_API_URL=http://localhost:3002
FIRECRAWL_API_KEY=
GROQ_API_KEY=your_groq_api_key_here
```

## How to run

```powershell
streamlit run docstoteles/app.py
```

Open http://localhost:8501 in your browser.

## Troubleshooting

- If you get `ImportError: Could not import sentence_transformers`, install `sentence-transformers`.
- If you get `ImportError: Could not import faiss`, install `faiss-cpu` (or `faiss-gpu` for CUDA).
- If a Groq model is decommissioned, change `model_name` in `docstoteles/service/rag.py` to an active model (e.g., `groq/compound`).

## Contributing

1. Fork the repo, create a branch, open a Pull Request.

---

