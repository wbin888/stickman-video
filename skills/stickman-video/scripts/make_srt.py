#!/usr/bin/env python3
"""Build an SRT subtitle file from approved narration.

Input: a UTF-8 text file with one shot per line, either
  "<seconds>|<narration>"  (explicit shot length), or
  "<narration>"            (uses --shot-length).
Long lines are split at punctuation into cues that share the shot's time
proportionally to their length.
"""
import argparse
import re
import sys

PUNCT = re.compile(r"(?<=[，。！？；：,.!?;:])\s*")


def fmt(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def split_cues(text: str, max_chars: int) -> list[str]:
    parts = [p.strip() for p in PUNCT.split(text) if p.strip()]
    cues, cur = [], ""
    for p in parts:
        if cur and len(cur) + len(p) > max_chars:
            cues.append(cur)
            cur = p
        else:
            cur = f"{cur} {p}".strip() if re.search(r"[A-Za-z]$", cur) else cur + p
    if cur:
        cues.append(cur)
    return cues or [text.strip()]


def build(lines: list[str], shot_length: float, max_chars: int) -> str:
    out, idx, t = [], 1, 0.0
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        dur = shot_length
        if "|" in raw:
            head, raw = raw.split("|", 1)
            dur = float(head)
        cues = split_cues(raw, max_chars)
        total = sum(len(c) for c in cues)
        start = t
        for c in cues:
            end = start + dur * len(c) / total
            out.append(f"{idx}\n{fmt(start)} --> {fmt(end)}\n{c.rstrip('，。,;；')}\n")
            idx += 1
            start = end
        t += dur
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="narration file, one shot per line")
    ap.add_argument("-o", "--output", default="subtitles.srt")
    ap.add_argument("--shot-length", type=float, default=8.0)
    ap.add_argument("--max-chars", type=int, default=18, help="max characters per cue (use ~42 for English)")
    a = ap.parse_args()
    with open(a.input, encoding="utf-8") as f:
        srt = build(f.readlines(), a.shot_length, a.max_chars)
    with open(a.output, "w", encoding="utf-8") as f:
        f.write(srt)
    print(f"wrote {a.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
