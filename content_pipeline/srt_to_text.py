#!/usr/bin/env python3
"""Linearize YouTube .srt → timestamped `{n}. {Title}.txt` (lecture folder) + titled plain text (transcript root).

Rolling auto-captions overlap. This emits each word once, then:
  `{slug}/{n}. {Title}.txt`  — [clock → clock] lines (cut planning)
  `{n}. {Title}.txt`         — paragraphs, no clocks (ebook) in the transcript main folder
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from transcribe import export_transcripts, format_timestamp

SRT_TIME = re.compile(
    r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})"
)
CENSOR = re.compile(r"\[\s*__\s*\]")


def _hms(h: str, m: str, s: str, ms: str) -> float:
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def parse_srt(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8-sig")
    cues: list[dict] = []
    for block in re.split(r"\n\s*\n", raw.strip()):
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        tline = next((ln for ln in lines if "-->" in ln), None)
        if not tline:
            continue
        match = SRT_TIME.search(tline)
        if not match:
            continue
        text = " ".join(ln for ln in lines if ln != tline and not ln.isdigit())
        text = re.sub(r"<[^>]+>", "", text)
        text = CENSOR.sub("fuck", text)
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        g = match.groups()
        cues.append({"start": _hms(*g[:4]), "end": _hms(*g[4:]), "text": text})
    return cues


def linearize(cues: list[dict]) -> list[dict]:
    """Drop words already shown in the previous rolling caption."""
    out: list[dict] = []
    prev: list[str] = []
    for cue in cues:
        words = cue["text"].split()
        cut = 0
        for i in range(min(len(words), len(prev)), 0, -1):
            if words[:i] == prev[-i:]:
                cut = i
                break
        new = words[cut:]
        if new:
            out.append({"start": cue["start"], "end": cue["end"], "text": " ".join(new)})
        prev = words
    return out


def to_paragraphs(chunks: list[dict], gap_sec: float = 2.5) -> str:
    paras: list[str] = []
    buf: list[str] = []
    last_end: float | None = None

    def flush() -> None:
        text = " ".join(buf).strip()
        text = re.sub(r"\s+", " ", text)
        if text:
            paras.append(text)
        buf.clear()

    for chunk in chunks:
        if last_end is not None and chunk["start"] - last_end >= gap_sec:
            flush()
        buf.append(chunk["text"])
        last_end = chunk["end"]
        joined = " ".join(buf)
        if len(joined) > 480 and re.search(r"[.!?][\"']?$", chunk["text"]):
            flush()
    flush()
    return "\n\n".join(paras) + ("\n" if paras else "")


def find_srt(folder: Path) -> Path | None:
    named = folder / "captions.srt"
    if named.exists():
        return named
    matches = sorted(folder.glob("*.srt"))
    return matches[0] if matches else None


LECTURE_TITLES = {
    "13-future-ready-the-program": "Future Ready, The Program",
    "14-first-principles": "First Principles",
    "15-systems-thinking": "Systems Thinking",
    "16-ai-leadership-and-partnership": "AI, Leadership and Partnership",
    "17-design-fundamentals": "Design Fundamentals",
    "18-entrepreneurs-the-engineering-mindset": "Entrepreneurs, The Engineering Mindset",
}


def clock_txt_name(folder: Path) -> str:
    """`13. Future Ready, The Program.txt` — priority + video title, not transcript.txt."""
    slug = folder.name
    title = LECTURE_TITLES.get(slug)
    if title:
        num = slug.split("-", 1)[0]
        return f"{num}. {title}.txt"
    return f"{slug}.txt"


def clock_txt_path(folder: Path) -> Path:
    return folder / clock_txt_name(folder)


def plain_txt_path(folder: Path) -> Path:
    """Ebook plain text lives in the transcript root, not the lecture subfolder."""
    return folder.parent / clock_txt_name(folder)


def find_clock_txt(folder: Path) -> Path | None:
    named = clock_txt_path(folder)
    if named.exists():
        return named
    legacy = folder / "transcript.txt"
    if legacy.exists():
        return legacy
    return None


def convert_folder(folder: Path, *, write_clocks: bool) -> dict:
    srt = find_srt(folder)
    if not srt:
        raise FileNotFoundError(f"No .srt in {folder}")
    chunks = linearize(parse_srt(srt))
    if not chunks:
        raise ValueError(f"Empty SRT: {srt}")

    plain_path = plain_txt_path(folder)
    plain_path.write_text(to_paragraphs(chunks), encoding="utf-8")

    clock_path = clock_txt_path(folder)
    if write_clocks:
        export_transcripts(
            chunks,
            segments_json_path=folder / "segments.json",
            transcript_txt_path=clock_path,
        )

    return {
        "folder": folder.name,
        "title": LECTURE_TITLES.get(folder.name, folder.name),
        "srt": srt.name,
        "chunks": len(chunks),
        "plain": plain_path,
        "span": f"{format_timestamp(chunks[0]['start'])} → {format_timestamp(chunks[-1]['end'])}",
        "words": sum(len(c["text"].split()) for c in chunks),
        "plain_text": plain_path.read_text(encoding="utf-8"),
    }


def write_ebook(results: list[dict], out_path: Path) -> None:
    parts = ["# Future Ready\n", "The G.A.F. program lectures.\n"]
    for item in results:
        parts.append(f"\n# {item['title']}\n")
        parts.append(item["plain_text"].rstrip() + "\n")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(parts), encoding="utf-8")
    print(f" Ebook → {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="YouTube SRT → plain text + optional clocks")
    parser.add_argument("--project", help="Project ID under projects/")
    parser.add_argument("--dir", help="One transcript folder containing a .srt")
    parser.add_argument(
        "--clocks",
        action="store_true",
        help="Also write `{n}. {Title}.txt` + segments.json from the SRT",
    )
    parser.add_argument(
        "--ebook",
        action="store_true",
        help="Write output/ebook/Future-Ready.md from all converted lectures",
    )
    args = parser.parse_args()

    folders: list[Path] = []
    ebook_path: Path | None = None
    if args.dir:
        folders = [Path(args.dir)]
    elif args.project:
        from project_paths import load_project_paths

        paths = load_project_paths(args.project)
        folders = sorted(p for p in paths.transcript_dir.iterdir() if p.is_dir())
        ebook_path = paths.root / "output" / "ebook" / "Future-Ready.md"
    else:
        print(" Pass --project or --dir")
        sys.exit(1)

    results = []
    for folder in folders:
        if not find_srt(folder):
            print(f" skip (no srt) {folder.name}")
            continue
        has_clocks = find_clock_txt(folder) is not None
        # Never overwrite Whisper clocks on 13. Other lectures get SRT clocks
        # so we can cut later without a second full transcribe.
        write_clocks = (not has_clocks) or (
            args.clocks and folder.name != "13-future-ready-the-program"
        )
        info = convert_folder(folder, write_clocks=write_clocks)
        print(
            f" {info['folder']}: {info['words']} words  {info['span']}  "
            f"from {info['srt']} → {plain_txt_path(folder).name}"
            + (f" + {clock_txt_name(folder)}" if write_clocks else "")
        )
        results.append(info)

    if args.ebook and ebook_path and results:
        write_ebook(results, ebook_path)


if __name__ == "__main__":
    main()
