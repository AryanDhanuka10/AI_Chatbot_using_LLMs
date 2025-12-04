#!/usr/bin/env bash
set -e

# load .env if present (makes it easier inside container)
if [ -f /app/.env ]; then
  export $(grep -v '^#' /app/.env | xargs)
fi

# Optional: prebuild or seed RAG index if script exists
if [ -n "$RAG_SEED_PATH" ] && [ -f "$RAG_SEED_PATH" ]; then
  echo "[entrypoint] seeding RAG from $RAG_SEED_PATH"
  python -c "from src.rag.rag_pipeline import RAGPipeline; rp=RAGPipeline(); rp.build_store_from_pdf('$RAG_SEED_PATH'); import pickle; pickle.dump(rp.store, open('/app/rag_index/store.pkl','wb'))" || true
fi

# Run gunicorn with uvicorn workers
exec gunicorn src.api.server:app \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --workers ${GUNICORN_WORKERS:-2} \
  --timeout ${GUNICORN_TIMEOUT:-120}
