# Evaluation and metric interpretation

> BundleRecommender — Day 20/100 · Research documentation, not production certification.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Definitions

For a rule A → B across N baskets: **support** = count(baskets containing A∪B)/N; **confidence** = count(A∪B)/count(A); **lift** = confidence(A→B)/support(B). Values embedded in exported rules are training-period associations. Independently computed held-out diagnostic metrics must be labeled as such. Lift 2 does not imply twice the revenue.

## Saved evaluation

| Reported evidence | Value | Source |
|---|---:|---|
| Instacart train rules | 13 | `reports/final_summary.json` |
| Holdout baskets | 25,000 | `reports/instacart_heldout_metrics.json` |
| Supported rules (≥30 antecedent baskets) | 13 | same |
| Held-out vocabulary item coverage | 0.241269 | same |
| Median supported held-out confidence | 0.228909 | same |
| Median supported held-out lift | 2.419521 | same |
| UCI train/later invoices | 34,264 / 8,567 | `reports/uci_metrics.json` |
| UCI exported rules | 150 | same |

## Bias and claim discipline

Mining and threshold selection use training data. Don't reuse a held-out set for development and continue describing it as untouched. A median supported lift is not top-K hit rate, CTR, probability of an individual buying or incremental revenue. UCI and Instacart are different retail domains and should not be pooled into one score.

## Figures

![Training versus holdout confidence](../../assets/plots/train_vs_holdout_confidence.png)

![High-lift bundle rules](../../assets/plots/top_bundle_lift.png)

These are research plots, not business KPI dashboards.
