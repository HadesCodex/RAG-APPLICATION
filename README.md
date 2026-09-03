# Enterprise Agentic RAG

An agentic Retrieval-Augmented Generation system built with **LangGraph**, **FastAPI**, and **Qdrant**, featuring input/output guardrails, an LLM gateway with automatic fallback, and a RAGAS-based evaluation suite.

## Architecture

```
Streamlit Chat UI → FastAPI /query → NeMo Guardrails → LangGraph Agent
                                                          ├─ Planner (intent classification)
                                                          ├─ Retriever → Qdrant + FlashRank rerank
                                                          └─ Responder → Portkey Gateway → Groq (Llama 3.3 70B, fallback 3.1 8B)
```

Documents are parsed (PDF / HTML / DOCX / PPTX / TXT) → chunked → embedded with Gemini embeddings → indexed in Qdrant Cloud. Every request is traced with Pydantic Logfire and LangSmith. See `ARCHITECTURE.md` for the full diagram.

## Features

- **Agentic pipeline** — LangGraph state machine with Planner, Retriever, and Responder nodes, plus conversation memory (`MemorySaver`).
- **Guardrails** — NeMo Guardrails blocks off-topic queries, jailbreak attempts, and PII/secret leakage before they reach the agent.
- **LLM Gateway** — Portkey routes requests to Groq with automatic fallback, retries, and caching.
- **Retrieval** — Qdrant vector search with FlashRank local reranking.
- **Evaluation** — RAGAS metrics (faithfulness, relevancy, precision, recall, correctness) plus guardrail and tool-correctness tests against a golden dataset, run through a dedicated Streamlit eval app.
- **Observability** — Logfire spans + LangSmith traces across ingestion, retrieval, and generation.

## Project Structure

```
app/
├── agents/          # LangGraph graph, state, and nodes (planner, retriever, responder)
├── gateway/          # Portkey LLM gateway client
├── guardrails/        # NeMo Guardrails config and rails
├── ingestion/         # Document loaders, chunking, and processing pipeline
├── services/retrieval/  # Embeddings, Qdrant service, reranking
├── config.py          # Settings loaded from environment variables
└── main.py            # FastAPI app (/query, /graph endpoints)

evals/                 # RAGAS + guardrails evaluation pipeline and Streamlit app
ui/                    # Streamlit chat interface
notebooks/             # Exploratory notebooks (guardrails, gateway, evals)
processed_data/        # Locally cached parsed/chunked document JSON
```

## Setup

1. **Clone and install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables** — create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=
   GROQ_FALLBACK_API_KEY=
   PORTKEY_API_KEY=
   QDRANT_CLUSTER_ENDPOINT=
   QDRANT_API_KEY=
   GEMINI_API_KEY=
   LOGFIRE_TOKEN=
   ```
   `.env` is gitignored — never commit real keys.

3. **Ingest documents** — place source files under your input directory and run the ingestion pipeline (`app/ingestion/processor.py`) to parse, chunk, embed, and index them into Qdrant.

## Running

**API**
```bash
uvicorn app.main:app --reload
```
- `GET /` — health check
- `POST /query` — `{"q": "your question", "thread_id": "optional"}`
- `GET /graph` — PNG of the LangGraph agent workflow

**Chat UI**
```bash
streamlit run ui/app.py
```

**Evaluation dashboard**
```bash
streamlit run evals/app.py
```
Runs RAGAS metrics and guardrail tests against `evals/golden_dataset.json`.

## Tech Stack

Python · FastAPI · LangGraph · LangChain · Qdrant · FlashRank · Gemini Embeddings · Groq (Llama 3.3 70B) · Portkey · NeMo Guardrails · RAGAS · Logfire · LangSmith · Streamlit
