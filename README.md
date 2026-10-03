# Tool Selection at Scale — an ADK benchmark

**Research question.** An LLM agent with 10 tools works. What happens at 50,
100, 400 — and what is the cheapest way to keep it working?

This repo measures that. Scope is deliberately narrow: **tool selection only**.
A task succeeds when the agent calls the right tool. Nothing is executed, there
are no multi-hop tasks, and argument values are not scored. Narrow scope is what
makes the numbers mean something.

---

## What actually breaks at scale

Four things, and they are not equally expensive:

1. **Context cost.** Each tool schema is ~200–800 tokens. 400 tools is 80k–300k
   tokens *before the user says anything*, paid on every turn.
2. **Selection accuracy.** Degrades with near-duplicates, not with raw count.
3. **Latency and cache.** A bigger prefix is slower. Worse — changing the tool
   list between turns invalidates the prompt cache, so naive dynamic selection
   can cost more than it saves.
4. **Governance.** Versioning, ownership, deprecation. Not measured here.

Point 3 is the sharp one, and it is an open problem in ADK itself:
[adk-python#7241](https://github.com/google/adk-python/issues/7241) proposes
deferred tools with a per-turn selector hook, and names cache instability,
unbounded tool growth, and the absence of a non-LLM selection path as the gaps.
This harness is built to put numbers on exactly that trade-off.

---

## Design

### The seam

`BaseToolset.get_tools(readonly_context)` is called by ADK **once per model
request**, and whatever it returns is what gets declared. `ReadonlyContext`
carries `user_content`, so the toolset can see the query and select on it.

That gives a clean single-variable ablation: one agent, one model, one prompt,
one task set — swap the toolset, change nothing else.

```
SelectionStrategy          plain Python: (query, k) -> list[ToolSpec]
      |                    no ADK, no API key, unit-testable
      v
StrategyToolset            the only ADK-aware class in the project
      |
      v
LlmAgent(tools=[toolset])
```

### Measurement

Token cost comes from `usage_metadata.prompt_token_count` on the real response,
not from estimating schema size. Declared tools are captured in
`before_model_callback` off the assembled `LlmRequest`, so it reflects what ADK
actually sent after expanding toolsets.

**Two accuracy numbers, never conflated:**

| metric | question | what a failure means |
|---|---|---|
| `recall` | was the gold tool declared? | retriever failed — fix retrieval |
| `accuracy` | did the model call it? | — |
| `accuracy_given_recall` | gold was declared; did the model still pick it? | model confusion — fix descriptions or dedupe tools |

Reporting only `accuracy` hides which of the two you are looking at. They have
completely different fixes.

### Catalog

**50 core tools** across `github`, `jira`, `slack`, `gcalendar`, `gdrive`,
hand-written with **deliberately seeded collisions** (31 of 50 carry a
`confusable_with` label):

- *cross-domain homonyms* — `github_create_issue` ↔ `jira_create_issue`
- *within-domain near-synonyms* — `gdrive_list_files` ↔ `gdrive_search_files`
- *semantic overlap* — `gdrive_share_file` ↔ `github_add_collaborator`

Distractor density, not raw count, is what degrades selection. The catalog is
built around that claim.

**Scaling** holds the task set fixed. `load_catalog(n)` keeps all 50 core tools
and pads with generated filler from 20 plausible neighbouring SaaS systems.
Filler is never a gold answer, so sweeping 50 → 400 varies exactly one thing:
the number of wrong answers to reject. `confusable_with` is never read by any
strategy — it is used only to split errors into *fell into a designed trap* vs
*picked something unrelated*.

### Tasks

60 labelled queries, 12 per domain, balanced 20/20/20 across tiers:

- **easy** — names the system (`"Open a GitHub issue..."`)
- **medium** — system implied (`"Where is validate_jwt defined?"`)
- **hard** — sits on a seeded trap

All 50 core tools appear as gold at least once.

### Strategies

| name | API key | what it is |
|---|---|---|
| `all_tools` | no | declare everything — the status quo, and the accuracy ceiling |
| `random` | no | k at random — the signal floor |
| `bm25` | no | sparse keyword retrieval — the baseline people skip |
| `embedding` | yes | Gemini dense retrieval, asymmetric query/document |
| `embedding_symmetric` | yes | ablation: same embedding both sides (the common mistake) |
| `hierarchical` | yes | LLM routes to a namespace, then declares its tools |
| `oracle` | no | declare only the gold tool — retrieval ceiling, not deployable |

Report all of them. A single embedding number with no brackets says nothing.

**Cost honesty.** `hierarchical` spends an LLM call before any tool is declared.
Every strategy reports `aux_cost`, and the report adds it back —
`mean_total_prompt_tokens` includes it. A strategy cannot look cheap by hiding
its spend in a second model call.

---

## Running it

```bash
pip install -r requirements.txt
```

Offline — no key, free, instant:

```bash
python run_eval.py --retrieval-only --strategies bm25,random --sizes 50,100,200,400
```

Full sweep through a real ADK agent — needs a key:

```bash
cp .env.example .env    # then paste your AI Studio key
python run_eval.py --strategies bm25,all_tools,random --sizes 50 --k 5
```

Results are written to `results/` as CSV (a summary row per configuration, plus
one row per task). Embeddings are cached on disk, so re-running a sweep costs
nothing for documents already embedded.

Useful flags: `--k` tools declared per request, `--sizes` catalog sweep,
`--sleep` to stay under rate limits, `--tag` to label output files.

---

## Findings so far

**Retrieval-only, BM25 vs random, recall@k:**

| catalog | strategy | R@1 | R@3 | R@5 | R@10 |
|---|---|---|---|---|---|
| 50 | bm25 | 0.65 | 0.82 | 0.85 | 0.90 |
| 50 | random | 0.00 | 0.00 | 0.07 | 0.22 |
| 400 | bm25 | 0.62 | 0.82 | 0.83 | 0.92 |
| 400 | random | 0.00 | 0.00 | 0.02 | 0.02 |

**1. BM25 recall is nearly flat from 50 → 400 tools** (R@1 0.65 → 0.62) while
random collapses — confirming the padding genuinely adds distractors and the
metric is sensitive to them. If this holds under the full agent run, the
headline is that **scaling to 400 tools is a token-cost problem, not a retrieval
problem.** That reframes the whole optimisation: spend effort on what you
*declare*, not on ranking harder.

*Caveat:* filler padding is lexically distant from the core vocabulary, so BM25
rejects it easily. All the hard traps live in the core 50 and are present at
every size, so difficulty is constant by construction. A harder test is padding
with near-duplicates *of the core tools* — that is the obvious next ablation.

**2. The tiers separate cleanly** (BM25 R@1 at size 50): easy 0.95, medium 0.65,
hard 0.35. The task design works, and a blended number would have hidden a
3× spread.

**3. BM25 almost never falls into the designed traps** — 0 of 21 errors at size
50. It fails on *vocabulary mismatch* (it does not know "give someone access"
means `github_add_collaborator`), while the traps were built for *semantic*
confusion. Prediction: the traps will bite the embedding strategy and the LLM
much harder than they bite BM25. Untested — this is the next thing to run.

---

## Status

Working: catalog, scaling, task set, offline retrieval eval, all strategies,
ADK integration (constructs and wires correctly end to end).

Not yet run: the full agent sweep — needs an API key in `.env`.

Open next steps, roughly in value order:

1. Full agent sweep; compare `accuracy` against `recall` to locate the
   bottleneck.
2. **Cache-stability experiment** — the #7241 question. Measure
   `cached_content_token_count` under a fixed vs per-turn-varying tool list and
   find the break-even catalog size where dynamic selection stops paying.
3. Harder padding: filler that are near-duplicates of core tools.
4. Tool consolidation arm — collapse CRUD families into parameterised tools and
   measure accuracy per declared token.

---

## Layout

```
catalog/     schema.py (ToolSpec, ADK StubTool) · domains.py (50 core tools) · __init__.py (scaling)
tasks/       60 labelled queries across 3 tiers
strategies/  base.py (interface + ADK bridge) · lexical.py · embedding.py · hierarchical.py
harness/     runner.py (ADK execution + instrumentation) · metrics.py
run_eval.py  CLI
results/     CSV output
```
