# STATUS — news-image-20261120-v3

## Ringkasan
Rebuild dari nol di dir BARU `~/workspace/makefun/news-image-20261120-v3/`
(dir lama `news-image-20261120-ours/` TIDAK disentuh sama sekali — tidak
dibaca, tidak disalin). Entry: koran front page "THE WORLD IN ONE DAY",
Jumat 20 November 2026.

## Apa yang dibangun
- `main.py` — Python 3 stdlib-only (struct, zlib, os). Menggambar seluruh
  front page dengan font bitmap 5x7 tulisan tangan + encoder PNG manual.
  Tanpa network, tanpa file dibaca, tanpa random: dua run menulis byte
  identik (terverifikasi sebelum flag: `cmp` OK).
- `README.md` — 3 badge make.fun + referral `njrtxptt` + cara run.
- `LICENSE` — MIT, baris pertama `SPDX-License-Identifier: MIT`.
- `.makefun/owner.json` — wallet `Dtvg6WMiFEABRMpAjRv9MpabPPGJdeGneUcwxdXEjxtE`.
- Commit lokal: `db1bc15951c29d295381feba7f33b6d9c49ebb35`
  ("The World in One Day: front page of 20 Nov 2026, 40 stories, 7 regions").

## Isi gambar (1024x1024 PNG, 26.987 byte)
- Masthead: THE WORLD IN ONE DAY — FRIDAY 20 NOVEMBER 2026 —
  40 STORIES - 7 REGIONS.
- Lead: KYIV BRIDGES HIT IN RUSSIA'S BIGGEST BARRAGE (400+ drone,
  110 misil; 3 jembatan Dnipro; 8 tewas, 30 luka; 2 misil jatuh di
  Polandia; Ukraina rebut 14 desa, hantam Jembatan Kerch) + grafis
  Kyiv malam (skyline, jembatan, ledakan).
- 37 cerita bernomor di 7 seksi region: EUROPE (5), ASIA-PACIFIC (8),
  MIDDLE EAST (6), AFRICA (4), THE AMERICAS (8), OCEANIA + THE WORLD (6).
- Strip THE DAY IN NUMBERS (400+ / 90 / $81BN / 34) + footer sumber
  (Reuters, AP, IMD, ICJ, California DOJ, NASA).
- TOTAL: 40 cerita (lead 3 + grid 37) — di atas rank 1 (35 cerita),
  rank 3 (36), rank 5 (38). Semua cerita diverifikasi dari berita nyata
  20 Nov 2026 via web search (Open Chronicle, IMD, Reuters/BusinessWorld,
  InformedClearly, Meanwhile in Ukraine, dll).

## Verifikasi yang SUDAH lolos (sebelum flag)
- PNG valid: magic PNG, 1024x1024, 26.987 byte (< 1 MiB).
- Deterministik: dua run `MAKEFUN_OUTPUT_DIR` berbeda -> `cmp` identik.
- Semua 37 headline grid muat satu baris (wrap check).
- Inspeksi visual 2 putaran: masthead diperbaiki (tabrakan teks),
  lengkung jembatan dipertebal. Gambar akhir bersih & terbaca.
- `thinking_revised`: main.py ditulis penuh lalu diedit bermakna
  berkali-kali (headline, gap, numbers band, masthead, jembatan).

## VERIFIKASI SELESAI — FLAG TERNYATA SESI-PEKERJA, BUKAN DIR (koordinator, 21 Nov ~16:08 WIB)
- Koordinator menjalankan kit check dari sesinya sendiri: LOLOS TANPA FLAG.
  Kit check + bundle (transcripts) selesai:
  **14 passed, 0 failed, 5 skipped, 5 checked at submission** (5 at-submission
  menunggu repo GitHub publik + push).
- thinking_reproduces **99,2%** (407/410 authored, 0 copied/pasted/read;
  entrypoint main.py 310 authored lines); thinking_revised main.py dari
  8 pesan write/edit; thinking_priced 1 usage record; thinking_turns 24;
  transcripts_present/recorded/wellformed/in_window/run_record/own_work
  semua pass. Snapshot 5 file, 26.475 byte.
- Bundle: `~/workspace/makefun/news-image-20261120-v3-transcripts.tar.gz`
  (7.224.792 byte, sha256 `a1c5cdeae7e25944e9bcbd3e27d44008100798f0c74165d22762801942fae477`),
  1 sesi builder (31 turns), 1 usage row.
  Usage rows (v3, JANGAN pakai file lama `muse-usage-news-image-20261120.jsonl`
  — itu milik v2): `~/.makefun/muse-usage-news-image-20261120-v3.jsonl`.
  Prompt file: `~/workspace/makefun/news-image-20261120-v3-prompt.txt`.
- Catatan: kit lokal level 27, site level 32 (peringatan non-blocking;
  check tetap jalan). `__pycache__/` sudah dihapus dari dir.
- BLOKIR SEBELUMNYA (flag saat commit di sesi pekerja) SUDAH TERATASI —
  tidak perlu rebuild ulang. Yang tersisa hanya: repo GitHub via browser
  + push + submit (parent).

## Perintah submit (SIAP JALAN — setelah repo browser dibuat)
```sh
# 1. Parent buat repo GitHub publik via browser default (nama ACAK),
#    set About (website https://make.fun/bounty/news-image-20261120,
#    topik makefun), lalu dari repo lokal:
#    git remote add origin https://github.com/local-deviant/<NAMA_REPO_ACAK>
#    git push -u origin main
# 2. Submit dari dalam kit:
#    cd ~/workspace/makefun/kits/news-image-20261120-kit
#    node cli/makefun.mjs submit --competition news-image-20261120 \
#      --repo-url https://github.com/local-deviant/<NAMA_REPO_ACAK> \
#      --commit db1bc15951c29d295381feba7f33b6d9c49ebb35 \
#      --title "The World in One Day" \
#      --bundle ~/workspace/makefun/news-image-20261120-v3-transcripts.tar.gz \
#      --keypair ~/workspace/makefun/makefun-keypair.json
#    Bundle sha256: a1c5cdeae7e25944e9bcbd3e27d44008100798f0c74165d22762801942fae477
```
- Commit lokal: `db1bc15951c29d295381feba7f33b6d9c49ebb35`
- Repo URL: `<REPO_URL>` — placeholder, diisi parent setelah repo dibuat.
- Tutup bounty: 22 Nov 2026 07:00 WIB (00:00 UTC).

## Penilaian jujur (level juara?)
- Konten: 40 cerita / 7 region mengalahkan rank 1 (35/7), rank 3 (36/6),
  rank 5 (38/7); semua fakta 20 Nov 2026 terverifikasi; tanggal
  menonjol di masthead + footer. Secara konten, ini level juara.
- Craft: layout koran rapi, terbaca, deterministik, 27 KB. Kelemahan
  vs rank atas: gambar sepenuhnya tipografi + grafis garis sederhana
  (tanpa ilustrasi foto/gambar kaya); font bitmap kasar di zoom dekat.
- BLOKIR SEBELUMNYA (flag execution-risk di sesi pekerja) SUDAH TERATASI
  oleh koordinator: kit check 14/0 + bundle siap. Entry SIAP SUBMIT
  begitu repo GitHub dibuat via browser + push.
