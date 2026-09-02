"""Load per-project pipeline / playbook configuration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = BASE_DIR / "projects"
PLAYBOOKS_DIR = BASE_DIR.parent / "planning" / "playbooks"

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
    return PLAYBOOKS_DIR / f"{playbook_id}.json"


def load_playbook(playbook_id: str) -> dict[str, Any]:
    path = playbook_path(playbook_id)
    if not path.exists():
        raise FileNotFoundError(f"Playbook not found: {playbook_id} ({path})")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def list_playbooks() -> list[str]:
    if not PLAYBOOKS_DIR.exists():
        return []
    return sorted(p.stem for p in PLAYBOOKS_DIR.glob("*.json") if p.name != "README.md")


def pipeline_path(project_id: str) -> Path:
    return PROJECTS_DIR / project_id / "pipeline.json"


def load_pipeline(project_id: str) -> dict[str, Any]:
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
    pipeline = load_pipeline(project_id)
    return pipeline.get("module_order") or pipeline.get("workflow") or []


def module_enabled(project_id: str, module: str) -> bool:
    pipeline = load_pipeline(project_id)
    mod = pipeline.get("modules", {}).get(module, {})
    return bool(mod.get("enabled", False))


def chapter_cut_mode(project_id: str) -> str:
    return load_pipeline(project_id).get("chapters", {}).get("cut_mode", "contiguous")


def shorts_cut_mode(project_id: str) -> str:
    return load_pipeline(project_id).get("shorts", {}).get("cut_mode", "contiguous")
