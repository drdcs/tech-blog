# HLD Article Format — Tech Blog by Dip

Internal reference. Not deployed to GitHub Pages.

Every High-Level Design essay follows this structure. Panels are the primary layout unit — scannable, dense, principal-engineer tone. Prefer primary sources (white papers, vendor architecture docs, RFCs) over blog rewrites.

---

## Required sections (in order)

### 0. Opening
- Title + one-line thesis (what problem, what architectural bet)
- Meta: topic pill, read time, date
- Table of contents linking to all panels below

### 1. Design Details Collection
**Panel layout — two columns on desktop, stack on mobile.**

| Functional (max 3–4) | Non-functional |
|----------------------|----------------|
| What the system must *do* — user-visible capabilities, bounded scope | Latency, throughput, availability, consistency, cost, operability |

Rules:
- Functional: verbs + outcomes. No implementation leakage.
- Non-functional: measurable where possible (p99, RPO/RTO, req/s).
- Cap functional items at four. If you need more, the scope is too wide.

### 2. Back-of-Envelope Discussion
**Single panel or callout.**

- Order-of-magnitude math: QPS, storage, fan-out, partition count.
- State assumptions explicitly ("10k req/s peak, 2 KB metadata each").
- Show the bottleneck before the diagram.
- One paragraph: "what breaks first at 10× scale."

### 3. Ingress & Request Routing
**Full-width diagram + two panels.**

Must include:
- **GSLB** — geo routing, regional failover
- **L7 LB** — TLS, WAF, rate limits
- **Request router** — affinity by tenant/queue/shard
- **App service** — stateless API pods

### 4. Storage & Queue Layers
**Full-width diagram + four panels (2×2 grid).**

Must document four distinct stores:
- **PostgreSQL** — relational DB for task/job config and run state
- **Redis** — in-memory timers and scheduling buffer (not durable)
- **Message broker** — durable execution queue (Kafka / SQS)
- **Cassandra** — wide-column store for logs and run history

### 5. API & Database Design

**API:** formatted table (`.api-table`) with Method, Endpoint, Purpose, Idempotent columns.

**Database:** bullet-list panels per store (`.hld-panel`) — tables, topics, partition keys. Do not use Mermaid ER diagrams.

### 6. Core End-to-End Flow
**Full-width diagram panel — animated Mermaid.**

Requirements:
- Sequence or flowchart showing distributed failure points
- Label lease, heartbeat, retry, and commit boundaries
- Annotate at-least-once vs exactly-once choices
- Use animated dashed edges (site standard)
- Show ingress layer in at least one diagram

Sub-sections allowed:
- Happy path
- Failure path (worker death, partition, duplicate delivery)
- Scale path (shard routing, worker pool expansion)

### 7. Core Design Principles
**Panel grid (2×2 or 3 columns).**

Each principle card:
- Name (e.g. "Redis for speed, Postgres for truth")
- One sentence rule
- One sentence trade-off

Draw from systems literature — Borg, Omega, Dynamo, Sagas — cite in prose, not footnote dumps.

### 8. Pain Points
**Panel list — honest production scars.**

- Operational complexity
- Edge cases (clock skew, thundering herd, poison jobs, Redis OOM)
- What we deferred and why

### 9. Conclusion
**Short panel — 2–3 paragraphs.**

- Restate the architectural bet
- When to build vs buy (Temporal, Airflow, cloud schedulers)
- One memorable line for the reader

---

## Visual & tone rules

- **Panels:** `.hld-panel`, `.hld-panel-grid`, `.hld-panel-label`
- **API table:** `.api-table-wrap` + `.api-table`
- **DB panels:** bullet-list `.hld-panel` per store (no ER diagrams)
- **No fluff:** every paragraph earns its place
- **Diagrams:** min. 3 per essay; ingress topology, sequence, scale path
- **Code:** only when it clarifies API contracts or state transitions (Lua/SQL)
- **Length:** 25–30 min read target for HLD essays
- **Responsive:** must read well on mobile and desktop (site CSS handles this)

---

## Checklist before publish

- [ ] Functional requirements ≤ 4
- [ ] Back-of-envelope at stated scale (e.g. 10k req/s)
- [ ] GSLB / LB / router / app service documented
- [ ] Four-store architecture documented (Postgres, Redis, broker, Cassandra)
- [ ] API table + DB bullet panels present
- [ ] Animated end-to-end flow diagrams
- [ ] Failure path documented
- [ ] Pain points section is honest
- [ ] HLD hub + homepage links updated
- [ ] Reviewed on mobile viewport
