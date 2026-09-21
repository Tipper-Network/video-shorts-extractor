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


# Hard speech leveling — live yells need dynaudnorm + a tight LRA, not loudnorm alone.
VOICE_AF = (
    "acompressor=threshold=-24dB:ratio=8:attack=3:release=80:makeup=5,"
    "dynaudnorm=f=75:g=25:p=0.6:m=12,"
    "alimiter=limit=0.75:attack=3:release=30,"
    "loudnorm=I=-16:TP=-1.5:LRA=4"
)


def aspect_filter(aspect: str) -> str:
    if aspect == "9:16":
        # Full 16:9 frame placed inside 1080x1920 vertical canvas
        # Background: fills 1080x1920 (blurred)
        # Foreground: scales 16:9 original to 1080 width (unblurred)
        return (
            "split[v1][v2];"
            "[v1]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:10,setsar=1[v1out];"
            "[v2]scale=1080:trunc(1080*ih/iw/2)*2,setsar=1[v2out];"
            "[v1out][v2out]overlay=(W-w)/2:(H-h)/2"
        )
    return "scale=1920:1080"


def cut_video(
    source: Path,
    start: float,
    end: float,
    aspect: str,
    output_path: Path,
    *,
    level_audio: bool = False,
) -> None:
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
    ]
    if level_audio:
        cmd.extend(["-af", VOICE_AF])
    cmd.extend(
        [
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-c:a",
            "aac",
            str(output_path),
        ]
    )
    run_cmd(cmd)


def concat_parts(parts: list[Path], output_path: Path) -> None:
    list_file = output_path.with_suffix(".concat.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for part in parts:
            # use absolute path to avoid confusion
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
        str(list_file.resolve()),
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(output_path.resolve()),
    ]
    run_cmd(cmd)
    list_file.unlink(missing_ok=True)


def level_speech(input_path: Path) -> None:
    """Re-encode audio on the finished file so spikes always hit the leveler."""
    tmp = input_path.with_name(input_path.stem + ".level.mp4")
    cmd = [
        "ffmpeg",
        "-y",
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-i",
        str(input_path),
        "-c:v",
        "copy",
        "-af",
        VOICE_AF,
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(tmp),
    ]
    run_cmd(cmd)
    tmp.replace(input_path)
    print(f" Audio leveled → {input_path.name}")


def still_to_video(image_path: Path, duration: float, aspect: str, output_path: Path) -> None:
    """Turn a still into a vertical/horizontal video segment with silent audio."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-loop",
        "1",
        "-i",
        str(image_path),
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=48000:cl=stereo",
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
        "-ar",
        "48000",
        "-ac",
        "2",
        "-shortest",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    run_cmd(cmd)


def segment_duration(seg: dict) -> float:
    if seg.get("type") == "image":
        return float(seg["duration"])
    return seg["end"] - seg["start"]


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
        if seg.get("type") == "image":
            still_to_video(Path(seg["path"]), segment_duration(seg), aspect, part)
        else:
            cut_video(source, seg["start"], seg["end"], aspect, part)
        parts.append(part)

    concat_parts(parts, output_path)

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

    level_speech(output_path)
