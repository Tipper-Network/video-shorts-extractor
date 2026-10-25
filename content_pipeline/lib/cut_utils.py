"""Shared video cut, montage, and post-render trim utilities."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

_PIPELINE = Path(__file__).resolve().parents[1]
for _d in (_PIPELINE / "lib", _PIPELINE / "cli", _PIPELINE):
    _s = str(_d)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from _root import PIPELINE_ROOT  # noqa: E402
from trim_profiles import TrimLevel, get_profile  # noqa: E402


def run_cmd(cmd: list[str], *, fatal: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a subprocess and print the command.

    Args:
        cmd: argv list (usually ffmpeg).
        fatal: If True, raise ``CalledProcessError`` on non-zero exit.

    Returns:
        Completed process (stdout/stderr captured as text).
    """
    print(f" Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0 and fatal:
        print(f" Error: {result.stderr}")
        raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
    return result


# Presence and de-ess sit in front of the leveler. Loudness stays one number for every file.
PRESENCE_AF = (
    "deesser=i=0.5:m=0.5:f=0.5:s=o,"
    "equalizer=f=220:t=q:w=1:g=2.5,"
    "equalizer=f=3200:t=q:w=1.2:g=3"
)
# Room tone only. A job opts in with ``room_tone: true``. It is not the default.
ROOM_AF = "afftdn=nr=12:nf=-40"
# Loudness only. A compressor here was riding the gap between words.
VOICE_AF = "loudnorm=I=-16:TP=-1.5:LRA=11"


def voice_chain(room_tone: bool = False) -> str:
    """De-esser and presence EQ, then ``VOICE_AF``. ``afftdn`` only when the job has room tone."""
    head = f"{ROOM_AF}," if room_tone else ""
    return f"{head}{PRESENCE_AF},{VOICE_AF}"


# One grade for a flat lecture. Foreground only. The 16:9 frame stays whole.
GRADE_AF = "eq=contrast=1.06:saturation=1.08:gamma=1.02,colorbalance=rs=0.03:gs=0.01:bs=-0.03,"


CHUNK_MAX_W = 1920


def aspect_filter(aspect: str, *, grade: bool = False) -> str:
    """ffmpeg ``-vf`` graph for the deliverable aspect.

    Args:
        aspect: ``9:16`` (blurred fill + centered 16:9) or ``16:9`` (cap width 1920, never upscale).
        grade: Apply one color step on the picture. The blur ground stays ungraded. No crop.

    Returns:
        Filter string for ``-vf``.
    """
    grade_f = GRADE_AF if grade else ""
    if aspect == "9:16":
        # Full 16:9 frame placed inside 1080x1920 vertical canvas.
        # Background fills the vertical frame and is blurred. It is not a face crop.
        # Foreground keeps the whole 16:9 frame at 1080 wide, board included.
        return (
            "split[v1][v2];"
            "[v1]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:10,setsar=1[v1out];"
            f"[v2]{grade_f}scale=1080:trunc(1080*ih/iw/2)*2,setsar=1[v2out];"
            "[v1out][v2out]overlay=(W-w)/2:(H-h)/2"
        )
    # 16:9 chunks: never upscale. 1280×720 stays 1280×720. 4K caps at 1920 wide.
    return f"{grade_f}scale='min({CHUNK_MAX_W},iw)':-2"


def cut_video(
    source: Path,
    start: float,
    end: float,
    aspect: str,
    output_path: Path,
    *,
    level_audio: bool = False,
    room_tone: bool = False,
    grade: bool = False,
) -> None:
    """Cut ``[start, end)`` from ``source`` with the aspect filter.

    The in-point is sample-accurate. A fast seek lands one second early, then
    ``-ss`` after ``-i`` trims to the script clock so the first phoneme is not
    the previous keyframe.

    Args:
        source: Master / source video.
        start: In-point seconds.
        end: Out-point seconds.
        aspect: ``16:9`` or ``9:16``.
        output_path: Destination mp4.
        level_audio: If True, apply the voice chain during the cut (usually level after instead).
        room_tone: Add ``afftdn`` in front of the voice chain.
        grade: One color step on a flat picture. Full frame stays.
    """
    duration = end - start
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pre = 1.0
    cmd = [
        "ffmpeg",
        "-y",
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "warning",
    ]
    if start > pre:
        cmd.extend(["-ss", f"{start - pre:.3f}", "-i", str(source), "-ss", f"{pre:.3f}"])
    else:
        cmd.extend(["-i", str(source), "-ss", f"{start:.3f}"])
    cmd.extend(
        [
            "-t",
            f"{duration:.3f}",
            "-vf",
            aspect_filter(aspect, grade=grade),
        ]
    )
    if level_audio:
        cmd.extend(["-af", voice_chain(room_tone)])
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
    """Join supercut parts. Stream-copy first; re-encode only if copy fails.

    Args:
        parts: Ordered mp4 slices.
        output_path: Concat destination.
    """
    list_file = output_path.with_suffix(".concat.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for part in parts:
            f.write(f"file '{part.resolve()}'\n")

    common = [
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
    ]
    dest = str(output_path.resolve())
    copy_cmd = [*common, "-c", "copy", "-movflags", "+faststart", dest]
    result = run_cmd(copy_cmd, fatal=False)
    if result.returncode != 0:
        print(" Concat copy failed (stream mismatch) — re-encode")
        run_cmd(
            [
                *common,
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-c:a",
                "aac",
                "-movflags",
                "+faststart",
                dest,
            ]
        )
    list_file.unlink(missing_ok=True)


def level_speech(input_path: Path, *, room_tone: bool = False) -> None:
    """Re-encode audio on the finished file so spikes hit the leveler.

    Args:
        input_path: Rendered mp4 (replaced in place).
        room_tone: Run ``afftdn`` before the de-esser. Off unless this job recorded room tone.
    """
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
        voice_chain(room_tone),
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
    """Turn a still into a video segment with silent audio.

    Args:
        image_path: JPG/PNG/WebP.
        duration: Hold time in seconds.
        aspect: ``16:9`` or ``9:16``.
        output_path: Destination mp4.
    """
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
    """Seconds for one montage piece.

    Args:
        seg: Still ``{type: image, duration}`` or video ``{start, end}``.

    Returns:
        Duration in seconds.
    """
    if seg.get("type") == "image":
        return float(seg["duration"])
    return seg["end"] - seg["start"]


def cut_montage(
    source: Path,
    segments: list[dict],
    aspect: str,
    output_path: Path,
    *,
    grade: bool = False,
) -> None:
    """Render each video/image segment, concat them, delete temp parts.

    Args:
        source: Master video for timed slices.
        segments: Montage pieces (video clocks or stills).
        aspect: ``16:9`` or ``9:16``.
        output_path: Final concat mp4.
    """
    tmp_dir = output_path.parent / ".tmp" / output_path.stem
    tmp_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []

    for i, seg in enumerate(segments):
        part = tmp_dir / f"part_{i:02d}.mp4"
        if seg.get("type") == "image":
            still_to_video(Path(seg["path"]), segment_duration(seg), aspect, part)
        else:
            cut_video(source, seg["start"], seg["end"], aspect, part, grade=grade)
        parts.append(part)

    concat_parts(parts, output_path)

    shutil.rmtree(tmp_dir, ignore_errors=True)


def apply_trim(input_path: Path, output_path: Path, level: TrimLevel) -> Path:
    """Trim silence on a rendered clip.

    Args:
        input_path: Source mp4.
        output_path: Trimmed destination (may be the same path).
        level: ``off`` / ``light`` / ``moderate`` / ``aggressive``.

    Returns:
        Path actually written (copy of input when ``level`` is ``off``).
    """
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
    room_tone: bool = False,
    grade: bool = False,
) -> None:
    """Render one manifest chapter or short, then level speech.

    Args:
        source: Master video.
        entry: Manifest chapter/short dict (``start``/``end`` or ``segments``).
        aspect: ``16:9`` or ``9:16``.
        output_path: Destination mp4.
        default_cut_mode: Used when the entry has no ``cut_mode``.
        trim_level: Silence trim after the cut; ``off`` skips trim.
        room_tone: ``afftdn`` before the voice chain.
        grade: One color step. Set from the entry when this call's flags are omitted.
    """
    cut_mode = entry.get("cut_mode", default_cut_mode)
    segments = entry.get("segments") or []
    room_tone = room_tone or bool(entry.get("room_tone"))
    grade = grade or bool(entry.get("flat"))

    if cut_mode == "supercut" and segments:
        cut_montage(source, segments, aspect, output_path, grade=grade)
    elif segments and "start" not in entry:
        cut_montage(source, segments, aspect, output_path, grade=grade)
    elif "start" in entry and "end" in entry:
        cut_video(source, entry["start"], entry["end"], aspect, output_path, grade=grade)
    else:
        raise ValueError(f"Clip {entry.get('id')}: need start/end or segments[]")

    if trim_level != "off":
        apply_trim(output_path, output_path, trim_level)

    level_speech(output_path, room_tone=room_tone)
