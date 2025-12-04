# Stage 1: builder - install dependencies
FROM python:3.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for FAISS, PDF, and typical ML libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    wget \
    poppler-utils \
    libopenblas-dev \
    libomp-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Stage 2: runtime
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# copy system-level libs from builder (helpful for compiled pip packages)
COPY --from=builder /usr/lib /usr/lib
COPY --from=builder /usr/local /usr/local

# app code
COPY . /app

# make entrypoint executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD curl -f http://127.0.0.1:8000/health || exit 1

# run server with gunicorn + uvicorn workers
CMD ["/app/entrypoint.sh"]
