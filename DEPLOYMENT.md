# Deployment Guide

## Prerequisites
- Python 3.12 (local run) or Docker (containerized run)
- `artifacts/models/` must be present (contains the trained CatBoost model, preprocessing pipeline, and metadata — already committed in this repo)

## Option A — Local (dev)
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```
Visit http://127.0.0.1:8000/docs

## Option B — Docker (recommended)
```bash
docker build -t incident-intelligence-api .
docker run -d -p 8000:8000 --name incident-api incident-intelligence-api
curl http://localhost:8000/health
```

## Option C — Docker Compose (recommended for local orchestration)
```bash
docker compose up --build -d
docker compose logs -f
docker compose down
```
The compose file mounts `artifacts/` as a read-only volume, so you can swap in a newly trained model without rebuilding the image — just restart the container.

## CI/CD
`.github/workflows/ci.yml` runs on every push/PR to `main`:
1. Installs deps, runs `pytest tests/ -v` (15 tests)
2. Builds the Docker image
3. Runs the container and curls `/health` as a smoke test

## Production checklist (next steps, not yet done)
- [ ] Move `artifacts/models/*.joblib` out of git into S3/artifact registry, pull at build or startup
- [ ] Add `pydantic-settings` for env-var driven config (port, log level, CORS origins)
- [ ] Put behind a reverse proxy / load balancer (nginx, ALB) with TLS
- [ ] Add rate limiting and auth (API key or OAuth) before exposing publicly
- [ ] Wire structured logs to a central sink (ELK/CloudWatch) — `src/logging/logger.py` already gives structured JSON-ish logs, just needs a shipper
- [ ] Add Prometheus metrics endpoint for latency/error-rate monitoring
- [ ] For Kubernetes: Deployment + Service + HPA, with `/health` as both liveness and readiness probe
