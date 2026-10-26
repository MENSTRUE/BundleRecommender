# Troubleshooting dan FAQ

> BundleRecommender — Day 20/100 · Dokumen riset, bukan bukti kesiapan produksi.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Gejala → perbaikan

| Gejala | Tindakan aman |
|---|---|
| `ModuleNotFoundError: app.main` | Cek `backend/app/main.py`; pulihkan file tertentu dari Git, jangan semua folder |
| `No module named app.schemas` | Cek `backend/app/schemas/recommendation.py` dan struktur package |
| Katalog kosong atau `Unsupported rule columns` | Lihat header CSV. Instacart menggunakan `antecedent_id`,`consequent_id`; UCI `antecedent_sku`,`consequent_sku` |
| UCI tampil angka/kode | Itu StockCode; jalankan ekstraksi `Description` asli ke `models/uci_product_catalog.csv` |
| `/kaggle/working/.../uci_rules.csv` hilang | Sesi baru tidak memiliki output lama. Gunakan notebook ekstraksi SKU standalone; tidak perlu training ulang |
| PowerShell error `Missing expression after '--'` | Gunakan satu baris atau backtick PowerShell, bukan `\` Bash |
| React import `Metric` gagal | Pastikan `frontend/src/components/Metric.tsx` ada |
| Vite gagal `./styles/main.css` | Pastikan `frontend/src/styles/main.css` ada |
| `import.meta.env` salah tipe | Periksa `vite-env.d.ts` dan `tsconfig.json` |
| Tidak ada rekomendasi | Coba produk yang muncul di `catalog`; tidak semua basket cocok rule |
| Git warning `LF replaced by CRLF` | Hanya notifikasi normalisasi line endings; bukan error commit |

## FAQ

**Apakah ini model AI generatif?** Tidak; engine menggunakan *association rule mining* yang dapat dijelaskan.

**Perlu training ulang agar nama SKU tampil?** Tidak. Nama bersumber dari metadata UCI dan ditampilkan tanpa mengubah aturan.

**Kenapa katalog aplikasi lebih kecil dari dataset asli?** Katalog hanya berisi produk yang muncul dalam aturan hasil filter.

**Kenapa lift tidak berarti penjualan naik?** Lift adalah asosiasi relatif antara dua item dalam data historis, bukan efek mengiklankan bundel.

**Apakah hasil UCI dan Instacart bisa digabung?** Tidak; identitas produk, pelanggan, dan domainnya berbeda.

**Apakah aplikasi live online?** Tidak; bukti yang tersedia baru penggunaan lokal.

**Bisakah ZIP dokumentasi ditimpa ke seluruh proyek?** Jangan; ekstrak hanya file/folder dokumentasi dan periksa `git diff --stat`.
