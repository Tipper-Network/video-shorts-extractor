#!/usr/bin/env python3
"""Stage-1 viral captions — kinetic burn-in from word timestamps + brand caption.json."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

_PIPELINE = Path(__file__).resolve().parents[1]
for _d in (_PIPELINE / "lib", _PIPELINE / "cli", _PIPELINE):
    _s = str(_d)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from faster_whisper import WhisperModel  # noqa: E402

from _root import CONFIG_DIR, PIPELINE_ROOT, WORKSPACE_ROOT  # noqa: E402

ASSETS = WORKSPACE_ROOT / "brands" / "assets"
CENSOR_PATH = CONFIG_DIR / "censor_words.json"

WORDS_PER_LINE = 4
DEFAULT_FONT_SIZE = 72


def load_censor() -> set[str]:
    if not CENSOR_PATH.exists():
        return set()
    data = json.loads(CENSOR_PATH.read_text(encoding="utf-8"))
    return {w.lower() for w in data.get("words", [])}


def resolve_caption(entity: str) -> dict:
    path = ASSETS / entity / "caption.json"
    if not path.exists():
        raise SystemExit(f"Missing caption config: {path}")
    cfg = json.loads(path.read_text(encoding="utf-8"))
    font = ASSETS / entity / cfg["font_file"]
    if not font.exists():
        fallback = ASSETS / entity / cfg.get("font_fallback", "")
        if fallback.exists():
            font = fallback
        else:
            raise SystemExit(f"Missing font: {font}")
    cfg["_font_path"] = font
    cfg["_fonts_dir"] = font.parent
    return cfg


def extract_audio(video: Path, wav: Path) -> None:
    cmd = [
        "ffmpeg", "-y", "-i", str(video),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        str(wav),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr[-800:])


def whisper_words(wav: Path, model_size: str = "small") -> list[dict]:
    print(f" Whisper words ({model_size})…")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(wav), beam_size=5, word_timestamps=True)
    words: list[dict] = []
    for seg in segments:
        if not seg.words:
            continue
        for w in seg.words:
            token = (w.word or "").strip()
            if not token:
                continue
            words.append({
                "word": token,
                "start": float(w.start),
                "end": float(w.end),
            })
    print(f"  {len(words)} words")
    return words


def display_word(raw: str, censor: set[str]) -> str:
    cleaned = re.sub(r"^[^\w']+|[^\w']+$", "", raw, flags=re.UNICODE)
    if cleaned.lower() in censor:
        return "****"
    return raw.strip().upper()


def ass_time(seconds: float) -> str:
    if seconds < 0:
        seconds = 0.0
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def hex_to_ass_bgr(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"&H00{b:02X}{g:02X}{r:02X}"


def font_family_name(font_path: Path) -> str:
    try:
        from fontTools.ttLib import TTFont
        font = TTFont(str(font_path))
        for rec in font["name"].names:
            if rec.nameID == 1 and rec.platformID in (1, 3):
                return rec.toUnicode()
    except Exception:
        pass
    return font_path.stem.split("-")[0].replace("SourceSans3", "Source Sans 3").replace("WorkSans", "Work Sans")


def build_ass(words: list[dict], cfg: dict, censor: set[str], out_ass: Path) -> None:
    body = hex_to_ass_bgr(cfg["body"])
    active = hex_to_ass_bgr(cfg["active"])
    stroke = hex_to_ass_bgr(cfg["stroke"])
    stroke_w = int(cfg.get("stroke_width", 4))
    font_size = int(cfg.get("font_size", DEFAULT_FONT_SIZE))
    margin_v = int(cfg.get("margin_v", 200))
    family = font_family_name(cfg["_font_path"])

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Body,{family},{font_size},{body},{active},{stroke},&H80000000,-1,0,0,0,100,100,0,0,1,{stroke_w},0,2,40,40,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines: list[str] = [header]
    n = WORDS_PER_LINE
    for i in range(0, len(words), n):
        chunk = words[i : i + n]
        if not chunk:
            continue
        texts = [display_word(w["word"], censor) for w in chunk]
        for j, w in enumerate(chunk):
            parts = []
            for k, t in enumerate(texts):
                if k == j:
                    parts.append(f"{{\\c{active}}}{t}{{\\c{body}}}")
                else:
                    parts.append(t)
            line = " ".join(parts)
            start = w["start"]
            end = w["end"]
            if j + 1 < len(chunk):
                end = max(end, chunk[j + 1]["start"])
            if end <= start:
                end = start + 0.12
            lines.append(
                f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Body,,0,0,0,,{line}\n"
            )
    out_ass.write_text("".join(lines), encoding="utf-8")
    print(f"  ASS → {out_ass}")


def burn(video: Path, ass: Path, fonts_dir: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    # Escape for ffmpeg filter (colon / backslash)
    ass_esc = str(ass).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
    fonts_esc = str(fonts_dir).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
    vf = f"ass={ass_esc}:fontsdir={fonts_esc}"
    cmd = [
        "ffmpeg", "-y", "-i", str(video),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "copy",
        str(output),
    ]
    print(" Burning captions…")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr[-1200:])
    print(f"  → {output}")


def main() -> None:
    p = argparse.ArgumentParser(description="Stage-1 kinetic captions")
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--entity", default="founder", help="tipper | gaf | founder")
    p.add_argument("--model", default="small")
    p.add_argument("--words-out", type=Path, help="Optional words.json path")
    p.add_argument("--words-in", type=Path, help="Reuse existing words.json (skip Whisper)")
    args = p.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Missing input: {args.input}")

    cfg = resolve_caption(args.entity)
    censor = load_censor()

    with tempfile.TemporaryDirectory(prefix="viral_s1_") as tmp:
        tmp_p = Path(tmp)
        ass = tmp_p / "captions.ass"
        if args.words_in and args.words_in.exists():
            words = json.loads(args.words_in.read_text(encoding="utf-8"))
            print(f"  reused {len(words)} words from {args.words_in}")
        else:
            wav = tmp_p / "audio.wav"
            extract_audio(args.input, wav)
            words = whisper_words(wav, args.model)
            if args.words_out:
                args.words_out.parent.mkdir(parents=True, exist_ok=True)
                args.words_out.write_text(json.dumps(words, indent=2), encoding="utf-8")
                print(f"  words → {args.words_out}")
        build_ass(words, cfg, censor, ass)
        # Keep a copy of ASS next to output for debug
        ass_keep = args.output.with_suffix(".ass")
        ass_keep.parent.mkdir(parents=True, exist_ok=True)
        ass_keep.write_text(ass.read_text(encoding="utf-8"), encoding="utf-8")
        burn(args.input, ass_keep, cfg["_fonts_dir"], args.output)


if __name__ == "__main__":
    main()
