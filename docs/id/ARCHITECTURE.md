# Arsitektur dan kontrak sistem

> BundleRecommender — Day 20/100 · Dokumen riset, bukan bukti kesiapan produksi.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Komponen dan aliran data

`notebooks/bundlerecommender.ipynb` adalah penelitian offline. Dataset transaksi dipisah secara ketat: Instacart beridentitas `product_id`, UCI beridentitas `StockCode`. Output ditulis ke `models/`, `reports/`, `assets/plots/`, dan `exports/`. Runtime FastAPI **tidak** melatih ulang; ia membaca aturan CSV dan mencocokkan antecedent basket, kemudian mengembalikan consequent beserta support, confidence, lift, dan sumber aturan. Frontend React memilih namespace dataset, mengambil katalog dan metadata, lalu mengirim keranjang produk. JSON hasil bisa diekspor dari browser.

## API dan validasi

- `GET /api/v1/health`: status server dan keberadaan artefak, bukan jaminan kualitas.
- `GET /api/v1/catalog?dataset=instacart|uci`: ID produk yang terdapat dalam file aturan.
- `GET /api/v1/catalog/details?dataset=uci`: metadata label tampilan dengan key SKU, fallback SKU bila nama tidak ditemukan.
- `POST /api/v1/recommend`: body `{"dataset":"uci","items":["20719"],"limit":8}`. Nilai `items` adalah ID internal; jangan kirim nama sebagai key.

Algoritma runtime hanya mengembalikan produk yang memiliki rule cocok; jika tidak ada, respons kosong adalah hasil valid. CORS saat ini mengizinkan localhost Vite; deployment umum memerlukan konfigurasi khusus. Jangan mencampur instacart ID dengan SKU UCI.

## Risiko teknis

CSV tidak tersedia, perubahan schema, cache path, nama file hilang saat ekstraksi ZIP, atau aturan yang tidak cocok harus ditangani jelas. Pertahankan file bootstrap `backend/app/main.py`, `frontend/src/main.tsx`, dan CSS. Data bukan layanan real-time dan tidak ada personalization.
