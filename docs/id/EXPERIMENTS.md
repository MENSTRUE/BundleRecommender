# Eksperimen dan pilihan metode

> BundleRecommender — Day 20/100 · Dokumen riset, bukan bukti kesiapan produksi.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Pertanyaan penelitian

Mampukah aturan pasangan produk yang ditambang dari basket pelatihan tetap menunjukkan asosiasi pada basket yang tidak dipakai membentuk aturan? Ini bukan eksperimen A/B dan tidak mengestimasi efek penyajian bundel.

## Protokol Instacart

Pemilihan basket mengutamakan urutan per pengguna. *Earlier prior orders* ditambang sebagai training; latest prior order per pengguna dipisahkan untuk holdout. Eksperimen berbatas 100.000 train dan 25.000 held-out basket, sehingga populasi penelitian lebih kecil dari corpus asli. Kode melibatkan inventaris dan pemeriksaan ID, lalu menyusun matrix basket produk dengan domain top-products. Parameter pada `models/model_config.json`: `top_products=120`, `min_support=0.012`, `min_confidence=0.15`, `min_lift=1.05`. Jangan mengubah angka tanpa evaluasi ulang.

## Metode

Benchmark tunggal: FP-Growth 3,67 s dan Apriori 2,65 s, masing-masing 92 frequent itemsets. Perbedaan waktu bergantung lingkungan dan pilihan subset; hasil ini **bukan klaim Apriori selalu lebih cepat**. Rule diekspor sebagai pasangan ID dan metrik; 13 rule Instacart terpilih. Hindari klaim 'best model' tanpa kriteria champion yang tercatat eksplisit.

## UCI

Urutkan invoice menurut `InvoiceDate`; train 34.264 invoice lebih awal dan test 8.567 invoice lebih akhir. Mining memakai ruang SKU UCI sendiri; ekspor 150 aturan yang menggunakan 46 kode unik. Evaluasi per periode tersedia di `reports/uci_later_period_rule_evaluation.csv` tetapi tidak sama dengan validasi conversion.

Notebook utama `notebooks/bundlerecommender.ipynb`; notebook `bundlerecommender no retraining.ipynb` adalah utilitas ekstraksi label SKU, bukan model kedua.
