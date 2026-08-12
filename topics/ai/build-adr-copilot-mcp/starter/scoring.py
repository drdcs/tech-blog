"""Score TRACE completeness and detect ledger drift via git."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from trace_schema import TRACE_SECTIONS, ParsedAdr


@dataclass
class TraceScore:
    total: int
    max_score: int
    grade: str
    gaps: list[str]


def score_adr(adr: ParsedAdr) -> TraceScore:
    gaps: list[str] = []
    total = 0
    max_score = 100

    for section in TRACE_SECTIONS:
        text = adr.sections.get(section, "").strip()
        if not text or text == "_TBD_":
            gaps.append(f"Missing or placeholder section: {section}")
        elif len(text) < 40:
            gaps.append(f"Section too thin: {section}")
            total += 8
        else:
            total += 16

    if not adr.frontmatter.linked_paths:
        gaps.append("No linked_paths — decision is not anchored to code")
    else:
        total += 10

    if not adr.frontmatter.authors:
        gaps.append("No authors recorded")
    else:
        total += 5

    if adr.frontmatter.relates_to or adr.frontmatter.supersedes:
        total += 5

    total = min(total, max_score)
    grade = "A" if total >= 90 else "B" if total >= 75 else "C" if total >= 60 else "D" if total >= 45 else "F"
    return TraceScore(total=total, max_score=max_score, grade=grade, gaps=gaps)


def _git_last_touch(repo_root: Path, rel_path: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", rel_path],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        value = result.stdout.strip()
        return value or None
    except OSError:
        return None


def _file_mtime_iso(abs_path: Path) -> str | None:
    try:
        return datetime.fromtimestamp(abs_path.stat().st_mtime).isoformat()
    except OSError:
        return None


def detect_drift(repo_root: Path, adrs: list[ParsedAdr]) -> list[dict]:
    findings: list[dict] = []

    for adr in adrs:
        if adr.frontmatter.status in ("deprecated", "superseded"):
            continue

        adr_updated = adr.frontmatter.updated or adr.frontmatter.created
        cutoff = f"{adr_updated}T00:00:00"

        for linked in adr.frontmatter.linked_paths:
            abs_path = (repo_root / linked).resolve()
            changed_at = _git_last_touch(repo_root, linked) or _file_mtime_iso(abs_path)

            if not changed_at:
                findings.append(
                    {
                        "adr_id": adr.frontmatter.id,
                        "adr_title": adr.frontmatter.title,
                        "path": linked,
                        "adr_updated": adr_updated,
                        "path_changed_at": "unknown",
                        "severity": "warn",
                        "reason": "Linked path not found in workspace",
                    }
                )
                continue

            if changed_at > cutoff:
                severity = "critical" if adr.frontmatter.reversibility == "irreversible" else "warn"
                findings.append(
                    {
                        "adr_id": adr.frontmatter.id,
                        "adr_title": adr.frontmatter.title,
                        "path": linked,
                        "adr_updated": adr_updated,
                        "path_changed_at": changed_at,
                        "severity": severity,
                        "reason": "Linked code changed after ADR was last updated",
                    }
                )

    return findings
