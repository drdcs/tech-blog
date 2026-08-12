"""Filesystem ledger for TRACE markdown decisions."""

from __future__ import annotations

import re
from dataclasses import asdict
from datetime import date
from pathlib import Path

import yaml

from trace_schema import (
    TRACE_SECTIONS,
    ParsedAdr,
    TraceFrontmatter,
    empty_trace_body,
    slug_from_id_and_title,
)


def _parse_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    pattern = re.compile(r"^## (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(body))

    for i, match in enumerate(matches):
        heading = match.group(1).strip()
        if heading not in TRACE_SECTIONS:
            continue
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sections[heading] = body[start:end].strip()

    return sections


def _frontmatter_from_dict(data: dict) -> TraceFrontmatter:
    return TraceFrontmatter(
        id=str(data["id"]),
        title=str(data["title"]),
        status=data.get("status", "proposed"),
        created=str(data.get("created", "")),
        updated=data.get("updated"),
        authors=list(data.get("authors", [])),
        reversibility=data.get("reversibility", "moderate"),
        supersedes=data.get("supersedes"),
        superseded_by=data.get("superseded_by"),
        relates_to=list(data.get("relates_to", [])),
        linked_paths=list(data.get("linked_paths", [])),
        tags=list(data.get("tags", [])),
    )


def _read_markdown(path: Path) -> tuple[TraceFrontmatter, str]:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise ValueError(f"Missing frontmatter: {path}")
    _, fm_block, body = raw.split("---", 2)
    data = yaml.safe_load(fm_block) or {}
    return _frontmatter_from_dict(data), body.strip()


def _write_markdown(path: Path, frontmatter: TraceFrontmatter, body: str) -> None:
    payload = asdict(frontmatter)
    if payload.get("superseded_by") is None:
        payload.pop("superseded_by", None)
    if payload.get("updated") is None:
        payload.pop("updated", None)
    text = "---\n" + yaml.safe_dump(payload, sort_keys=False) + "---\n\n" + body
    path.write_text(text, encoding="utf-8")


class AdrStore:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir

    def ensure_root(self) -> None:
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def list_all(self) -> list[ParsedAdr]:
        self.ensure_root()
        adrs: list[ParsedAdr] = []
        for path in sorted(self.root_dir.glob("*.md")):
            parsed = self.get_by_slug(path.stem)
            if parsed:
                adrs.append(parsed)
        return sorted(adrs, key=lambda a: a.frontmatter.id)

    def get_by_slug(self, slug: str) -> ParsedAdr | None:
        path = self.root_dir / f"{slug}.md"
        if not path.exists():
            return None
        try:
            frontmatter, body = _read_markdown(path)
            return ParsedAdr(
                file_path=str(path),
                slug=slug,
                frontmatter=frontmatter,
                body=body,
                sections=_parse_sections(body),
            )
        except (OSError, ValueError, yaml.YAMLError):
            return None

    def get_by_id(self, adr_id: str) -> ParsedAdr | None:
        for adr in self.list_all():
            if adr.frontmatter.id == adr_id:
                return adr
        return None

    def draft(
        self,
        adr_id: str,
        title: str,
        trigger: str,
        authors: list[str] | None = None,
        reversibility: str = "moderate",
        tags: list[str] | None = None,
        linked_paths: list[str] | None = None,
    ) -> ParsedAdr:
        today = date.today().isoformat()
        frontmatter = TraceFrontmatter(
            id=adr_id,
            title=title,
            status="proposed",
            created=today,
            updated=today,
            authors=authors or [],
            reversibility=reversibility or "moderate",
            linked_paths=linked_paths or [],
            tags=tags or [],
        )
        slug = slug_from_id_and_title(adr_id, title)
        path = self.root_dir / f"{slug}.md"
        body = empty_trace_body(trigger)
        self.ensure_root()
        _write_markdown(path, frontmatter, body)
        result = self.get_by_slug(slug)
        if not result:
            raise RuntimeError("Failed to write ADR")
        return result

    def link_paths(self, adr_id: str, paths: list[str]) -> ParsedAdr:
        adr = self.get_by_id(adr_id)
        if not adr:
            raise ValueError(f"ADR {adr_id} not found")

        merged = sorted(set(adr.frontmatter.linked_paths) | set(paths))
        fm = adr.frontmatter
        fm.linked_paths = merged
        fm.updated = date.today().isoformat()
        _write_markdown(Path(adr.file_path), fm, adr.body)

        result = self.get_by_slug(adr.slug)
        if not result:
            raise RuntimeError("Failed to update ADR")
        return result

    def build_index_markdown(self) -> str:
        adrs = self.list_all()
        lines = [
            "# TRACE decision ledger",
            "",
            f"_{len(adrs)} recorded decision(s)_",
            "",
            "| ID | Status | Title | Reversibility |",
            "| --- | --- | --- | --- |",
        ]
        for adr in adrs:
            fm = adr.frontmatter
            lines.append(f"| {fm.id} | {fm.status} | {fm.title} | {fm.reversibility} |")
        return "\n".join(lines) + "\n"
