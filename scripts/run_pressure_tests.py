#!/usr/bin/env python3
"""Static pressure tests for role coverage and research SOP completeness."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_CASES = {
    "simple-direct-answer",
    "literature-review",
    "systematic-review-meta",
    "academic-word",
    "research-code",
    "notebook-reproducibility",
    "future-skill-routing",
    "missing-skill",
    "historian",
    "privacy-boundary",
    "safe-install",
    "risky-recruitment",
    "paper-writing",
    "abaqus-fea",
    "abaqus-contact-thermal",
    "public-language",
    "source-audit",
}

REQUIRED_DOCUMENT_TERMS = {
    "SKILL.md": ["总帅", "军师", "斥候", "主将", "副将", "监军", "军需官", "史官", "工部", "可见技能列表"],
    "README.md": ["Research-first", "九角色军制", "动态点将", "与其他方式的区别", "--path .", "--name codex-skill-army"],
    "docs/quick-start.md": ["--path .", "--name codex-skill-army", "重启 Codex"],
    "references/maps/research-skill-routing.md": ["未来 skill 纳入规则", "防侵权边界", "Abaqus 热/耦合"],
    "references/protocols/historian-protocol.md": ["不默认保存", "AGENTMEMORY_INJECT_CONTEXT=false", "token", "写入前", "删除"],
    "references/protocols/recruitment-protocol.md": ["安全排除", "默认排除", "征召令"],
    "scripts/install-local.ps1": ["ConfirmOverwrite", "WhatIf", "Target path"],
    "scripts/source_audit.py": ["MIN_NORMALIZED_CHARS", "DEFAULT_SOURCE_SKILLS"],
    "references/workflows/literature-review.md": ["数据库", "检索式", "纳入", "DOI", "PRISMA", "Meta 分析", "偏倚风险"],
    "references/workflows/academic-word.md": ["OMML", "交叉引用", "参考文献", "PDF", "Times New Roman", "页边距"],
    "references/workflows/research-code.md": ["环境锁定", "随机种子", "Notebook", "数据路径脱敏"],
    "references/workflows/abaqus-fea.md": ["材料模型", "单元类型", "网格收敛", "ODB", "接触算法", "热边界"],
    "references/workflows/paper-writing.md": ["论证链", "审稿回复", "数据可用性"],
    "examples/abaqus-fea.md": ["Abaqus", "ODB", "单位"],
    "examples/historian.md": ["史官", "长期记忆", "确认"],
}

REQUIRED_CASE_FIELDS = ["id", "prompt", "route", "required_actions", "forbidden_actions", "validation"]


def as_text(value) -> str:
    return json.dumps(value, ensure_ascii=False)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    case_path = root / "tests" / "pressure_cases.json"
    cases = json.loads(case_path.read_text(encoding="utf-8"))
    by_id = {case["id"]: case for case in cases if "id" in case}
    errors: list[str] = []

    missing = REQUIRED_CASES - set(by_id)
    if missing:
        errors.append(f"missing pressure cases: {', '.join(sorted(missing))}")

    for case in cases:
        case_id = case.get("id", "<missing id>")
        for field in REQUIRED_CASE_FIELDS:
            if field not in case:
                errors.append(f"{case_id} is missing field: {field}")
        for field in ["route", "required_actions", "forbidden_actions", "validation"]:
            value = case.get(field)
            if not isinstance(value, list) or not value:
                errors.append(f"{case_id}.{field} must be a non-empty list")

        case_text = as_text(case)
        no_main_case = {
            "simple-direct-answer",
            "missing-skill",
            "historian",
            "privacy-boundary",
            "safe-install",
            "risky-recruitment",
            "public-language",
            "source-audit",
        }
        if case_id not in no_main_case:
            for term in ["主将", "监军"]:
                if term not in case_text:
                    errors.append(f"{case_id} should define routing or validation around: {term}")
        if "forbidden_actions" in case and any("默认安装" in item for item in case.get("forbidden_actions", [])):
            errors.append(f"{case_id} should phrase install risks specifically, not as a vague default-install ban")

    simple = by_id.get("simple-direct-answer", {})
    if "直接回答" not in as_text(simple) or "完整调度令" not in as_text(simple):
        errors.append("simple-direct-answer must require direct answer and forbid full dispatch order")

    for case_id in ["privacy-boundary", "risky-recruitment", "safe-install", "source-audit"]:
        text = as_text(by_id.get(case_id, {}))
        for term in ["forbidden_actions", "validation"]:
            if term not in text:
                errors.append(f"{case_id} must contain {term}")

    for rel, terms in REQUIRED_DOCUMENT_TERMS.items():
        text = (root / rel).read_text(encoding="utf-8", errors="ignore")
        for term in terms:
            if term not in text:
                errors.append(f"{rel} is missing release-gate term: {term}")

    if errors:
        print("Pressure tests failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Pressure tests passed: {len(cases)} cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
