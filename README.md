# kho-sound-meme

100 sound effects + 100 meme images for TikTok videos. Diverse topics, viral/trending first. Office videos are one use case, not the whole library.

## Contents

| Type | Count | Viral | Size |
| --- | --- | --- | --- |
| Sounds (MP3) | 100 | 25 | ~68.5 MiB |
| Meme images | 100 | 58 | ~26.1 MiB |
| **Total** | **200** | | **~95.2 MiB** |

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
2. Prefer viral: sounds `viral == true` (25), memes `viral_trending == true` (58).
3. Sounds: filter by `duration_s`. Short punchlines are usually < 5s. **25 sounds are longer than 30s** (longest 612.68s, ocean waves ambience) — do not use ambience as a punchline; trim or loop with ffmpeg if needed.
4. Memes: check `width` / `height`. Most images are square or landscape — crop or place on a background for vertical 1080×1920. Convert the 2 AVIF files (ids 21, 22) to PNG/JPG first if your editor cannot read AVIF.
5. File path is always `sounds/<group_slug>/<file>` or `memes/<group_slug>/<file>`. Never guess a filename outside the maps.

## Copyright

- tiengdong.com warns that some meme / music sounds may still be flagged on TikTok / YouTube / Facebook. You are responsible for checking the platform policy before posting. Nothing here is claimed "100% copyright-free".
- Brand-IP memes (SpongeBob, Minion, Pikachu, Doge, Grumpy Cat, Conan) are for short reactions only. Do not claim them as your own, and do not use them as a channel logo or for resale.
- Roblox OOF and Windows XP error are originally copyrighted sounds — use as short effects only.

## Verified / not verified

Verified on disk:

- 100/100 sounds are real MP3 files, duration measured with ffprobe. 10 files were initially downloaded wrong (sidebar MP3) and re-downloaded from the correct page player — see `audit` in the maps.
- 100/100 memes are real image files, pixel size measured (PIL; AVIF via ffprobe).
- All 18 JSON maps parse and match the files on disk.

Not verified:

- Sounds were not listened to one by one — file-to-name matching relies on the MP3 coming from the correct tiengdong page player.
- Meme images were not eye-checked one by one — content is based on the research description (`desc_vi`), not a visual check.
- `viral` / `viral_note` are qualitative notes from research, not re-measured view/download counts.
