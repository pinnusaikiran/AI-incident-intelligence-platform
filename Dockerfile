FROM python:3.12-slim

# System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first for Docker layer caching
COPY requirements.txt .

# CPU-only PyTorch for CPU deployment
RUN pip install --no-cache-dir \
    torch==2.11.0 \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining application dependencies   
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source and runtime resources
COPY api/ ./api/
COPY src/ ./src/
COPY rag/ ./rag/
COPY rag_data/ ./rag_data/
COPY artifacts/ ./artifacts/

# Create non-root application user
RUN useradd \
        --create-home \
        --shell /bin/bash \
        appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Container health check
HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=30s \
    --retries=3 \
    CMD python -c \
    "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" \
    || exit 1

# Start FastAPI
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]