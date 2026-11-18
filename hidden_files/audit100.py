"""Audit + fix pass for the 100 downloaded tiengdong sounds.
Finding: download19.py's method (prefer slug match, else FIRST mp3 in HTML)
is unreliable — the first mp3 in the HTML is a "Moi nhat" sidebar item, and
the slug match is case-sensitive so capitalised filenames fall through to
the sidebar pick. The page's REAL main audio is:
  (a) <audio class="wp-audio-shortcode"> -> <source src="...mp3">, or
  (b) the playPauseAudio button whose data-post-id == <article id="post-N">.
This script re-fetches all 100 pages, extracts the main mp3 by (a)/(b)
(case-insensitive slug match as fallback), compares with the report's
source_mp3, and REPLACES any wrong file with the correct main audio.
Nothing is invented: every replacement URL comes from the live page HTML.
"""
import re, os, json, urllib.request, urllib.parse, time, subprocess

BASE = os.path.expanduser("~/workspace/kho-sound-meme")
SRC = os.path.expanduser("~/workspace/tiengdong-sounds/research/diverse-100.json")
REPORT = os.path.join(BASE, "hidden_files", "sounds-download-report.json")
HDR = {"User-Agent": "Mozilla/5.0"}

def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers=HDR)
    return urllib.request.urlopen(req, timeout=timeout)

def norm(u):
    return (u or "").split("?")[0]

def main_mp3(html, slug):
    """Return (method, url-or-None)."""
    m = re.search(r'<audio[^>]*wp-audio-shortcode[^>]*>.*?</audio>', html, re.S)
    if m:
        s = re.search(r'src="([^"]+\.mp3)', m.group(0))
        if s:
            return ("wp-audio-shortcode", norm(s.group(1)))
    art = re.search(r'<article[^>]*id="post-(\d+)"', html)
    if art:
        pid = art.group(1)
        for pm, mp3 in re.findall(
                r'data-post-id="(\d+)" onclick="playPauseAudio\(\'[^\']+\', \'([^\']+\.mp3)\'\)', html):
            if pm == pid:
                return (f"article-post-{pid}", norm(mp3))
        return (f"article-post-{pid}-button-not-found", None)
    mp3s = re.findall(r'https://tiengdong\.com/wp-content/uploads/[^"\'<> ]+\.mp3', html)
    seen = []
    for x in mp3s:
        x = norm(x)
        if x not in seen:
            seen.append(x)
    low = slug.lower()
    for x in seen:
        if low[:25] in x.lower() or low.replace("-", "")[:15] in x.lower().replace("-", ""):
            return ("slug-match-case-insensitive", x)
    return ("unresolved", None)

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

def download(url, dest_dir, used):
    fname = urllib.parse.unquote(os.path.basename(norm(url)))
    if fname in used or os.path.exists(os.path.join(dest_dir, fname)):
        base_name, ext = os.path.splitext(fname)
        n = 2
        while f"{base_name}-{n}{ext}" in used or os.path.exists(
                os.path.join(dest_dir, f"{base_name}-{n}{ext}")):
            n += 1
        fname = f"{base_name}-{n}{ext}"
    out = os.path.join(dest_dir, fname)
    last_err = None
    for _ in range(2):
        try:
            req = urllib.request.Request(url, headers=HDR)
            with urllib.request.urlopen(req, timeout=60) as r, open(out, "wb") as fh:
                while True:
                    chunk = r.read(65536)
                    if not chunk:
                        break
                    fh.write(chunk)
            used.add(fname)
            return out, fname, None
        except Exception as e:
            last_err = e
            time.sleep(2)
    return None, fname, f"mp3 download failed: {last_err}"

def main():
    with open(SRC, encoding="utf-8") as f:
        items = json.load(f)
    with open(REPORT, encoding="utf-8") as f:
        rep = json.load(f)
    by_slug = {r["slug"]: r for r in rep["items"]}
    used_map = {}
    for gslug in set(r["group_slug"] for r in rep["items"]):
        d = os.path.join(BASE, "sounds", gslug)
        used_map[gslug] = set(os.listdir(d)) if os.path.isdir(d) else set()
    fixed, kept, unresolved = [], [], []
    for i, it in enumerate(items, 1):
        slug, gslug = it["slug"], {v: k for k, v in {}.items()}.get(it["group"])  # placeholder
        # group slug from report (authoritative mapping already applied)
        rec = by_slug[slug]
        gslug = rec["group_slug"]
        dest_dir = os.path.join(BASE, "sounds", gslug)
        try:
            html = None
            last_err = None
            for _ in range(2):
                try:
                    html = fetch(it["url"]).read().decode("utf-8", errors="ignore")
                    break
                except Exception as e:
                    last_err = e
                    time.sleep(2)
            if html is None:
                print(f"[{i}/100] {slug} AUDIT-ERROR page fetch failed: {last_err}", flush=True)
                unresolved.append(slug)
                rec["audit"] = f"page fetch failed: {last_err}; kept previous file"
                continue
            method, main_url = main_mp3(html, slug)
            old_url = norm(rec.get("source_mp3"))
            if main_url is None:
                print(f"[{i}/100] {slug} UNRESOLVED method={method}; kept {rec.get('file')}", flush=True)
                unresolved.append(slug)
                rec["audit"] = f"unresolved ({method}); kept download19-method file"
                continue
            if main_url == old_url:
                print(f"[{i}/100] {slug} OK method={method} {os.path.basename(main_url)}", flush=True)
                kept.append(slug)
                rec["audit"] = f"ok ({method})"
                continue
            # WRONG FILE — replace with the page's real main audio
            print(f"[{i}/100] {slug} WRONG method={method}", flush=True)
            print(f"  old: {old_url}", flush=True)
            print(f"  new: {main_url}", flush=True)
            old_path = os.path.join(BASE, rec["file"]) if rec.get("file") else None
            if old_path and os.path.isfile(old_path):
                used_map[gslug].discard(os.path.basename(old_path))
                os.remove(old_path)
                print(f"  removed wrong file {old_path}", flush=True)
            out, fname, err = download(main_url, dest_dir, used_map[gslug])
            if err:
                print(f"  !! re-download failed: {err}", flush=True)
                rec["audit"] = f"WRONG file removed, re-download FAILED: {err}"
                rec["file"] = None
                rec["bytes"] = None
                rec["duration_s"] = None
                rec["file_check"] = f"ERROR: {err}"
                unresolved.append(slug)
                continue
            size = os.path.getsize(out)
            fc, dur, perr = probe(out)
            rec["source_mp3"] = main_url
            rec["file"] = f"sounds/{gslug}/{fname}"
            rec["bytes"] = size
            rec["duration_s"] = dur
            rec["file_check"] = fc + (f" | ffprobe ERROR: {perr}" if perr else "")
            rec["audit"] = (f"FIXED ({method}): replaced wrong sidebar mp3 "
                            f"{os.path.basename(old_url)} with page main player mp3")
            print(f"  -> {fname} {size} bytes duration={dur} | {fc}", flush=True)
            fixed.append(slug)
        except Exception as e:
            print(f"[{i}/100] {slug} AUDIT-ERROR {e}", flush=True)
            unresolved.append(slug)
            rec["audit"] = f"audit error: {e}; kept previous file"
        time.sleep(0.5)

    ok = [r for r in rep["items"] if r["file"] and r["duration_s"] is not None]
    missing = [r for r in rep["items"] if r not in ok]
    rep["downloaded"] = len(ok)
    rep["missing_count"] = len(missing)
    rep["total_bytes"] = sum(r["bytes"] for r in ok if r["bytes"])
    rep["missing"] = [{"group": r["group"], "group_slug": r["group_slug"], "name": r["name"],
                       "slug": r["slug"], "page_url": r["page_url"],
                       "source_mp3": r["source_mp3"], "file_check": r["file_check"]}
                      for r in missing]
    rep["audit_summary"] = {"checked": len(items), "kept_ok": len(kept),
                            "fixed_wrong": len(fixed), "unresolved": len(unresolved),
                            "fixed_slugs": fixed, "unresolved_slugs": unresolved}
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=2)
    print(f"AUDIT DONE kept={len(kept)} fixed={len(fixed)} unresolved={len(unresolved)} "
          f"downloaded={len(ok)}/100 total_bytes={rep['total_bytes']}")
    print("FIXED:", fixed)
    print("UNRESOLVED:", unresolved)

if __name__ == "__main__":
    main()
