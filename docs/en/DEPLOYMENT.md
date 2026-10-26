# Local operation and deployment readiness

> BundleRecommender — Day 20/100 · Research documentation, not production certification.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Local Windows development

Use two terminals from repository root:

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

```powershell
cd frontend
npm ci
npm run build
npm run dev
```

Swagger: `http://127.0.0.1:8000/docs`; UI: `http://127.0.0.1:5173`. Place rule artifacts and optional UCI name metadata in `models/`. `VITE_API_BASE_URL` configures frontend API origin; backend supports `BR_MODEL_DIR` and `BR_EXPORT_DIR`.

## Public deployment gate

No verified public production deployment or container pipeline is present. Before shipping publicly: precise CORS origins, TLS, per-request input limits, rate limits, appropriate health/readiness, logging without customer PII, secure dependency management, immutable artifacts/checksums, integration tests, observability, license audit and no unapproved raw dataset distribution. A local success or green artifact badge does not imply uptime or sales effectiveness.
