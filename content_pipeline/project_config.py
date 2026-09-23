"""Load per-project pipeline / playbook configuration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = BASE_DIR.parent
PROJECTS_DIR = WORKSPACE_ROOT / "projects"
PLAYBOOKS_DIR = WORKSPACE_ROOT / "planning" / "playbooks"

DEFAULT_PIPELINE: dict[str, Any] = {
    "project_id": "",
    "playbook_id": None,
    "modules": {
        "concat": {"enabled": False},
        "transcribe": {"enabled": True},
        "detect_topics": {"enabled": True, "method": "heuristic"},
        "plan_manifest": {"enabled": True, "planner": "cursor-agent"},
        "compose_shorts": {"enabled": False},
        "render": {"enabled": True, "trim_on_render": True},
        "trim_silence": {"enabled": False},
        "polish": {"enabled": False},
    },
    "chapters": {
        "cut_mode": "contiguous",
        "min_sec": 600,
        "max_sec": 1800,
        "default_trim": "light",
    },
    "shorts": {
        "cut_mode": "contiguous",
        "default_trim": "moderate",
    },
    "flywheel": {
        "enabled": True,
        "tag_shorts": True,
    },
}


def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge ``overlay`` onto a copy of ``base``.

    Args:
        base: Playbook or default pipeline.
        overlay: Project ``pipeline.json`` (ids/overrides keys are skipped here).

    Returns:
        New dict; nested dicts are merged, other values replaced.
    """
    result = json.loads(json.dumps(base))
    for key, value in overlay.items():
        if key in ("playbook_id", "project_id", "overrides"):
            continue
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def playbook_path(playbook_id: str) -> Path:
    """Path to ``planning/playbooks/{playbook_id}.json``.

    Args:
        playbook_id: Stem, e.g. ``flywheel-episode``.

    Returns:
        Absolute playbook path (may not exist yet).
    """
    return PLAYBOOKS_DIR / f"{playbook_id}.json"


def load_playbook(playbook_id: str) -> dict[str, Any]:
    """Read one playbook JSON.

    Args:
        playbook_id: Stem under ``planning/playbooks/``.

    Returns:
        Parsed playbook dict.

    Raises:
        FileNotFoundError: No such playbook file.
    """
    path = playbook_path(playbook_id)
    if not path.exists():
        raise FileNotFoundError(f"Playbook not found: {playbook_id} ({path})")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def list_playbooks() -> list[str]:
    """Sorted playbook ids (filename stems) under ``planning/playbooks/``.

    Returns:
        Playbook ids, excluding README.
    """
    if not PLAYBOOKS_DIR.exists():
        return []
    return sorted(p.stem for p in PLAYBOOKS_DIR.glob("*.json") if p.name != "README.md")


def find_project_dir(project_id: str) -> Path:
    """Resolve the project folder by folder name or ``pipeline.json`` ``project_id``.

    Args:
        project_id: Folder slug or the id written inside ``pipeline.json``.

    Returns:
        ``projects/{folder}/``. Falls back to ``projects/{project_id}/`` if unmatched.
    """
    direct = PROJECTS_DIR / project_id
    if (direct / "pipeline.json").exists() or direct.is_dir():
        if (direct / "pipeline.json").exists():
            return direct

    if not PROJECTS_DIR.exists():
        return direct

    for path in sorted(PROJECTS_DIR.iterdir()):
        if not path.is_dir() or path.name.startswith("_"):
            continue
        pipeline_file = path / "pipeline.json"
        if not pipeline_file.exists():
            if path.name == project_id:
                return path
            continue
        try:
            data = json.loads(pipeline_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if data.get("project_id") == project_id:
            return path
    return direct


def pipeline_path(project_id: str) -> Path:
    """``pipeline.json`` inside the resolved project folder.

    Args:
        project_id: Slug or pipeline id.

    Returns:
        Path to ``pipeline.json``.
    """
    return find_project_dir(project_id) / "pipeline.json"


def load_pipeline(project_id: str) -> dict[str, Any]:
    """Merge playbook + project ``pipeline.json`` + ``overrides``.

    Args:
        project_id: Slug or pipeline id.

    Returns:
        Full pipeline dict. Uses ``DEFAULT_PIPELINE`` when no file exists.
    """
    path = pipeline_path(project_id)
    if not path.exists():
        data = json.loads(json.dumps(DEFAULT_PIPELINE))
        data["project_id"] = project_id
        return data

    with open(path, encoding="utf-8") as f:
        project_data = json.load(f)

    # Start from playbook template if playbook_id set
    playbook_id = project_data.get("playbook_id")
    if playbook_id:
        base = load_playbook(playbook_id)
        # legacy alias
        if "workflow" in project_data and "module_order" not in project_data:
            project_data["module_order"] = project_data["workflow"]
    else:
        base = json.loads(json.dumps(DEFAULT_PIPELINE))

    merged = _deep_merge(base, project_data)
    merged["project_id"] = project_id
    if playbook_id:
        merged["playbook_id"] = playbook_id

    overrides = project_data.get("overrides", {})
    if overrides:
        merged = _deep_merge(merged, overrides)

    return merged


def module_order(project_id: str) -> list[str]:
    """Module names in run order.

    Args:
        project_id: Slug or pipeline id.

    Returns:
        ``module_order`` or legacy ``workflow``, else ``[]``.
    """
    pipeline = load_pipeline(project_id)
    return pipeline.get("module_order") or pipeline.get("workflow") or []


def module_enabled(project_id: str, module: str) -> bool:
    """Whether a module is on for this project.

    Args:
        project_id: Slug or pipeline id.
        module: Key under ``modules`` (``concat``, ``srt_to_text``, …).

    Returns:
        True if ``modules.{module}.enabled`` is set.
    """
    pipeline = load_pipeline(project_id)
    mod = pipeline.get("modules", {}).get(module, {})
    return bool(mod.get("enabled", False))


def chapter_cut_mode(project_id: str) -> str:
    """How chapters are cut.

    Args:
        project_id: Slug or pipeline id.

    Returns:
        ``contiguous`` (default) or ``supercut``.
    """
    return load_pipeline(project_id).get("chapters", {}).get("cut_mode", "contiguous")


def shorts_cut_mode(project_id: str) -> str:
    """How shorts are cut.

    Args:
        project_id: Slug or pipeline id.

    Returns:
        ``contiguous`` (default) or ``supercut``.
    """
    return load_pipeline(project_id).get("shorts", {}).get("cut_mode", "contiguous")
