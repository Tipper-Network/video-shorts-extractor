"""Resolve per-project paths — each project lives under workspace/projects/{id}/."""

from __future__ import annotations

from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = BASE_DIR.parent
PROJECTS_ROOT = WORKSPACE_ROOT / "projects"


def project_root(project_id: str) -> Path:
    """Absolute ``projects/{folder}/`` for this id.

    Args:
        project_id: Slug or ``pipeline.json`` ``project_id`` (folder name may differ).

    Returns:
        Project root directory.
    """
    from project_config import find_project_dir

    return find_project_dir(project_id)


class ProjectPaths:
    """All paths for one project, relative to projects/{id}/."""

    def __init__(self, project_id: str, cfg: dict[str, Any] | None = None):
        """Build path handles from ``pipeline.json`` ``paths``, else the default layout.

        Args:
            project_id: Project slug / id.
            cfg: Optional pipeline dict; uses ``cfg["paths"]`` overlays.
        """
        self.project_id = project_id
        self.root = project_root(project_id)
        paths = (cfg or {}).get("paths") or {}

        self.input_dir = self._resolve(paths.get("input", "input"))
        self.master_dir = self._resolve(paths.get("master_dir", "output/master"))
        self.master_file = self._resolve(
            paths.get("master", "output/master/timeline_normalized.mp4")
        )
        self.plan_dir = self._resolve(paths.get("plan_dir", "output/plan"))
        self.logs_dir = self._resolve(paths.get("logs_dir", "output/logs"))
        self.cache_dir = self._resolve(paths.get("cache_dir", "output/cache/normalized"))
        self.deliverables_dir = self._resolve(
            paths.get("deliverables_dir", "output/deliverables")
        )
        self.transcript_dir = self._resolve(
            paths.get("transcript_dir", "output/transcript")
        )
        self.audio_cache_dir = self._resolve(
            paths.get("audio_cache_dir", "output/cache/audio")
        )

    def _resolve(self, raw: str | Path) -> Path:
        """Turn a project-relative or absolute path into an absolute Path.

        Args:
            raw: Relative to the project root, or already absolute.

        Returns:
            Resolved absolute path.
        """
        path = Path(raw).expanduser()
        if path.is_absolute():
            return path
        return (self.root / path).resolve()

    def clip_map_path(self) -> Path:
        """`clip-map.json` at the project root (timelapse / multi-clip jobs)."""
        return self.root / "clip-map.json"

    def manifest_path(self) -> Path:
        """Approved cut plan: `output/plan/manifest.json`."""
        return self.plan_dir / "manifest.json"

    def segment_pool_path(self) -> Path:
        """Candidate slices for montage shorts: `output/plan/segment-pool.json`."""
        return self.plan_dir / "segment-pool.json"

    def shorts_dir(self) -> Path:
        """Draft 9:16 renders: `output/deliverables/shorts/`."""
        return self.deliverables_dir / "shorts"

    def shorts_approved_dir(self) -> Path:
        """Signed-off shorts: `output/deliverables/shorts_approved/`."""
        return self.deliverables_dir / "shorts_approved"

    def deliverable_dir(self, platform: str) -> Path:
        """Subfolder under deliverables named after ``platform`` (legacy layout).

        Args:
            platform: Folder name (``youtube``, ``tiktok``, …).

        Returns:
            ``output/deliverables/{platform}/``.
        """
        return self.deliverables_dir / platform

    def resolve(self, relative: str | Path) -> Path:
        """Resolve a path that may be project-relative.

        Args:
            relative: Project-relative or absolute path.

        Returns:
            Absolute path under this project (or the absolute path unchanged).
        """
        return self._resolve(relative)

    def transcript_txt_path(self) -> Path:
        """Legacy single-file Whisper clocks: `output/transcript/transcript.txt`."""
        return self.transcript_dir / "transcript.txt"

    def segments_json_path(self) -> Path:
        """Legacy single-file segments JSON next to `transcript.txt`."""
        return self.transcript_dir / "segments.json"

    def words_json_path(self) -> Path:
        """Legacy Vosk word JSON next to `transcript.txt`."""
        return self.transcript_dir / "words.json"

    def ensure_dirs(self) -> None:
        """Create the standard input / output / cache folders if they are missing."""
        for path in (
            self.input_dir,
            self.master_dir,
            self.plan_dir,
            self.logs_dir,
            self.cache_dir,
            self.transcript_dir,
            self.audio_cache_dir,
            self.deliverables_dir,
            self.deliverables_dir / "shorts",
            self.deliverables_dir / "shorts_approved",
            self.deliverables_dir / "chunks",
        ):
            path.mkdir(parents=True, exist_ok=True)


def load_project_paths(project_id: str) -> ProjectPaths:
    """Load ``pipeline.json`` (if any) and return path handles.

    Args:
        project_id: Slug or ``pipeline.json`` ``project_id``.

    Returns:
        Path object for that project (empty config if pipeline load fails).
    """
    try:
        from project_config import load_pipeline

        pipeline = load_pipeline(project_id)
    except Exception:
        pipeline = {}
    return ProjectPaths(project_id, pipeline)
