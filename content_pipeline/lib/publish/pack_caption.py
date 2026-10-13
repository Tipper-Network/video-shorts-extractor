"""Read platform captions from step-4 pack markdown.

Canonical example:
  step-4-ready-to-post/founder/origin-story/03-trust/sh01_reaction-vs-response_story-first.md

Pack shape (after YAML frontmatter):

```markdown
## Instagram

**Caption:**
What if there's a 5% chance I'm an idiot?

…

#ReactionVsResponse #OriginStory …
```
"""

from __future__ import annotations

import re
from pathlib import Path

_SECTION = re.compile(
    r"^##\s+(YouTube|Instagram|TikTok)\s*$",
    re.MULTILINE | re.IGNORECASE,
)
_CAPTION_LABEL = re.compile(r"^\*\*Caption:\*\*\s*$", re.MULTILINE | re.IGNORECASE)


def caption_from_pack(md_path: Path, platform: str = "instagram") -> str:
    """Extract the Caption block under ``## {platform}``. Empty if missing."""
    text = md_path.read_text(encoding="utf-8")
    # Drop YAML frontmatter
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :]

    target = platform.strip().lower()
    matches = list(_SECTION.finditer(text))
    for i, m in enumerate(matches):
        if m.group(1).lower() != target:
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[start:end]
        return _extract_caption(section)
    return ""


def _extract_caption(section: str) -> str:
    m = _CAPTION_LABEL.search(section)
    if not m:
        # Fall back: whole section minus other **Title:** style labels
        body = section.strip()
        return body
    body = section[m.end() :]
    # Stop at next **Label:** heading inside the section
    stop = re.search(r"^\*\*[A-Za-z].*:\*\*\s*$", body, re.MULTILINE)
    if stop:
        body = body[: stop.start()]
    return body.strip()


# Reference pack for credential dry-runs / docs
EXAMPLE_PACK_MD = (
    "step-4-ready-to-post/founder/origin-story/03-trust/"
    "sh01_reaction-vs-response_story-first.md"
)
EXAMPLE_PACK_MP4 = (
    "step-4-ready-to-post/founder/origin-story/03-trust/"
    "sh01_reaction-vs-response_story-first.mp4"
)
