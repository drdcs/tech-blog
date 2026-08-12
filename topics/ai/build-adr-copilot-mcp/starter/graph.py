"""Decision graph edges from frontmatter relationships."""

from __future__ import annotations

from dataclasses import dataclass

from trace_schema import ParsedAdr


@dataclass
class GraphNode:
    id: str
    title: str
    status: str


@dataclass
class GraphEdge:
    from_id: str
    to_id: str
    kind: str


def build_decision_graph(adrs: list[ParsedAdr]) -> dict:
    nodes = [
        {"id": a.frontmatter.id, "title": a.frontmatter.title, "status": a.frontmatter.status}
        for a in adrs
    ]
    edges: list[GraphEdge] = []

    for adr in adrs:
        adr_id = adr.frontmatter.id
        if adr.frontmatter.supersedes:
            edges.append(GraphEdge(adr_id, adr.frontmatter.supersedes, "supersedes"))
        if adr.frontmatter.superseded_by:
            edges.append(GraphEdge(adr.frontmatter.superseded_by, adr_id, "supersedes"))
        for related in adr.frontmatter.relates_to:
            edges.append(GraphEdge(adr_id, related, "relates_to"))

    return {
        "nodes": nodes,
        "edges": [{"from": e.from_id, "to": e.to_id, "kind": e.kind} for e in edges],
    }
