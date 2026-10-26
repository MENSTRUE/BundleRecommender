# Troubleshooting and FAQ

> BundleRecommender — Day 20/100 · Research documentation, not production certification.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Symptom → safe fix

| Symptom | Correct action |
|---|---|
| `ModuleNotFoundError: app.main` | Confirm `backend/app/main.py`; restore just that file |
| `No module named app.schemas` | Confirm `backend/app/schemas/recommendation.py` |
| Empty catalog / `Unsupported rule columns` | Inspect CSV headers: native Instacart IDs and UCI StockCode columns differ |
| UCI shows alphanumeric IDs | Those are StockCodes; map source `Description` to SKU via metadata CSV |
| Missing `/kaggle/working/.../uci_rules.csv` | Fresh Kaggle sessions lose previous output; use standalone names extraction; no retraining |
| PowerShell says `Missing expression after --` | Use a single line or PowerShell backticks rather than Bash backslashes |
| React cannot resolve `Metric` | Restore `frontend/src/components/Metric.tsx` if absent |
| Vite cannot resolve `./styles/main.css` | Restore `frontend/src/styles/main.css` if absent |
| `import.meta.env` TS error | Check Vite typing and `tsconfig.json` |
| No rules match selected basket | Valid outcome; only basket combinations in exported rules produce suggestions |
| CRLF warning from Git | Line-ending warning, not commit failure |

## FAQ

**Is this generative AI?** No. It is transparent association-rule mining over historical baskets.

**Do names require model retraining?** No. StockCode→Description mapping is separate metadata.

**Why are catalogs small?** Only products present in filtered exported rules are available for selection.

**Does lift indicate greater sales?** No. Lift compares co-occurrence to an independence baseline.

**Can UCI and Instacart be combined?** No. They are different identity namespaces/domains.

**Is it deployed publicly?** Not from the evidence in this repo; demos are local.

**Should I replace the entire app directory with a documentation ZIP?** No. Update only documentation files; inspect Git changes.
