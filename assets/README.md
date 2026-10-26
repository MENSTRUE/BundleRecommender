# Asset index — BundleRecommender

Assets are existing screenshots and notebook-generated research plots; avoid relabeling or fabricating metrics. **Do not assume screenshots constitute a quantitative evaluation.**

## Product demonstration screenshots

### `screenshots/new.png`

![Screenshot new](screenshots/new.png)

Tracked local dashboard capture. Use as a visual demonstration of the current UI at that point in development; check the actual captured dataset/selection before describing specific products in social content.

### `screenshots/new2.png`

![Screenshot new2](screenshots/new2.png)

Tracked local dashboard capture. The README pairs the two screenshots with both Instacart/UCI demos; if ordering differs in actual files, correct those captions after visually verifying the files.

## Saved research plots

| Artifact | Purpose | Caveat |
|---|---|---|
| ![Basket size plot](plots/train_basket_sizes.png) | Distribution of training basket sizes | Experimental subset, not full population |
| ![Top products plot](plots/top_products.png) | Product frequency in training | Does not prove sales impact |
| ![Train and holdout confidence plot](plots/train_vs_holdout_confidence.png) | Compare association confidence between sets | Not calibrated user purchase probability |
| ![Lift plot](plots/top_bundle_lift.png) | Strength of association rules | Not causal uplift |

## Asset rules

- Keep filenames and Markdown paths aligned; do not invent missing screenshots.
- Never put customer PII in screenshots.
- Re-export plots only from a reproducible notebook run and update report references.
- `diagrams/` currently has a `.gitkeep` placeholder; no architecture illustration is claimed to exist.
