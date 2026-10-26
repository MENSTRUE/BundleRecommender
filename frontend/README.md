# Frontend — BundleRecommender Research Workspace

React 18, TypeScript, Vite, Lucide icons. Single-page local interface for selecting Instacart or UCI rules, adding products to a basket, viewing rule-backed suggestions, reading support/confidence/lift and downloading JSON.

## Structure

- `src/main.tsx`: React entry, imports `styles/main.css`.
- `src/pages/Workspace.tsx`: dataset selector, catalog search, basket, recommendation results, metadata display, export.
- `src/components/Metric.tsx`: summary stat card.
- `src/services/api.ts`: typed HTTP fetch and errors; base URL from `VITE_API_BASE_URL`.
- `src/types/api.ts`: shared frontend response types.
- `src/styles/main.css`: original UI layout; `src/styles/product-names.css`: name/SKU styles.
- `src/vite-env.d.ts` (or existing Vite client typing): `import.meta.env` definitions.

## Local commands

```powershell
cd frontend
npm ci
npm run build
npm run dev
```

Visit `http://127.0.0.1:5173`. Backend required at `http://127.0.0.1:8000` by default. Copy `.env.example` to `.env` only if a non-default API origin is needed; do not commit credentials.

## Demo validation

1. Set **Instacart**, use a product shown in rule catalog, run suggestions and verify metrics.
2. Switch to **UCI**; search for `WOODLAND CHARLOTTE BAG` or SKU `20719` if present, observe display label while submission uses SKU.
3. Download JSON and verify raw product identifiers and rule metrics.
4. Confirm no matching rule yields an empty result with a human-readable notice.
5. Capture a screenshot only after data shown matches an actual API response.

## Known limitations

No accounts, stock availability, transactions, conversion tracking, personalization or real deployment. Displayed associations are historical and do not imply purchases or revenue gains. See [limitations](../docs/en/LIMITATIONS.md).

## Troubleshooting

`Cannot find module ../components/Metric`: restore `src/components/Metric.tsx`. `Failed to load src/main.tsx`: verify entrypoint. `Could not resolve ./styles/main.css`: restore CSS. `Property env does not exist on ImportMeta`: ensure Vite typings. Do not replace the whole `frontend/` directory during fixes; it previously deleted critical files.
