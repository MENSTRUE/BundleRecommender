# Dataset, hak penggunaan, dan audit

> BundleRecommender — Day 20/100 · Dokumen riset, bukan bukti kesiapan produksi.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Sumber data

**Instacart Market Basket Analysis** berasal dari rangkaian file resmi kompetisi Kaggle, diunduh lewat mirror untuk eksperimen. Source path Kaggle: `/kaggle/input/datasets/wafabila/bundlerecommender-dataset/instacart/instacart/`. File wajib: `orders.csv`, `order_products__prior.csv`, `order_products__train.csv`, `products.csv`, `aisles.csv`, `departments.csv`. Total yang diaudit: 3.421.083 orders, 32.434.489 baris prior, 49.688 nama produk, 3.214.874 prior orders, 206.209 pengguna. Dataset **tidak** otomatis berlisensi MIT mengikuti repository; Kaggle memberi pembatasan competition rules, dan mirror bukan bukti lisensi.

**UCI Online Retail II** adalah workbook dua sheet `onlineretailii/online_retail_II.xlsx` dari dataset UCI ID 502, DOI 10.24432/C5CG6D, pencipta Daqing Chen, berlisensi CC BY 4.0. Source audit mencatat 1.067.371 baris, yang setelah filter menjadi 1.020.658 kombinasi invoice-item unik. Data memuat transaksi, pembatalan dan kemungkinan nilai hilang sehingga perlu pembersihan eksplisit. Atribusi sumber wajib saat memakai turunan.

## Ruang lingkup yang berbeda

Produk Instacart berupa `product_id`; produk UCI berupa `StockCode` teks (termasuk alfanumerik seperti `85123A`). **Tidak** boleh join lintas dataset; baik deskripsi maupun kecocokan nama bukan kunci identitas. UCI top-100 SKU dipakai di tahap eksperimen, namun yang benar-benar muncul pada 150 rule yang diekspor hanya 46 SKU. Katalog nama 46/46 berasal dari pencarian frekuensi `Description` pada kedua sheet, bukan training ulang.

## Data audit & perlindungan

Lihat `reports/input_inventory.csv`, `reports/instacart_integrity.json`, `reports/uci_cleaning.json`, `reports/source_contract.json`, serta `models/uci_product_catalog_audit.json`. Hindari memasukkan baris transaksi mentah atau ID pelanggan ke Git. Periksa hak distribusi CSV katalog turunan sebelum dipublikasikan.
