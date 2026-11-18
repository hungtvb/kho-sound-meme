"""Resume download100.py after runtime restart killed it at item 40/100.
Recovers items 1-39 from download100.log (chosen URL + filename + bytes +
duration) and RE-VERIFIES each file on disk with fresh `file` + ffprobe.
Items 40-100 (and any recovered item failing verification) are downloaded
with the same verified method as download100.py. No invented URLs.
"""
import re, os, json, urllib.request, urllib.parse, time, subprocess

BASE = os.path.expanduser("~/workspace/kho-sound-meme")
SRC = os.path.expanduser("~/workspace/tiengdong-sounds/research/diverse-100.json")
LOG = os.path.join(BASE, "hidden_files", "download100.log")
GROUP_SLUG = {
    "Văn phòng": "van-phong",
    "Cười/Reaction": "cuoi-reaction",
    "Meme punch/fail/dramatic": "meme-punch",
    "Gia đình/Thành phố/Đời sống": "gia-dinh-doi-song",
    "Câu nói viral Việt": "cau-noi-viral",
    "Thiên nhiên/Động vật": "thien-nhien-dong-vat",
    "Công nghệ/UI": "cong-nghe-ui",
    "Điện ảnh/Trailer": "dien-anh-trailer",
}
HDR = {"User-Agent": "Mozilla/5.0"}

def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers=HDR)
    return urllib.request.urlopen(req, timeout=timeout)

def find_mp3s(html):
    mp3s = re.findall(r'https://tiengdong\.com/wp-content/uploads/[^"\'<> ]+\.mp3', html)
    seen = []
    for m in mp3s:
        m = m.split("?")[0].replace("&amp;", "&")
        if m not in seen:
            seen.append(m)
    return seen

def probe(path):
    try:
        fc = subprocess.run(["file", path], capture_output=True, text=True, timeout=30)
        file_check = (fc.stdout or fc.stderr).strip()
    except Exception as e:
        file_check = f"file command error: {e}"
    try:
        p = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, timeout=30)
        dur = p.stdout.strip()
        if p.returncode == 0 and dur:
            return file_check, round(float(dur), 3), None
        return file_check, None, f"ffprobe rc={p.returncode} stderr={p.stderr.strip()}"
    except Exception as e:
        return file_check, None, f"ffprobe error: {e}"

def parse_old_log():
    """slug -> {source_mp3, fname, bytes, duration} for items with a '->' line."""
    done = {}
    cur_slug = None
    cur_url = None
    with open(LOG, encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = re.match(r"\[\d+/100\] (\S+) mp3 candidates=\d+ chosen=(\S+)", line)
            if m:
                cur_slug, cur_url = m.group(1), m.group(2)
                continue
            m = re.match(r"  -> (\S+) (\d+) bytes duration=([\d.]+) \|", line)
            if m and cur_slug:
                done[cur_slug] = {"source_mp3": cur_url, "fname": m.group(1),
                                  "bytes": int(m.group(2)),
                                  "duration": float(m.group(3))}
                cur_slug = None
    return done

def download_one(it, gslug, used):
    """Normal path (same as download100.py). Returns record dict."""
    slug, page, name = it["slug"], it["url"], it["name"]
    dest_dir = os.path.join(BASE, "sounds", gslug)
    os.makedirs(dest_dir, exist_ok=True)
    rec = {"group": it["group"], "group_slug": gslug, "name": name, "slug": slug,
           "page_url": page, "source_mp3": None, "file": None,
           "bytes": None, "duration_s": None,
           "viral": it.get("viral", False), "file_check": None}
    try:
        html = None
        last_err = None
        for _ in range(2):
            try:
                html = fetch(page).read().decode("utf-8", errors="ignore")
                break
            except Exception as e:
                last_err = e
                time.sleep(2)
        if html is None:
            raise RuntimeError(f"page fetch failed: {last_err}")
        mp3s = find_mp3s(html)
        chosen = None
        stem = slug[:25]
        for m in mp3s:
            if stem in m or slug.replace("-", "")[:15] in m.replace("-", ""):
                chosen = m
                break
        if not chosen and mp3s:
            chosen = mp3s[0]
        print(f"{slug} mp3 candidates={len(mp3s)} chosen={chosen}", flush=True)
        if not chosen:
            rec["file_check"] = "ERROR: no mp3 found in page HTML"
            return rec
        rec["source_mp3"] = chosen
        fname = urllib.parse.unquote(os.path.basename(chosen))
        if fname in used or os.path.exists(os.path.join(dest_dir, fname)):
            base_name, ext = os.path.splitext(fname)
            n = 2
            while f"{base_name}-{n}{ext}" in used or os.path.exists(
                    os.path.join(dest_dir, f"{base_name}-{n}{ext}")):
                n += 1
            fname = f"{base_name}-{n}{ext}"
            print(f"  duplicate filename -> renamed to {fname}", flush=True)
        out = os.path.join(dest_dir, fname)
        last_err = None
        ok_dl = False
        for _ in range(2):
            try:
                req = urllib.request.Request(chosen, headers=HDR)
                with urllib.request.urlopen(req, timeout=60) as r, open(out, "wb") as fh:
                    while True:
                        chunk = r.read(65536)
                        if not chunk:
                            break
                        fh.write(chunk)
                ok_dl = True
                break
            except Exception as e:
                last_err = e
                time.sleep(2)
        if not ok_dl:
            raise RuntimeError(f"mp3 download failed: {last_err}")
        used.add(fname)
        size = os.path.getsize(out)
        fc, dur, perr = probe(out)
        rec["file"] = f"sounds/{gslug}/{fname}"
        rec["bytes"] = size
        rec["duration_s"] = dur
        rec["file_check"] = fc + (f" | ffprobe ERROR: {perr}" if perr else "")
        print(f"  -> {fname} {size} bytes duration={dur} | {fc}", flush=True)
        if perr or dur is None:
            print(f"  !! VERIFY PROBLEM: {perr}", flush=True)
    except Exception as e:
        rec["file_check"] = f"ERROR: {e}"
        print(f"{slug} ERROR {e}", flush=True)
    return rec

def main():
    with open(SRC, encoding="utf-8") as f:
        items = json.load(f)
    done = parse_old_log()
    print(f"RECOVERED from old log: {len(done)} items with '->' lines", flush=True)
    results = []
    # seed used-names per group from files already on disk
    used_map = {}
    for gslug in set(GROUP_SLUG.values()):
        d = os.path.join(BASE, "sounds", gslug)
        used_map[gslug] = set(os.listdir(d)) if os.path.isdir(d) else set()
    for i, it in enumerate(items, 1):
        gslug = GROUP_SLUG[it["group"]]
        slug = it["slug"]
        if slug in done:
            d = done[slug]
            path = os.path.join(BASE, "sounds", gslug, d["fname"])
            if os.path.isfile(path) and os.path.getsize(path) == d["bytes"]:
                fc, dur, perr = probe(path)
                rec = {"group": it["group"], "group_slug": gslug, "name": it["name"],
                       "slug": slug, "page_url": it["url"], "source_mp3": d["source_mp3"],
                       "file": f"sounds/{gslug}/{d['fname']}", "bytes": d["bytes"],
                       "duration_s": dur, "viral": it.get("viral", False),
                       "file_check": fc + (f" | ffprobe ERROR: {perr}" if perr else "")}
                print(f"[{i}/100] {slug} RECOVERED+REVERIFIED {d['fname']} "
                      f"{d['bytes']} bytes duration={dur} (log said {d['duration']})", flush=True)
                if perr or dur is None:
                    print(f"  !! re-verify failed, re-downloading", flush=True)
                    rec = download_one(it, gslug, used_map[gslug])
                    print(f"[{i}/100] {slug} re-downloaded", flush=True)
                results.append(rec)
                continue
            print(f"[{i}/100] {slug} log says done but file missing/size mismatch "
                  f"-> re-downloading", flush=True)
        print(f"[{i}/100] {slug} downloading...", flush=True)
        results.append(download_one(it, gslug, used_map[gslug]))
        time.sleep(0.5)

    ok = [r for r in results if r["file"] and r["duration_s"] is not None]
    missing = [r for r in results if r not in ok]
    total_bytes = sum(r["bytes"] for r in ok if r["bytes"])
    report = {
        "total": len(results),
        "downloaded": len(ok),
        "missing_count": len(missing),
        "total_bytes": total_bytes,
        "missing": [{"group": r["group"], "group_slug": r["group_slug"], "name": r["name"],
                     "slug": r["slug"], "page_url": r["page_url"],
                     "source_mp3": r["source_mp3"], "file_check": r["file_check"]}
                    for r in missing],
        "items": results,
    }
    out_path = os.path.join(BASE, "hidden_files", "sounds-download-report.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"DONE downloaded={len(ok)}/100 missing={len(missing)} total_bytes={total_bytes}")
    print(f"report: {out_path}")
    for r in missing:
        print(f"  MISSING: {r['slug']} | {r['file_check']}")

if __name__ == "__main__":
    main()
