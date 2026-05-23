#!/usr/bin/env python3
"""Check that public docs do not copy long passages from selected local skills."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


TEXT_EXTENSIONS = {".md", ".txt", ".yaml", ".yml", ".json", ".py", ".ps1", ".toml"}
IGNORE_DIRS = {".git", "__pycache__", "node_modules", ".pytest_cache"}
IGNORE_REPO_FILES = {"scripts/source_audit.py"}
DEFAULT_SOURCE_SKILLS = [
    "skill-001",
    "skill-scout",
    "skill-quartermaster",
    "literature-review",
    "officecli-docx",
    "officecli-academic-paper",
    "abaqus",
]
MIN_NORMALIZED_CHARS = 220


def normalize(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def paragraphs(text: str) -> list[str]:
    chunks = re.split(r"\n\s*\n", text)
    return [normalize(chunk) for chunk in chunks if len(normalize(chunk)) >= MIN_NORMALIZED_CHARS]


def iter_text_files(root: Path, ignore_files: set[str] | None = None):
    ignore_files = ignore_files or set()
    for path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        rel = path.relative_to(root).as_posix()
        if rel in ignore_files:
            continue
        yield path


def source_roots() -> list[Path]:
    configured = os.environ.get("CODEX_SKILL_ARMY_SOURCE_AUDIT_ROOTS")
    if configured:
        return [Path(item).expanduser() for item in configured.split(os.pathsep) if item.strip()]

    skills_root = Path.home() / ".codex" / "skills"
    return [skills_root / name for name in DEFAULT_SOURCE_SKILLS]


def main() -> int:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    sources: list[tuple[Path, str]] = []
    findings: list[str] = []

    for root in source_roots():
        if not root.exists() or not root.is_dir():
            continue
        for path in iter_text_files(root):
            sources.append((path, normalize(path.read_text(encoding="utf-8", errors="ignore"))))

    if not sources:
        print("Source audit skipped: no local source skills found.")
        return 0

    for path in iter_text_files(repo, IGNORE_REPO_FILES):
        rel = path.relative_to(repo)
        text = path.read_text(encoding="utf-8", errors="ignore")
        for para in paragraphs(text):
            for source_path, source_text in sources:
                if para and para in source_text:
                    findings.append(f"{rel} appears to copy a long passage from {source_path.name}")
                    break

    if findings:
        print("Source audit failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("Source audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
