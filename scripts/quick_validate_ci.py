#!/usr/bin/env python3
"""CI-friendly minimal Codex skill validation without external dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", frontmatter, re.M)
    if not match:
        return None
    value = match.group(1).strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        print("SKILL.md not found")
        return 1

    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        print("No YAML frontmatter found")
        return 1

    frontmatter = match.group(1)
    name = frontmatter_value(frontmatter, "name")
    description = frontmatter_value(frontmatter, "description")

    if name != "codex-skill-army":
        print(f"Invalid skill name: {name!r}")
        return 1
    if not description:
        print("Missing description")
        return 1
    if len(description) > 1024:
        print("Description too long")
        return 1
    if "<" in description or ">" in description:
        print("Description cannot contain angle brackets")
        return 1

    print("Skill quick validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
