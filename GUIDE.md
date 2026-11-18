# Guide — Tìm nhanh sound / meme trong kho-sound-meme

Dùng 1 lệnh duy nhất: `find.py`. Không cần cài gì thêm, chỉ cần Python 3
(chỉ dùng thư viện chuẩn). Chạy từ thư mục gốc của repo đã clone.

```bash
git clone https://github.com/hungtvb/kho-sound-meme.git
cd kho-sound-meme
```

## Lệnh nhanh

| Muốn gì | Lệnh |
| --- | --- |
| Xem tất cả nhóm + số lượng | `python3 find.py groups` |
| Tìm sound theo từ khóa | `python3 find.py sound cười` |
| Tìm meme theo từ khóa | `python3 find.py meme mèo` |
| Sound viral, ngắn ≤ 5 giây | `python3 find.py sound --viral --max 5` |
| Sound 1 nhóm, viral | `python3 find.py sound --group van-phong --viral` |
| Meme 1 nhóm, viral | `python3 find.py meme --group meo-cho-dong-vat --viral` |
| Meme dọc (ghép video 1080×1920) | `python3 find.py meme --portrait --min-width 720` |
| Meme vuông | `python3 find.py meme --square` |
| Chọn ngẫu nhiên 1 cái | `python3 find.py random sound --viral` |
| Chọn ngẫu nhiên 1 meme 1 nhóm | `python3 find.py random meme --group reaction-chung` |
| Xem nhiều kết quả hơn | Thêm `--limit 20` (mặc định 10) |
| Lấy kết quả dạng JSON (cho agent/script) | Thêm `--json` |

Tìm kiếm **không phân biệt dấu**: gõ `cuoi`, `meo`, `thu hai` đều ra
`cười`, `mèo`, `thứ Hai`.

## Ví dụ thật

```bash
# Punchline fail ngắn, viral nhất
python3 find.py sound --viral --max 5
# → 🔥 Tiếng đánh Rắm meme | 0.31s | sounds/meme-punch/...

# Tiếng cười để chêm vào đoạn sếp mắng
python3 find.py sound cuoi --limit 5

# Meme mèo ngạc nhiên, viral
python3 find.py meme meo --viral --limit 5

# Meme văn phòng cho video thứ 2 đầu tuần
python3 find.py meme --group van-phong-di-lam --viral
```

Kết quả in ra luôn **đường dẫn file thật** trong repo, vd:
`sounds/meme-punch/pop-sound-effect-www_tiengdong_com.mp3`.
Dùng đúng đường dẫn đó, đừng đoán tên file ngoài danh sách.

## Bộ lọc đầy đủ

Sound: `--group <slug>`, `--viral`, `--min <giây>`, `--max <giây>`.
Meme: `--group <slug>`, `--viral`, `--min-width <pixel>`, `--portrait`, `--square`.
Chung: `--limit N`, `--json`.

Kết quả xếp theo thứ tự: **viral trước**, rồi sound ngắn trước / meme rộng trước.

## Cho agent: copy đoạn này vào prompt

> Repo `kho-sound-meme` đã clone ở thư mục hiện tại. Khi cần sound hoặc
> meme, **đừng đoán tên file, đừng mở hết file JSON để đọc**. Chạy
> `python3 find.py` theo guide trong `GUIDE.md`:
> - `python3 find.py sound <từ khóa> --viral --max 5 --json` cho sound ngắn viral
> - `python3 find.py meme <từ khóa> --viral --json` cho meme viral
> - Lọc nhóm bằng `--group <slug>` (xem slug bằng `python3 find.py groups`)
> - Lấy `path` trong kết quả JSON làm đường dẫn file thật để dùng.
> - Sound dài > 30s là ambience, không dùng làm punchline. Meme AVIF
> (id 21, 22) cần convert sang PNG/JPG trước khi đưa vào editor.

## Lưu ý

- `find.py` chỉ đọc `sounds.json` / `memes.json` ở cùng thư mục, không tải
  gì từ mạng, không sửa file nào.
- Sau mỗi lần repo cập nhật (thêm/bớt asset), chạy lại lệnh là ra dữ liệu mới.
- Chi tiết schema JSON map, bản quyền, đã verify / chưa verify: xem `README.md`.
