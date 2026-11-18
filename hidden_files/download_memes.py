#!/usr/bin/env python3
"""Download 100 memes from ~/workspace/meme-diverse-100/meme-diverse-100.json
per task spec. Uses curl -L UA Mozilla/5.0, timeout 30s, retry 1.
Verifies with `file` + PIL. Writes report JSON."""
import json, os, re, subprocess, unicodedata, sys
from pathlib import Path

SRC = Path.home() / "workspace/meme-diverse-100/meme-diverse-100.json"
BASE = Path.home() / "workspace/kho-sound-meme/memes"
REPORT = Path.home() / "workspace/kho-sound-meme/hidden_files/memes-download-report.json"
LOG = Path.home() / "workspace/kho-sound-meme/hidden_files/memes-download.log"

GROUP_MAP = {
    "Văn phòng/đi làm": "van-phong-di-lam",
    "Mèo/chó/động vật": "meo-cho-dong-vat",
    "Học tập/thi cử": "hoc-tap-thi-cu",
    "Tình yêu/gia đình": "tinh-yeu-gia-dinh",
    "Tiền bạc/lương": "tien-bac-luong",
    "Thể thao/game": "the-thao-game",
    "Du lịch/ăn uống": "du-lich-an-uong",
    "Reaction chung": "reaction-chung",
}
CT_EXT = {
    "image/jpeg": "jpg", "image/png": "png", "image/gif": "gif",
    "image/webp": "webp", "image/avif": "avif",
}
PIL_FMT_EXT = {"JPEG": "jpg", "PNG": "png", "GIF": "gif", "WEBP": "webp", "AVIF": "avif"}

def slugify(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("đ", "d").replace("Đ", "d").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    return s[:60].rstrip("-") or "meme"

def main():
    items = json.loads(SRC.read_text(encoding="utf-8"))
    assert len(items) == 100, f"expected 100 items, got {len(items)}"
    from PIL import Image
    results, missing = [], []
    log_lines = []
    for it in items:
        mid = it["id"]
        gslug = GROUP_MAP[it["group"]]
        slug = slugify(it["title_vi"])
        ext0 = CT_EXT.get(it.get("content_type", ""), "jpg")
        d = BASE / gslug
        d.mkdir(parents=True, exist_ok=True)
        tmp = d / f".tmp-{mid:03d}"
        fname0 = f"{mid:03d}-{slug}.{ext0}"
        url = it["url"]
        # curl: -L, UA Mozilla/5.0, --max-time 30, --retry 1, capture http code
        cmd = ["curl", "-L", "-A", "Mozilla/5.0", "--max-time", "30", "--retry", "1",
               "-s", "-S", "-w", "\n%{http_code}", "-o", str(tmp), url]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        out = (p.stdout or "").strip()
        http_code = out.splitlines()[-1] if out else ""
        curl_err = (p.stderr or "").strip()
        entry = {"id": mid, "group": it["group"], "group_slug": gslug,
                 "title_vi": it["title_vi"], "page": it.get("page"),
                 "source_url": url, "research_content_type": it.get("content_type"),
                 "http_code": http_code, "curl_stderr": curl_err,
                 "file": None, "bytes": None, "width": None, "height": None,
                 "format": None, "file_output": None, "viral_trending": it.get("viral_trending"),
                 "status": None, "error": None}
        ok = False
        if p.returncode != 0 or http_code != "200" or not tmp.exists() or tmp.stat().st_size == 0:
            entry["status"] = "missing"
            entry["error"] = f"curl rc={p.returncode} http={http_code!r} stderr={curl_err!r} size={tmp.stat().st_size if tmp.exists() else 'no-file'}"
            if tmp.exists():
                tmp.unlink()
        else:
            # file command
            f = subprocess.run(["file", "-b", str(tmp)], capture_output=True, text=True)
            entry["file_output"] = (f.stdout or "").strip()
            try:
                with Image.open(tmp) as im:
                    im.load()
                    fmt = im.format
                    w, h = im.size
                real_ext = PIL_FMT_EXT.get(fmt)
                if real_ext is None:
                    entry["status"] = "missing"
                    entry["error"] = f"PIL format {fmt!r} not in allowed image types; file={entry['file_output']}"
                    tmp.unlink()
                else:
                    final = d / f"{mid:03d}-{slug}.{real_ext}"
                    if tmp != final:
                        tmp.rename(final)
                    entry.update({"file": str(final), "bytes": final.stat().st_size,
                                  "width": w, "height": h, "format": fmt,
                                  "status": "ok",
                                  "ext_changed_from_research": (real_ext != ext0)})
                    ok = True
            except Exception as e:
                entry["status"] = "missing"
                entry["error"] = f"not a valid image per PIL: {e}; file={entry['file_output']}"
                if tmp.exists():
                    tmp.unlink()
        if not ok:
            missing.append({"id": mid, "title_vi": it["title_vi"], "group": it["group"],
                            "url": url, "error": entry["error"], "http_code": http_code})
        results.append(entry)
        line = f"id={mid:03d} status={entry['status']} http={http_code} file={entry['file']} bytes={entry['bytes']} {entry['width']}x{entry['height']} fmt={entry['format']} err={entry['error']}"
        log_lines.append(line)
        print(line, flush=True)
    ok_n = sum(1 for r in results if r["status"] == "ok")
    total_bytes = sum(r["bytes"] for r in results if r["bytes"])
    report = {"total_items": len(items), "downloaded_ok": ok_n, "missing": len(missing),
              "total_bytes_ok": total_bytes,
              "missing_list": missing,
              "items": results}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    LOG.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(f"SUMMARY ok={ok_n}/100 missing={len(missing)} total_bytes={total_bytes}")
    print(f"missing ids: {[m['id'] for m in missing]}")

if __name__ == "__main__":
    main()
