# Reproduksibilitas dan integritas

> BundleRecommender — Day 20/100 · Dokumen riset, bukan bukti kesiapan produksi.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Jalur reproduksi

1. Clone repository `MENSTRUE/BundleRecommender`; catat commit hash dan versi Python/Node/Kaggle environment. Gunakan data Instacart kompetisi dari sumber yang diizinkan dan workbook UCI II asli.
2. Cocokkan 7 input melalui `reports/input_inventory.csv` serta kolom identitas sesuai `reports/source_contract.json`. Nama folder mirror tidak sepenting schema sumber.
3. Jalankan notebook utama di Kaggle dengan input dataset terpasang. Jangan jalankan training pada test set; simpan semua artefak keluaran, inventaris, dan statistik split.
4. Cocokkan `reports/instacart_integrity.json`, `reports/uci_cleaning.json`, `reports/split_stats.csv`, `reports/algorithm_benchmark.csv`, dan `reports/final_summary.json` terhadap hasil run.
5. Jalankan ulang ekstraksi nama hanya untuk metadata SKU bila diperlukan; `notebooks/bundlerecommender no retraining.ipynb` dan `scripts/extract_uci_catalog.py` bukan retraining. Output `models/uci_product_catalog.csv` dan audit harus sesuai sumber asli.
6. Verifikasi hash dalam `reports/release_sha256.json` **hanya untuk berkas yang tercantum**; hash tidak otomatis membuktikan keamanan data atau lisensi.
7. Jalankan tes API dan Vite build. Catat hasil sebagai run baru; jangan menyalin angka lama jika versi file berubah.

## Hal-hal yang perlu dinyatakan eksplisit

Eksperimen terbatas pada subset; path Kaggle tidak berlaku untuk PowerShell; gunakan `.venv\Scripts\python.exe` pada Windows. Instal `mlxtend`, pandas, numpy, matplotlib, scipy, openpyxl untuk notebook sesuai kebutuhannya, bukan untuk FastAPI ringan. Raw data tidak boleh dimasukkan ke rilis. Jika run baru berbeda, investigasi urutan data, versi dependency, seed 42, dan sorting/threshold sebelum mengklaim reproduksi identik.
