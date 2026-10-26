# Experiments and method selection

> BundleRecommender — Day 20/100 · Research documentation, not production certification.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Research question

Do item-pair associations learned from earlier purchase baskets persist in a withheld basket slice? This is not an intervention or causal evaluation of displaying a bundle.

## Instacart protocol

Orders are grouped chronologically per user: earlier *prior* orders provide candidate training baskets; the user's latest prior order is held out. The bounded experiment uses 100,000 training and 25,000 held-out baskets, much smaller than full raw corpus. Notebook audits join keys, constructs baskets, restricts vocabulary, mines itemsets and exports directed rules. `models/model_config.json` records top_products=120, min_support=0.012, min_confidence=0.15, min_lift=1.05.

## Algorithm benchmark and selection caveat

In one run, FP-Growth took 3.67 seconds and Apriori took 2.65 seconds, each finding 92 itemsets. Those are not general algorithm speed rankings. Instacart export contains 13 rules. Do not call a particular approach a statistically validated 'champion' without a formal selection policy recorded in reports.

## UCI protocol

Sort by InvoiceDate; earlier 34,264 invoices for training, later 8,567 for an out-of-time diagnostic. Mine in a distinct UCI StockCode namespace. Export includes 150 directed rules across 46 identifiers. `reports/uci_later_period_rule_evaluation.csv` is offline association evidence, not purchase probability or conversion rate.

Main research notebook: `notebooks/bundlerecommender.ipynb`. `bundlerecommender no retraining.ipynb` is a metadata extraction utility, not a second trained recommender.
