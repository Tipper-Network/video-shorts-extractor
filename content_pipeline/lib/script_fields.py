"""Read a short script for the opening line, the land, and the words captions must keep."""

from __future__ import annotations

import re

_STOP = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "is", "it",
    "that", "this", "i", "you", "we", "my", "me",
}


def _cells(line: str) -> list[str]:
    return [p.strip() for p in line.split("|") if p.strip()]


def _first_sentence(text: str) -> str:
    text = " ".join(text.split())
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)
    return parts[0].strip()


def _tokens(text: str) -> list[str]:
    raw = re.sub(r"[^a-z0-9'\s]", " ", text.lower())
    return [t for t in raw.split() if t not in _STOP and len(t) > 1]


def lines_match(opening: str, reference: str) -> bool:
    """True when the opening line is the punchline or the situation."""
    if not opening or not reference:
        return False
    if opening.lower() in reference.lower() or reference.lower() in opening.lower():
        return True
    a, b = _tokens(opening), _tokens(reference)
    if not a or not b:
        return False
    overlap = len(set(a) & set(b))
    return overlap >= max(3, int(0.5 * min(len(a), len(b))))


def parse_script(text: str) -> dict[str, str]:
    """Pull the opening line, punchline, situation, and land from a script markdown."""
    statement = pressure = resolve = problem = ""
    hook = ""
    first_segment = ""
    first_playback = ""
    spoken = ""

    spoken_m = re.search(r"^## spoken_as\s*\n+(.+?)(?=^## |\Z)", text, re.M | re.S)
    if spoken_m:
        spoken = " ".join(spoken_m.group(1).split())

    for line in text.splitlines():
        if "|" in line and "**" in line:
            parts = _cells(line)
            if len(parts) >= 2:
                key = re.sub(r"[*_]", "", parts[0]).strip().lower()
                val = parts[-1]
                if key == "statement":
                    statement = val
                elif key == "pressure":
                    pressure = val
                elif key in ("resolve", "land"):
                    resolve = val
                elif key == "problem":
                    problem = val
        if re.match(r"\|\s*\d+\s*\|", line):
            parts = _cells(line)
            if len(parts) >= 2:
                label = parts[1].lower()
                cell = parts[-1] if len(parts) >= 5 else ""
                if cell and not re.fullmatch(r"[\d:–\-—. ]+", cell):
                    if not first_segment:
                        first_segment = cell
                    if "hook" in label and not hook:
                        hook = cell
        play = re.match(
            r"\d+\.\s+(Hook|Setup|Resolve|Pressure|Land)\b\s+(.+)$",
            line.strip(),
            re.I,
        )
        if play:
            label = play.group(1).lower()
            quote = re.split(r"\s+[—–-]\s+", play.group(2), maxsplit=1)[-1].strip()
            if not first_playback:
                first_playback = quote
            if "hook" in label and not hook:
                hook = quote

    opening = _first_sentence(first_segment or first_playback or spoken)
    punchline = hook or statement
    situation = statement or problem or pressure
    land = resolve
    wording = spoken or " ".join(
        p for p in (first_segment, hook, statement, pressure, resolve) if p
    )
    return {
        "opening": opening,
        "punchline": punchline,
        "situation": situation,
        "pressure": pressure,
        "land": land,
        "wording": wording,
    }


def opening_failure(fields: dict[str, str]) -> str | None:
    """None when the first line is the punchline or the situation. Otherwise the reason."""
    opening = fields.get("opening") or ""
    punchline = fields.get("punchline") or ""
    situation = fields.get("situation") or ""
    pressure = fields.get("pressure") or ""
    if not opening:
        return "no opening line in the script"
    if not punchline and not situation and not pressure:
        return "script has no punchline or situation"
    if lines_match(opening, punchline) or lines_match(opening, situation) or lines_match(opening, pressure):
        return None
    return (
        "first line does not match the punchline or the situation. "
        f"opening={opening!r} punchline={punchline!r} situation={situation!r}"
    )
