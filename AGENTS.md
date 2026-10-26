# AGENTS.md — BundleRecommender Engineering Contract

## Project definition and non-negotiable scope

BundleRecommender (Day 20/100) is an experimental, non-personalized product-basket **association-rule** recommender. Its purpose is to serve and inspect historical product co-occurrence; it does **not** estimate causal uplift, personalized conversion or guaranteed revenue. Maintain parity with `README.md`, `docs/`, current model CSVs, and executed reports. No demo fixtures should ever be silently substituted for missing model artifacts.

## Canonical evidence / source of truth (in descending order)

1. Original notebook run and persisted `models/*.csv`, `reports/*.json`, `reports/*.csv`, hashes in `reports/release_sha256.json`, dataset inventory, split logic.
2. API implementation in `backend/app/` and automated test assertions; actual local run logs.
3. Frontend source, validated browser demos, tracked `assets/screenshots/`.
4. This document and README; edit prose if inconsistent with measured artifacts, never the other way round.

**Current source state:** main app has Instacart and UCI rule CSVs, UCI product name metadata and audit. Current backend tests include `test_product_names.py` (3 tests in user-provided latest run); the older `test_api.py` is deleted. No false claims about ongoing or restored coverage.

## Before → Now → Next

- **Before:** scaffolding, dataset selection, notebooks and rule mining.
- **Now:** 13 Instacart rules, 150 UCI rules, optional UCI name lookup 46/46 SKU; local FastAPI + React demos, no online deployment.
- **Next:** restore API regression suite; run clean-install integration tests; build honest eval dashboard; strengthen input/cache and provenance checks; plan secure optional deployment.

## Critical invariants

- Keep **Instacart and UCI namespaces distinct**. Never match product IDs or join data across these datasets.
- UCI API basket inputs and rule matching use **StockCode** strings, not descriptions. Descriptions are optional display metadata, from the source-derived CSV only; fallback to SKU for unknown names.
- Never invent SKU descriptions or association metrics. Never auto-populate fabricated mock recommendations when CSV absent or mismatch.
- Preserve `support`, `confidence`, `lift`, `matched_input`, `scanned_rules`, `matched_rules`, source file metadata; don't confuse rule score with price, purchase probability, recommendation precision or causal effect.
- No test/training leakage: Instacart later-order holdout and UCI last-20%-by-date invoices are for evaluation only. No tuning on final holdout without defining fresh test set.
- Protect PII, raw transaction rows, secrets and third-party dataset/license obligations. Do not add raw data or checkpoints to Git.
- A green `Artifact available` badge only confirms a file exists; it does not validate semantic quality, user outcome, production uptime or full artifact hashes.

## Work safely in the existing repository

- **Never replace whole `backend/` or `frontend/` directories** during updates. Previous replacements accidentally removed `backend/app/main.py`, `app/api/routes.py`, `app/services/rules.py`, `frontend/src/main.tsx`, `frontend/src/components/Metric.tsx`, `frontend/src/styles/main.css`.
- Patch narrowly, respect uncommitted changes and use `git status --short` before and after. No `git restore .`, blind `git clean -fd`, `git push --force`, or whole-directory ZIP overwrites.
- For Python modules keep proper `__init__.py` where needed; ensure `from app.main import app` works from `backend/`.
- For frontend keep `frontend/src/main.tsx` importing `./styles/main.css` and `Workspace`; TS `import.meta.env` must be typed using Vite client declarations.
- PowerShell commands use one line or the backtick continuation; never give Bash `\` line-continuation with `/kaggle/...` paths in a local Windows terminal.
- Document every file touched and provide **fully formatted, complete files** on request (no 11-line minification). Favor small focused modules, human-readable code and semantic naming.

## Architecture and contracts

- `backend/app/main.py` creates API with CORS for local Vite.
- `backend/app/api/routes.py`: `GET /api/v1/health`, `GET /api/v1/catalog`, `GET /api/v1/catalog/details`, `POST /api/v1/recommend`.
- `backend/app/services/rules.py`: parses both native CSV schemas: Instacart `antecedent_id` and `consequent_id`, UCI `antecedent_sku` and `consequent_sku`, plus backwards-compatible `antecedents` and `consequents` fixtures. Confirm live schema before changing parser.
- `backend/app/services/product_names.py`: optional SKU-description lookup; report unmatched rather than inventing.
- `frontend/src/pages/Workspace.tsx`: controls dataset, product search, basket, recommendations, metrics, exporting result JSON. API types in `frontend/src/types/api.ts` must match backend.
- Exact features not currently implemented must be identified as **planned** rather than called available.

## Guardrails for changes and claims

- Read `models/model_config.json`, `reports/final_summary.json`, `reports/instacart_heldout_metrics.json`, `reports/uci_metrics.json`, `reports/uci_product_catalog_audit.json` before writing metrics. (Catalog audit lives under `models/`, not reports.)
- Instacart: 100,000 train baskets; 25,000 holdout; 13 rules; vocabulary item coverage 0.241269..., median supported holdout confidence 0.228909..., lift 2.419520...
- UCI: 34,264 earlier train invoices; 8,567 later invoices; 150 exported rules; 46 exported SKU IDs with 46 mapped names; research selection reports 100 SKUs. Never conflate.
- Benchmark: FP-Growth 3.67s, Apriori 2.65s, 92 itemsets each **for one experiment only**; do not claim algorithmic speed superiority generally.
- Never claim real-world conversion, causal improvement, sales lift, customer CTR, statistical representativeness, model accuracy, deployment, or personalization absent evidence.

## Verification gate before completion

1. `python -m pytest -v` in `backend` (do not claim unrun tests passed).
2. `python -c "from app.main import app; print(app.title)"` in backend.
3. `npm run build` and `npm run dev` in frontend.
4. Verify all datasets: GET `/api/v1/catalog?dataset=instacart`, GET `/api/v1/catalog/details?dataset=uci`, POST `/api/v1/recommend` with a product *from returned catalog*. Confirm no fake result for unmatched basket.
5. Ensure JSON export includes exact evidence and names are display-only.
6. `git status --short` and `git diff --check`; review deletions. Commit/push only as requested.
7. State **verified, unverified, and blocked** in the final handoff.

## Documentation protocol

- Indonesian and English topics mirror one another (`docs/id`, `docs/en`). Update root README, backend/frontend README and asset references when behavior changes.
- Screenshots `assets/screenshots/new.png`, `new2.png`; plot artifacts live under `assets/plots`. Do not fabricate new screenshots, logos, diagrams or source figure interpretations.
- Third-party attribution: UCI Online Retail II CC BY 4.0; Instacart Kaggle data subject to competition rules. MIT applies only to original code/docs unless other permissions confirmed.

## Failure playbook

| Symptom | First check |
|---|---|
| `No module named app.main` | Existence of `backend/app/main.py`; never reset all files |
| `No module named app.schemas` | `backend/app/schemas/recommendation.py` |
| `Unsupported rule columns` | Actual CSV headers; preserve native schemas |
| Empty search/catalog | HTTP status/details, file availability, product namespace and parser |
| Vite cannot resolve `./styles/main.css` | `frontend/src/styles/main.css` |
| `Property env does not exist on ImportMeta` | Vite types / `vite-env.d.ts` |
| Kaggle source exists but rules file missing | Extract name mapping from current CSV / verified SKU allowlist; no retraining |
| PowerShell `Missing expression after --` | Do not paste Bash multiline command |

## Security / deployment gate

Currently local research app only. Before public hosting add bounded inputs, rate limits, CORS allowlist, logging without personal basket histories, dependency audit, controlled artifacts/hashes, health/readiness checks, automated tests and data-license review. Do not expose local testing endpoints as if public production.

## Completion / commit convention

Every change response must include: rationale, exact edited files, commands to verify, observed outcomes and caveats, and one reasonable commit message. Preferred form `fix(api): ...`, `feat(ui): ...`, `docs: ...`. Never create metrics or screenshot evidence merely to make README impressive.
