"""TRACE decision record schema — frontmatter fields and section headings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

AdrStatus = Literal["proposed", "accepted", "deprecated", "superseded"]
Reversibility = Literal["easy", "moderate", "hard", "irreversible"]

TRACE_SECTIONS: tuple[str, ...] = (
    "Trigger",
    "Reversibility notes",
    "Alternatives considered",
    "Consequences",
    "Evidence",
)


@dataclass
class TraceFrontmatter:
    id: str
    title: str
    status: AdrStatus = "proposed"
    created: str = ""
    updated: str | None = None
    authors: list[str] = field(default_factory=list)
    reversibility: Reversibility = "moderate"
    supersedes: str | None = None
    superseded_by: str | None = None
    relates_to: list[str] = field(default_factory=list)
    linked_paths: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


@dataclass
class ParsedAdr:
    file_path: str
    slug: str
    frontmatter: TraceFrontmatter
    body: str
    sections: dict[str, str]


def slug_from_id_and_title(adr_id: str, title: str) -> str:
    kebab = "".join(c if c.isalnum() else "-" for c in title.lower())
    while "--" in kebab:
        kebab = kebab.replace("--", "-")
    kebab = kebab.strip("-")[:48]
    return f"{adr_id}-{kebab}"


def empty_trace_body(trigger: str) -> str:
    parts: list[str] = []
    for heading in TRACE_SECTIONS:
        content = trigger if heading == "Trigger" else "_TBD_"
        parts.append(f"## {heading}\n\n{content}")
    return "\n\n".join(parts) + "\n"
