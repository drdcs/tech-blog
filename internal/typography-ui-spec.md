TECH BLOG TYPOGRAPHY & UI SPECIFICATION
=======================================

ROLE / DESIGN INTENT
--------------------
Design the typography and reading experience for a high-quality software engineering / architecture technical blog.

The visual language should feel like it was designed by a Principal Engineer:

- Clean
- Technical
- Precise
- Minimal
- High information density without feeling crowded
- Excellent long-form readability
- Strong hierarchy
- Professional rather than flashy
- Suitable for architecture, distributed systems, AI/ML, databases, cloud, Kafka, search, RAG, and system design articles
- Avoid excessive visual decoration
- Typography should communicate engineering credibility

PRIMARY FONT SYSTEM
-------------------

Use:

BODY / UI FONT:
Inter

CODE / MONOSPACE FONT:
JetBrains Mono

Do NOT use decorative fonts.

Do NOT use more than two primary font families.

FONT STACKS
-----------

Primary:

font-family:
"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;

Code:

font-family:
"JetBrains Mono", "SFMono-Regular", Consolas, "Liberation Mono", monospace;


FONT WEIGHTS
------------

Inter:

400 = regular body text
500 = emphasized text / navigation
600 = section headings / labels
700 = major headings

Avoid excessive use of 700.

JetBrains Mono:

400 = normal code
500 = highlighted code / important code


TYPOGRAPHIC SCALE
-----------------

Desktop:

H1:
font-size: 44px
line-height: 1.12
font-weight: 700
letter-spacing: -0.025em

H2:
font-size: 32px
line-height: 1.2
font-weight: 700
letter-spacing: -0.02em

H3:
font-size: 24px
line-height: 1.3
font-weight: 600
letter-spacing: -0.015em

H4:
font-size: 20px
line-height: 1.35
font-weight: 600

Body:
font-size: 18px
line-height: 1.7
font-weight: 400

Small text:
font-size: 14px
line-height: 1.5

Metadata:
font-size: 13px
line-height: 1.4
font-weight: 500


MOBILE TYPOGRAPHY
-----------------

H1:
font-size: 34px
line-height: 1.15

H2:
font-size: 27px
line-height: 1.2

H3:
font-size: 22px
line-height: 1.3

Body:
font-size: 17px
line-height: 1.7

Code:
font-size: 13px
line-height: 1.6


ARTICLE WIDTH
-------------

Optimize for reading rather than maximum screen utilization.

Main article content:

max-width: 720px

Preferred range:

680px - 760px

Do NOT use full-width paragraphs.

Long paragraphs should never span the entire desktop viewport.

For wide screens, the article can sit inside a larger layout, but the actual prose column should remain approximately 720px wide.


PAGE LAYOUT
-----------

Recommended desktop layout:

--------------------------------------------------
| Header                                         |
--------------------------------------------------
|                                                |
|              Article Container                 |
|                                                |
|              H1                                |
|              Metadata                          |
|              Introduction                      |
|                                                |
|              Main Content                      |
|                                                |
--------------------------------------------------

For very long technical articles, optionally support:

Left:
Table of Contents

Center:
Article

Right:
Optional contextual information

However, the article itself must remain approximately 720px wide.


BODY TEXT
---------

Body text should be optimized for technical reading.

Use:

font-size: 18px
line-height: 1.7

Paragraph spacing:

margin-bottom: approximately 1.2em

Avoid extremely long paragraphs.

Prefer paragraphs of approximately 2-5 sentences.

Technical explanations should use short paragraphs combined with:

- diagrams
- bullet lists
- tables
- code examples
- callouts
- architecture diagrams


HEADINGS
--------

Headings should communicate information hierarchy clearly.

Example:

H1
Building a Distributed Job Scheduler

H2
Architecture

H3
Scheduling Model

H3
Worker Coordination

H2
Failure Handling

H3
Worker Failure

H3
Scheduler Failure


Do NOT use headings only for visual styling.

Headings should represent semantic document structure.


HEADING STYLE
-------------

Use strong but restrained typography.

Avoid:

- Huge marketing-style headings
- Gradient text
- Excessive uppercase
- Decorative typography
- Excessive emojis
- Text shadows

Recommended:

H1 = 44px / 700
H2 = 32px / 700
H3 = 24px / 600

Use negative letter spacing for large headings.


CODE TYPOGRAPHY
---------------

Use JetBrains Mono for:

- inline code
- code blocks
- terminal commands
- configuration
- JSON
- YAML
- SQL
- logs
- stack traces

Example:

```python
def process_event(event):
    return event_service.process(event)
```

Code should visually separate itself from prose.

Recommended code block:

font-size: 14px
line-height: 1.6
font-weight: 400

For very dense code:

font-size: 13px


INLINE CODE
-----------

Inline code should use JetBrains Mono.

Example:

The service publishes an event to `Kafka` and stores the result in `PostgreSQL`.

Inline code should have subtle background contrast and small horizontal padding.

Do not make inline code visually louder than the surrounding sentence.


CODE BLOCK DESIGN
-----------------

Code blocks should have:

- rounded corners: 6-10px
- subtle border
- comfortable padding
- horizontal scrolling when required
- line numbers for long examples
- syntax highlighting
- copy button
- language indicator

Recommended padding:

16px - 20px

Do NOT wrap long code lines if wrapping makes the code harder to understand.

Prefer horizontal scrolling.


TECHNICAL CALLOUTS
------------------

Support semantic callouts:

NOTE
TIP
WARNING
IMPORTANT
DECISION

Example:

NOTE

Kafka partitions provide ordering only within a partition.
Do not assume global ordering across partitions.

Callouts should be visually subtle.

Avoid excessive colored boxes.

The content is more important than decoration.


LINKS
-----

Links should be clearly identifiable but not visually distracting.

Use a consistent accent color.

Hover state should be obvious.

Avoid underlining every link if the design remains accessible without it.

External technical references should open predictably.

Examples:

OpenSearch
Kafka
PostgreSQL
Kubernetes


TABLES
------

Technical blogs frequently require tables.

Tables should prioritize information density and scanning.

Example:

| Component | Responsibility | Storage |
|-----------|----------------|---------|
| API       | Request handling | Redis |
| Worker    | Job execution   | Kafka |
| Scheduler | Job coordination | PostgreSQL |

Recommended:

font-size: 14px - 15px

Header:

font-weight: 600

Avoid excessive borders.

Use subtle row separation.


LISTS
-----

Use lists extensively for technical explanations.

Unordered lists:

- clear
- concise
- scannable

Ordered lists should be used for:

1. workflows
2. algorithms
3. implementation steps
4. deployment procedures

Keep list line-height close to body line-height.


ARCHITECTURE DIAGRAMS
---------------------

Technical blogs should support architecture diagrams.

Diagrams should have a visual language consistent with the typography.

Recommended:

Labels:
Inter 13-14px

Technical identifiers:
JetBrains Mono

Examples:

Kafka
API Gateway
OpenSearch
PostgreSQL
Redis
Embedding Service
Vector DB
LLM


METADATA
--------

Article metadata should be understated.

Example:

12 min read · Aug 9, 2026 · Distributed Systems

Use:

font-size: 13-14px
font-weight: 500

Metadata should never compete with the article title.


AUTHOR SECTION
--------------

Keep author information compact.

Recommended:

Author name
Role / expertise
Published date
Reading time

Avoid oversized author cards.


COLOR / CONTRAST
----------------

Typography should work in both light and dark themes.

Light theme:

Background:
near-white rather than pure white

Body text:
very dark gray

Secondary text:
medium gray

Code:
slightly contrasting surface

Dark theme:

Background:
dark gray rather than absolute black

Body:
light gray

Headings:
near-white

Code:
slightly lighter/different surface than page background

Do NOT use pure black and pure white everywhere.

Maintain WCAG AA contrast at minimum.


DARK MODE
---------

Dark mode is important for a technical blog.

The typography must remain readable without excessive brightness.

Avoid:

#000000 background
#FFFFFF body text everywhere

Prefer slightly softened colors.

Code blocks should have enough contrast from the surrounding page.


RESPONSIVE DESIGN
-----------------

Desktop:

720px article width

Tablet:

approximately 90% viewport width

Mobile:

approximately 92% viewport width

Do not allow horizontal page overflow.

Code blocks may scroll horizontally.

Images and diagrams should scale responsively.


READING RHYTHM
-------------

Optimize for long-form technical reading.

A typical article should visually follow:

Title
↓
Metadata
↓
Short introduction
↓
Key idea / problem
↓
Architecture diagram
↓
Detailed explanation
↓
Code
↓
Trade-offs
↓
Failure modes
↓
Operational considerations
↓
Conclusion


PRINCIPAL ENGINEER WRITING STYLE
--------------------------------

The typography and UI should support an engineering writing style that emphasizes:

1. Problem definition
2. Constraints
3. Assumptions
4. Architecture
5. Design decisions
6. Trade-offs
7. Failure modes
8. Scalability
9. Reliability
10. Observability
11. Security
12. Operational complexity
13. Cost
14. Alternatives considered
15. Final recommendation

Avoid making the blog look like a generic AI-generated content site.

The design should feel like an experienced engineer explaining a system to another experienced engineer.


ARTICLE STRUCTURE
-----------------

Prefer this structure for technical articles:

# Title

Short thesis / executive summary.

## Problem

What problem are we solving?

## Requirements

Functional requirements.

Non-functional requirements.

## Constraints

Scale
Latency
Availability
Cost
Security
Data volume

## Architecture

Architecture diagram.

## Design

Detailed component discussion.

## Data Flow

Request/event/data lifecycle.

## Key Decisions

Explain why each important decision was made.

## Trade-offs

Explain what is gained and what is sacrificed.

## Failure Modes

Explain how the system behaves when dependencies fail.

## Scalability

Discuss bottlenecks and scaling strategy.

## Observability

Metrics
Logs
Tracing
Alerts

## Security

Authentication
Authorization
Data protection
PII handling
Threat model

## Alternatives

Explain alternatives considered and why they were rejected.

## Conclusion

Summarize the key engineering decisions.


DESIGN PRINCIPLES
-----------------

The blog UI should follow these principles:

1. Content > decoration
2. Readability > density
3. Hierarchy > visual effects
4. Consistency > novelty
5. Technical credibility > marketing aesthetics
6. Accessibility > visual cleverness
7. Performance > unnecessary UI components


AVOID
-----

Do NOT use:

- Comic Sans
- decorative serif fonts for technical content
- excessive gradients
- glassmorphism everywhere
- excessive animations
- huge hero sections
- excessive rounded cards
- excessive shadows
- rainbow syntax highlighting
- oversized code blocks
- tiny body text
- full-width paragraphs
- excessive emojis
- overly colorful dashboards
- unnecessary AI-generated visual decorations


FINAL FONT DECISION
-------------------

Primary:

Inter

Monospace:

JetBrains Mono

Use the same typography system consistently across:

- homepage
- article pages
- navigation
- search
- tags
- author pages
- archive pages
- code blocks
- architecture diagrams
- tables
- callouts

The final visual result should resemble a high-quality engineering publication or internal architecture knowledge base rather than a generic personal blog.

PRIMARY GOAL
------------

When a senior engineer opens an article, the first impression should be:

"This is technically serious, easy to scan, and worth reading."

Typography should disappear into the reading experience rather than becoming the subject of attention.