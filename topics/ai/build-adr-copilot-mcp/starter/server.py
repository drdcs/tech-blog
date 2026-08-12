#!/usr/bin/env python3
"""ADR Copilot MCP — TRACE ledger server built with FastMCP."""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path

from fastmcp import FastMCP

from adr_store import AdrStore
from graph import build_decision_graph
from scoring import detect_drift, score_adr

REPO_ROOT = Path(os.environ.get("ADR_REPO_ROOT", Path.cwd()))
ADR_ROOT = Path(os.environ.get("ADR_ROOT", REPO_ROOT / "docs" / "decisions"))
store = AdrStore(ADR_ROOT)

mcp = FastMCP(
    name="adr-copilot",
    instructions=(
        "TRACE architecture decision ledger. Use trace_list/trace_get for context, "
        "trace_drift_check before releases, and adr:// resources for full records."
    ),
)


# --- Step 5+: Tools -----------------------------------------------------------

@mcp.tool
def trace_list(status: str | None = None) -> str:
    """List TRACE decisions with optional status filter (proposed, accepted, deprecated, superseded)."""
    adrs = store.list_all()
    if status:
        adrs = [a for a in adrs if a.frontmatter.status == status]
    payload = [
        {
            "id": a.frontmatter.id,
            "title": a.frontmatter.title,
            "status": a.frontmatter.status,
            "reversibility": a.frontmatter.reversibility,
            "resource": f"adr://decisions/{a.slug}",
        }
        for a in adrs
    ]
    return json.dumps(payload, indent=2)


@mcp.tool
def trace_get(adr_id: str) -> str:
    """Fetch one decision by four-digit id with TRACE sections and completeness score."""
    adr = store.get_by_id(adr_id)
    if not adr:
        return json.dumps({"error": f"ADR {adr_id} not found"})
    score = score_adr(adr)
    return json.dumps(
        {
            **asdict(adr.frontmatter),
            "slug": adr.slug,
            "sections": adr.sections,
            "score": asdict(score),
            "resource": f"adr://decisions/{adr.slug}",
        },
        indent=2,
    )


@mcp.tool
def trace_draft(
    adr_id: str,
    title: str,
    trigger: str,
    authors: list[str] | None = None,
    reversibility: str = "moderate",
    tags: list[str] | None = None,
    linked_paths: list[str] | None = None,
) -> str:
    """Create a proposed TRACE decision with section skeletons."""
    adr = store.draft(
        adr_id=adr_id,
        title=title,
        trigger=trigger,
        authors=authors,
        reversibility=reversibility,  # type: ignore[arg-type]
        tags=tags,
        linked_paths=linked_paths,
    )
    return json.dumps(
        {
            "created": adr.slug,
            "path": adr.file_path,
            "resource": f"adr://decisions/{adr.slug}",
            "message": "Proposed TRACE decision drafted. Review sections before accepting.",
        },
        indent=2,
    )


@mcp.tool
def trace_link_paths(adr_id: str, paths: list[str]) -> str:
    """Attach repository paths to a decision for drift detection."""
    adr = store.link_paths(adr_id, paths)
    return json.dumps(
        {"id": adr.frontmatter.id, "linked_paths": adr.frontmatter.linked_paths},
        indent=2,
    )


@mcp.tool
def trace_graph() -> str:
    """Return decision graph nodes and edges (supersedes, relates_to)."""
    return json.dumps(build_decision_graph(store.list_all()), indent=2)


@mcp.tool
def trace_drift_check() -> str:
    """Find ADRs whose linked_paths changed in git after the record was last updated."""
    findings = detect_drift(REPO_ROOT, store.list_all())
    return json.dumps(
        {
            "checked_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
            "finding_count": len(findings),
            "findings": findings,
        },
        indent=2,
    )


@mcp.tool
def trace_score(adr_id: str) -> str:
    """Grade ADR completeness (A–F) and list gaps to fix before review."""
    adr = store.get_by_id(adr_id)
    if not adr:
        return json.dumps({"error": f"ADR {adr_id} not found"})
    return json.dumps(asdict(score_adr(adr)), indent=2)


# --- Step 8: Resources --------------------------------------------------------

@mcp.resource("adr://index")
def decision_index() -> str:
    """Tabular index of all TRACE architecture decisions."""
    return store.build_index_markdown()


@mcp.resource("adr://decisions/{slug}")
def decision_resource(slug: str) -> str:
    """Full TRACE markdown for one decision, with score header."""
    adr = store.get_by_slug(slug)
    if not adr:
        raise ValueError(f"Decision not found: {slug}")
    score = score_adr(adr)
    header = (
        f"# {adr.frontmatter.id} — {adr.frontmatter.title}\n\n"
        f"**Status:** {adr.frontmatter.status}\n"
        f"**Reversibility:** {adr.frontmatter.reversibility}\n"
        f"**Completeness:** {score.grade} ({score.total}/{score.max_score})\n\n"
    )
    return header + adr.body


# --- Step 9: Prompts ----------------------------------------------------------

@mcp.prompt
def red_team_adr(adr_id: str) -> str:
    """Stress-test a decision record before accepting it in review."""
    adr = store.get_by_id(adr_id)
    if not adr:
        return f"ADR {adr_id} not found."
    score = score_adr(adr)
    return f"""You are a staff engineer reviewing architecture decision {adr_id}.

Decision title: {adr.frontmatter.title}
Status: {adr.frontmatter.status}
Reversibility: {adr.frontmatter.reversibility}
Completeness grade: {score.grade}
Known gaps: {"; ".join(score.gaps) or "none"}

Challenge this ADR:
1. What assumptions are unstated?
2. What failure mode appears in year two?
3. Which alternative was dismissed too quickly?
4. What metric would falsify this decision in production?
5. If we had to reverse this in 48 hours, what breaks?

Be direct. Cite missing TRACE sections where evidence is thin."""


@mcp.prompt
def onboard_teammate(adr_id: str) -> str:
    """Explain a decision and its blast radius to a new engineer."""
    adr = store.get_by_id(adr_id)
    if not adr:
        return f"ADR {adr_id} not found."
    graph = build_decision_graph(store.list_all())
    related = [e for e in graph["edges"] if e["from"] == adr_id or e["to"] == adr_id]
    paths = ", ".join(adr.frontmatter.linked_paths) or "none linked yet"
    rel = ", ".join(f"{e['kind']} {e['from']}->{e['to']}" for e in related) or "none"
    return f"""You are onboarding a mid-level engineer to decision {adr_id}: "{adr.frontmatter.title}".

Explain in plain language:
1. What problem triggered this decision
2. What we chose and what we rejected
3. Which files implement it ({paths})
4. Related decisions: {rel}
5. One question they should ask in their first PR touching this area

Keep it under 300 words. No jargon without definition."""


@mcp.prompt
def deprecation_plan(adr_id: str) -> str:
    """Draft a safe rollback or supersession plan for an accepted ADR."""
    adr = store.get_by_id(adr_id)
    if not adr:
        return f"ADR {adr_id} not found."
    paths = ", ".join(adr.frontmatter.linked_paths) or "none"
    return f"""Decision {adr_id} ("{adr.frontmatter.title}") may need deprecation or supersession.

Reversibility class: {adr.frontmatter.reversibility}
Linked paths: {paths}

Produce a deprecation plan with:
1. Preconditions to deprecate (metrics, traffic, ownership)
2. Migration steps ordered by risk
3. Rollback triggers
4. Communication template for dependent teams
5. Suggested superseding ADR outline if reversal is impossible"""


if __name__ == "__main__":
    store.ensure_root()
    mcp.run()
