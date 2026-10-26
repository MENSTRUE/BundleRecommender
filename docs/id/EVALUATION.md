# Evaluasi dan makna metrik

> BundleRecommender — Day 20/100 · Dokumen riset, bukan bukti kesiapan produksi.

[Sumber utama](../../README.md) · [Indeks dokumen](README.md) · [Aturan agen](../../AGENTS.md)

## Definisi

Untuk aturan A → B pada N basket, **support** = jumlah basket memuat A∪B / N; **confidence** = jumlah basket memuat A∪B / jumlah basket memuat A; **lift** = confidence(A→B) / support(B). Gunakan metrik train untuk mempresentasikan aturan yang diekspor; bila mengutip heldout, sebut hasil heldout secara terpisah. Lift 2 bukan dua kali pendapatan.

## Angka tersimpan

| Bukti | Nilai | File |
|---|---:|---|
| Instacart rules | 13 | `reports/final_summary.json` |
| Holdout baskets | 25.000 | `reports/instacart_heldout_metrics.json` |
| Supported rules (≥30 antecedent baskets) | 13 | idem |
| Holdout vocabulary item coverage | 0,241269 | idem |
| Median holdout confidence yang didukung | 0,228909 | idem |
| Median holdout lift yang didukung | 2,419521 | idem |
| UCI train/later invoices | 34.264 / 8.567 | `reports/uci_metrics.json` |
| UCI exported rules | 150 | idem |

## Potensi bias

Pilih top-products dan threshold dari data training; jangan menyisipkan informasi held-out saat memilih rule lalu mengklaim evaluasi independen. Median lift atas supported rules bukan recall@K, CTR, conversion maupun penghematan biaya. Laporan tidak membuktikan kemampuan generalisasi lintas toko, musim atau promosi; khusus UCI tidak boleh dipool dengan hasil Instacart.

## Bukti visual

![Confidence train dibanding holdout](../../assets/plots/train_vs_holdout_confidence.png)

![Lift aturan](../../assets/plots/top_bundle_lift.png)

Dua plot ini perlu dibaca sebagai visualisasi eksperimen, bukan peramalan dampak bisnis.
