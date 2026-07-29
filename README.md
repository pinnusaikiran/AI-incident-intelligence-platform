# AI Incident Intelligence Platform

A production-ready FastAPI application for predicting IT Incident SLA breaches using a trained CatBoost machine learning model with SHAP-based explainability.

---

## Features

- FastAPI REST API
- CatBoost ML model
- SHAP explainability
- Custom feature engineering
- Structured logging
- Global exception handling
- Request ID middleware
- Dependency Injection
- Health endpoint
- OpenAPI/Swagger documentation

---

## Project Structure

```
api/
src/
artifacts/
tests/
```

---

## Installation

```bash
git clone <repository-url>

cd AI-incident-intelligence-platform

pip install -r requirements.txt
```

---

## Run the API

```bash
uvicorn api.main:app --reload
```

---

## Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## Health Check

```
GET /health
```

---

## Prediction Endpoint

```
POST /predict
```

---

## Technologies

- Python
- FastAPI
- CatBoost
- SHAP
- Scikit-learn
- Pandas
- NumPy

---

## Author

Sai Kiran