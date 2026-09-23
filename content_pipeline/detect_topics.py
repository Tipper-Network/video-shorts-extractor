#!/usr/bin/env python3
"""
Heuristic topic detection from Whisper transcript segments.

Layer 1 (this script): pause boundaries + lexical shift → topic blocks + chapter candidates.
Layer 2 (Cursor agent): refine titles, merge/split, write manifest.json.

No local LLM — output is always review.status = needs_agent_review.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SUB_DIR = BASE_DIR / "subtitles"

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "that", "this", "was", "are",
    "be", "have", "has", "had", "do", "does", "did", "will", "would", "can",
    "could", "should", "may", "might", "must", "shall", "been", "being",
    "we", "you", "they", "he", "she", "i", "my", "your", "our", "their",
    "so", "if", "then", "than", "when", "what", "which", "who", "how", "why",
    "just", "like", "really", "very", "also", "about", "into", "through",
    "during", "before", "after", "above", "below", "up", "down", "out", "off",
    "over", "under", "again", "further", "once", "here", "there", "all",
    "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
    "only", "own", "same", "too", "very", "um", "uh", "ah", "er", "hm",
}


def tokenize(text: str) -> set[str]:
    """Lowercase word set with stopwords and 1–2 letter tokens removed.

    Args:
        text: Transcript fragment.

    Returns:
        Content tokens for Jaccard compare.
    """
    words = re.findall(r"\b[a-zA-Z']+\b", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 2}


def jaccard(a: set[str], b: set[str]) -> float:
    """Jaccard similarity of two token sets.

    Args:
        a: Left token set.
        b: Right token set.

    Returns:
        ``0.0``–``1.0`` (``0.0`` if either set is empty).
    """
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def load_segments(path: Path) -> list[dict]:
    """Load Whisper/SRT segment JSON (bare list or ``{segments: [...]}``).

    Args:
        path: ``segments.json``.

    Returns:
        List of ``{start, end, text}``.
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "segments" in data:
        return data["segments"]
    return data


def preview_text(segments: list[dict], max_chars: int = 120) -> str:
    """Join segment texts and truncate for a topic preview.

    Args:
        segments: Pieces with a ``text`` field.
        max_chars: Max preview length (ellipsis after).

    Returns:
        Single-line preview string.
    """
    text = " ".join(s["text"] for s in segments).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."


def build_blocks(segments: list[dict], pause_threshold: float) -> list[dict]:
    """Group consecutive segments split by pauses ≥ ``pause_threshold``.

    Args:
        segments: Timed transcript lines.
        pause_threshold: Gap in seconds that starts a new block.

    Returns:
        Topic blocks with clocks, preview, and token sample.
    """
    if not segments:
        return []

    blocks: list[dict] = []
    current: list[dict] = [segments[0]]

    for seg in segments[1:]:
        gap = seg["start"] - current[-1]["end"]
        if gap >= pause_threshold:
            blocks.append(current)
            current = [seg]
        else:
            current.append(seg)
    blocks.append(current)

    result = []
    for i, segs in enumerate(blocks, 1):
        tokens: set[str] = set()
        for s in segs:
            tokens |= tokenize(s["text"])
        result.append(
            {
                "id": f"blk{i:02d}",
                "start": round(segs[0]["start"], 2),
                "end": round(segs[-1]["end"], 2),
                "duration": round(segs[-1]["end"] - segs[0]["start"], 2),
                "segment_count": len(segs),
                "preview": preview_text(segs),
                "tokens": sorted(tokens)[:40],
            }
        )
    return result


def score_boundaries(blocks: list[dict], segments: list[dict]) -> list[dict]:
    """Score the cut between each pair of adjacent blocks.

    Args:
        blocks: From ``build_blocks``.
        segments: Original segments (for pause measurement).

    Returns:
        Boundary dicts with ``score``, ``lexical_shift``, ``pause_sec``.
    """
    boundaries = []
    for i in range(len(blocks) - 1):
        left = blocks[i]
        right = blocks[i + 1]
        left_tokens = set(tokenize(left["preview"]))
        right_tokens = set(tokenize(right["preview"]))
        lexical_shift = 1.0 - jaccard(left_tokens, right_tokens)

        # find actual pause between blocks
        pause = 0.0
        for j, seg in enumerate(segments):
            if abs(seg["start"] - right["start"]) < 0.01:
                if j > 0:
                    pause = seg["start"] - segments[j - 1]["end"]
                break

        pause_boost = min(pause / 5.0, 1.0) * 0.3
        score = round(min(lexical_shift + pause_boost, 1.0), 3)

        reasons = []
        if lexical_shift > 0.55:
            reasons.append("lexical_shift")
        if pause >= 3.0:
            reasons.append(f"pause_{pause:.1f}s")

        boundaries.append(
            {
                "at": right["start"],
                "between": [left["id"], right["id"]],
                "score": score,
                "lexical_shift": round(lexical_shift, 3),
                "pause_sec": round(pause, 2),
                "reason": "+".join(reasons) or "weak_boundary",
            }
        )
    return boundaries


def merge_chapter_candidates(
    blocks: list[dict],
    boundaries: list[dict],
    *,
    min_sec: float,
    max_sec: float,
    context_pad: float = 10.0,
) -> list[dict]:
    """Merge topic blocks into chapter-length candidates.

    Args:
        blocks: Pause-split blocks.
        boundaries: Scores from ``score_boundaries``.
        min_sec: Prefer not to flush a chapter shorter than this.
        max_sec: Flush before the running group exceeds this.
        context_pad: Seconds pulled back onto the start clock.

    Returns:
        Candidates with ``needs_agent_review`` (titles left empty).
    """
    if not blocks:
        return []

    boundary_at = {b["at"]: b["score"] for b in boundaries}
    candidates: list[dict] = []
    group: list[dict] = [blocks[0]]
    duration = blocks[0]["duration"]

    def flush(end_block: dict, force: bool = False) -> None:
        """Emit the current group as a candidate if it is long enough (or ``force``)."""
        nonlocal group, duration
        if not group:
            return
        start = max(0.0, group[0]["start"] - context_pad)
        end = end_block["end"]
        dur = end - start
        if dur >= min_sec or force:
            candidates.append(
                {
                    "id": f"cand{len(candidates) + 1:02d}",
                    "start": round(start, 2),
                    "end": round(end, 2),
                    "duration": round(dur, 2),
                    "block_ids": [b["id"] for b in group],
                    "preview": preview_text(
                        [{"text": b["preview"]} for b in group], max_chars=200
                    ),
                    "suggested_title": None,
                    "status": "needs_agent_review",
                }
            )
        group = []
        duration = 0.0

    for i in range(1, len(blocks)):
        blk = blocks[i]
        prev = blocks[i - 1]
        boundary_score = boundary_at.get(blk["start"], 0.0)
        projected = duration + blk["duration"]

        strong_boundary = boundary_score >= 0.65 and duration >= min_sec
        over_max = projected > max_sec and duration >= min_sec * 0.8

        if strong_boundary or over_max:
            flush(prev)
            group = [blk]
            duration = blk["duration"]
        else:
            group.append(blk)
            duration = projected

    if group:
        flush(group[-1], force=True)

    return candidates


def detect_topics(
    transcript_path: Path,
    *,
    pause_threshold: float = 2.5,
    min_chapter_sec: float = 600,
    max_chapter_sec: float = 1800,
    context_pad: float = 10.0,
) -> dict:
    """Run heuristic topic detection on a transcript JSON.

    Args:
        transcript_path: ``segments.json``.
        pause_threshold: Seconds of silence that start a new block.
        min_chapter_sec: Minimum chapter candidate length.
        max_chapter_sec: Maximum chapter candidate length.
        context_pad: Seconds of lead-in on each candidate start.

    Returns:
        Topics payload for the agent to title and snap.

    Raises:
        ValueError: Empty transcript.
    """
    segments = load_segments(transcript_path)
    if not segments:
        raise ValueError(f"No segments in {transcript_path}")

    video_duration = segments[-1]["end"]
    blocks = build_blocks(segments, pause_threshold)
    boundaries = score_boundaries(blocks, segments)
    candidates = merge_chapter_candidates(
        blocks,
        boundaries,
        min_sec=min_chapter_sec,
        max_sec=max_chapter_sec,
        context_pad=context_pad,
    )

    # strip token lists from blocks in output (keep previews)
    blocks_out = [{k: v for k, v in b.items() if k != "tokens"} for b in blocks]

    return {
        "method": "heuristic",
        "source_transcript": str(transcript_path),
        "video_duration": round(video_duration, 2),
        "pause_threshold_sec": pause_threshold,
        "chapter_min_sec": min_chapter_sec,
        "chapter_max_sec": max_chapter_sec,
        "block_count": len(blocks_out),
        "blocks": blocks_out,
        "boundaries": boundaries,
        "chapter_candidates": candidates,
        "review": {
            "status": "needs_agent_review",
            "notes": "Agent: assign titles/themes, snap to sentence edges, write manifest chapters[]",
        },
    }


def main() -> None:
    """CLI: write ``*.topics.json`` next to a transcript (or ``--output``)."""
    parser = argparse.ArgumentParser(description="Heuristic topic detection from transcript")
    parser.add_argument("--transcript", required=True, help="Path to subtitles/{stem}.json")
    parser.add_argument("--output", help="Output topics.json (default: alongside transcript)")
    parser.add_argument("--pause-threshold", type=float, default=2.5)
    parser.add_argument("--min-chapter", type=float, default=600)
    parser.add_argument("--max-chapter", type=float, default=1800)
    parser.add_argument("--project", help="Project ID — reads pipeline.json chapter min/max if set")
    args = parser.parse_args()

    min_sec = args.min_chapter
    max_sec = args.max_chapter
    if args.project:
        from project_config import load_pipeline

        ch = load_pipeline(args.project).get("chapters", {})
        min_sec = ch.get("min_sec", min_sec)
        max_sec = ch.get("max_sec", max_sec)

    transcript_path = Path(args.transcript)
    out_path = Path(args.output) if args.output else transcript_path.with_name(
        transcript_path.stem + ".topics.json"
    )

    result = detect_topics(
        transcript_path,
        pause_threshold=args.pause_threshold,
        min_chapter_sec=min_sec,
        max_chapter_sec=max_sec,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f" Topics: {out_path}")
    print(f"  Blocks: {result['block_count']}")
    print(f"  Boundaries: {len(result['boundaries'])}")
    print(f"  Chapter candidates: {len(result['chapter_candidates'])}")
    for cand in result["chapter_candidates"]:
        print(f"    {cand['id']}  {cand['duration']:.0f}s  {cand['start']:.0f}–{cand['end']:.0f}")


if __name__ == "__main__":
    main()
