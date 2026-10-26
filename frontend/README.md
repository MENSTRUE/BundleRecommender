# Frontend — React + TypeScript + Vite

```powershell
cd frontend
npm install
npm run build
npm run dev
```

Navigate to http://127.0.0.1:5173. Start FastAPI beforehand.

Select a dataset, type product name, add products to basket, and click Generate.
Catalog and recommendation results are requested from the local backend; there are no hard-coded recommendations.

`VITE_API_BASE_URL` defaults to `http://127.0.0.1:8000`. Copy `.env.example` to `.env` to override it.
