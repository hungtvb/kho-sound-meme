#!/usr/bin/env python3
"""Find sounds / memes in kho-sound-meme, fast.

Usage (run from the repo root, no dependencies, stdlib only):

    python3 find.py sound <keyword>            # search sounds by name
    python3 find.py meme <keyword>             # search memes by title/desc
    python3 find.py sound --group van-phong --viral --max 5
    python3 find.py meme --group meo-cho-dong-vat --viral
    python3 find.py groups                     # list all groups + counts
    python3 find.py random sound --viral       # pick one random viral sound
    python3 find.py random meme --group reaction-chung

Add --json to get machine-readable output (for agents / scripts).
Search is Vietnamese-insensitive: "cuoi" matches "cười", "meo" matches "mèo".
"""
import argparse
import json
import random
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOUNDS_FILE = ROOT / "sounds.json"
MEMES_FILE = ROOT / "memes.json"


def norm(text: str) -> str:
    """Lowercase + strip Vietnamese diacritics, so 'cuoi' matches 'cười'."""
    if not isinstance(text, str):
        return ""
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def load(kind: str) -> list:
    path = SOUNDS_FILE if kind == "sound" else MEMES_FILE
    if not path.exists():
        print(f"Missing {path.name} — run from the repo root.", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)["items"]


def search_fields(item: dict, kind: str) -> str:
    if kind == "sound":
        return " ".join([item.get("name", ""), item.get("slug", ""),
                         item.get("viral_note", ""), " ".join(item.get("tags", []))])
    return " ".join([item.get("title_vi", ""), item.get("desc_vi", ""),
                     item.get("use_case", ""), item.get("viral_note", "")])


def is_viral(item: dict, kind: str) -> bool:
    return bool(item.get("viral" if kind == "sound" else "viral_trending"))


def path_of(item: dict, kind: str) -> str:
    folder = "sounds" if kind == "sound" else "memes"
    return f"{folder}/{item['group_slug']}/{item['file']}"


def fmt_sound(item: dict) -> str:
    star = "🔥 " if item.get("viral") else ""
    return (f"{star}{item['name']} | {item['duration_s']}s | "
            f"{item['group']} | {path_of(item, 'sound')}")


def fmt_meme(item: dict) -> str:
    star = "🔥 " if item.get("viral_trending") else ""
    return (f"{star}#{item['id']} {item['title_vi']} | "
            f"{item['width']}x{item['height']} {item['format']} | "
            f"{item['group']} | {path_of(item, 'meme')}")


def fmt(item: dict, kind: str) -> str:
    return fmt_sound(item) if kind == "sound" else fmt_meme(item)


def item_kind(item: dict) -> str:
    """'original' or 'clip'; items from before 2026-11-18 have no field."""
    return item.get("kind", "original")


def apply_filters(items: list, kind: str, args) -> list:
    out = items
    if args.group:
        out = [i for i in out if i["group_slug"] == args.group]
    if args.viral:
        out = [i for i in out if is_viral(i, kind)]
    if getattr(args, "kind_filter", None) and kind == "sound":
        out = [i for i in out if item_kind(i) == args.kind_filter]
    if getattr(args, "tag", None):
        needle = norm(args.tag)
        out = [i for i in out
               if any(needle in norm(t) for t in i.get("tags_ascii", []) + i.get("tags", []))]
    if args.keyword:
        needle = norm(args.keyword)
        out = [i for i in out if needle in norm(search_fields(i, kind))]
    if kind == "sound":
        if args.min is not None:
            out = [i for i in out if i["duration_s"] >= args.min]
        if args.max is not None:
            out = [i for i in out if i["duration_s"] <= args.max]
    else:
        if args.min_width is not None:
            out = [i for i in out if i["width"] >= args.min_width]
        if args.portrait:
            out = [i for i in out if i["height"] > i["width"]]
        if args.square:
            out = [i for i in out if i["width"] == i["height"]]
    # Viral first, then clips before originals, then shortest (sounds) / biggest (memes).
    if kind == "sound":
        out.sort(key=lambda i: (not is_viral(i, kind), item_kind(i) != "clip",
                                i["duration_s"]))
    else:
        out.sort(key=lambda i: (not is_viral(i, kind), -i["width"]))
    return out


def print_results(items: list, kind: str, args):
    shown = items[: args.limit]
    if args.json:
        for item in shown:
            print(json.dumps({**item, "path": path_of(item, kind)},
                             ensure_ascii=False))
        return
    if not shown:
        print("Không tìm thấy. Thử bỏ bớt bộ lọc hoặc gõ từ khóa khác.")
        return
    for item in shown:
        print(fmt(item, kind))
    if len(items) > len(shown):
        print(f"... và {len(items) - len(shown)} kết quả khác "
              f"(tổng {len(items)}). Thêm --limit N để xem thêm.")


def cmd_search(kind: str, args):
    items = apply_filters(load(kind), kind, args)
    print_results(items, kind, args)


def cmd_random(kind: str, args):
    items = apply_filters(load(kind), kind, args)
    if not items:
        print("Không tìm thấy. Thử bỏ bớt bộ lọc hoặc gõ từ khóa khác.")
        return
    item = random.choice(items)
    if args.json:
        print(json.dumps({**item, "path": path_of(item, kind)},
                         ensure_ascii=False))
    else:
        print(fmt(item, kind))


def cmd_groups(_args):
    for kind, path in (("sound", SOUNDS_FILE), ("meme", MEMES_FILE)):
        items = load(kind)
        print(f"== {kind} ({len(items)}) ==")
        groups = {}
        for item in items:
            groups.setdefault((item["group_slug"], item["group"]), 0)
            groups[(item["group_slug"], item["group"])] += 1
        for (slug, name), count in sorted(groups.items()):
            print(f"  {slug:<22} {count:>3}  {name}")


def add_common(parser):
    parser.add_argument("keyword", nargs="?", default=None,
                        help="từ khóa tìm trong tên/mô tả (không dấu vẫn được)")
    parser.add_argument("--group", help="chỉ lấy 1 nhóm, vd: van-phong")
    parser.add_argument("--viral", action="store_true",
                        help="chỉ lấy asset viral/trending")
    parser.add_argument("--limit", type=int, default=10,
                        help="số kết quả tối đa (mặc định 10)")
    parser.add_argument("--json", action="store_true",
                        help="in ra JSON từng dòng, để agent/script đọc")


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="find.py",
        description="Tìm nhanh sound / meme trong kho-sound-meme.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_sound = sub.add_parser("sound", help="tìm sound effect")
    add_common(p_sound)
    p_sound.add_argument("--min", type=float, help="thời lượng tối thiểu (giây)")
    p_sound.add_argument("--max", type=float, help="thời lượng tối đa (giây)")
    p_sound.add_argument("--kind", dest="kind_filter", choices=["original", "clip"],
                         help="chỉ lấy file gốc (original) hoặc đoạn cắt (clip)")
    p_sound.add_argument("--tag", help="lọc theo tag, không dấu vẫn được, vd: --tag cuoi")

    p_meme = sub.add_parser("meme", help="tìm ảnh meme")
    add_common(p_meme)
    p_meme.add_argument("--tag", help="lọc theo tag, không dấu vẫn được, vd: --tag meo")
    p_meme.add_argument("--min-width", type=int,
                        help="chiều rộng tối thiểu (pixel)")
    p_meme.add_argument("--portrait", action="store_true",
                        help="chỉ lấy ảnh dọc (cao hơn rộng)")
    p_meme.add_argument("--square", action="store_true",
                        help="chỉ lấy ảnh vuông")

    p_random = sub.add_parser("random", help="chọn ngẫu nhiên 1 asset")
    p_random.add_argument("kind", choices=["sound", "meme"])
    add_common(p_random)
    p_random.add_argument("--min", type=float)
    p_random.add_argument("--max", type=float)
    p_random.add_argument("--kind", dest="kind_filter", choices=["original", "clip"])
    p_random.add_argument("--tag")
    p_random.add_argument("--min-width", type=int)
    p_random.add_argument("--portrait", action="store_true")
    p_random.add_argument("--square", action="store_true")

    sub.add_parser("groups", help="liệt kê tất cả nhóm + số lượng")

    args = parser.parse_args(argv)
    # random reuses the same filter fields; meme-only flags are harmless.
    if not hasattr(args, "min"):
        args.min = args.max = None
    if not hasattr(args, "min_width"):
        args.min_width = None
        args.portrait = args.square = False

    if args.cmd == "sound":
        cmd_search("sound", args)
    elif args.cmd == "meme":
        cmd_search("meme", args)
    elif args.cmd == "random":
        cmd_random(args.kind, args)
    elif args.cmd == "groups":
        cmd_groups(args)


if __name__ == "__main__":
    main()
