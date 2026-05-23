#!/usr/bin/env python3
"""Audit public-facing text for release leftovers and personal traces."""

from __future__ import annotations

import sys
from pathlib import Path


TEXT_EXTENSIONS = {".md", ".txt", ".yaml", ".yml", ".json", ".py", ".ps1", ".toml"}
IGNORE_DIRS = {".git", "__pycache__", "node_modules", ".pytest_cache"}
IGNORE_FILES = {"scripts/content_audit.py", "scripts/privacy_scan.py"}

BLOCKED_PHRASES = [
    "OWNER/codex-skill-army",
    "如果 `KW-Zh` 不是你的 GitHub 用户名",
    "如果 KW-Zh 不是你的 GitHub 用户名",
    "发布前把命令替换",
    "替换为真实",
    "真实仓库名",
    "本机状态",
    "已在本机安装",
    "Codex MCP 配置已加入",
    "D:\\",
    "C:\\Users\\",
    "xbnlkjdxzkw",
    "@nwafu.edu.cn",
    "张凯文",
]


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        rel = path.relative_to(root).as_posix()
        if rel in IGNORE_FILES:
            continue
        yield path


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    findings: list[str] = []

    for path in iter_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(root)
        for phrase in BLOCKED_PHRASES:
            if phrase in text:
                line = text[: text.index(phrase)].count("\n") + 1
                findings.append(f"{rel}:{line} contains blocked phrase: {phrase}")

    if findings:
        print("Content audit failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("Content audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
