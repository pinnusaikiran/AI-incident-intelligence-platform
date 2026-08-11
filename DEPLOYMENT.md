# AI Incident Intelligence Platform
# Deployment Guide

This document describes how to run, test, build, and deploy the AI Incident
Intelligence Platform locally and using Docker.

The application provides:

- SLA breach prediction using CatBoost
- SHAP-based model explainability
- RAG-based incident knowledge retrieval
- LLM-powered incident assistance
- Combined incident intelligence analysis
- FastAPI REST API
- Docker-based deployment
- Automated CI testing and Docker smoke testing

---

# 1. Prerequisites

## Local Development

Required:

- Python 3.12
- Virtual environment or Conda environment
- Git

The project has been validated with:

- Python 3.12
- pytest 9.x

## Docker Deployment

Required:

- Docker
- Docker Compose

The production container uses:

- Python 3.12
- CPU-only PyTorch
- FastAPI
- CatBoost
- SHAP
- Sentence Transformers

---

# 2. Project Runtime Artifacts

The following model artifacts are required:

```text
artifacts/
└── models/
    ├── catboost_native_pipeline.joblib
    ├── final_catboost_native.joblib
    └── metadata.json