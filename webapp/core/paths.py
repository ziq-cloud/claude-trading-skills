"""Repository path helpers (resolved dynamically; no hardcoded user paths)."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"
SKILLS_INDEX = REPO_ROOT / "skills-index.yaml"
REPORTS_DIR = REPO_ROOT / "reports"
