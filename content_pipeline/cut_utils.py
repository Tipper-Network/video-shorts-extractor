"""Shared video cut, montage, and post-render trim utilities."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from trim_profiles import TrimLevel, get_profile

BASE_DIR = Path(__file__).resolve().parent


def run_cmd(cmd: list[str], *, fatal: bool = True) -> subprocess.CompletedProcess[str]:
    print(f" Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0 and fatal:
        print(f" Error: {result.stderr}")
        raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
    return result


def aspect_filter(aspect: str) -> str:
    if aspect == "9:16":
        return "crop=ih*(9/16):ih,scale=1080:1920"
    return "scale=1920:1080"


def cut_video(source: Path, start: float, end: float, aspect: str, output_path: Path) -> None:
    duration = end - start
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-ss",
        str(start),
        "-i",
        str(source),
        "-t",
        str(duration),
        "-vf",
        aspect_filter(aspect),
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-c:a",
        "aac",
        str(output_path),
    ]
    run_cmd(cmd)


def concat_parts(parts: list[Path], output_path: Path) -> None:
    list_file = output_path.with_suffix(".concat.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for part in parts:
            f.write(f"file '{part.resolve()}'\n")

    cmd = [
        "ffmpeg",
        "-y",
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_file),
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    run_cmd(cmd)
    list_file.unlink(missing_ok=True)


def cut_montage(
    source: Path,
    segments: list[dict],
    aspect: str,
    output_path: Path,
) -> None:
    tmp_dir = output_path.parent / ".tmp" / output_path.stem
    tmp_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []

    for i, seg in enumerate(segments):
        part = tmp_dir / f"part_{i:02d}.mp4"
        cut_video(source, seg["start"], seg["end"], aspect, part)
        parts.append(part)

    concat_parts(parts, output_path)

    import shutil

    shutil.rmtree(tmp_dir, ignore_errors=True)


def apply_trim(input_path: Path, output_path: Path, level: TrimLevel) -> Path:
    """Trim silence on a rendered clip. Returns path actually written."""
    profile = get_profile(level)
    if profile is None:
        if input_path != output_path:
            shutil.copy2(input_path, output_path)
        return output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = output_path.with_suffix(".pretrim.mp4")

    if profile.method == "ffmpeg":
        from trim_silence import trim_long_pauses_ffmpeg

        trim_long_pauses_ffmpeg(
            input_path,
            tmp,
            profile.min_silence or 2.5,
            profile.threshold_db or -40.0,
        )
    else:
        from trim_silence import trim_with_auto_editor

        trim_with_auto_editor(input_path, tmp, profile.margin or "0.6sec")

    if output_path.exists():
        output_path.unlink()
    tmp.rename(output_path)
    print(f" Trim ({level}) → {output_path.name}")
    return output_path


def render_clip_entry(
    source: Path,
    entry: dict,
    aspect: str,
    output_path: Path,
    *,
    default_cut_mode: str = "contiguous",
    trim_level: TrimLevel = "off",
) -> None:
    cut_mode = entry.get("cut_mode", default_cut_mode)
    segments = entry.get("segments") or []

    if cut_mode == "supercut" and segments:
        cut_montage(source, segments, aspect, output_path)
    elif segments and "start" not in entry:
        cut_montage(source, segments, aspect, output_path)
    elif "start" in entry and "end" in entry:
        cut_video(source, entry["start"], entry["end"], aspect, output_path)
    else:
        raise ValueError(f"Clip {entry.get('id')}: need start/end or segments[]")

    if trim_level != "off":
        apply_trim(output_path, output_path, trim_level)
