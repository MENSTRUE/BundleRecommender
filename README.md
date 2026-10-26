# BundleRecommender

**Day 20/100 — 100 Days of Projects** · **Research prototype** · **Association-rule product bundling**

> Find products that historically appear together in shopping baskets, with inspectable support, confidence and lift. This is a decision-support demonstration, **not** an online sales-optimization service, personalized recommender or causal uplift estimator.

[Documentation hub](docs/README.md) · [Bahasa Indonesia](docs/id/README.md) · [English](docs/en/README.md) · [Backend](backend/README.md) · [Frontend](frontend/README.md) · [Agent instructions](AGENTS.md)

## Demonstration

![Instacart dashboard and recommendations](assets/screenshots/new.png)

![UCI Online Retail recommendations with mapped product names](assets/screenshots/new2.png)

Screenshots are repository assets (`new.png`, `new2.png`); identify them by what is visible, not by asserting an unverified capture date or claiming benchmarks from UI images. The application displays **rule-backed suggestions**, a selected basket, and research notices. If screenshot contents change, update the captions as well.

## Problem, deliverable, and scope

A merchant may want interpretable candidates for product bundles or cross-selling. The question here is narrower: **which product pairs co-occurred in historical training baskets**, and do such associations persist when assessed on held-out baskets? Association rules are transparent and inexpensive to serve from CSV. They do **not** establish that presenting these items together will increase conversions or profit.

The delivered code has a FastAPI adapter for real rule CSVs, a React/TypeScript research dashboard, two non-overlapping product namespaces (Instacart grocery products and UCI retail StockCodes), browser-side JSON export, and UCI StockCode → Description lookup built from original records. There is **no remote deployed product, A/B test, or real-time learning**.

## Before → Now → Next

| Stage | Meaning | Evidence |
|---|---|---|
| Before | Repository scaffold, empty app/documentation, selected transactional datasets | Commit history; initial README |
| Now | Working Instacart and UCI rule-backed local demos; local API and UI; UCI names 46/46; exploratory offline reports | `models/`, `reports/`, screenshots, backend tests, local build logs |
| Next | Restore wider API regression suite, rerun from clean checkout, stress-test absent rules, provenance/license audit, evaluate on additional time windows, add observability and deployment safeguards | [Roadmap](docs/en/ROADMAP.md) |

## Datasets and source rights

| Dataset | Source | Input | Role |
|---|---|---|---|
| Instacart Market Basket Analysis | [Kaggle competition dataset](https://www.kaggle.com/c/instacart-market-basket-analysis/data) via user-provided mirror | `orders.csv`, `order_products__prior.csv`, `order_products__train.csv`, `products.csv`, `aisles.csv`, `departments.csv` | Primary grocery basket study |
| UCI Online Retail II | [UCI original dataset](https://archive.ics.uci.edu/dataset/502/online+retail+ii), DOI: 10.24432/C5CG6D | `online_retail_II.xlsx` (2009–2011, two worksheets) | Separate time-split domain and product description lookup |

The source was mounted in Kaggle at `/kaggle/input/datasets/wafabila/bundlerecommender-dataset`; its local path is **not** itself evidence of redistribution permission. Raw third-party datasets are not bundled in this repo. **UCI Online Retail II is CC BY 4.0** (credit the original creator Daqing Chen); the Kaggle Instacart competition data is **subject to its competition rules**—verify the particular mirror and terms before redistributing raw rows or derived material. See [dataset provenance](docs/en/DATASET.md).

## Data audit and methodology

- Instacart inventory: **3,421,083 orders**, **32,434,489 prior line items**, **49,688 catalog products**, **3,214,874 distinct prior orders**, **206,209 users** (`reports/instacart_integrity.json`). These are corpus counts, **not** the model-training basket count.
- Train: **100,000** sampled earlier baskets, **1,004,573** line items; holdout: **25,000** later-order baskets, **259,594** line items (`reports/split_stats.csv`). The code describes holding out the latest *prior* order per selected user, not claiming a full chronological external production evaluation.
- UCI: **1,067,371** raw rows; **1,020,658** filtered unique invoice-item entries; **34,264** training invoices and **8,567** later invoices according to `reports/uci_cleaning.json`. Dates sorted into earliest 80% and later 20%; no cross-dataset join.
- UCI `models/uci_rules.csv` contains **150** exported directed rules across **46 distinct SKU identifiers**. `reports/uci_metrics.json` records an experimental top-**100 SKU** scope, which must not be confused with exported-rule catalog size.
- Product-name display mapping: **46/46** exported UCI rule SKUs mapped; **1,067,371** source rows scanned across two worksheets. Name is selected by most frequent nonblank description per SKU, with lexical tie-breaking (`models/uci_product_catalog_audit.json`). This **does not retrain** the recommendation rules.
- Research method uses frequent-itemset mining (FP-Growth / Apriori comparison), rule filtering and offline analysis. Actual algorithm and thresholds should always be checked against exported `models/model_config.json` and notebook runs.

## Research results — use with scope

| Evidence | Value | What it actually means |
|---|---:|---|
| Instacart train-rule count | **13** | Directed rules available in export |
| Instacart holdout baskets | **25,000** | Out-of-sample basket co-occurrence assessment |
| Holdout vocabulary item coverage | **0.2413** | Vocabulary coverage metric as reported, **not user hit rate** |
| Median supported holdout confidence | **0.2289** | Median conditional basket co-occurrence over eligible rules |
| Median supported holdout lift | **2.4195** | Association relative to independent occurrence |
| Supported rules with ≥30 antecedent baskets | **13/13** | Adequacy threshold for this diagnostic, not business efficacy |
| UCI training / later-period baskets | **34,264 / 8,567** | Independent time-ordered split |
| UCI rule count | **150** | Exported rule list |
| FP-Growth / Apriori benchmark | **3.67s / 2.65s** | Single recorded experiment; both found **92 itemsets** |

All numbers are from saved reports in this repository. A rule's **confidence is not a customer-specific purchase probability**; **lift is not incremental revenue or causal conversion lift**. Do not compare UCI vs Instacart lift as a pooled score. Full interpretation and threats to validity: [Evaluation](docs/en/EVALUATION.md) and [Limitations](docs/en/LIMITATIONS.md).

### Research plots

![Instacart training basket sizes](assets/plots/train_basket_sizes.png)

![Most frequent training products](assets/plots/top_products.png)

![Train vs holdout rule confidence](assets/plots/train_vs_holdout_confidence.png)

![Top bundle lift](assets/plots/top_bundle_lift.png)

These are experiment output figures, not production dashboards. See [asset index](assets/README.md) for exact roles and update rules.

## Architecture

```text
Original datasets (Kaggle; external) --> notebooks/bundlerecommender.ipynb
           |                                |-- reports/* (audit, splits, metrics)
           |                                |-- models/instacart_rules.csv
           |                                `-- models/uci_rules.csv
UCI Excel -- names-only extractor --> models/uci_product_catalog.csv (+ audit JSON)
                                                   |
React + TypeScript (Vite) <-- HTTP/JSON --> FastAPI --> rule CSV adapter + optional UCI names
       |                                                 |
       `-- basket, suggestions, evidence, JSON export    `-- no fabricated recommendations
```

`backend/app/services/rules.py` is responsible for rule matching; `product_names.py` handles product metadata. The frontend retains SKU as the stable key, even when showing descriptions. Neither dataset is merged into a common product ontology.

## Repo structure (current tracked paths)

```text
BundleRecommender/
├── README.md                 # canonical project entry
├── AGENTS.md                 # engineering & agent contract
├── LICENSE                   # MIT for original project code/docs
├── .env.example
├── assets/
│   ├── README.md              # asset index added in this documentation pack
│   ├── diagrams/.gitkeep
│   ├── screenshots/{new.png,new2.png}
│   └── plots/{train_basket_sizes.png,top_products.png,
│             train_vs_holdout_confidence.png,top_bundle_lift.png}
├── data/{raw,interim,processed,external}/.gitkeep
├── notebooks/{bundlerecommender.ipynb,bundlerecommender no retraining.ipynb}
├── ml/{data,features,training,evaluation,inference}/ # Python scaffold
├── models/{instacart_rules.csv,uci_rules.csv,model_config.json,
│           uci_product_catalog.csv,uci_product_catalog_audit.json}
├── reports/{final_summary.json,instacart_heldout_metrics.json,
│           instacart_heldout_rule_evaluation.csv,uci_metrics.json,
│           uci_later_period_rule_evaluation.csv,algorithm_benchmark.csv,
│           instacart_integrity.json,uci_cleaning.json,source_contract.json,
│           input_inventory.csv,split_stats.csv,top_products_training.csv,
│           release_sha256.json}
├── exports/{product_catalog.csv,instacart_bundle_suggestions.csv}
├── backend/{app,tests,requirements.txt,README.md}
├── frontend/{src,public,package.json,package-lock.json,tsconfig.json,
│            vite.config.ts,vite-env.d.ts,index.html,README.md}
├── scripts/{extract_uci_catalog.py,find_uci_source.ps1}
├── tests/.gitkeep
└── docs/{README.md,id/,en/}
```

**Note:** `.venv/`, `node_modules/`, compiled output, and private/raw datasets are intentionally not in version control. The source snapshot includes only three current product-name tests; the older `backend/tests/test_api.py` was deleted in commit `2de0264`, and is a regression coverage gap to address.

## Run locally (Windows PowerShell)

Prerequisites: Python **3.11**, Node.js/npm, and tracked rule CSVs in `models/`.

```powershell
# Terminal 1 — from repository root
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

```powershell
# Terminal 2 — from repository root
cd frontend
npm ci
npm run build
npm run dev
```

Backend: `http://127.0.0.1:8000/docs`; UI: `http://127.0.0.1:5173`. The Vite setting is `VITE_API_BASE_URL`; backend paths can use `BR_MODEL_DIR` / `BR_EXPORT_DIR`. Verify that `/api/v1/catalog?dataset=instacart`, `/api/v1/catalog/details?dataset=uci` and `/api/v1/recommend` respond before claiming demo readiness. API details in [backend README](backend/README.md).

## Testing and reproducibility

The known local run reported **3 passing product-name tests, 1 deprecation warning**, FastAPI startup completion, and a successful frontend Vite production build (**1,580 modules**). A broader four-test API suite passed earlier **before** its test file was deleted; do not describe it as part of the current test suite. The current repository's clean-checkout build or production deployment has **not** been independently verified by this documentation update. Re-run tests after installation and preserve terminal output; check dataset provenance, split construction, CSV schema, source checksum and model artifacts. Read [Reproducibility](docs/en/REPRODUCIBILITY.md).

## Known limitations / claim boundaries

- **Association ≠ causation**: no incremental conversions, revenue, user-specific predicted purchase probability or uplift.
- **Dataset coverage**: bounded top-product vocabulary and filtered rules can omit much of the source catalog; nine Instacart items or 46 UCI SKUs visible in the app do not mean the full underlying datasets are that small.
- **Offline evaluation only**: no blind online A/B test, inventory checks, price/margin optimization, customer preferences, demographic targeting or cold-start solution.
- **Temporal and selection bias**: UCI later-period drift and Instacart prior-order selection matter; train-generated rules must be checked on distinct held-out baskets.
- **UCI name metadata**: mapping is inferred from observed original descriptions, not universal retail product taxonomy; ambiguous renames/collisions remain possible.
- **Licensing**: MIT applies to project-authored code/docs, **not automatically to third-party datasets, screenshots, trademarks or linked assets**.

## Docs, troubleshooting, and FAQ

- [Documentation index](docs/README.md); [Bahasa Indonesia](docs/id/README.md); [English](docs/en/README.md).
- [Architecture](docs/en/ARCHITECTURE.md), [Dataset](docs/en/DATASET.md), [Experiment protocol](docs/en/EXPERIMENTS.md), [Metrics](docs/en/EVALUATION.md), [Limits](docs/en/LIMITATIONS.md).
- [Deployment](docs/en/DEPLOYMENT.md), [Troubleshooting + FAQ](docs/en/TROUBLESHOOTING.md), [Roadmap](docs/en/ROADMAP.md).

## License and citations

Original code/documentation: [MIT License](LICENSE), © 2026 Wafa Bila Syaefurokhman. Data attribution: **Chen, D. (2012). Online Retail II. UCI Machine Learning Repository. DOI: [10.24432/C5CG6D](https://doi.org/10.24432/C5CG6D)**. Instacart data: [Kaggle competition](https://www.kaggle.com/c/instacart-market-basket-analysis/data), whose data page states **subject to competition rules**. This README is informational and not legal advice. Validate rights for any redistributable product catalog derived from source data.

---

**Research contract:** publish the observed offline evidence, clearly label what has not been measured, and keep all recommendations auditable back to the rule CSV.
