# Menjalankan lokal dan kesiapan deployment

> BundleRecommender — Day 20/100 · Dokumen riset, bukan bukti kesiapan produksi.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Pengembangan lokal Windows

Dari root repository buat dua terminal terpisah:

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

```powershell
cd frontend
npm ci
npm run build
npm run dev
```

Swagger `http://127.0.0.1:8000/docs`, frontend `http://127.0.0.1:5173`. Pastikan file aturan dan metadata opsional ada di `models/`. `VITE_API_BASE_URL` tersedia untuk frontend; `BR_MODEL_DIR` / `BR_EXPORT_DIR` untuk backend.

## Pemeriksaan sebelum deployment publik

Saat ini belum ada image/container CI atau deployment terverifikasi. Perlu CORS yang spesifik domain, HTTPS, batas beban dan panjang input, rate limiting, logging tanpa PII, error handling, health/readiness yang lebih kuat, pengelolaan secret, artifact hashing, monitoring, test integration, egress policy, serta review lisensi data. Jangan publikasi dataset yang lisensinya belum dipastikan. File CSV ringan cocok untuk serving, tetapi belum ada SLA atau sistem pemutakhiran real-time.
