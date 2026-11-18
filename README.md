# kho-sound-meme

100 sound effects + 100 meme images for TikTok videos. Diverse topics, viral/trending first. Office videos are one use case, not the whole library.

## Contents

| Type | Count | Viral | Size |
| --- | --- | --- | --- |
| Sounds (MP3) | 100 | 9 | ~14.5 MiB |
| Meme images | 100 | 30 | ~17.3 MiB |
| **Total** | **200** | | **~31.7 MiB** |

## Sounds — 8 groups, all from tiengdong.com

| Group | Slug | Count |
| --- | --- | --- |
| Office | `van-phong` | 15 |
| Laugh / Reaction | `cuoi-reaction` | 15 |
| Meme punch / fail / dramatic | `meme-punch` | 15 |
| Family / City / Daily life | `gia-dinh-doi-song` | 15 |
| Viral Vietnamese quotes | `cau-noi-viral` | 10 |
| Nature / Animals | `thien-nhien-dong-vat` | 10 |
| Tech / UI | `cong-nghe-ui` | 10 |
| Cinema / Trailer | `dien-anh-trailer` | 10 |

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
├── sounds.json          # all 100 sounds
├── memes.json           # all 100 memes
├── sounds/<group_slug>/ # MP3 files + sound-map.json
└── memes/<group_slug>/  # image files + meme-map.json
```

## JSON maps

One map per group, plus a root index for each type.

- `sounds/<group_slug>/sound-map.json` — `{ group, group_slug, count, items[] }`
- `memes/<group_slug>/meme-map.json` — `{ group, group_slug, count, items[] }`
- `sounds.json` — `{ total: 100, items[] }`, same fields as group maps plus `group` / `group_slug`
- `memes.json` — `{ total: 100, items[] }`, same fields as group maps plus `group` / `group_slug`

Sound item:

| Field | Type | Notes |
| --- | --- | --- |
| `name` | string | Name on tiengdong.com |
| `slug` | string | tiengdong page slug |
| `file` | string | MP3 filename in the same group folder |
| `duration_s` | number | Real duration, measured with ffprobe |
| `bytes` | number | File size in bytes |
| `viral` | bool | Viral sound (see `viral_note`) |
| `viral_note` | string | Why it is viral, or `""` |
| `source_url` | string | tiengdong page URL |
| `source_mp3` | string | Original MP3 URL |
| `audit` | string | `ok` or `FIXED (...)` if a wrong file was replaced |

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

## How to pick an asset

1. Pick a group first (`group_slug`), then filter inside it.
2. Prefer viral: sounds `viral == true` (9), memes `viral_trending == true` (30).
3. Sounds: every sound is ≤ 8s (longest 7.95s) — ready to drop into a video as-is, no trimming needed.
4. Memes: check `width` / `height`. Most images are square or landscape — crop or place on a background for vertical 1080×1920.
5. File path is always `sounds/<group_slug>/<file>` or `memes/<group_slug>/<file>`. Never guess a filename outside the maps.

## Copyright cleanup — 2026-11-18

- Removed 41 assets that could carry copyright risk: 23 sounds + 18 memes. All 41 were replaced with safer assets, so the library is back to 100 sounds + 100 memes.
- Removal criteria: sounds taken from games, films, TV shows, or brands (Roblox OOF, Windows XP error, iOS / Samsung / Casio / WeChat tones, game-show stings); voice clips of identifiable creators; memes showing copyrighted characters / IP (SpongeBob, Minion, Pikachu, Doge, Grumpy Cat, Conan, Kermit, Thỏ Bảy Màu).
- tiengdong.com warns that some meme / music sounds may still be flagged on TikTok / YouTube / Facebook. You are responsible for checking the platform policy before posting. Nothing here is claimed "100% copyright-free".
- Remaining caveats: the licence of each individual file was not fully verified; meme images were not all eye-checked; replacement sounds were format/duration-checked, not listened to one by one.

## Two new rules — 2026-11-18

- **No watermarked memes.** Any meme image with a visible watermark is rejected, not kept. 27 old images were dropped for watermarks and replaced with 27 new ones (all `viral_trending == false`). The 27 new images were eye-checked; their licences were not absolutely verified.
- **No sound longer than 8s.** Any sound over 8s must be split down to ≤ 8s — split at a silence gap, never cut mid-sound. 52 sounds were split: 21 kept one segment cut at a silence gap (SEGMENT), 31 kept the loudest 8s window (WINDOW8). 0 sounds were dropped for length, 0 sounds remain over 8s (longest 7.95s). See `audit` in the maps (`SPLIT from …s, …`). Split sounds were duration-checked with ffprobe, not listened to one by one.

## Verified / not verified

Verified on disk:

- 100/100 sounds are real MP3 files, duration measured with ffprobe. 10 files were initially downloaded wrong (sidebar MP3) and re-downloaded from the correct page player — see `audit` in the maps.
- 100/100 memes are real image files, pixel size measured with PIL.
- All 18 JSON maps parse and match the files on disk.

Not verified:

- Sounds were not listened to one by one — file-to-name matching relies on the MP3 coming from the correct tiengdong page player. The 52 split sounds were not listened to one by one either.
- Meme images were not eye-checked one by one — content is based on the research description (`desc_vi`), not a visual check. Exception: the 27 watermark replacements (2026-11-18) were eye-checked, but their licences were not absolutely verified.
- `viral` / `viral_note` are qualitative notes from research, not re-measured view/download counts.
