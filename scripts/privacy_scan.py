#!/usr/bin/env python3
"""扫描公开仓库中不应出现的本机路径、凭据和隐私痕迹。"""

from __future__ import annotations

import re
import sys
from pathlib import Path


TEXT_EXTENSIONS = {".md", ".txt", ".yaml", ".yml", ".json", ".py", ".ps1", ".toml"}
IGNORE_DIRS = {".git", "__pycache__", "node_modules", ".pytest_cache"}
IGNORE_FILES = {"scripts/privacy_scan.py", "scripts/content_audit.py"}
RISKY_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".npmrc",
    ".pypirc",
    ".netrc",
    "credentials.json",
    "service-account.json",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "known_hosts",
    "config",
}
RISKY_SUFFIXES = {".pem", ".p12", ".pfx", ".key", ".kdbx"}
PATTERNS = [
    ("Windows 用户目录", re.compile(r"C:\\Users\\[^\\\s]+", re.I)),
    ("D 盘个人路径", re.compile(r"D:\\(?:0大学|codex-d盘项目库)")),
    ("个人邮箱", re.compile(r"\b[A-Za-z0-9._%+-]+@(?!users\.noreply\.github\.com\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("中国手机号", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")),
    ("身份证号", re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)")),
    ("OpenAI/Anthropic key", re.compile(r"\b(?:sk-[A-Za-z0-9_-]{20,}|sk-ant-[A-Za-z0-9_-]{20,})\b")),
    ("GitHub token", re.compile(r"\b(?:ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("Bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{24,}\b", re.I)),
    ("npm token", re.compile(r"\bnpm_[A-Za-z0-9]{20,}\b")),
    ("PyPI token", re.compile(r"\bpypi-[A-Za-z0-9_-]{20,}\b")),
    ("HuggingFace token", re.compile(r"\bhf_[A-Za-z0-9]{20,}\b")),
    ("Notion token", re.compile(r"\bsecret_[A-Za-z0-9]{20,}\b")),
    ("Sentry DSN", re.compile(r"https://[A-Za-z0-9]+@[A-Za-z0-9.-]+/\d+")),
    ("Vercel/Netlify token", re.compile(r"\b(?:vercel|netlify)[_-]?(?:token|auth)\s*[:=]\s*['\"][^'\"]+['\"]", re.I)),
    ("私钥块", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("数据库 URL", re.compile(r"\b(?:postgres|mysql|mongodb(?:\+srv)?)://[^\s)>'\"]+", re.I)),
    ("硬编码密钥", re.compile(r"\b(?:api[_-]?key|token|secret|password)\s*=\s*['\"][^'\"]+['\"]", re.I)),
]


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        rel = path.relative_to(root).as_posix()
        if rel in IGNORE_FILES:
            continue
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    findings: list[str] = []

    for path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.is_dir() and path.name in {".agentmemory", ".codex", ".ssh", ".kube"}:
            findings.append(f"仓库包含不应发布的敏感目录：{path.relative_to(root)}")
        if path.is_file() and (path.name in RISKY_FILE_NAMES or path.suffix.lower() in RISKY_SUFFIXES):
            findings.append(f"仓库包含不应发布的敏感文件：{path.relative_to(root)}")

    for path in iter_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(root)
        for name, pattern in PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                snippet = match.group(0)
                findings.append(f"{rel}:{line} 命中 {name}: {snippet}")

    if findings:
        print("Privacy scan found risks:")
        for item in findings:
            print(f"- {item}")
        return 1

    print("Privacy scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
