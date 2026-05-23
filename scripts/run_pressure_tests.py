#!/usr/bin/env python3
"""Static pressure tests for role coverage and research SOP completeness."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_CASES = {
    "simple-direct-answer",
    "literature-review",
    "academic-word",
    "research-code",
    "missing-skill",
    "historian",
    "privacy-boundary",
    "safe-install",
    "risky-recruitment",
    "paper-writing",
    "abaqus-fea",
}

REQUIRED_TERMS = {
    "simple-direct-answer": ["直接回答", "不进入完整军制"],
    "literature-review": ["文献", "引用", "史官", "检索式"],
    "academic-word": ["Word", "公式", "排版", "交叉引用"],
    "research-code": ["CodeGraph", "分兵", "合围"],
    "missing-skill": ["斥候", "征召令", "不默认安装"],
    "historian": ["史官", "长期偏好", "token"],
    "privacy-boundary": ["凭据", "隐私", "不默认保存"],
    "safe-install": ["不覆盖", "确认", "目标路径"],
    "risky-recruitment": ["排除", "高风险", "批量"],
    "paper-writing": ["论证链", "摘要", "审稿回复"],
    "abaqus-fea": ["材料模型", "单元类型", "ODB"],
}

REQUIRED_DOCUMENT_TERMS = {
    "SKILL.md": ["总帅", "军师", "斥候", "主将", "副将", "监军", "军需官", "史官", "工部"],
    "references/protocols/historian-protocol.md": ["不默认保存", "AGENTMEMORY_INJECT_CONTEXT=false", "token", "写入前", "删除"],
    "references/protocols/recruitment-protocol.md": ["安全排除", "默认排除", "征召令"],
    "scripts/install-local.ps1": ["ConfirmOverwrite", "WhatIf", "Target path"],
    "references/workflows/literature-review.md": ["数据库", "检索式", "纳入", "DOI", "PRISMA"],
    "references/workflows/academic-word.md": ["OMML", "交叉引用", "参考文献", "PDF"],
    "references/workflows/abaqus-fea.md": ["材料模型", "单元类型", "网格收敛", "ODB"],
    "references/workflows/paper-writing.md": ["论证链", "审稿回复", "数据可用性"],
    "examples/abaqus-fea.md": ["Abaqus", "ODB", "单位"],
    "examples/historian.md": ["史官", "长期记忆", "确认"],
}


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    case_path = root / "tests" / "pressure_cases.json"
    cases = json.loads(case_path.read_text(encoding="utf-8"))
    by_id = {case["id"]: case for case in cases}
    errors: list[str] = []

    missing = REQUIRED_CASES - set(by_id)
    if missing:
        errors.append(f"missing pressure cases: {', '.join(sorted(missing))}")

    for case_id, terms in REQUIRED_TERMS.items():
        if case_id not in by_id:
            continue
        case_text = json.dumps(by_id[case_id], ensure_ascii=False)
        for term in terms:
            if term not in case_text:
                errors.append(f"{case_id} does not cover term: {term}")

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
