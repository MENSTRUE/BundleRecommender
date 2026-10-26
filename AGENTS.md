# BundleRecommender — AGENTS.md

## Project Identity

Day 20/100. Experimental product bundle recommender.

## Source of Truth

1. Executed experiment outputs and saved artifacts
2. Dataset provenance and audit reports
3. Validated application and test outputs
4. Documentation consistent with the above

## Mandatory Engineering Rules

- Never fabricate model predictions or evaluation scores.
- Do not claim production readiness without evaluation.
- Never train on held-out test transactions.
- Prevent transaction or customer leakage across splits.
- Treat association rules as associations, not causation.
- Do not present lift or confidence as purchase probabilities.
- Avoid exposing customer-identifying transaction records.
- Do not commit private datasets, secrets, or large checkpoints.
- Maintain documentation in Indonesian and English.
- Keep README, architecture, and experiment reports consistent.
- Report errors and incomplete features explicitly.

## Before — Now — Next

Before: Repository initialized and GitHub synchronized.

Now: Project structure and documentation scaffolding.

Next: Select and audit a transactional basket dataset,
establish baseline methods, and define evaluation.

## Change Requirements

For every implementation update:
1. Explain changed files.
2. Provide complete working code when requested.
3. Run relevant tests where possible.
4. Report what was and was not verified.
5. Supply a descriptive commit message.
