---
id: "0001"
title: "Adopt TRACE ledger for architecture decisions"
status: accepted
created: 2026-08-12
updated: 2026-08-12
authors:
  - platform-team
reversibility: easy
relates_to: []
linked_paths:
  - docs/decisions
  - .vscode/mcp.json
tags:
  - governance
  - mcp
---

## Trigger

Engineering decisions live in Slack threads, PR comments, and tribal memory. New hires cannot find why we chose Kafka over Pub/Sub, and agents in the IDE have no structured decision context to cite.

## Reversibility notes

Switching to another ADR format is a markdown migration. MCP server config is a one-line change in `.vscode/mcp.json`.

## Alternatives considered

- **Confluence-only ADRs** — searchable but invisible to coding agents.
- **Plain README** — no lifecycle, no graph, no drift detection.
- **Nygard ADR template** — good narrative, but no machine-readable links to code paths.

## Consequences

- Positive: decisions become agent-readable resources via `adr://` URIs.
- Positive: drift checks flag stale records when linked files change.
- Negative: team must maintain `linked_paths` discipline.
- Negative: proposed records with `_TBD_` sections score poorly until completed.

## Evidence

Pilot with VS Code Copilot Agent mode showed faster onboarding answers for "why is this queue here?" questions when `trace_get` and decision resources were available.
