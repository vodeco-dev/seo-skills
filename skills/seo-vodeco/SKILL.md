---
name: seo-vodeco
description: "Audit on-page SEO artikel atau URL berdasarkan Master Panduan SEO Vodeco: keyword di 100 kata pertama, slug, SEO title, meta description, H1-H3, gambar, internal/eksternal link, AIDA, breadcrumb, search intent, batas konten AI. Output skor 0-100 dan daftar perbaikan."
user-invocable: true
argument-hint: "[url | teks artikel] [keyword utama]"
license: MIT
metadata:
  author: Vodeco
  version: "1.1.0"
  category: seo
  source: "Master Panduan SEO Vodeco Draft 1.1 (On Page SEO Checklist 2024 + Update 2025)"
---

# SEO Vodeco: Checklist On-Page

Skill ini memeriksa satu artikel (URL atau teks/HTML yang ditempel) terhadap aturan on-page di Master Panduan SEO Vodeco, lalu menghasilkan skor dan daftar perbaikan berurutan prioritas. Bisa dipakai sendiri (`/seo-vodeco`) atau sebagai sub-skill dari skill `seo` (claude-seo).

Balas dalam bahasa pengguna (default Bahasa Indonesia).

## Input

1. Sumber artikel: URL, atau teks/HTML yang ditempel.
2. Keyword utama (focus keyword). Jika tidak diberikan, tanyakan sekali. Jika pengguna tidak tahu, simpulkan dari H1/slug dan sebutkan bahwa itu asumsi.
3. Opsional: keyword turunan, domain situs (untuk membedakan link internal dan eksternal).

## Langkah Kerja

1. **Ambil data halaman.** Untuk URL, jalankan `python3 scripts/extract_onpage.py <url>` (hanya library standar Python). Skrip mengeluarkan JSON: title, meta description, canonical, slug, H1-H6, 100 kata pertama, gambar (nama file, alt, title), link internal/eksternal (target, rel), jumlah kata, tanda breadcrumb. Jika skrip gagal (diblokir, perlu JS), gunakan WebFetch atau minta pengguna menempel HTML/teks, dan tandai item yang tidak bisa diverifikasi sebagai `N/A` (bukan gagal).
2. **Jalankan checklist** di `references/checklist.md`. Setiap item bernilai Lulus / Sebagian / Gagal / N/A.
3. **Penilaian kualitatif** (tidak bisa otomatis): AIDA pada pembuka, search intent, gaya paragraf, kewajaran keyword, penutup. Nilai dari teks, beri kutipan singkat sebagai bukti.
4. **Verifikasi manual yang perlu bantuan pengguna** (jangan dikarang, tulis sebagai "perlu dicek"): otoritas domain eksternal: **DA (Domain Authority, Moz)** via https://moz.com/domain-analysis, atau **DR (Domain Rating, Ahrefs)** via https://ahrefs.com/website-authority-checker. Keduanya skala 0-100 tetapi tidak setara; tulis metrik dan alatnya di laporan, jangan dicampur; persentase konten AI (ZeroGPT, https://www.zerogpt.com/), link rusak (https://www.brokenlinkcheck.com/).
5. **Hitung skor** dengan bobot di bawah, abaikan item N/A dan normalkan ke 100.
6. **Tulis laporan** memakai format di `references/output-template.md`.

## Bobot Skor (total 100)

| Kelompok | Bobot | Item |
|---|---|---|
| Penempatan keyword | 30 | keyword di 100 kata pertama (6), slug hanya keyword (6), SEO title keyword di awal (6), keyword di H1/H2/H3 (6), pemakaian natural tanpa stuffing (3), keyword turunan (3) |
| Meta & judul | 12 | meta description ada, menarik, memuat keyword (8; panjang 120-160 karakter hanya rekomendasi tambahan, bukan aturan panduan), judul menjawab search intent (4) |
| Struktur heading | 10 | satu H1, urutan H1-H2-H3 rapi tanpa loncat, subjudul informatif |
| Gambar | 10 | nama file deskriptif dengan strip (4), ALT terisi pada semua gambar (4), title text (1), format WebP/ukuran wajar (1) |
| Link | 14 | internal link relevan (6), eksternal ke DA/DR 70-100, masih fresh, bisa diakses, buka tab baru (6), tidak ada link rusak (2) |
| Pembuka & struktur isi | 10 | AIDA (5), prolog-isi-kesimpulan (3), penutup yang mengajak (2) |
| Keterbacaan | 6 | paragraf 1-2 kalimat dan 1 ide pokok, transisi halus, diksi sesuai audiens |
| Search intent & kedalaman | 8 | menjawab intent tanpa mengejar jumlah kata |

Item pass/fail mendapat 100% atau 0%, item "Sebagian" mendapat 50%. Tambahan di luar 100 ditangani sebagai **gerbang** (lihat berikut).

## Gerbang (Update 2025)

Tampilkan sebagai status terpisah, bukan pengurang skor, tetapi cantumkan di atas laporan jika gagal:

- **Konten AI maksimal 50%** (cek ZeroGPT). Jika tidak ada hasil cek dari pengguna: status "belum dicek", minta angkanya. Jika di atas 50%: status GAGAL, prioritas tertinggi.
- **Breadcrumb aktif** (Yoast Breadcrumbs / Rank Math), diperiksa dari HTML atau schema BreadcrumbList.
- **Core Web Vitals / mobile friendly**: Google Mobile-Friendly Test sudah dihentikan. Gunakan PageSpeed Insights (https://pagespeed.web.dev/) atau Lighthouse di Chrome DevTools, serta laporan Core Web Vitals dan Pengalaman Halaman di Google Search Console. Minta pengguna menempel hasilnya bila tidak bisa diakses.

## Prinsip

- Panduan menyebut beberapa aturan sebagai "jika memungkinkan" (keyword di 100 kata pertama, keyword di nama file). Beri "Sebagian" dan catatan, bukan gagal keras, bila pembuka sudah jelas menyebut topik.
- Konten ditulis untuk pembaca. Jangan sarankan keyword stuffing demi skor. Kepadatan keyword hanya indikator kasar (umumnya di bawah sekitar 2-3%, bukan target). Jangan pernah menyarankan menambah pengulangan keyword hanya untuk mencapai persentase; bila kepadatan rendah tetapi bacaan natural, tetap Lulus. Bila kepadatan tinggi atau terdengar dipaksakan, sarankan mengurangi atau memakai sinonim dan turunan.
- Jangan menyalin kredensial, email akun, atau password apa pun dari dokumen internal Vodeco ke laporan.
- Setiap temuan Gagal harus punya perbaikan konkret (teks pengganti atau tindakan), bukan hanya kritik.
- Pisahkan fakta terukur (hasil skrip) dari penilaian (hasil bacaan Anda).

## File Referensi

- `references/checklist.md`: seluruh aturan, ambang, dan cara cek per item.
- `references/output-template.md`: format laporan.
- `scripts/extract_onpage.py`: ekstraksi data on-page dari URL.

## Penggunaan sebagai Sub-Skill claude-seo

Untuk audit gabungan (claude-seo + aturan Vodeco) pakai skill `seo-vodeco-audit` (`/seo-vodeco-audit <url> "keyword"`). Skill ini tetap berdiri sendiri dan tanpa ketergantungan lain. Lihat `skills/seo-vodeco-audit/SKILL.md`.

Untuk siklus penuh dari keyword sampai terbit (riset, brief, draft, audit, gerbang, laporan, drift) pakai `seo-vodeco-workflow` (`/seo-vodeco-workflow mulai <keyword>`). Tahap auditnya tetap skill ini juga. Lihat `skills/seo-vodeco-workflow/SKILL.md`.

## Penanganan Error

| Situasi | Tindakan |
|---|---|
| URL tidak bisa diambil | Minta HTML/teks ditempel, tandai item HTML-only sebagai N/A |
| Halaman dirender JavaScript | Sampaikan keterbatasan, minta view-source atau teks artikel |
| Keyword utama tidak diketahui | Tanya sekali, lalu pakai asumsi dari H1 dan nyatakan jelas |
| Tidak ada hasil DA / ZeroGPT | Tulis "perlu dicek" dengan tautan alatnya, jangan menebak angka |

## Pratinjau Markdown (markdownlivepreview.com)

Setelah laporan selesai:

1. Simpan laporan sebagai file `.md` di direktori kerja: `seo-audit-<slug-domain>-<YYYY-MM-DD>.md`. Sebutkan path-nya.
2. Salin isi file ke clipboard bila ada perintah yang tersedia (`pbcopy` di macOS, `clip` di Windows, `xclip -selection clipboard` atau `wl-copy` di Linux). Jika tidak ada, lewati.
3. Buka https://markdownlivepreview.com/ di browser bila lingkungan mengizinkan (`open` di macOS, `xdg-open` di Linux, `start` di Windows). Jika tidak bisa (sesi jarak jauh/tanpa browser), cukup tampilkan tautannya.
4. Beri tahu pengguna dengan jujur: situs itu editor tempel, isi tidak bisa dimuat otomatis. Pengguna perlu menempel (Ctrl+V / Cmd+V) isi file ke panel kiri; pratinjau muncul di kanan. Jangan menyatakan laporan "sudah terbuka" di pratinjau.
