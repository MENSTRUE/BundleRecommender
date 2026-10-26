# Dataset, usage rights and audit

> BundleRecommender — Day 20/100 · Research documentation, not production certification.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Source and provenance

**Instacart Market Basket Analysis** consists of the competition's relational CSV files, obtained through a mirror for the Kaggle experiment. Expected inputs: `orders.csv`, `order_products__prior.csv`, `order_products__train.csv`, `products.csv`, `aisles.csv`, `departments.csv`. Audited corpus counts: 3,421,083 orders; 32,434,489 prior line items; 49,688 catalog products; 3,214,874 prior orders; 206,209 users. Kaggle states data are subject to competition rules; a mirror does not grant redistribution permission.

**UCI Online Retail II** is the two-sheet `online_retail_II.xlsx` workbook, original UCI dataset 502 (DOI 10.24432/C5CG6D), creator Daqing Chen, CC BY 4.0. Source contains 1,067,371 rows and cleaning report lists 1,020,658 distinct filtered invoice-item lines. Document cancelled invoices, invalid quantities, missing descriptions and time ordering when reproducing cleaning.

## Separate vocabularies

Instacart products use numeric `product_id`. UCI retail products use string `StockCode` (some alphanumeric, e.g. `85123A`). Never merge IDs or match on guessed names. UCI experimental top-100 SKU scope differs from the 46 unique SKUs in 150 exported rules; 46/46 descriptions were recovered from original data without retraining.

## Audit and permissions

References: `reports/input_inventory.csv`, `instacart_integrity.json`, `uci_cleaning.json`, `source_contract.json`, and `models/uci_product_catalog_audit.json`. Do not commit original transaction/customer-level data, and validate redistribution permission for any derived retail metadata.
