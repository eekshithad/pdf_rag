# Local PDF RAG & Document Assistant

A privacy-focused, local Retrieval-Augmented Generation (RAG) application built to perform accurate, hallucination-resistant Q&A over PDF documents without sending data to third-party APIs.

The system runs entirely on-premise using **LangChain**, **ChromaDB**, **Ollama**, and **Sentence Transformers**, making it suitable for secure enterprise environments, confidential document review, and local network (LAN) deployments.

---

## Key Features

- **100% Local & Privacy-Preserving:** All vector embeddings and LLM inference run on-premise using Ollama (`nomic-embed-text` and `llama3.1`). No cloud APIs or data leakage.
- **Two-Stage Retrieval Pipeline:** Combines dense vector similarity search in ChromaDB with a Cross-Encoder reranker (`BAAI/bge-reranker-base`) to score semantic relevance and prioritize the most accurate context.
- **Strict Grounding & Hallucination Prevention:** Context-locked prompt templates force the model to answer strictly from retrieved document snippets, returning fallback notices when information is missing.
- **Incremental Index Tracking:** Uses a local index registry (`indexed_files.json`) to track processed documents and page counts, preventing redundant re-embeddings.
- **Report Generation Agent:** Dedicated agent workflow (`ReportAgent`) that queries the document store, reranks sources, and exports formatted `.docx` summary reports with page citations.
- **Local Network (LAN) Ready:** Streamlit-powered user interface that can be hosted on a local subnet for shared team access over Wi-Fi.

---

## Architecture & Workflow

```text
[PDF Upload] 
     │
     ▼
[PyMuPDF Loader] ──► [Recursive Text Splitter] (chunk_size=800, overlap=150)
     │
     ▼
[Ollama nomic-embed-text] ──► [ChromaDB Vector Store]
                                       │
[User Query] ──────────────────────────┤
                                       ▼
                     [Dense Vector Search (Top-20)]
                                       │
                                       ▼
              [Cross-Encoder Reranker: bge-reranker-base]
                                       │
                                       ▼ (Top-4 Chunks)
                      [System Prompt + Context Assembly]
                                       │
                                       ▼
                       [ChatOllama: llama3.1 / mistral]
                                       │
                                       ▼
                         [Grounded Answer / DOCX Report]
```

---

## Project Structure

```text
├── agents/
│   └── report.py              # Autonomous report generation agent
├── rag/
│   ├── embeddings.py          # Ollama embedding configuration
│   ├── llm.py                 # ChatOllama model interface
│   ├── prompt.py              # Context-grounded prompt templates
│   ├── reranker.py            # BGE cross-encoder reranking module
│   ├── retriever.py           # ChromaDB search & candidate retrieval
│   └── vectorstore.py         # ChromaDB persistence & document loader
├── services/
│   └── report_service.py      # DOCX export and synthesis service
├── utils/
│   ├── chunker.py             # Document splitting utilities
│   ├── index_tracker.py       # JSON-based incremental ingestion tracker
│   ├── metadata.py            # Document metadata enrichment
│   └── pdf_loader.py          # PyMuPDF batch directory loader
├── app.py                     # Streamlit web interface
├── ingest.py                  # Batch ingestion CLI pipeline
├── rag.py                     # Direct CLI query script
├── config.py                  # Centralized configuration variables
└── requirements.txt           # Project dependencies
```

---

## Tech Stack

- **Framework:** LangChain, LangChain-Ollama, LangChain-Chroma
- **Vector Database:** ChromaDB
- **Embedding Model:** `nomic-embed-text` (via Ollama)
- **Reranker:** `BAAI/bge-reranker-base` (Cross-Encoder / Sentence Transformers)
- **LLM:** `llama3.1` (or `mistral` via Ollama)
- **Document Parsing:** PyMuPDF (`fitz`)
- **Frontend / UI:** Streamlit
- **Document Generation:** `python-docx`

---

## Getting Started

### 1. Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally.

Pull the required models in Ollama:
```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

### 2. Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/eekshithad/pdf_rag.git
cd pdf_rag

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

---

## Usage

### Option A: Streamlit Web UI (Recommended)
Run the interactive application:
```bash
streamlit run app.py
```
To expose the app across your local Wi-Fi or LAN network:
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### Option B: Batch Document Ingestion
Place your PDF files into the `uploads/` folder and run the ingestion pipeline:
```bash
python ingest.py
```
This parses new PDFs, chunks the text, creates embeddings, updates ChromaDB, and records indexed files in `data/indexed_files.json`.

### Option C: CLI Querying
Run queries against the existing ChromaDB store directly from your terminal:
```bash
python rag.py
```

---

## Configuration

Adjust chunking, retrieval parameters, and models in `config.py`:

```python
UPLOAD_FOLDER = "uploads"
CHROMA_DB_PATH = "chroma_db"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.1"

TOP_K = 20          # Initial candidate retrieval
RERANK_TOP_K = 4    # Final reranked context count
```

---

## License

MIT License. Feel free to use and adapt for your own document workflows.
