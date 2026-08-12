# ADR Copilot MCP (Python + FastMCP)

Original TRACE ledger server for the Tech Blog tutorial.

## Quick start

```bash
cd starter
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python server.py            # stdio — started by VS Code, not manually in most cases
```

Open the `starter/` folder in VS Code, configure `.vscode/mcp.json`, switch Copilot Chat to **Agent** mode.

## Layout

```
starter/
├── server.py           # FastMCP entry — tools, resources, prompts
├── trace_schema.py     # TRACE sections + dataclasses
├── adr_store.py        # read / write markdown ledger
├── graph.py            # supersedes + relates_to graph
├── scoring.py          # completeness rubric + git drift
├── docs/decisions/     # sample ADR markdown files
└── .vscode/mcp.json    # VS Code MCP client config (servers key)
```

## Environment

| Variable | Default | Purpose |
| --- | --- | --- |
| `ADR_ROOT` | `./docs/decisions` | Ledger directory |
| `ADR_REPO_ROOT` | cwd | Repo root for `trace_drift_check` |
