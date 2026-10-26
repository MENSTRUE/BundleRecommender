# Reproducibility and integrity

> BundleRecommender — Day 20/100 · Research documentation, not production certification.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Reproduction procedure

1. Clone `MENSTRUE/BundleRecommender` and record the Git commit, Python/Node versions and Kaggle runtime details. Obtain datasets via permitted sources; do not assume this repository includes raw input.
2. Verify the seven source inputs using `reports/input_inventory.csv` and documented column contracts; schemas matter more than mirror directory names.
3. Run the master notebook with inputs mounted in Kaggle and preserve all generated model/report outputs. Ensure held-out baskets are not mined into rules.
4. Compare audit files (`instacart_integrity.json`, `uci_cleaning.json`, `split_stats.csv`, `algorithm_benchmark.csv`, `final_summary.json`) and reconcile discrepancies.
5. If descriptions are required, run the standalone names-only notebook or `scripts/extract_uci_catalog.py`; this creates UCI metadata **without** retraining models.
6. Use `reports/release_sha256.json` to check exactly the files listed in that manifest; it is not proof of data usage rights or security.
7. Run API tests and Vite production build; capture fresh logs, not prior-run outcomes.

## Environment and drift

Notebook dependencies may include pandas, numpy, scipy, matplotlib, mlxtend and openpyxl; API dependencies are separately pinned by `backend/requirements.txt` ranges. Kaggle `/kaggle/...` paths do not exist on Windows. If reruns differ, inspect deterministic seed, chronological sort, package versions and filtering first. Raw customer-level datasets must never be shipped in releases.
