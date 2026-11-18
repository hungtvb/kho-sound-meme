# kho-sound-meme

100 sound effects (+ 158 short clips cut from them) + 100 meme images for TikTok videos. Diverse topics, viral/trending first. Office videos are one use case, not the whole library.

## Contents

| Type | Count | Viral | Size |
| --- | --- | --- | --- |
| Sounds — originals (MP3) | 100 | 9 | ~67.5 MiB |
| Sounds — clips `__cNN` (MP3, 0.3–10 s) | 158 | 13 (inherited from viral originals) | ~7.2 MiB |
| Meme images | 100 | 43 | ~16.5 MiB |
| **Total** | **358** | | **~91.2 MiB** |

Sounds total: 258 files in `sounds.json` (`kind: "original"` = 100, `kind: "clip"` = 158).

## Sounds — 8 groups, all from tiengdong.com

| Group | Slug | Originals | Clips |
| --- | --- | --- | --- |
| Office | `van-phong` | 15 | 42 |
| Laugh / Reaction | `cuoi-reaction` | 15 | 25 |
| Meme punch / fail / dramatic | `meme-punch` | 15 | 7 |
| Family / City / Daily life | `gia-dinh-doi-song` | 15 | 21 |
| Viral Vietnamese quotes | `cau-noi-viral` | 10 | 2 |
| Nature / Animals | `thien-nhien-dong-vat` | 10 | 21 |
| Tech / UI | `cong-nghe-ui` | 10 | 15 |
| Cinema / Trailer | `dien-anh-trailer` | 10 | 25 |

Note: group `cau-noi-viral` keeps its slug and name, but its 10 items are now generic sound effects — the original creator voice clips were removed in the 2026-11-18 copyright cleanup (see below).

Group counts above are the number of items in each `sound-map.json` (original + clip). Originals per group are the ones listed in the table; the group map `count` field is the sum of both.

## Memes — 8 groups, from many meme sites

| Group | Slug | Count |
| --- | --- | --- |
| Office / Work | `van-phong-di-lam` | 20 |
| Cats / Dogs / Animals | `meo-cho-dong-vat` | 20 |
| Study / Exams | `hoc-tap-thi-cu` | 10 |
| Love / Family | `tinh-yeu-gia-dinh` | 10 |
| Money / Salary | `tien-bac-luong` | 10 |
| Sports / Games | `the-thao-game` | 10 |
| Travel / Food | `du-lich-an-uong` | 10 |
| General reactions | `reaction-chung` | 10 |

## Layout

```text
kho-sound-meme/
├── README.md
├── GUIDE.md
├── find.py              # search CLI (stdlib only)
├── sounds.json          # all 258 sound items (originals + clips)
├── memes.json           # all 100 memes
├── tools/validate.py    # checks maps vs files on disk (run before commit)
├── sounds/<group_slug>/ # MP3 files + sound-map.json
└── memes/<group_slug>/  # image files + meme-map.json
```

Clip files are named `<parent-slug>__cNN.mp3` (NN = 01, 02, ...), in the same folder as their parent original. A clip is a short 0.3–6 s piece cut from a long original (a loop is ~10 s with a crossfade). Clips have `kind: "clip"` and `parent_slug` pointing to the original's `slug`. Original files are unchanged.

## JSON maps

One map per group, plus a root index for each type.

- `sounds/<group_slug>/sound-map.json` — `{ group, group_slug, count, items[] }`
- `memes/<group_slug>/meme-map.json` — `{ group, group_slug, count, items[] }`
- `sounds.json` — `{ total, items[] }`, same fields as group maps plus `group` / `group_slug`
- `memes.json` — `{ total, items[] }`, same fields as group maps plus `group` / `group_slug`

Sound item:

| Field | Type | Notes |
| --- | --- | --- |
| `name` | string | Name on tiengdong.com (clips: parent name + `(đoạn NN)` or `(nền lặp ~10 giây)`) |
| `slug` | string | tiengdong page slug (clips: `<parent-slug>__cNN`) |
| `file` | string | MP3 filename in the same group folder |
| `duration_s` | number | Real duration, measured with ffprobe |
| `bytes` | number | File size in bytes |
| `viral` | bool | Viral sound (see `viral_note`); clips inherit it from the parent |
| `viral_note` | string | Why it is viral, or `""` |
| `source_url` | string | tiengdong page URL (clips: parent page) |
| `source_mp3` | string | Original MP3 URL (clips: parent's) |
| `audit` | string | `ok` / `FIXED (...)` / `REPLACEMENT ...` / `CLIP ...` describing the history |
| `kind` | string | `original` or `clip` (added 2026-11-18b) |
| `long` | bool | Only on originals longer than 30 s |
| `parent_slug` | string | Clips only: slug of the original they were cut from |
| `start_s` / `end_s` | number | Clips only: position in the original (seconds) |
| `tags` | string[] | Vietnamese keywords with diacritics (added 2026-11-18b) |
| `tags_ascii` | string[] | Same keywords without diacritics, for search |
| `use_case_vi` | string | One sentence: when to use it (added 2026-11-18b) |
| `loudness_peak_db` | number | Clips (and new items): measured peak after normalising to about -3 dBFS |
| `license_note` | string | Only on items added from outside tiengdong (see changelog) |

Meme item:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | number | 1–100 |
| `title_vi` | string | Vietnamese title |
| `desc_vi` | string | Image description |
| `use_case` | string | When to use it |
| `file` | string | Image filename in the same group folder |
| `file_jpg` | string | Only ids 21, 22: JPG copy of the AVIF original (`file` is kept) |
| `width` / `height` | number | Real pixel size |
| `format` | string | JPEG / PNG / WEBP / GIF / AVIF |
| `bytes` | number | File size in bytes |
| `orientation` | string | `portrait` (h > w), `square`, or `landscape` (added 2026-11-18b) |
| `fit_vertical` | bool | `true` if width ≥ 600 px: fits a 1080×1920 frame well (added 2026-11-18b) |
| `tags` / `tags_ascii` | string[] | Keywords, with and without diacritics (added 2026-11-18b) |
| `viral_trending` | bool | Viral / trending meme |
| `viral_note` | string | Why it is viral, or `""` |
| `source_url` | string | Original image URL |
| `page` | string | Source page URL (may be `""`) |

## How to pick an asset

1. Pick a group first (`group_slug`), then filter inside it.
2. Prefer clips for punchlines: `kind == "clip"` (158). They are 0.3–6 s and ready to drop in. Use the original only when you need the full length.
3. Prefer viral: sounds `viral == true` (22 incl. clips), memes `viral_trending == true` (43).
4. Do not use ambience as a punchline. **24 original sounds are longer than 30 s** (`long: true`, longest 612.68 s, ocean waves). If you need a bed, use a clip with `"loop"` in its `tags` (about 10 s, crossfaded), not the whole original.
5. Memes: use `fit_vertical` / `orientation` to pick images for a 1080×1920 frame. Most images are square or landscape — crop or place on a background otherwise. Ids 21 and 22 are AVIF: use `file_jpg`.
6. File path is always `sounds/<group_slug>/<file>` or `memes/<group_slug>/<file>`. Never guess a filename outside the maps.

## Copyright cleanup — 2026-11-18

- Removed 41 assets that could carry copyright risk: 23 sounds + 18 memes. All 41 were replaced with safer assets, so the library is back to 100 sounds + 100 memes.
- Removal criteria: sounds taken from games, films, TV shows, or brands (Roblox OOF, Windows XP error, iOS / Samsung / Casio / WeChat tones, game-show stings); voice clips of identifiable creators; memes showing copyrighted characters / IP (SpongeBob, Minion, Pikachu, Doge, Grumpy Cat, Conan, Kermit, Thỏ Bảy Màu).
- tiengdong.com warns that some meme / music sounds may still be flagged on TikTok / YouTube / Facebook. You are responsible for checking the platform policy before posting. Nothing here is claimed "100% copyright-free".
- Remaining caveats: the licence of each individual file was not fully verified; meme images were not all eye-checked; replacement sounds were format/duration-checked, not listened to one by one.

## Changelog 2026-11-18b — normalisation and clips

- **Clips:** 52 originals longer than 8 s were cut into 2–5 clips each: 158 clips in total (`__cNN.mp3`, MP3 128 kbps, same channel layout as the source, 5 ms fade-in, 20 ms fade-out, peak normalised to about -3 dBFS, each < 600 KB). Ambience and music files (rain, waves, traffic, market, music) also got one ~10 s crossfaded loop clip. Clips were chosen automatically by energy (silence detection + loudest windows), not by ear.
- **Maps:** every item now has `kind`, `tags`, `tags_ascii`, `use_case_vi`; originals over 30 s have `long: true`. Clips carry `parent_slug`, `start_s`, `end_s`, `loudness_peak_db`. Old fields were not changed. `count` / `total` were updated everywhere.
- **Memes:** `orientation`, `tags`, `tags_ascii`, `fit_vertical` added to all 100. Ids 21 and 22 have a JPG copy (`file_jpg`).
- **Tools:** `find.py` got `--kind original|clip` and `--tag <từ khóa>`; clips rank before originals by default. `tools/validate.py` checks counts, files, slugs/ids and durations.
- **Not done in this pass:** the planned new office sounds and memes from external sources (Phần C) were not added. Wikimedia Commons rate-limited the downloads and the download was then blocked, so the library still has 100 original sounds and 100 memes. Only the clips and maps above were added.

## Verified / not verified

Verified on disk:

- 100/100 original sounds are real MP3 files, duration measured with ffprobe. 10 files were initially downloaded wrong (sidebar MP3) and re-downloaded from the correct page player — see `audit` in the maps.
- 158/158 clips are MP3 files; `duration_s` matches ffprobe within ±0.05 s (checked by `tools/validate.py`).
- 100/100 memes are real image files, pixel size measured (PIL; AVIF via ffprobe).
- 10 random memes (seed 20261118) were opened and compared with `desc_vi`. Most match. Known doubts: id 84 (`desc_vi` says a travel-tiredness cartoon; the image is a cat with the caption "Sao cứ đi mãi một nước thế?" and a watermark), id 44 (the desc is roughly right, but the figure is an illustrated woman, not a student), id 49 (the comic reads as a school cheating story, but the teacher is not clearly visible). Their `desc_vi` was NOT changed.
- All JSON maps parse and match the files on disk (`tools/validate.py`: OK).

Not verified:

- Sounds were not listened to one by one — file-to-name matching relies on the MP3 coming from the correct tiengdong page player. Clip boundaries were picked by energy, so a clip can cut a word or land on a noise.
- Meme images were not eye-checked one by one — content is based on the research description (`desc_vi`), not a visual check, except for the 10-image sample above.
- `viral` / `viral_note` are qualitative notes from research, not re-measured view/download counts.
- `tags`, `tags_ascii`, `use_case_vi` on the original items are generated by keyword rules from the file name / title; they are not hand-written, so check them when they matter.
