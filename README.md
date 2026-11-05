# seo-skills

Kumpulan skill Claude Code / Command Code untuk SEO.

## Skill

- `skills/seo-vodeco`: audit on-page artikel/URL berdasarkan Master Panduan SEO Vodeco (skor 0-100 + daftar perbaikan).
- `skills/seo-vodeco-audit`: orkestrator audit gabungan, [claude-seo](https://github.com/AgriciDaniel/claude-seo) untuk teknis, schema, performa, GEO, dan seo-vodeco untuk on-page standar Vodeco.
- `skills/seo-vodeco-workflow`: siklus konten end-to-end dengan standar Vodeco (riset → brief → draft → audit on-page → gerbang AI/breadcrumb/CWV → revisi → laporan → drift).
- `agents/seo-vodeco.md`: (opsional) subagen agar claude-seo dapat memanggil seo-vodeco.

## Instalasi

Skill ada di `skills/seo-vodeco/` (berisi `SKILL.md`, `references/`, `scripts/`).

### Claude Code

Personal (semua proyek):
```bash
git clone https://github.com/vodeco-dev/seo-skills.git
mkdir -p ~/.claude/skills && cp -r seo-skills/skills/seo-vodeco ~/.claude/skills/
```

Per proyek (ikut ter-commit, tim otomatis dapat):
```bash
mkdir -p .claude/skills && cp -r /path/ke/seo-skills/skills/seo-vodeco .claude/skills/
```

Pakai: `/seo-vodeco https://situs.com/artikel "keyword utama"`. Restart sesi Claude Code bila skill belum muncul.

### Command Code

```bash
cmd skills add vodeco-dev/seo-skills/skills/seo-vodeco            # proyek: .commandcode/skills/
cmd skills add vodeco-dev/seo-skills/skills/seo-vodeco --global   # personal: ~/.commandcode/skills/
cmd skills list
```

Manual: salin folder `seo-vodeco` ke `~/.commandcode/skills/` atau `.commandcode/skills/`. Command Code juga membaca `.agents/skills/`.

Skrip `scripts/extract_onpage.py` membutuhkan Python 3 (tanpa library tambahan).

## Integrasi dengan claude-seo

claude-seo tidak diubah. Ada dua cara memakainya bersama seo-vodeco:

1. **Cara utama, `seo-vodeco-audit`** (Claude Code dan Command Code). Pasang `seo-vodeco` dan `seo-vodeco-audit` berdampingan, lalu:
   ```
   /seo-vodeco-audit https://situs.com/artikel "keyword utama"
   ```
   Skill menjalankan `/seo page` / `/seo audit` (bila claude-seo terpasang) untuk teknis, schema, performa, GEO, lalu seo-vodeco untuk aturan on-page Vodeco, dan menggabungkan hasilnya (dua skor terpisah + satu rencana tindakan). Tanpa claude-seo, hanya bagian Vodeco yang jalan.
2. **Subagen claude-seo (opsional, Claude Code)**: salin `agents/seo-vodeco.md` ke `~/.claude/agents/` agar audit claude-seo dapat mendelegasikan pemeriksaan on-page Vodeco.

Pasang claude-seo di Claude Code: `/plugin marketplace add AgriciDaniel/claude-seo` lalu `/plugin install claude-seo@agricidaniel-claude-seo`, kemudian `/seo setup`. Di Command Code, pasang claude-seo sesuai README-nya; `seo-vodeco-audit` otomatis jatuh ke mode Vodeco-saja bila `/seo` tidak ada.

Pasang ketiga skill:
```bash
cp -r skills/seo-vodeco skills/seo-vodeco-audit skills/seo-vodeco-workflow ~/.claude/skills/
cmd skills add vodeco-dev/seo-skills/skills/seo-vodeco-audit        # Command Code
cmd skills add vodeco-dev/seo-skills/skills/seo-vodeco-workflow     # Command Code
```

Catatan: otoritas domain ditulis eksplisit sebagai DA (Moz) atau DR (Ahrefs); meta description 120-160 karakter hanyalah rekomendasi, bukan aturan panduan.

## Workflow konten

`seo-vodeco-workflow` merangkai semua tahap menjadi satu alur, dengan `seo-vodeco` sebagai gerbang mutu di akhir:

```bash
/seo-vodeco-workflow mulai <keyword>          # konten baru
/seo-vodeco-workflow mulai <url> "keyword"    # perbaikan halaman yang sudah ada
/seo-vodeco-workflow audit <url> "keyword"    # audit + laporan saja
/seo-vodeco-workflow publish <url> "keyword"  # baseline drift setelah tayang
```

Tahap: intake → riset → brief → draft → audit on-page → gerbang (AI, breadcrumb, CWV, spam) → revisi (maks 2 putaran) → laporan `.md` → drift baseline. Aturan on-page tetap satu sumber: `seo-vodeco/references/checklist.md`.

## Pratinjau laporan

Setelah audit, kedua skill menyimpan laporan ke `seo-audit-<domain>-<tanggal>.md`, menyalinnya ke clipboard (bila ada `pbcopy`/`clip`/`xclip`/`wl-copy`), dan membuka https://markdownlivepreview.com/ bila browser tersedia. Situs itu editor tempel, jadi tempel isi file ke panel kiri untuk melihat pratinjau.
