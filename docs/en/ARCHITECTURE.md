# Architecture and system contracts

> BundleRecommender — Day 20/100 · Research documentation, not production certification.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Components and data flow

`notebooks/bundlerecommender.ipynb` is the offline experiment; Instacart `product_id` and UCI `StockCode` are unrelated namespaces. Offline outputs are written to `models/`, `reports/`, `assets/plots/`, and `exports/`. FastAPI never retrains at request time: it loads CSV rules, matches antecedents against the selected basket, and returns consequents with support, confidence, lift, and source information. React lets users choose a dataset, find products, submit a basket, inspect evidence, and export JSON.

## API contracts

- `GET /api/v1/health`: server/artifact presence, **not** model-quality certification.
- `GET /api/v1/catalog?dataset=instacart|uci`: identifiers represented in mined rules.
- `GET /api/v1/catalog/details?dataset=uci`: optional human-readable descriptions while retaining SKU keys.
- `POST /api/v1/recommend`: `{"dataset":"uci","items":["20719"],"limit":8}`. `items` must use underlying identifiers, not display names.

A basket with no matched rules yields no suggestions, not a fabricated fallback. Local CORS currently permits Vite development origins. Avoid mixing UCI StockCodes and Instacart IDs.

## Engineering hazards

Missing artifacts, malformed rule columns, lost package entrypoints from replacing whole directories, absent CSS, and stale catalogs are operational risks. Preserve bootstrap entrypoints and test both domains after changing parsing or display code. No online personalization or real-time training is implemented.
