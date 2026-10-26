# Roadmap berbasis bukti

> BundleRecommender — Day 20/100 · Dokumen riset, bukan bukti kesiapan produksi.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Status aktual

- [x] Inventaris data Instacart & UCI; audit sumber/relasi.
- [x] Split eksperimen dan aturan association-rule terpisah per domain.
- [x] Ekspor laporan, plot, model CSV dan contoh saran.
- [x] Demo lokal FastAPI ↔ React untuk Instacart & UCI.
- [x] Katalog UCI nama produk 46/46, tanpa training ulang.
- [ ] Pulihkan tes `backend/tests/test_api.py` dan perluas pengujian kontrak API yang hilang.
- [ ] Uji clean clone dan checksum terbaru pasca update metadata.
- [ ] Uji no-match, malformed CSV, salah namespace, dan empty inventory secara otomatis.
- [ ] Replikasi eksperimen dalam lingkungan terkunci dengan versi dependensi.
- [ ] Audit lebih banyak periode waktu serta ketahanan perubahan distribusi.
- [ ] Evaluasi kualitas saran dengan ahli merchandising dan aturan inventaris.
- [ ] Kalau perlu: eksperimen online dengan persetujuan dan pengukuran konversi; jangan menjanjikan dampak sebelum ada hasil.
- [ ] Keamanan, deploy pipeline, monitoring, dan pematuhan lisensi sebelum produk publik.

## Prioritas

P0: Restore suite API dan dokumentasikan versi artifact. P1: Validasi offline robustness dan errors. P2: UX nama, daftar aset, evidence; P3: protokol online test serta deployment hardening. Semua milestone perlu bukti, bukan status semata.
