# Current App Snapshot

This document describes how the app works at this stage of the project. It is
intended as a reference point for future changes, when the retrieval pipeline,
frontend, persistence layer, and reasoning components have evolved.

Snapshot date: 2026-05-24

## Current Purpose

The app is a deployed prototype for multilingual retrieval-augmented generation
research. It lets a user:

- ingest English or Turkish documents,
- query the indexed documents,
- inspect retrieved chunks and similarity scores,
- run a simple tokenization/morphology probe,
- and access the system through a browser-hosted research console.

The app is deployed on Render as a Docker-backed FastAPI service. The frontend is
served by the same FastAPI app.

## High-Level Architecture

```text
Browser UI
  |
  | JSON requests
  v
FastAPI routes
  |
  v
RagPipeline
  |
  +--> chunking
  +--> embedding
  +--> in-memory vector store
  +--> simple context-based answer generation

Tokenization endpoint
  |
  v
regex-based token and suffix-like pattern analysis
```

## Frontend

The frontend is a static browser interface stored in:

```text
app/web/index.html
app/web/styles.css
app/web/app.js
```

It is served by FastAPI from the root route:

```text
GET /
```

The frontend currently has three main panels:

- Document Ingestion
- Cross-Lingual Query
- Tokenization Probe

The JavaScript file `app/web/app.js` listens for form submissions, converts form
values into JSON payloads, sends them to the backend with `fetch`, and prints the
JSON response into the page.

There is no frontend framework yet. The app does not currently use React, Next.js,
Vue, Svelte, or client-side routing.

## Backend

The backend is a FastAPI app defined in:

```text
app/main.py
```

The API routes are defined in:

```text
app/api/routes.py
```

Current endpoints:

```text
GET  /api/health
POST /api/documents
POST /api/query
POST /api/evaluate/retrieval
POST /api/experiments/tokenization
GET  /
HEAD /
```

The `HEAD /` route exists so Render health checks do not produce a `405 Method
Not Allowed` response.

## Document Ingestion

The document ingestion form sends data to:

```text
POST /api/documents
```

The expected payload shape is represented by `DocumentInput` in:

```text
app/core/schemas.py
```

The payload contains:

```text
doc_id
text
language
title
metadata
```

The route calls:

```python
pipeline.ingest(document)
```

The ingestion logic lives in:

```text
app/rag/pipeline.py
```

The ingestion process is:

1. Split the document into chunks with `chunk_text`.
2. Embed each chunk with the configured embedding model.
3. Store chunks and vectors in the vector store.
4. Return the number of indexed chunks.

## Chunking

Chunking is implemented in:

```text
app/rag/chunking.py
```

The current chunking strategy is word-window chunking:

```text
max_words = 120
overlap_words = 20
```

This means a long document is split into windows of up to 120 words. Consecutive
windows overlap by 20 words.

This is intentionally simple. It is not sentence-aware, paragraph-aware,
language-aware, or morphology-aware yet.

## Embeddings

Embeddings are implemented in:

```text
app/rag/embeddings.py
```

The default backend is:

```text
EMBEDDING_BACKEND=hashing
```

The hashing embedding model is deterministic and local. It:

1. tokenizes text with a Unicode word regex,
2. hashes each token,
3. maps the token to a vector bucket,
4. adds or subtracts from that bucket,
5. normalizes the final vector.

This is not a neural embedding model. It is a lightweight baseline so the app can
run without API keys, downloads, GPUs, or external model hosting.

The code already includes a hook for Sentence Transformers:

```text
EMBEDDING_BACKEND=sentence-transformers:<model-name>
```

However, using Sentence Transformers requires installing the optional ML
dependencies.

## Vector Store

The vector store is implemented in:

```text
app/rag/vector_store.py
```

The current vector store is `InMemoryVectorStore`.

It stores:

```python
self._chunks
self._vectors
```

inside the running Python process.

Search is performed by taking the dot product between the query vector and stored
document vectors:

```python
scores = self._vectors @ query_vector.reshape(-1)
```

The vectors are normalized, so this behaves like cosine similarity for the
current embedding backend.

Important limitation: this storage is temporary. Documents indexed through the UI
can disappear when:

- the Render service restarts,
- the service redeploys,
- the free service sleeps and wakes,
- or the Python process otherwise resets.

There is no persistent vector database yet.

## Cross-Lingual Query

The query form sends data to:

```text
POST /api/query
```

The expected payload shape is represented by `QueryInput` in:

```text
app/core/schemas.py
```

The payload contains:

```text
query
language
top_k
```

The query route calls:

```python
pipeline.query(request)
```

The query process is:

1. Embed the user query.
2. Search the in-memory vector store.
3. Retrieve the top `k` chunks.
4. Wrap retrieved chunks in response schemas.
5. Generate a simple answer from retrieved context.

Although the UI calls this panel "Cross-Lingual Query", the current default
hashing embedding model is not a true multilingual semantic embedding model.
Real cross-lingual behavior will require a multilingual embedding model such as a
Sentence Transformers model or an external embedding API.

## Reasoning

Reasoning is implemented in:

```text
app/rag/reasoning.py
```

The current reasoner is `ContextualReasoner`.

It does not call an LLM yet. Instead, it creates a simple answer by concatenating
the first retrieved contexts and returning a template-style response:

```text
Based on the retrieved context...
```

This is a placeholder for future LLM-based reasoning. It is useful right now
because it keeps the app deterministic and free to run.

## Tokenization Probe

The tokenization form sends data to:

```text
POST /api/experiments/tokenization
```

The implementation lives in:

```text
app/experiments/tokenization.py
```

The current probe:

1. extracts tokens with a Unicode word regex,
2. counts total tokens,
3. counts unique tokens,
4. computes average token length,
5. checks for a small set of Turkish suffix-like endings.

Current suffix-like endings:

```text
lar
ler
dan
den
daki
deki
imiz
ımız
```

This is not a full Turkish morphological analyzer. It is a simple surface-form
probe that gives the project a starting point for morphology-aware experiments.

## Retrieval Evaluation

Retrieval evaluation is implemented in:

```text
app/evaluation/retrieval.py
```

The endpoint is:

```text
POST /api/evaluate/retrieval
```

It accepts evaluation cases with:

```text
case_id
query
language
relevant_doc_ids
notes
```

It computes:

```text
recall_at_k
mean_reciprocal_rank
cases_evaluated
```

There is no frontend panel for this endpoint yet, but it is available through the
API and the interactive docs at:

```text
/docs
```

## Configuration

Configuration is handled in:

```text
app/core/config.py
```

The example environment variables are in:

```text
.env.example
```

Current deployed configuration:

```text
APP_ENV=production
EMBEDDING_BACKEND=hashing
VECTOR_BACKEND=memory
OPENAI_MODEL=gpt-4.1-mini
```

`OPENAI_API_KEY` exists as a future configuration option, but the current app does
not require it.

## Deployment

The app is deployed on Render using Docker.

Docker files:

```text
Dockerfile
docker-compose.yml
```

The Docker container starts the app with Uvicorn:

```text
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

Render provides the `PORT` environment variable in production. Local Docker runs
fall back to port `8000`.

## Current Limitations

- Indexed documents are not persistent.
- There is no authentication.
- Anyone with the public URL can add documents to the shared in-memory index.
- The default embedding model is a deterministic hashing baseline, not a neural
  multilingual embedding model.
- The "reasoning" step is template-based and does not call an LLM yet.
- The tokenization probe is regex-based and not a full morphological analyzer.
- There is no experiment history or saved benchmark result store.
- The evaluation endpoint exists, but there is no frontend evaluation dashboard.

## Good Next Steps

- Add persistent vector storage with Qdrant, Chroma, Postgres/pgvector, or
  another durable backend.
- Add a real multilingual embedding model.
- Add OpenAI or another LLM provider for context-grounded reasoning.
- Add dataset IDs so different users or experiments do not share one global
  in-memory index.
- Add an evaluation dashboard.
- Add saved experiment runs and downloadable results.
- Add authentication or a read-only public demo mode.

