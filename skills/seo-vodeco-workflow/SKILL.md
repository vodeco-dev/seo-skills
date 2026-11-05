---
name: seo-vodeco-workflow
description: "Workflow konten SEO end-to-end dengan standar Vodeco: riset keyword, brief, draft, audit on-page seo-vodeco, gerbang AI/breadcrumb/CWV, laporan, lalu baseline drift. Pakai saat pengguna minta 'workflow seo', 'alur konten seo', 'bikin artikel seo', atau ingin satu alur dari keyword sampai terbit."
user-invocable: true
argument-hint: "[mulai|brief|draft|audit|publish] <url|keyword> [keyword utama]"
license: MIT
metadata:
  author: Vodeco
  version: "1.0.0"
  category: seo
---

# SEO Vodeco Workflow

Satu alur kerja konten SEO dari keyword sampai terbit, dengan `seo-vodeco` sebagai
gerbang mutu di akhir. Skill ini **mengorkestrasi** sub-skill `seo-*` yang sudah ada;
tidak menduplikasi aturannya.

Balas dalam bahasa pengguna (default Bahasa Indonesia).

## Peta Tahapan

| # | Tahap | Dikerjakan oleh | Output |
|---|---|---|---|
| 0 | Intake | skill ini | Tujuan, URL/keyword, mode (baru / perbaikan) |
| 1 | Riset | `seo-cluster`, opsional `seo-dataforseo` / `seo-backlinks` | Struktur cluster, daftar keyword turunan |
| 2 | Brief | `seo-content-brief` + aturan Vodeco | `brief-<slug>.md` |
| 3 | Draft | skill ini (tulis) + `seo-content` (bersihkan) | `draft-<slug>.md` |
| 4 | Audit on-page | `seo-vodeco` | Skor 0-100 + daftar perbaikan |
| 5 | Gerbang | `seo-vodeco` (G-AI, G-BC, G-CWV, G-SPAM) | Status lulus/gagal |
| 6 | Revisi | skill ini, ulang tahap 4 | Skor naik sampai ambang |
| 7 | Laporan | skill ini | `seo-audit-<slug-domain>-<YYYY-MM-DD>.md` |
| 8 | Monitor | `seo-drift baseline` | Snapshot pembanding |

Tahap 4-6 adalah inti. Tidak ada konten yang dianggap selesai sebelum lolos.

## Checklist (jalankan berurutan, centang saat selesai)

```
[ ] 0. Intake      - tujuan, mode, keyword utama, domain, target skor
[ ] 1. Riset       - 30-50 keyword turunan, intent, 5 kompetitor SERP
[ ] 2. Brief       - judul, slug, meta, outline H2-H3, rencana gambar & link
[ ] 3. Draft       - artikel utuh + AIDA, paragraf 1-2 kalimat, CTA penutup
[ ] 4. Audit       - extract_onpage.py + checklist A-H, skor dihitung
[ ] 5. Gerbang      - AI <=50%, breadcrumb, CWV, spam komentar
[ ] 6. Revisi      - perbaiki temuan Kritis/Tinggi, audit ulang
[ ] 7. Laporan     - .md tersimpan, path disebutkan, markdownlivepreview
[ ] 8. Monitor     - baseline drift (hanya bila sudah tayang)
```

## Cara Pakai

| Perintah | Yang dijalankan |
|---|---|
| `/seo-vodeco-workflow mulai <keyword>` | Tahap 0-7 untuk konten baru |
| `/seo-vodeco-workflow mulai <url> "kw"` | Mode perbaikan halaman yang sudah ada |
| `/seo-vodeco-workflow brief <keyword>` | Mulai dari tahap 2 |
| `/seo-vodeco-workflow draft <brief-file>` | Mulai dari tahap 3 |
| `/seo-vodeco-workflow audit <url> "kw"` | Tahap 4-7 saja (paling cepat) |
| `/seo-vodeco-workflow publish <url> "kw"` | Tahap 8 saja |

Tanpa sub-command: jalankan tahap 0, tanya yang kurang, lalu lanjut.

## Tahap 0: Intake

Tanyakan sekaligus, sekali saja:

1. Konten baru atau perbaikan halaman yang sudah ada? (menentukan mode brief)
2. Keyword utama. Jika pengguna tidak tahu, simpulkan dari H1/slug dan nyatakan sebagai asumsi.
3. Domain situs (untuk memisahkan link internal/eksternal).
4. Target skor. Default **90 (grade A)**.

Jangan lanjut ke tahap 1 sebelum keyword utama jelas.

## Tahap 1: Riset

- Seed keyword → `/seo cluster <keyword>` (ekspansi 30-50 varian + intent).
- Jika DataForSEO tersedia, ambil volume & difficulty lewat `/seo dataforseo`. Jika tidak, pakai WebSearch dan katakan datanya gratis/kasar.
- Ambil 5 hasil organik teratas untuk keyword utama; saring non-kompetitor (Wikipedia, Reddit, marketplace, direktori).
- Kumpulkan daftar **keyword turunan** — ini dipakai lagi di tahap 2 dan dinilai di item A6.

Output tahap ini ditulis ke `riset-<slug>.md`: tabel keyword, intent, 5 kompetitor, celah topik.

## Tahap 2: Brief

Jalankan `/seo content-brief <url-or-keyword> <page-type>` untuk kerangka kompetitifnya,
lalu **paksa** kolom berikut masuk ke brief (aturan Vodeco menang atas saran claude-seo):

| Kolom brief | Aturan Vodeco |
|---|---|
| Judul / SEO title | Keyword utama di **awal** (~60 karakter) |
| Slug | Hanya keyword, huruf kecil, strip, tanpa tanggal/angka acak |
| Meta description | Ada, memuat keyword, menjelaskan keunggulan, mengundang klik. 120-160 karakter hanya rekomendasi, bukan syarat |
| H1 | Tepat satu, memuat keyword, menjawab intent |
| Outline H2-H3 | Rapi tanpa loncat level; sebar keyword turunan secara alami |
| Gambar | Nama file deskriptif berstrip, ALT wajib, format WebP |
| Internal link | Minimal 2-3 ke halaman sekonteks, anchor deskriptif |
| Eksternal | DA/DR 70-100, fresh (maks 2 tahun), `target="_blank"` |
| Pembuka | AIDA 4 unsur |
| Penutup | CTA selaras brand |

Simpan `brief-<slug>.md`. Setiap baris outline wajib punya perkiraan jumlah kata;
jangan kejar jumlah kata sebagai target (aturan H1 Vodeco).

## Tahap 3: Draft

1. Tulis artikel mengikuti brief. Paragraf 1-2 kalimat, satu ide pokok per paragraf.
2. Sisipkan keyword utama di 100 kata pertama secara natural.
3. Jangan menambah pengulangan keyword demi persentase. Kepadatan 2-3% hanya indikator kasar.
4. Setelah draft utuh, jalankan `/seo content` untuk membersihkan frasa khas AI dan karakter Unicode tersembunyi.
5. Simpan `draft-<slug>.md`.

Draft belum boleh dianggap final sebelum tahap 4.

## Tahap 4: Audit On-Page (wajib)

Untuk URL:

```bash
python3 "${COMMANDCODE_PROJECT_DIR}/.commandcode/skills/seo-vodeco/scripts/extract_onpage.py" <url> "<keyword utama>"
```

Di Claude Code, ganti path-nya dengan `~/.claude/skills/seo-vodeco/scripts/extract_onpage.py`
(atau path relatif `scripts/extract_onpage.py` dari folder `seo-vodeco/`).

Untuk draft lokal, baca file dan perlakukan sebagai sumber teks; item yang hanya bisa
dilihat dari HTML (canonical, `target`, schema breadcrumb) ditandai `N/A`.

Lalu jalankan checklist `seo-vodeco/references/checklist.md` (A-H) dan hitung skor
dengan bobot di `seo-vodeco/SKILL.md`. Jangan mengubah bobot.

## Tahap 5: Gerbang

Tampilkan sebagai status terpisah di atas laporan, bukan pengurang skor:

- **G-AI** konten AI maksimal 50% (ZeroGPT). Tanpa angka dari pengguna: `belum dicek`.
- **G-BC** breadcrumb aktif (HTML atau schema BreadcrumbList).
- **G-CWV** Core Web Vitals lewat PageSpeed Insights / GSC.
- **G-SPAM** komentar WordPress disetujui manual atau ada plugin anti-spam.

Gerbang gagal = prioritas tertinggi, di atas semua temuan lain.

## Tahap 6: Revisi

1. Perbaiki semua temuan **Kritis** dan **Tinggi**.
2. Audit ulang (tahap 4). Maksimal **2 putaran**; setelah itu laporkan sisa temuan
   beserta alasannya, jangan berputar tanpa henti.
3. Berhenti lebih awal bila skor >= target dan gerbang lulus.
4. Jangan pernah menurunkan standar demi skor. Jika skor mentok karena data eksternal
   (DA/DR, ZeroGPT), tulis `perlu dicek`, bukan menebak.

## Tahap 7: Laporan

Format mengikuti `seo-vodeco/references/output-template.md`, ditambah:

```
Siklus: <baru | perbaikan>
Target skor: <NN> | Tercapai: <ya/tidak>
Riwayat revisi: <skor awal> -> <skor akhir> (<n> putaran)
Tahap sebelumnya: riset-<slug>.md, brief-<slug>.md, draft-<slug>.md
```

Simpan sebagai `seo-audit-<slug-domain>-<YYYY-MM-DD>.md` di direktori kerja dan sebutkan path-nya.
Setelah itu ikuti bagian Pratinjau Markdown di `seo-vodeco/SKILL.md` (clipboard +
https://markdownlivepreview.com/), termasuk peringatan bahwa isi harus ditempel manual.

## Tahap 8: Monitor

Hanya setelah halaman tayang:

1. `/seo drift baseline <url>` untuk menyimpan snapshot.
2. Sebutkan bahwa `/seo drift compare <url>` dipakai untuk mendeteksi regresi.
3. Untuk pemantauan berkelanjutan, arahkan ke `/seo-vodeco-workflow audit <url> "kw"`
   secara berkala.

## Satu Sumber Kebenaran

- Topik title, meta, slug, heading, gambar, link, keyword, AIDA, intent: **aturan Vodeco menang**.
  Saran claude-seo yang bertentangan dicatat sebagai catatan, tidak dihitung dua kali.
- Topik teknis, schema, performa, sitemap, GEO: **sub-skill `seo-*` menang**.
  Vodeco hanya meneruskan gerbang breadcrumb & CWV.
- Setiap temuan diberi label sumber: `[Vodeco]` atau `[seo]`.

## Degradasi

| Situasi | Tindakan |
|---|---|
| `seo-content-brief` tidak tersedia | Susun brief manual dari 5 kompetitor SERP, tetap pakai tabel aturan Vodeco |
| `seo-cluster` tidak tersedia | Ekspansi keyword manual via WebSearch + Google Related/PAA |
| DataForSEO tidak ada | Pakai WebSearch, tandai metrik volume sebagai perkiraan |
| URL tidak bisa diambil | Minta HTML/teks ditempel, item HTML-only jadi `N/A` |
| Halaman render JavaScript | Minta view-source atau teks artikel, jangan menebak isi |
| ZeroGPT/DA tidak tersedia | Tulis `perlu dicek` + tautan alatnya, jangan mengarang angka |

## Larangan

- Jangan menyarankan keyword stuffing atau menambah keyword demi skor.
- Jangan mengarang DA/DR, persentase AI, atau skor CWV.
- Jangan menyalin kredensial/email/password dari dokumen internal Vodeco.
- Jangan menyatakan laporan "sudah terbuka" di markdownlivepreview.
- Setiap temuan Gagal wajib punya perbaikan konkret (teks pengganti atau tindakan).

## File Terkait

- `../seo-vodeco/SKILL.md` — aturan, bobot skor, gerbang.
- `../seo-vodeco/references/checklist.md` — 8 kelompok item.
- `../seo-vodeco/references/output-template.md` — format laporan.
- `../seo-vodeco/scripts/extract_onpage.py` — ekstraksi on-page.
- `../seo-vodeco-audit/SKILL.md` — audit menyeluruh situs (teknis + Vodeco), pakai
  skill itu bila yang diminta audit seluruh domain, bukan siklus konten.
