# oikos-api

FastAPI service exposing listings collected by `oikos-scrapper`.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
uvicorn app.main:app --reload
```

## Endpoints

- `GET /health`
- `GET /api/listings`
- `GET /api/listings/{listing_id}`
- `GET /api/summary`
