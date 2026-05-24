# Multilingual Retrieval and Reasoning Research

This project is a reproducible web app and research platform for studying how
multilingual and morphologically rich languages behave in retrieval-augmented
generation systems.

The initial focus is English and Turkish, with special attention to agglutinative
morphology, cross-lingual retrieval, tokenization effects, embedding choices, and
retrieval-induced reasoning errors.

## Research Question

How do multilingual embedding and retrieval systems perform on morphologically rich
agglutinative languages under cross-lingual retrieval conditions, and how does
retrieval quality affect downstream LLM reasoning?

## What Is Included

- FastAPI backend
- Browser-based experiment console
- Multilingual document ingestion
- Semantic retrieval pipeline
- Deterministic local embedding baseline for reproducibility
- Retrieval evaluation metrics: recall@k and mean reciprocal rank
- Tokenization/morphology probe for Turkish suffix-like patterns
- Docker-ready deployment skeleton

## Live Deployment

The app is deployed on Render as a Docker-backed web service.

- Frontend experiment console: served from `/`
- Backend API: served from `/api`
- Interactive API docs: served from `/docs`
- Health check: served from `/api/health`

Render builds the repository's `Dockerfile` and starts the FastAPI app with
Uvicorn. The container binds to Render's `PORT` environment variable in
production and falls back to port `8000` locally.

Current deployment environment:

```text
APP_ENV=production
EMBEDDING_BACKEND=hashing
VECTOR_BACKEND=memory
```

Because the current vector store is in memory, documents indexed through the web
UI are temporary. They may disappear when the Render service restarts or wakes
from inactivity. Persistent storage is planned for later experiments.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Run Tests

```bash
pytest
```

## Docker

```bash
docker compose up --build
```

## API Sketch

- `POST /api/documents`: index a multilingual document
- `POST /api/query`: retrieve context and generate a context-grounded answer
- `POST /api/evaluate/retrieval`: compute retrieval metrics over labeled cases
- `POST /api/experiments/tokenization`: inspect token-level properties
- `GET /api/health`: service health check

## Experiment Roadmap

1. Compare embedding models:
   - deterministic hashing baseline
   - multilingual Sentence Transformers
   - OpenAI embeddings
2. Compare chunking strategies:
   - word windows
   - sentence windows
   - morphology-aware segmentation
3. Evaluate retrieval:
   - monolingual English
   - monolingual Turkish
   - English query to Turkish document
   - Turkish query to English document
4. Evaluate reasoning:
   - answer faithfulness
   - context attribution
   - hallucination rate by language pair
5. Publish reproducible benchmark datasets and experiment configs.

## Current Baseline

The default `EMBEDDING_BACKEND=hashing` is intentionally lightweight. It makes the
app runnable in any environment without network access or model downloads. For real
experiments, switch to a multilingual model, for example:

```bash
EMBEDDING_BACKEND=sentence-transformers:sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Install ML dependencies first:

```bash
pip install -e ".[ml,dev]"
```
