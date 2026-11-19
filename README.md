# kho-sound-meme

258 sound effects + 100 meme images for TikTok videos. Diverse topics, viral/trending first. Office videos are one use case, not the whole library.

## Contents

| Type | Count | Viral | Size |
| --- | --- | --- | --- |
| Sounds (MP3) — 100 original + 158 clips | 258 | 22 (9 orig + 13 clip) | ~21.7 MiB |
| Meme images | 100 | 30 | ~17.3 MiB |
| **Total** | **358** | | **~39.0 MiB** |

## Sounds — 8 groups, all from tiengdong.com

| Group | Slug | Original | Clips | Total |
| --- | --- | --- | --- | --- |
| Office | `van-phong` | 15 | 42 | 57 |
| Laugh / Reaction | `cuoi-reaction` | 15 | 25 | 40 |
| Meme punch / fail / dramatic | `meme-punch` | 15 | 7 | 22 |
| Family / City / Daily life | `gia-dinh-doi-song` | 15 | 21 | 36 |
| Viral Vietnamese quotes | `cau-noi-viral` | 10 | 2 | 12 |
| Nature / Animals | `thien-nhien-dong-vat` | 10 | 21 | 31 |
| Tech / UI | `cong-nghe-ui` | 10 | 15 | 25 |
| Cinema / Trailer | `dien-anh-trailer` | 10 | 25 | 35 |

Note: group `cau-noi-viral` keeps its slug and name, but its 10 items are now generic sound effects — the original creator voice clips were removed in the 2026-11-18 copyright cleanup (see below).
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
├── sounds.json          # all 258 sounds
├── memes.json           # all 100 memes
├── sounds/<group_slug>/ # MP3 files + sound-map.json
├── memes/<group_slug>/  # image files + meme-map.json
```

## JSON maps

- `sounds/<group_slug>/sound-map.json` — `{ group, group_slug, count, items[] }`
- `memes/<group_slug>/meme-map.json` — `{ group, group_slug, count, items[] }`
- `sounds.json` — `{ total: 258, items[] }`, same fields as group maps plus `group` / `group_slug`
- `memes.json` — `{ total: 100, items[] }`, same fields as group maps plus `group` / `group_slug`

Sound item:
| Field | Type | Notes |
| --- | --- | --- |
| `name` | string | Name on tiengdong.com |
| `slug` | string | tiengdong page slug (`<parent-slug>__cNN` for clips) |
| `file` | string | MP3 filename in the same group folder |
| `duration_s` | number | Real duration, measured with ffprobe |
| `bytes` | number | File size in bytes |
| `viral` | bool | Viral sound (see `viral_note`) |
| `viral_note` | string | Why it is viral, or `""` |
| `source_url` | string | tiengdong page URL |
| `source_mp3` | string | Original MP3 URL |
| `audit` | string | `ok` or `FIXED (...)` if a wrong file was replaced; `SPLIT ...` / `CLIP ...` for cut files |
| `kind` | string | `original` (full file, ≤ 8s) or `clip` (short cut from an original) |
| `parent_slug` | string | Clip only: slug of the original this clip was cut from |
| `start_s` / `end_s` | number | Clip only: cut window in the original file, in seconds |
| `loudness_peak_db` | number | Clip only: peak loudness in dBFS (range −3.9 to −2.5) |
| `tags` | string[] | Vietnamese search tags (use with `find.py --tag`) |
| `tags_ascii` | string[] | Same tags without diacritics |
| `use_case_vi` | string | When to use this sound, in Vietnamese |
| `long` | bool | `true` if the original source file was longer than 30s (24 originals) |

Meme item:
| Field | Type | Notes |
| --- | --- | --- |
| `id` | number | 1–100 |
| `title_vi` | string | Vietnamese title |
| `desc_vi` | string | Image description |
| `use_case` | string | When to use it |
| `file` | string | Image filename in the same group folder |
| `width` / `height` | number | Real pixel size |
| `format` | string | JPEG / PNG / WEBP / GIF / AVIF |
| `bytes` | number | File size in bytes |
| `viral_trending` | bool | Viral / trending meme |
| `viral_note` | string | Why it is viral, or `""` |
| `source_url` | string | Original image URL |
| `page` | string | Source page URL (may be `""`) |
| `orientation` | string | `square` (29) / `portrait` (24) / `landscape` (47) |
| `tags` | string[] | Vietnamese search tags (use with `find.py --tag`) |
| `tags_ascii` | string[] | Same tags without diacritics |
| `fit_vertical` | bool | `true` (88) if the image fits a vertical 1080×1920 frame without awkward cropping; `false` (12) if it needs a crop or background |

## How to pick an asset

1. Pick a group first (`group_slug`), then filter inside it.
2. Prefer viral: sounds `viral == true` (9 originals + 13 clips), memes `viral_trending == true` (30).
3. Sounds: every original is ≤ 8s (longest 7.95s). Clips are short cuts: 146 are ≤ 8s, 12 are 10.0s windows — check `duration_s` before dropping one in as-is.
4. Memes: `fit_vertical == true` (88) fits vertical 1080×1920 as-is; the 12 `false` ones need a crop or a background. `orientation` tells you square / portrait / landscape at a glance.
5. File path is always `sounds/<group_slug>/<file>` or `memes/<group_slug>/<file>`. Never guess a filename outside the maps.

## Clips — 2026-11-18

- 158 clips cut from 52 of the 100 originals (up to 5 clips per original). File name is `<parent-slug>__cNN.mp3`, `kind` is `"clip"`, `parent_slug` points back to the original.
- Use clips as punchlines / stingers; don't use a long original as a punchline. Find them with `python3 find.py sound --kind clip <keyword>` or `--tag <tag>`.
- Clips were cut at silence gaps or as the loudest window, duration-checked with ffprobe, not listened to one by one.

## Copyright cleanup — 2026-11-18

- Removed 41 assets that could carry copyright risk: 23 sounds + 18 memes. All 41 were replaced with safer assets, so the library is back to 100 sounds + 100 memes.
- Removal criteria: sounds taken from games, films, TV shows, or brands (Roblox OOF, Windows XP error, iOS / Samsung / Casio / WeChat tones, game-show stings); voice clips of identifiable creators; memes showing copyrighted characters / IP (SpongeBob, Minion, Pikachu, Doge, Grumpy Cat, Conan, Kermit, Thỏ Bảy Màu).
- tiengdong.com warns that some meme / music sounds may still be flagged on TikTok / YouTube / Facebook. You are responsible for checking the platform policy before posting. Nothing here is claimed "100% copyright-free". Remaining caveats: the licence of each individual file was not fully verified; meme images were not all eye-checked; replacement sounds were format/duration-checked, not listened to one by one.

## Two new rules — 2026-11-18

- **No watermarked memes.** Any meme image with a visible watermark is rejected, not kept. 27 old images were dropped for watermarks and replaced with 27 new ones (all `viral_trending == false`). The 27 new images were eye-checked; their licences were not absolutely verified.
- **No sound longer than 8s.** Applies to the 100 originals: 52 were split (21 kept one segment cut at a silence gap, 31 kept the loudest 8s window), 0 originals remain over 8s (longest 7.95s). The 158 clips added later include 12 ten-second windows (see Clips above). See `audit` in the maps (`SPLIT from …s, …` / `CLIP …`). Split sounds were duration-checked with ffprobe, not listened to one by one.

## Verified / not verified

Verified on disk:
- 258/258 sounds are real MP3 files, duration measured with ffprobe. 10 files were initially downloaded wrong (sidebar MP3) and re-downloaded from the correct page player — see `audit` in the maps.
- 100/100 memes are real image files, pixel size measured with PIL.
- All 18 JSON maps parse and match the files on disk (`python3 tools/validate.py` → `OK: 258 sounds, 100 memes`).

Not verified:
- Sounds were not listened to one by one — file-to-name matching relies on the MP3 coming from the correct tiengdong page player. The 52 split originals and the 158 clips were not listened to one by one either.
- Meme images were not eye-checked one by one — content is based on the research description (`desc_vi`), not a visual check. Exception: the 27 watermark replacements (2026-11-18) were eye-checked, but their licences were not absolutely verified.
- `viral` / `viral_note` are qualitative notes from research, not re-measured view/download counts.
