# Keterbatasan dan batas klaim

> BundleRecommender — Day 20/100 · Dokumen riset, bukan bukti kesiapan produksi.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Apa yang boleh diklaim

Aplikasi lokal telah menampilkan hasil recommendation berbasis aturan dari dua CSV. Nama produk UCI ditarik dari `StockCode/Description` asli dengan hasil 46 dari 46 kode aturan. API dan React telah diuji lokal; angka evaluasi hanya berlaku pada setup eksperimen yang didokumentasikan.

## Apa yang tidak boleh diklaim

Tidak ada bukti bahwa bundel meningkatkan penjualan, konversi, AOV, ROI, maupun CTR, bahwa prediksi dipersonalisasi untuk satu orang, atau bahwa score merupakan probabilitas pembelian. Model berbasis co-occurrence, tanpa inventory, margin, atau willingness-to-pay. Tidak ada evaluasi deployment publik, A/B test, fairness atau kegunaan berbasis riset pengguna.

## Keterbatasan teknis

Aturan hanya mencakup sebagian kecil katalog; Instacart 13 rule, UCI 150 rule. Produk tidak teramati di rule tidak muncul di pencarian. Cold start dan perubahan produk musiman memengaruhi rekomendasi. Katalog deskripsi UCI bisa memuat nama berubah-ubah; pemetaan mengambil paling sering, bukan keputusan editorial yang divalidasi vendor. JSON export dan API lokal bukan workflow merchandising approval produksi. Legacy `backend/tests/test_api.py` telah terhapus, sehingga regresi API inti perlu dipulihkan.

## Lisensi dan privasi

MIT repository tidak mencakup data Instacart yang terikat competition rules. Sumber UCI CC BY 4.0 memerlukan atribusi; dataset asli tidak di-commit. Jangan menggunakan data pelanggan pribadi untuk demo. Bandingkan seluruh klaim dengan laporan aktual sebelum publikasi konten.
