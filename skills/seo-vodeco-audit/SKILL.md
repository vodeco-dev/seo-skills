---
name: seo-vodeco-audit
description: "Audit SEO gabungan: claude-seo (teknis, schema, performa, GEO, konten) ditambah kepatuhan on-page Master Panduan SEO Vodeco (skill seo-vodeco). Pakai saat pengguna minta audit SEO sebuah URL dengan standar Vodeco, atau 'audit vodeco'."
user-invocable: true
argument-hint: "<url> [keyword utama]"
license: MIT
metadata:
  author: Vodeco
  version: "1.0.0"
  category: seo
---

# SEO Vodeco Audit (claude-seo + seo-vodeco)

Orkestrator tipis. Pembagian tugas:

| Area | Ditangani oleh |
|---|---|
| Teknis, crawlability, schema, performa/CWV, sitemap, GEO/AI search, visual | **claude-seo** (`/seo audit` atau `/seo page`) |
| Aturan on-page Vodeco (keyword 100 kata pertama, slug, title, meta, heading, gambar, link, AIDA, intent, gerbang AI/breadcrumb) | **seo-vodeco** |

Balas dalam bahasa pengguna (default Bahasa Indonesia).

## Prasyarat

- `seo-vodeco` wajib terpasang (folder `seo-vodeco/` berdampingan dengan skill ini).
- claude-seo opsional, tetapi ditawarkan lebih dulu (lihat "Cek claude-seo" di bawah).

## Cek claude-seo (sebelum audit)

1. Deteksi: skill `seo` / perintah `/seo` tersedia, atau ada `~/.claude/skills/seo/SKILL.md`, `.claude/skills/seo/SKILL.md`, atau plugin `claude-seo`. Jika ada, lanjut ke Langkah.
2. Jika **tidak ada**, tanyakan sekali, persis: **"claude-seo belum terpasang. Pasang sekarang? (yes/no)"** lalu berhenti dan tunggu jawaban pengguna.
3. **Hanya jika pengguna menjawab "yes" (atau "ya")** secara eksplisit:
   - Claude Code: minta/jalankan `/plugin marketplace add AgriciDaniel/claude-seo`, lalu `/plugin install claude-seo@agricidaniel-claude-seo`, lalu `/seo setup`. Perintah `/plugin` berupa slash command interaktif; bila tidak bisa dijalankan oleh Anda, tampilkan tiga perintah itu agar pengguna menjalankannya, dan tunggu konfirmasi selesai (mungkin perlu restart sesi).
   - Command Code (tidak butuh Claude Code; claude-seo hanyalah repo GitHub berisi skill): pasang dengan clone lalu salin skill ke folder skill Command Code. Jalankan, setelah pengguna "yes":
     ```bash
     d=$(mktemp -d) && git clone --depth 1 https://github.com/AgriciDaniel/claude-seo "$d/claude-seo"
     mkdir -p ~/.commandcode/skills
     cp -r "$d/claude-seo/skills/"* ~/.commandcode/skills/     # skill utama `seo` + semua sub-skill
     cp -r "$d/claude-seo/scripts" "$d/claude-seo/schema" "$d/claude-seo/bin" "$d/claude-seo/requirements.txt" ~/.commandcode/skills/seo/ 2>/dev/null
     ```
     Gunakan `.commandcode/skills/` (proyek) bila pengguna ingin per proyek. Alternatif per skill: `cmd skills add AgriciDaniel/claude-seo/skills/seo` (tambahkan `--global` untuk personal). Folder `agents/` claude-seo (subagen) dibuat untuk `~/.claude/agents`; jangan disalin ke folder skill. Jika Command Code punya folder agents sendiri, tanyakan pengguna dahulu. Tanpa subagen, `/seo audit` menjalankan pemeriksaan secara berurutan.
     Yang **belum terverifikasi**: apakah wrapper `bin/claude-seo` dan `claude-seo setup` (instal dependensi Python) berfungsi dari lokasi ini, karena installer resmi `install.sh` hanya menargetkan `~/.claude/`. Setelah menyalin, coba `python3 ~/.commandcode/skills/seo/bin/claude-seo setup` atau `pip install -r requirements.txt`, dan laporkan hasil/galatnya apa adanya. Jika gagal, tetap lanjutkan audit Vodeco-saja dan beri tahu pengguna.
   - Setelah terpasang, lanjutkan audit penuh.
4. Jika jawaban **"no"**, tidak dijawab, atau ambigu: **jangan memasang apa pun**. Lanjutkan mode Vodeco-saja dan sampaikan bahwa teknis/schema/performa/GEO tidak tercakup. Jangan menanyakan ulang pada sesi yang sama.
5. Jangan pernah memasang tanpa "yes" eksplisit.

## Langkah

1. Ambil URL dan keyword utama dari argumen (tanyakan keyword sekali bila kosong).
2. **Bagian claude-seo**: jika URL adalah halaman/artikel tunggal, jalankan `/seo page <url>` plus `/seo technical`, `/seo schema`, dan `/seo geo` bila tersedia; jika pengguna meminta seluruh situs, jalankan `/seo audit <url>`. Jangan menjalankan ulang pemeriksaan on-page claude-seo yang sama dengan Vodeco secara terpisah bila tidak perlu.
3. **Bagian Vodeco**: ikuti `seo-vodeco/SKILL.md` (ekstraksi dengan `scripts/extract_onpage.py`, checklist, gerbang, skor).
4. **Gabungkan** (lihat aturan di bawah) menjadi satu laporan.

## Aturan Penggabungan

- Satu sumber kebenaran per topik. Untuk title, meta, heading, gambar, link, keyword: **aturan Vodeco menang** (standar tim). Temuan claude-seo yang bertentangan dicatat sebagai catatan, bukan dihitung dua kali. Contoh: claude-seo menyarankan meta 150-160 karakter, panduan Vodeco tidak menetapkan panjang, jadi tampilkan sebagai rekomendasi, bukan kegagalan.
- Untuk teknis, schema, performa/CWV, sitemap, GEO: **claude-seo menang**; seo-vodeco hanya meneruskan gerbang (breadcrumb, CWV) ke hasil claude-seo bila tersedia, tanpa menjalankannya ulang.
- Hapus duplikat. Tiap temuan memuat sumber: `[Vodeco]` atau `[claude-seo]`.
- Jangan menyarankan keyword stuffing, dan jangan mengarang angka DA/DR atau persentase AI; tulis "perlu dicek" (Moz DA atau Ahrefs DR, sebut metriknya).

## Skor Gabungan

Tampilkan dua skor terpisah, jangan dirata-ratakan diam-diam:

- **Skor On-Page Vodeco** (0-100, dari seo-vodeco)
- **SEO Health Score claude-seo** (0-100, bila dijalankan)

Lalu satu **rencana tindakan** berurutan prioritas (Kritis, Tinggi, Sedang, Rendah) yang menggabungkan keduanya, gerbang gagal di paling atas.

## Format Laporan

1. Ringkasan (dua skor, gerbang, 3 temuan terpenting)
2. Gerbang (konten AI, breadcrumb, CWV)
3. Temuan per area, diberi label sumber
4. Rencana tindakan gabungan
5. Hal yang perlu dicek manual

## Pratinjau Markdown (markdownlivepreview.com)

Setelah laporan selesai:

1. Simpan laporan sebagai file `.md` di direktori kerja: `seo-audit-<slug-domain>-<YYYY-MM-DD>.md`. Sebutkan path-nya.
2. Salin isi file ke clipboard bila ada perintah yang tersedia (`pbcopy` di macOS, `clip` di Windows, `xclip -selection clipboard` atau `wl-copy` di Linux). Jika tidak ada, lewati.
3. Buka https://markdownlivepreview.com/ di browser bila lingkungan mengizinkan (`open` di macOS, `xdg-open` di Linux, `start` di Windows). Jika tidak bisa (sesi jarak jauh/tanpa browser), cukup tampilkan tautannya.
4. Beri tahu pengguna dengan jujur: situs itu editor tempel, isi tidak bisa dimuat otomatis. Pengguna perlu menempel (Ctrl+V / Cmd+V) isi file ke panel kiri; pratinjau muncul di kanan. Jangan menyatakan laporan "sudah terbuka" di pratinjau.
