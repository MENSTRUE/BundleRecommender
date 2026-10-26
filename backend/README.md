# Backend — BundleRecommender Research API

FastAPI serves **persisted rule CSV artifacts**. It does not train or download models per request. Scope: local non-personalized association-rule suggestions, with optional names for UCI StockCode metadata.

## Modules

- `app/main.py`: FastAPI application and localhost CORS.
- `app/api/routes.py`: health, catalog, catalog details and recommend endpoints.
- `app/core/config.py`: repository-aware paths; environment overrides `BR_MODEL_DIR`, `BR_EXPORT_DIR`.
- `app/schemas/recommendation.py`: Pydantic request and output schema.
- `app/services/rules.py`: loads native Instacart/UCI rules, finds matching antecedents, ranks consequents; no fake fallback.
- `app/services/product_names.py`: optional UCI SKU → source-derived Description mapping.
- `tests/test_product_names.py`: three current metadata mapping regression tests. Broader `test_api.py` was removed from current repository; restore in next update.

## Run — Windows PowerShell

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

API docs: `http://127.0.0.1:8000/docs`.

## Endpoints and examples

- `GET /api/v1/health` — availability indicator, not validation.
- `GET /api/v1/catalog?dataset=instacart` — product catalog identifiers.
- `GET /api/v1/catalog/details?dataset=uci` — description metadata for UCI.
- `POST /api/v1/recommend` — request example:

```json
{"dataset":"uci","items":["20719"],"limit":8}
```

Response includes `suggestions`, `matched_rules`, `scanned_rules`, item IDs, source CSV, historical `support/confidence/lift` and a non-causal disclaimer. If no rule matches, don't invent results. Dataset namespaces must remain distinct.

## Failure modes / safe fixes

- `No module named app.main`: check `app/main.py`, don't reinstall everything.
- Missing `app.schemas`: inspect `app/schemas/recommendation.py`.
- Unsupported CSV columns: Instacart has native `antecedent_id/consequent_id`; UCI uses `antecedent_sku/consequent_sku`.
- Missing UCI descriptions: CSV may be absent; display SKU instead.
- Missing rule artifacts: verify actual `models/` path.
- Starlette deprecation warning from HTTPX: nonblocking for documented local tests; revisit pinned compatible dependencies deliberately.

## Deployment boundary

The server currently uses local-dev CORS settings. Before public deployment, add authentication/abuse controls as needed, input/resource limits, rate limits, observability, secure secret management and a license/PII review. See [deployment](../docs/en/DEPLOYMENT.md) and [agent contract](../AGENTS.md).
