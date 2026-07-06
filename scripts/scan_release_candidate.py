#!/usr/bin/env python3
"""Fail closed on common private-course leakage patterns."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BLOCKED_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".m4a",
    ".vtt",
    ".srt",
    ".webm",
    ".zoom",
    ".cookie",
}

TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".toml",
    ".json",
    ".py",
    ".yml",
    ".yaml",
    ".html",
    ".css",
    ".ts",
    ".tsx",
}

BLOCKED_PATTERNS = [
    re.compile(r"https?://[^\\s]*(canvas|instructure)[^\\s]*", re.I),
    re.compile(r"https?://[^\\s]*zoom[^\\s]*", re.I),
    re.compile(r"cmu\.zoom", re.I),
    re.compile(r"Key-Pair-Id", re.I),
    re.compile(r"passcode", re.I),
    re.compile(r"cookie", re.I),
    re.compile(r"@andrew\.cmu\.edu", re.I),
    re.compile(r"/Users/pablo", re.I),
    re.compile(r"\b(52229|90803|90755|90-803|90-755)\b", re.I),
    re.compile(r"\bgrade(s|book)?\b", re.I),
    re.compile(r"\broster\b", re.I),
    re.compile(r"\bstudent submission\b", re.I),
    re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
    re.compile(r"sk-ant-[A-Za-z0-9_-]{12,}"),
]

ALLOWLISTED_TEXT = {
    "Do not publish video, audio, recording links, passcodes, or downloaded media.",
    "Exclude student submissions, grades, rosters, identifying student comments, raw",
    "Contains no Canvas, Zoom, LMS, transcript, recording, or media exports.",
    "Contains no student submissions, grades, rosters, or identifying comments.",
    "student submissions, generated PDFs, and professor-owned course content are excluded.",
    "Do not ingest student submissions, grades, rosters, identifying class discussion,",
    "Use this checklist before publishing any workflow, draft, or course book.",
    "Contains no student submissions, grades, rosters, or identifying comments.",
    "Student privacy review passes.",
    "student_submission",
    "Student work is outside the workflow boundary.",
    "recording metadata, passcodes, and any transcript text",
    "Contains no private local paths, keys, tokens, cookies, passcodes, or URLs.",
    "Do not claim a book is release-grade because one verification layer passed.",
    "recording passcodes, LMS snapshots, or raw video.",
}


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if path.name == "scan_release_candidate.py":
        return True
    return bool(parts & {".git", "__pycache__", ".pytest_cache", "node_modules"})


def is_allowlisted_line(line: str) -> bool:
    stripped = line.strip()
    lowered = stripped.lower()
    if lowered.startswith(("do not ", "- [ ] contains no ", "exclude ")):
        return True
    return any(item in stripped for item in ALLOWLISTED_TEXT)


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(root.rglob("*")):
        if should_skip(path) or not path.is_file():
            continue
        rel = path.relative_to(root)
        if path.suffix.lower() in BLOCKED_EXTENSIONS:
            findings.append(f"{rel}: blocked extension {path.suffix}")
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"{rel}: non-UTF-8 text-like file")
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if is_allowlisted_line(line):
                continue
            for pattern in BLOCKED_PATTERNS:
                if pattern.search(line):
                    findings.append(f"{rel}:{lineno}: matched {pattern.pattern!r}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings = scan(root)
    if findings:
        print("Release scan failed:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1
    print("Release scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
