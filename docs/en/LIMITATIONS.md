# Limitations and claim boundaries

> BundleRecommender — Day 20/100 · Research documentation, not production certification.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Defensible claims

A local FastAPI + React application presents product-bundle suggestions derived from two exported association-rule CSVs. UCI StockCodes from the exported rules have a 46/46 source-derived description mapping. Offline metrics apply to their documented subsets and split protocols only.

## Unsupported claims

There is **no evidence** for higher sales, conversions, average order value, ROI, CTR, individualized propensity, or purchase probability. The method is historical co-occurrence and does not check stock, product margins, promotions, brand constraints, or customer intent. Neither public production deployment nor randomized controlled evaluation has been completed.

## Operational limitations

Small exported catalog (13 Instacart rules, 150 UCI rules) omits many original products. Cold-start, seasonality, stock changes, and UCI Description ambiguity remain. UCI names are most-frequent values observed in the original workbook, not independently vendor-verified taxonomy. Browser JSON export is not a merchant approval workflow. Previous broad `test_api.py` coverage is absent from the current tree and must be restored.

## Licensing / privacy

Project MIT terms do not override Instacart competition rules; UCI data are CC BY 4.0 with attribution obligations. Avoid storing customer PII in examples. Audit external claims against the actual reports.
