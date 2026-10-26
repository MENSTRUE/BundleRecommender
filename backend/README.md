# Backend — FastAPI

Runs real association-rule inference from `models/instacart_rules.csv` or `models/uci_rules.csv`.

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

- `GET /api/v1/health` — artifacts present (not validity of rules).
- `GET /api/v1/catalog?dataset=instacart` — products appearing in local rule CSV.
- `POST /api/v1/recommend` — matched rule consequents, ranked by lift (fallback confidence/support), with evidence.

If CSV schema differs, the service reports its actual column names rather than fabricating output. No recommender quality metric is claimed by this service. `BR_MODEL_DIR` can override the models directory.
