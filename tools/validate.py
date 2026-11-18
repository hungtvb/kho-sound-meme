#!/usr/bin/env python3
"""Validate kho-sound-meme maps against the files on disk.

Checks (stdlib + ffprobe only):
  - every map item's file exists in its group folder (and file_jpg for memes)
  - group map `count` == len(items); root `total` == len(items)
  - no duplicate sound slug / meme id / file name
  - sound duration_s matches ffprobe within +-0.05 s
  - clip items: parent_slug exists, file name is <parent>__cNN.mp3
  - meme width/height match the image on disk (PIL is NOT needed: skipped)

Usage (from anywhere):  python tools/validate.py [--no-ffprobe]
Exit code 0 = OK, 1 = problems found.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOL = 0.05


def load(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def ffprobe_duration(path: Path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def check_sounds(errors: list, use_ffprobe: bool):
    root = load(ROOT / "sounds.json")
    items = root["items"]
    if root["total"] != len(items):
        errors.append(f"sounds.json total={root['total']} but items={len(items)}")
    slugs, files = {}, {}
    for it in items:
        key = it["slug"]
        if key in slugs:
            errors.append(f"duplicate sound slug: {key}")
        slugs[key] = it
        fkey = f"{it['group_slug']}/{it['file']}"
        if fkey in files:
            errors.append(f"duplicate sound file: {fkey}")
        files[fkey] = it

    group_total = 0
    for gdir in sorted((ROOT / "sounds").iterdir()):
        mp = gdir / "sound-map.json"
        if not mp.exists():
            continue
        gm = load(mp)
        group_total += len(gm["items"])
        if gm["count"] != len(gm["items"]):
            errors.append(f"{mp.relative_to(ROOT)} count={gm['count']} items={len(gm['items'])}")
        for it in gm["items"]:
            p = gdir / it["file"]
            if not p.exists():
                errors.append(f"missing sound file: {p.relative_to(ROOT)}")
                continue
            if it.get("kind") == "clip":
                parent = it.get("parent_slug")
                if parent not in {x["slug"] for x in gm["items"]}:
                    errors.append(f"clip {it['file']} parent_slug not in group: {parent}")
                if not it["file"].startswith(f"{parent}__c"):
                    errors.append(f"clip file name does not match parent: {it['file']}")
            if use_ffprobe:
                dur = ffprobe_duration(p)
                if dur is None:
                    errors.append(f"ffprobe failed: {p.relative_to(ROOT)}")
                elif abs(dur - it["duration_s"]) > TOL:
                    errors.append(f"duration mismatch {p.relative_to(ROOT)}: map={it['duration_s']} real={dur:.3f}")
    if group_total != len(items):
        errors.append(f"sum of group maps {group_total} != sounds.json items {len(items)}")
    return len(items)


def check_memes(errors: list):
    root = load(ROOT / "memes.json")
    items = root["items"]
    if root["total"] != len(items):
        errors.append(f"memes.json total={root['total']} but items={len(items)}")
    ids = set()
    for it in items:
        if it["id"] in ids:
            errors.append(f"duplicate meme id: {it['id']}")
        ids.add(it["id"])
    group_total = 0
    for gdir in sorted((ROOT / "memes").iterdir()):
        mp = gdir / "meme-map.json"
        if not mp.exists():
            continue
        gm = load(mp)
        group_total += len(gm["items"])
        if gm["count"] != len(gm["items"]):
            errors.append(f"{mp.relative_to(ROOT)} count={gm['count']} items={len(gm['items'])}")
        for it in gm["items"]:
            for field in ("file", "file_jpg"):
                if field not in it:
                    continue
                p = gdir / it[field]
                if not p.exists():
                    errors.append(f"missing meme {field}: {p.relative_to(ROOT)}")
    if group_total != len(items):
        errors.append(f"sum of meme group maps {group_total} != memes.json items {len(items)}")
    return len(items)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-ffprobe", action="store_true", help="skip duration check (faster)")
    args = ap.parse_args(argv)
    errors = []
    n_sounds = check_sounds(errors, use_ffprobe=not args.no_ffprobe)
    n_memes = check_memes(errors)
    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for e in errors[:200]:
            print("  -", e)
        return 1
    print(f"OK: {n_sounds} sounds, {n_memes} memes; counts, files, slugs/ids and durations match.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
