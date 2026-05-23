#!/usr/bin/env python3
"""Check whether codex-skill-army has a publishable single-skill structure."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    ".github/workflows/validate.yml",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/skill_proposal.md",
    ".github/ISSUE_TEMPLATE/workflow_example.md",
    ".github/ISSUE_TEMPLATE/documentation_improvement.md",
    "agents/openai.yaml",
    "docs/roadmap.md",
    "docs/share-kit.md",
    "references/roles/role-taxonomy.md",
    "references/maps/research-skill-routing.md",
    "references/protocols/orchestration-protocol.md",
    "references/protocols/recruitment-protocol.md",
    "references/protocols/historian-protocol.md",
    "references/protocols/subagent-protocol.md",
    "references/protocols/validation-protocol.md",
    "references/workflows/literature-review.md",
    "references/workflows/paper-writing.md",
    "references/workflows/academic-word.md",
    "references/workflows/research-code.md",
    "references/workflows/abaqus-fea.md",
    "examples/literature-review.md",
    "examples/academic-word.md",
    "examples/research-code.md",
    "examples/missing-skill.md",
    "examples/abaqus-fea.md",
    "examples/historian.md",
    "tests/pressure_cases.json",
    "reports/agentmemory-audit-template.md",
    "scripts/source_audit.py",
]

ROLE_TERMS = ["总帅", "军师", "斥候", "主将", "副将", "监军", "军需官", "史官", "工部"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_frontmatter(skill_md: Path) -> list[str]:
    errors: list[str] = []
    text = read_text(skill_md)
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        return ["SKILL.md has no valid YAML frontmatter"]
    frontmatter = match.group(1)
    if "name: codex-skill-army" not in frontmatter:
        errors.append("SKILL.md name must be codex-skill-army")
    desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
    if not desc_match:
        errors.append("SKILL.md is missing description")
    elif len(desc_match.group(1).strip()) > 1024:
        errors.append("description exceeds 1024 characters")
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")

    if (root / "SKILL.md").exists():
        errors.extend(check_frontmatter(root / "SKILL.md"))

    skill_text = read_text(root / "SKILL.md") if (root / "SKILL.md").exists() else ""
    for term in ROLE_TERMS:
        if term not in skill_text:
            errors.append(f"SKILL.md is missing role term: {term}")

    openai_yaml = root / "agents" / "openai.yaml"
    if openai_yaml.exists() and "$codex-skill-army" not in read_text(openai_yaml):
        errors.append("agents/openai.yaml default_prompt must contain $codex-skill-army")

    readme = root / "README.md"
    if readme.exists():
        readme_text = read_text(readme)
        for term in ["Research-first", "九角色军制", "动态点将", "source_audit.py"]:
            if term not in readme_text:
                errors.append(f"README.md is missing publish term: {term}")

    if errors:
        print("Structure check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Structure check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
