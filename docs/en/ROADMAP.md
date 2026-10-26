# Evidence-based roadmap

> BundleRecommender — Day 20/100 · Research documentation, not production certification.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Completed and pending

- [x] Dataset inventory, source audit and relational checks.
- [x] Distinct basket evaluation splits and rule exports.
- [x] CSV rules, reports, plot assets and evidence-backed demonstrations.
- [x] Local FastAPI ↔ React demos for both Instacart and UCI.
- [x] Verified source-derived UCI display names for 46/46 exported SKUs; no model retraining.
- [ ] Restore deleted `backend/tests/test_api.py` and extend API integration coverage.
- [ ] Test fresh clone, checksum verification and dependency-locked environment.
- [ ] Test no-rule matches, schema corruption and cross-dataset ID collisions.
- [ ] Reproduce held-out evaluation over more dates and product vintages.
- [ ] Assess merchandising relevance, constraints, stock availability and cold-start.
- [ ] If warranted, design a consent-aware online experiment to measure conversions.
- [ ] Hardening, CI/deployment, security/privacy and dataset rights review.

P0 is regression tests and reproducibility. P1 is evaluation robustness. P2 improves operator UX and explanations. P3 is the separate gate for public or commercial deployment. No milestone is complete without an audit trail.
