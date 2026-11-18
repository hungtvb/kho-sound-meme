# Kho Sound + Meme — kho-sound-meme

> Đọc file này trước khi chọn asset. Mọi con số dưới đây đều đếm/đo thật trên đĩa
> (xem mục [Đã verify](#đã-verify--bằng-chứng-đo-thật)).

## 1. Mục đích

Kho **âm thanh (sound effect)** + **ảnh meme** đa dạng, ưu tiên nội dung **viral /
trending**, phục vụ làm **video TikTok** (ghép sound + ảnh meme làm punchline /
reaction / minh họa). **Video văn phòng là 1 use case** trong kho — không phải
toàn bộ kho: kho còn có cười/reaction, meme punch, câu nói viral, thiên nhiên,
công nghệ/UI, điện ảnh, gia đình/đời sống, mèo/chó, học tập, tình yêu, tiền
bạc, thể thao/game, du lịch/ăn uống.

## 2. Số lượng thật đã tải (đếm trên đĩa)

| Loại | Target | Đã tải được | Tổng dung lượng file media (cộng `bytes` trong map) |
| --- | --- | --- | --- |
| Sound (MP3) | 100 | **100** | **71.789.673 byte (~68,46 MiB)** |
| Ảnh meme | 100 | **100** | **27.390.356 byte (~26,12 MiB)** |
| **Tổng** | **200** | **200** | **99.180.029 byte (~94,58 MiB)** |

- Đếm bằng `find sounds memes -type f`: **216 file** = 200 file media + 16 file
  `sound-map.json` / `meme-map.json` nhóm.
- `du -sb` toàn repo: **99.783.185 byte (~95,16 MiB)** — chênh với tổng trên
  603.156 byte, gồm 18 file JSON map/tổng (281.434 byte) + `README.md` +
  thư mục `hidden_files/` (báo cáo tải gốc, 301.955 byte).
- `du -sb sounds` = 71.845.385 byte; `du -sb memes` = 27.468.370 byte (gồm cả
  file map JSON trong từng thư mục, nên lớn hơn tổng `bytes` media một chút).

## 3. Bảng hạng mục

### 3.1. Sound — 100 mục, 8 nhóm (tất cả từ tiengdong.com)

| Nhóm | Slug | Số lượng thật | Ví dụ |
| --- | --- | --- | --- |
| Văn phòng | `van-phong` | 15 | Âm thanh Gõ Bàn Phím máy tính; Tiếng Bàn Phím Máy Tính ở văn phòng làm việc; Tiếng gõ Bàn Phím chậm |
| Cười/Reaction | `cuoi-reaction` | 15 | Tiếng cười Hahaha… – Bác Gấu Vlog; Tiếng cười Troll; Tiếng Cười đểu (giọng trẻ con) |
| Meme punch/fail/dramatic | `meme-punch` | 15 | Sad Trombone Wah Wah Wah Fail sound effect; Fail sound effect; Dramatic sound |
| Câu nói viral Việt | `cau-noi-viral` | 10 | Âm thanh Trừ Lương TikTok; Nhạc chuông Sếp Ơi có điện thoại; Nhạc chuông Báo Cáo Sếp có điện thoại |
| Thiên nhiên/Động vật | `thien-nhien-dong-vat` | 10 | Tiếng chim hót Buổi Sáng; Tiếng Mưa Rơi; Tiếng Sóng Biển nhẹ nhàng |
| Công nghệ/UI | `cong-nghe-ui` | 10 | Âm thanh thông báo MP3; Âm thanh thông báo iOS 17; Âm thanh Thông báo, Cảnh báo công nghệ cao |
| Điện ảnh/Trailer | `dien-anh-trailer` | 10 | SFX Lê Tuấn Khang – Cinematic Tension Trailer; Nhạc Trailer Kịch Tính; Âm thanh Nhịp Trống trong trailer phim |
| Gia đình/Thành phố/Đời sống | `gia-dinh-doi-song` | 15 | Tiếng xe Ô tô chạy qua lại trên đường; Tiếng Xe Tải chạy qua lại ở đường phố; Tiếng Xe cộ qua lại trên đường Cao tốc |

- Sound viral (`viral: true`): **25/100** (xem `viral_note` trong map để biết vì
  sao viral; 25 mục có `viral_note` khác rỗng).
- Thời lượng (`duration_s`, đo bằng ffprobe thật): ngắn nhất **0,31s**, dài
  nhất **612,68s** (Tiếng Sóng Biển nhẹ nhàng). **25 sound dài hơn 30s** — xem
  mục [Chưa kiểm chứng](#chưa-kiểm-chứng).

### 3.2. Meme — 100 mục, 8 nhóm

| Nhóm | Slug | Số lượng thật | Ví dụ |
| --- | --- | --- | --- |
| Văn phòng/đi làm | `van-phong-di-lam` | 20 | Cố sống sót qua thứ Hai; Doge đi làm thứ 2; Mèo cam văn phòng mặt đơ |
| Mèo/chó/động vật | `meo-cho-dong-vat` | 20 | Mèo ngạc nhiên; Mèo bối rối; Thú cưng hài hước tỉnh dậy |
| Học tập/thi cử | `hoc-tap-thi-cu` | 10 | Gấu nâu chăm chỉ học bài; Lên bảng trả bài: học hay không học cũng khóc; Chúc thi tốt (THI TỐT!!) |
| Tình yêu/gia đình | `tinh-yeu-gia-dinh` | 10 | Chó "Tôi vẫn ổn" giữa biển lửa tiền nhà; Tall Hot Lady / Small Funny Guy — cặp đôi lệch chiều cao; Làm gì mẹ cũng than: dậy sớm, dậy muộn đều sai |
| Tiền bạc/lương | `tien-bac-luong` | 10 | Lương đã về, thỏ vui sướng; Tết cướp mất lương; Mở phong bì hết tiền mà lo |
| Thể thao/game | `the-thao-game` | 10 | PC vs Console vs Mobile; Leo rank Liên Quân vui; Ảnh chế bóng đá hài hước nhất |
| Du lịch/ăn uống | `du-lich-an-uong` | 10 | Kermit trên máy bay: xa mọi người 40.000 feet; Sẵn sàng làm việc đổi dặm bay; Bạn đồng hành: "Không xa đâu, đi bộ được" |
| Reaction chung | `reaction-chung` | 10 | Pikachu sốc tột độ; SpongeBob hét thất thanh; Tranh đen trắng mắt trợn vì sốc |

- Meme viral/trending (`viral_trending: true`): **58/100**.
- Định dạng ảnh: JPEG 71, PNG 13, WEBP 12, GIF 2, AVIF 2 (id 21, 22).
- Kích thước ảnh: nhỏ nhất 288×417, lớn nhất 1200×2221 (xem `width`/`height`
  từng mục trong map — ảnh đa số vuông/ngang, ghép dọc 1080×1920 cần
  crop hoặc đặt trên nền).

## 4. Cấu trúc thư mục (cây thật)

```text
kho-sound-meme/
├── README.md                  # file này
├── sounds.json                # tổng 100 sound (xem §5.3)
├── memes.json                 # tổng 100 meme (xem §5.3)
├── sounds/
│   ├── van-phong/             # 15 mp3 + sound-map.json
│   ├── cuoi-reaction/         # 15 mp3 + sound-map.json
│   ├── meme-punch/            # 15 mp3 + sound-map.json
│   ├── cau-noi-viral/         # 10 mp3 + sound-map.json
│   ├── thien-nhien-dong-vat/  # 10 mp3 + sound-map.json
│   ├── cong-nghe-ui/          # 10 mp3 + sound-map.json
│   ├── dien-anh-trailer/      # 10 mp3 + sound-map.json
│   └── gia-dinh-doi-song/     # 15 mp3 + sound-map.json
├── memes/
│   ├── van-phong-di-lam/      # 20 ảnh + meme-map.json
│   ├── meo-cho-dong-vat/      # 20 ảnh + meme-map.json
│   ├── hoc-tap-thi-cu/        # 10 ảnh + meme-map.json
│   ├── tinh-yeu-gia-dinh/     # 10 ảnh + meme-map.json
│   ├── tien-bac-luong/        # 10 ảnh + meme-map.json
│   ├── the-thao-game/         # 10 ảnh + meme-map.json
│   ├── du-lich-an-uong/       # 10 ảnh + meme-map.json
│   └── reaction-chung/        # 10 ảnh + meme-map.json
└── hidden_files/              # báo cáo tải gốc (không phải asset)
    ├── sounds-download-report.json   # 100 sound, kèm file_check + audit
    └── memes-download-report.json    # 100 meme, kèm file_output + verify_note
```

## 5. Schema JSON map

### 5.1. `sounds/<group_slug>/sound-map.json` — 1 file mỗi nhóm

```json
{
  "group": "Văn phòng",
  "group_slug": "van-phong",
  "count": 15,
  "items": [ { ...mỗi sound 1 object... } ]
}
```

Mỗi sound (trường nào cũng lấy từ báo cáo tải thật; `duration_s` là số ffprobe
thật, làm tròn 2 chữ số; `file` chỉ là **tên file**, không đường dẫn tuyệt đối):

| Trường | Kiểu | Nghĩa |
| --- | --- | --- |
| `name` | string | Tên sound (theo trang tiengdong.com) |
| `slug` | string | Slug trang tiengdong |
| `file` | string | Tên file MP3 trong cùng thư mục nhóm |
| `duration_s` | number | Thời lượng giây, ffprobe thật, 2 chữ số thập phân |
| `bytes` | number | Dung lượng file (byte) |
| `viral` | bool | Có phải sound viral không (theo research) |
| `viral_note` | string | Ghi chú vì sao viral (từ research; `""` nếu không có) |
| `source_url` | string | URL trang tiengdong của sound |
| `source_mp3` | string | URL file MP3 gốc đã tải về |
| `audit` | string | Kết quả audit: `"ok (...)"` hoặc `"FIXED (...)"` nếu file đã bị tải sai và sửa lại |

Ví dụ thật (mục đầu tiên của `sounds/van-phong/sound-map.json`):

```json
{
  "name": "Âm thanh Gõ Bàn Phím máy tính",
  "slug": "am-thanh-go-ban-phim-may-tinh",
  "file": "Am-thanh-tieng-go-ban-phim-may-tinh-www_tiengdong_com.mp3",
  "duration_s": 6.95,
  "bytes": 369225,
  "viral": false,
  "viral_note": "",
  "source_url": "https://tiengdong.com/am-thanh-go-ban-phim-may-tinh",
  "source_mp3": "https://tiengdong.com/wp-content/uploads/Am-thanh-tieng-go-ban-phim-may-tinh-www_tiengdong_com.mp3",
  "audit": "FIXED (article-post-2003): replaced wrong sidebar mp3 tieng-may-ban-hang-tu-dong-www_tiengdong_com.mp3 with page main player mp3"
}
```

### 5.2. `memes/<group_slug>/meme-map.json` — 1 file mỗi nhóm

```json
{
  "group": "Văn phòng/đi làm",
  "group_slug": "van-phong-di-lam",
  "count": 20,
  "items": [ { ...mỗi meme 1 object... } ]
}
```

Mỗi meme (`width`/`height`/`format` đo thật bằng PIL, riêng 2 file AVIF đo
bằng ffprobe; `file` chỉ là **tên file**):

| Trường | Kiểu | Nghĩa |
| --- | --- | --- |
| `id` | number | ID 1–100 (khớp research gốc) |
| `title_vi` | string | Tiêu đề tiếng Việt |
| `desc_vi` | string | Mô tả ảnh (từ research) |
| `use_case` | string | Gợi ý lúc nào dùng (từ research) |
| `file` | string | Tên file ảnh trong cùng thư mục nhóm |
| `width` / `height` | number | Kích thước pixel đo thật |
| `format` | string | JPEG / PNG / WEBP / GIF / AVIF (loại thật do PIL/`file` đọc được) |
| `bytes` | number | Dung lượng file (byte) |
| `viral_trending` | bool | Có phải meme viral/trending không |
| `viral_note` | string | Ghi chú vì sao viral (từ research) |
| `source_url` | string | URL ảnh gốc đã tải về |
| `page` | string | URL trang chứa meme (có thể `""` nếu research không có trang nguồn) |

Ví dụ thật (mục đầu tiên của `memes/van-phong-di-lam/meme-map.json`):

```json
{
  "id": 1,
  "title_vi": "Cố sống sót qua thứ Hai",
  "desc_vi": "Nhân vật hoạt hình ngồi ở bàn làm việc chất đầy giấy tờ, chú thích 'ME TRYING TO SURVIVE MONDAY LIKE...'",
  "use_case": "Đăng sáng thứ 2, than mệt đầu tuần",
  "file": "001-co-song-sot-qua-thu-hai.png",
  "width": 1024,
  "height": 1024,
  "format": "PNG",
  "bytes": 1860064,
  "viral_trending": true,
  "viral_note": "Template 'survive Monday' quen thuộc trên các trang meme; MemeChor chuyên mục meme thứ 2",
  "source_url": "https://cdn.memechor.com/meme/1735569822935-1735569822944.jpg",
  "page": "https://www.memechor.com/meme/monday-meme-the-hilarious-struggle-we-all-face-6772b19ff1370dae2f1f8d8a"
}
```

Lưu ý: `file` có thể khác đuôi so với `source_url` — 5 mục đổi đuôi theo loại
thật do PIL đọc được (vd `source_url` là `.jpg` nhưng file thật là `.png`);
luôn dùng `file` + `format` trong map, đừng suy đuôi từ URL.

### 5.3. File tổng ở root

- `sounds.json`: `{"total": 100, "items": [...]}` — mỗi mục = đúng các trường
  của map nhóm (§5.1) **cộng thêm** `group` + `group_slug`.
- `memes.json`: `{"total": 100, "items": [...]}` — mỗi mục = đúng các trường
  của map nhóm (§5.2) **cộng thêm** `group` + `group_slug`.
- File tổng và các map nhóm khớp nhau 100% (cùng 100 sound + 100 meme, đối
  chiếu theo `group_slug` + `file`).

## 6. Cách agent chọn asset

1. **Chọn nhóm trước** theo chủ đề video (`group_slug` trong `sounds.json` /
   `memes.json`, hoặc mở thẳng `sound-map.json` / `meme-map.json` trong thư
   mục nhóm).
2. **Ưu tiên viral**: sound thì lọc `viral == true` (25 mục), đọc `viral_note`
   để biết ngữ cảnh; meme thì lọc `viral_trending == true` (58 mục).
3. **Sound — lọc theo `duration_s`** (ffprobe thật):
   - Punchline/reaction ngắn: `duration_s` nhỏ (vd < 5s).
   - Nhạc nền/ambience: `duration_s` lớn — lưu ý **25 sound dài hơn 30s**,
     dài nhất 612,68s (tiếng sóng biển); đừng lấy nhầm ambience dài làm
     punchline. Cắt/loop bằng ffmpeg khi cần.
   - Kiểm tra `audit`: mục nào có chuỗi bắt đầu bằng `FIXED` là file đã từng
     tải sai và đã được sửa lại từ player chính của đúng trang — dùng bình
     thường, nhưng nếu nghe thấy nội dung lạ thì báo lại (xem §8).
4. **Meme — lọc theo `width`/`height` + `format`**:
   - Ghép dọc 1080×1920: ưu tiên ảnh vuông/dọc có `width` ≥ 720; ảnh ngang
     nhỏ cần crop hoặc đặt trên nền.
   - `format` AVIF (id 21, 22) cần convert sang PNG/JPG trước khi đưa vào
     editor/video pipeline không đọc được AVIF.
   - Đọc `desc_vi` + `use_case` để chọn đúng ngữ cảnh, đừng chỉ chọn theo
     `title_vi`.
5. **Đường dẫn file thật**: `sounds/<group_slug>/<file>` và
   `memes/<group_slug>/<file>` — `file` trong map là tên file, ghép với
   `group_slug` là ra đường dẫn tương đối từ root repo. Không đoán tên file
   ngoài map.
6. **Muốn xem lại nguồn gốc**: sound dùng `source_url` (trang tiengdong) /
   `source_mp3`; meme dùng `source_url` (URL ảnh) / `page` (trang chứa meme).

## 7. Nguồn

- **Sound (100/100): tiengdong.com** — mỗi mục tải từ file MP3 của player
  chính trên đúng trang tiengdong của sound đó (`source_mp3` trong map).
- **Meme (100 mục): nhiều trang meme**, khác nhau theo nhóm (ghi theo trường
  `source` trong research gốc; `source_url` từng mục trong map là URL ảnh
  thật đã tải):
  - `van-phong-di-lam` (20): Pinterest ×2, Giphy ×2, MemeChor, GifVibe,
    Cheezburger, Imgflip, Petmaya, CafeLand, AnhNail, KhoAnhDep, QuanTriMang,
    Pancake, Piximus, ThriveMyWay, Digital Mom Blog, Similuxes, BaoMoi, TinhTe.
  - `meo-cho-dong-vat` (20): Imgflip ×3, MemeBoat (ImageKit) ×2, Bored Panda
    ×2, StingWorld ×2, HoiChimTroi ×2, Cheezburger ×2, VanVN, SForum, Vecteezy,
    Pinterest, Meme-Arsenal, Awkward.com, AnhNgheThuatDuLich.
  - `hoc-tap-thi-cu` (10): MemeChor ×2, Kenh14 ×2, anhnghethuatdulich.com,
    Pinterest/xaydungso.vn, MyTour/SForum, Pinterest, aztruyen.top, Imgflip.
  - `tinh-yeu-gia-dinh` (10): mỗi trang 1 ảnh — Bò và Gấu (bovagau.vn), Know
    Your Meme, truyen247.pro, Kenh14, SForum/CellphoneS, TVOvermind, MyTour,
    ZaloPay, anhnghethuatdulich.com, Tripi.
  - `tien-bac-luong` (10): khoanhdep.com ×2, Dân Trí, Tuổi Trẻ, Broke But
    Laughing (Blogspot), Imgflip, Giphy, Tinh Tế, Người Đưa Tin, 9GAG.
  - `the-thao-game` (10): mỗi trang 1 ảnh — 9GAG, shopgarena.net, 24h Thể
    Thao, Cheezburger, Pleated Jeans, GameHub, XemGame, GameDesigning,
    BongDa.com.vn, Imgflip.
  - `du-lich-an-uong` (10): BuzzFeed ×2, Loknam, The Takeoff Nap, TopiPhone
    (repost, watermark BoredPanda), Kenh14, Leslie's Travel Snacks, BoredPanda
    (via Mavink), Pleated Jeans, MauBanhKem.
  - `reaction-chung` (10): AnhNgheThuatDuLich (ảnh host tại CongCu.online)
    ×2, Know Your Meme, VJOL (ảnh host tại BangChuCai), VNTrade, MyTour/Tripi,
    ImgTag, Sforum (CellphoneS), ThuThuatPhanMem/Tripi, AnhAnime.

## 8. ⚠️ Cảnh báo bản quyền

- **Tiengdong cảnh báo: vài meme/nhạc nền trong kho có thể dính bản quyền
  trên TikTok / YouTube / Facebook.** Người dùng tự chịu trách nhiệm khi đăng
  — kiểm tra lại chính sách nền tảng trước khi đăng video thương mại, và gỡ /
  thay asset nếu nền tảng báo vi phạm.
- **Meme dùng nhân vật có IP hãng — chỉ dùng làm reaction ngắn, KHÔNG nhận là
  ảnh tự làm.** Các nhân vật có trong kho này (kiểm chứng theo `title_vi` /
  `desc_vi` trong research): SpongeBob (id 17, 65, 92), Minion (id 9),
  Pikachu (id 91), Doge (id 2, 15, 16), Grumpy Cat (id 4), Conan (id 46).
  Không dùng các ảnh này làm logo/thumbnail đại diện kênh hay bán lại.
- **Âm thanh có bản quyền gốc — chỉ dùng làm hiệu ứng ngắn, không nhận là âm
  thanh tự làm:** `OOF sound effect` (Roblox OOF,
  `sounds/meme-punch/Oof-sound-effect-www_tiengdong_com.mp3`) và `Windows XP
  error sound effect`
  (`sounds/meme-punch/windows-xp-error-sound-effect-www_tiengdong_com.mp3`).

## 9. Đã verify (bằng chứng đo thật)

- **Sound — 100/100**: mỗi file MP3 verify bằng lệnh `file` (đúng MPEG audio,
  có ID3) + `ffprobe` đo `duration_s` thật (xem `file_check` + `duration_s`
  trong `hidden_files/sounds-download-report.json`). Báo cáo ghi
  `total: 100, downloaded: 100, missing_count: 0, total_bytes: 71789673`.
- **Audit sound — 100 mục đã audit: 90 kept (`ok`), 10 fixed, 0 unresolved.**
  10 slug đã sửa (tải sai file rồi tải lại đúng từ player chính của trang):
  `am-thanh-go-ban-phim-may-tinh`, `tieng-click-chuot`, `tieng-vo-tay`,
  `tieng-huyt-sao`, `fail-sound-effect`, `boom-sound-effect`,
  `oof-sound-effect`, `tieng-chim-hot-buoi-sang`,
  `tieng-buoc-chan-di-len-cau-thang`, `tieng-chuong-cua`. Xem trường `audit`
  trong từng map nhóm.
- **Meme — 100/100**: mỗi ảnh verify bằng `file` + PIL đọc được loại thật,
  `width`/`height`/`format` (xem `file_output` trong
  `hidden_files/memes-download-report.json`). Báo cáo ghi `total_items: 100,
  downloaded_ok: 100, missing: 0, total_bytes_ok: 27390356`.
  - 2 file AVIF (id 21, 22 — "Mèo ngạc nhiên", "Mèo bối rối"): PIL Pillow
    10.2.0 không decode được AVIF (thiếu pillow-avif-plugin) nên verify bằng
    `file` + ffprobe (codec av1, 897×600 và 600×600) — giữ nguyên
    `width`/`height` trong báo cáo.
  - 5 mục đổi đuôi file theo loại thật do PIL đọc được
    (`ext_changed_from_research: true`); id 85 lần 1 trả về HTML, lần 2 trả
    về JPEG thật.
- **Map JSON — verify sau khi tạo** (xem §10): `python3 -m json.tool` pass
  18/18 file; số mục trong map khớp đúng số file thật trên đĩa từng nhóm;
  file tổng khớp map nhóm; 0 file trong map bị thiếu trên đĩa.

## 10. Chưa kiểm chứng

- **Chưa nghe bằng tai từng sound để khớp tên với nội dung.** Bằng chứng hiện
  có chỉ chứng minh file MP3 lấy từ **player chính của đúng trang tiengdong**
  của sound đó (audit đã loại 10 file tải sai từ sidebar/trang khác). Cách
  kiểm chứng: mở nghe từng file MP3 trong `sounds/<nhóm>/` và đối chiếu với
  `name` trong map.
- **Chưa xem bằng mắt từng ảnh meme.** Bằng chứng hiện có chỉ verify **loại
  file + kích thước pixel** (`file` + PIL/ffprobe), không xác nhận nội dung
  ảnh đúng như `title_vi`/`desc_vi`. Cách kiểm chứng: mở xem từng ảnh trong
  `memes/<nhóm>/` và đối chiếu với `desc_vi` trong map.
- **25 sound có `duration_s` > 30s** (đếm lại từ `sounds.json`), dài nhất
  **612,68s (≈612,7s) — "Tiếng Sóng Biển nhẹ nhàng"** (`thien-nhien-dong-vat`).
  Đây là ambience dài, không phải punchline ngắn — agent chọn asset cần lọc
  theo `duration_s` như §6.3.
- `viral` / `viral_note` (sound) và `viral_trending` / `viral_note` (meme) lấy
  từ **research gốc, không đo lại lượt xem/lượt tải** — chỉ là ghi chú định
  tính ("quen thuộc trên TikTok", "template viral"...), không phải số liệu
  lượt xem thật.
