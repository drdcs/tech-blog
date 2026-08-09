# Tech Blog by Dip

Technical essays on distributed systems, AI, data, and ML at scale. Static site for **GitHub Pages**.

## Repository layout

```
├── index.html
├── assets/
│   ├── css/styles.css
│   └── js/
│       ├── main.js
│       ├── reactions.js
│       └── reactions-config.example.js
├── topics/
│   ├── ai/
│   │   ├── index.html              # Topic hub
│   │   └── mcp-vs-agents/
│   │       └── index.html
│   ├── data/
│   │   ├── index.html
│   │   └── thin-pipe-kafka-bigquery/
│   │       └── index.html
│   ├── hld/index.html
│   └── lld/index.html
├── internal/                       # Not deployed
└── .github/workflows/pages.yml
```

## URLs

| Topic | Hub | Essay |
|-------|-----|-------|
| AI | `/topics/ai/` | `/topics/ai/mcp-vs-agents/` |
| Data | `/topics/data/` | `/topics/data/thin-pipe-kafka-bigquery/` |
| HLD | `/topics/hld/` | — |
| LLD | `/topics/lld/` | — |

## Reactions (like / dislike / double like)

**On GitHub Pages today:** reactions work via `localStorage` — each visitor's vote is saved on their device.

**Global counts across all readers** need a small external store (e.g. Supabase free tier). Copy `assets/js/reactions-config.example.js` → `reactions-config.js` and configure — see `internal/README.md`.

## Local preview

```bash
python3 -m http.server 8080
```

## Deploy

Push to `main`. GitHub Actions deploys `index.html`, `assets/`, and `topics/` only.
