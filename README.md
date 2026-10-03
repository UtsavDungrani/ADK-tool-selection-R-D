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

**100 hand-written core tools** across 10 domains, built around **deliberately
seeded collisions**:

| group | domains |
|---|---|
| base | `github` `jira` `slack` `gcalendar` `gdrive` |
| extended | `notion` `zendesk` `pagerduty` `stripe` `sentry` |

Three collision classes, escalating:

- *pairwise homonyms* — `github_create_issue` ↔ `jira_create_issue`
- *within-domain near-synonyms* — `gdrive_list_files` ↔ `gdrive_search_files`
- *multi-way* — "file a ticket" has **four** defensible destinations
  (`github_create_issue` / `jira_create_issue` / `zendesk_create_ticket` /
  `sentry_search_issues`, plus `pagerduty_trigger_incident`); "add a comment"
  has six. Disambiguation depends on *who reported it and what happens next* —
  the realistic hard case.

`stripe` is a control domain: payments vocabulary overlaps almost nothing, so
stripe tools surfacing for engineering queries means the index is broken.

Distractor density, not raw count, is what degrades selection. The catalog is
built around that claim.

### Two knobs, deliberately separate

| knob | varies | effect |
|---|---|---|
| `profile` | which hand-written core | **changes the questions** — `base` = 50 tools/60 tasks, `full` = 100/120 |
| `size` | total catalog incl. filler | **holds questions fixed**, adds wrong answers to reject |

Sweeping `size` at a fixed `profile` isolates distractor pressure. Changing
`profile` is a different experiment; its numbers are not directly comparable
because the question set changed — say so if you report both.

Filler comes from 25 plausible neighbouring SaaS systems and is **never** a gold
answer. Systems promoted into the core were removed from the filler vocabulary,
so a hierarchical router that correctly picks `sentry` is not handed a mix of
real and generated tools and then scored as if it had failed.

`size` below the core **raises** rather than truncating — silently dropping gold
tools would produce a quietly meaningless number, which is worse than a crash.

`confusable_with` is never read by any strategy. It only splits errors into
*fell into a designed trap* vs *picked something unrelated*.

### Tasks

120 labelled queries, 12 per domain, balanced 40/40/40 across tiers:

- **easy** — names the system (`"Open a GitHub issue..."`)
- **medium** — system implied (`"Where is validate_jwt defined?"`)
- **hard** — sits on a seeded trap

All 100 core tools appear as gold at least once.

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

## Seeing it in `adk web`

ADK ships a dev UI. There is **one agent folder per strategy** under `agents/`,
so the app dropdown becomes a live strategy switcher — same query, flip the
dropdown, watch the declared tool surface and the model's choice change.

```bash
adk web agents --port 8001
```

Then open <http://127.0.0.1:8001>.

Point it at `agents`, **not** the project root. From the root the agents end up
nested under an `agents/` folder in the picker and the search box does not
descend into folders.

What to look at, per turn:

| tab | shows | why it matters |
|---|---|---|
| **Events** | the `functionCall` the model emitted | the selection — the thing being measured |
| **State** | `declared_tools`, `declared_count` | what the strategy *exposed*, written by a `before_model_callback` |
| **Trace** | per-step latency | includes the hierarchical router's extra call |

Read State alongside Events. Gold tool missing from `declared_tools` → the
retriever failed. Gold present and the model still picked wrong → retrieval is
fine and the descriptions are the problem. Those have different fixes, and the
UI is the fastest way to tell them apart on a single query.

Tune without editing code — set in `.env`, restart:

```
TSRND_CATALOG_SIZE=400    # default 50
TSRND_K=5                 # tools declared per request
TSRND_MODEL=gemini-3.5-flash-lite
```

### One query across every strategy

```bash
python compare_query.py --gold github_add_collaborator --show-declared \
  "Our repo acme/infra needs sam to be able to merge - sort out their access."
```

```
strategy       declared  tokens      ms  called
all_tools            50    5552    6310  github_add_collaborator   CORRECT
bm25                  5     800    5135  github_add_collaborator   CORRECT
embedding             5     807    7146  github_add_collaborator   CORRECT
hierarchical          5     844   33854  github_add_collaborator   CORRECT
random_floor          5     647    6120  github_merge_pull_request wrong
```

**86% fewer prompt tokens with the selection preserved**, on a hard trap query.
`random_floor` is the control: it also spends few tokens and gets it wrong, so
the saving is attributable to selection quality, not to declaring less.

Qualitatively, embedding's top-5 was all GitHub tools with gold ranked first,
while BM25's included `jira_list_users` and `gcalendar_set_out_of_office` — it
surfaced the right answer with more noise around it.

`compare_query.py` is a demo tool and counts tokens more loosely than
`run_eval.py` (see its docstring). Quote `run_eval.py` in the write-up.

## Model availability is a real constraint

Picking a model turned out to be an experimental decision, not a detail:

| model | latency | result on the trap query |
|---|---|---|
| `gemini-2.5-flash` | — | 404, no longer available to new API keys |
| `gemini-3.5 / 3.6 / 3.7-flash` | — | 503, high demand |
| `gemini-3.8-flash` | 7.1s | **wrong** (`slack_list_users`) |
| `gemini-3.5-flash-lite` | 2.8s | correct |
| `gemini-3.1-flash-lite` | 1.5s | correct |

Default is `gemini-3.5-flash-lite` — available, fast enough for a 60-task
sweep, and pinned rather than `-latest` so runs stay reproducible.

Two things to watch for, because both cost hours if you do not know them:

- A 503 is **retried silently** by the SDK. A call that looks like it took 60
  seconds was usually retrying, and an eventual HTTP 500 from `adk web` is
  normally model capacity, not your code. Reproduce in-process to see the real
  traceback before debugging the harness.
- `gemini-3.8-flash` picking `slack_list_users` for a GitHub access request,
  with all 50 tools declared, is a single sample — but it is exactly the
  distractor-density failure this project exists to measure. Model choice is
  worth adding as a sweep axis.

## Running it

```bash
pip install -r requirements.txt
```

Offline — no key, free, instant:

```bash
python run_eval.py --retrieval-only --strategies bm25,random,oracle --sizes 100,200,400
```

Full sweep through a real ADK agent — needs a key:

```bash
cp .env.example .env    # then paste your AI Studio key
python run_eval.py --strategies bm25,all_tools,random --sizes 100 --k 5
```

Results are written to `results/` as CSV (a summary row per configuration, plus
one row per task). Embeddings are cached on disk, so re-running a sweep costs
nothing for documents already embedded.

Useful flags: `--k` tools declared per request, `--sizes` catalog sweep,
`--sleep` to stay under rate limits, `--tag` to label output files.

---

## Findings so far

All retrieval-only, `profile=full` (100-tool core, 120 tasks), so they cost
nothing to reproduce.

### 1. Baseline token cost scales linearly. Selection cost is flat.

Same query, measured through a real ADK agent:

| catalog | `all_tools` prompt tokens | `bm25` (k=5) |
|---|---|---|
| 50 | 5,552 | 800 |
| 100 | 10,262 | 702 |

Declaring everything doubles when the catalog doubles. Selecting 5 does not
move. Extrapolated to 400 tools that is ~40k tokens versus ~800, **on every
turn**. This is the core economic argument for selection, and it holds
regardless of how good the retriever is.

### 2. BM25 recall is nearly invariant to catalog size

R@1 across sizes at `profile=full`: 0.667 (100) → 0.658 (200) → 0.650 (400),
while `random` collapses — confirming the padding genuinely adds distractors
and the metric is sensitive to them.

**Scaling to 400 tools is a token-cost problem, not a retrieval problem.** Spend
effort on what you *declare*, not on ranking harder.

### 3. Doubling the core did not make retrieval harder

Going from 50 → 100 hand-written tools (and 60 → 120 tasks), including the new
four- and six-way collisions, moved BM25 R@1 from 0.650 to 0.667. More tools and
*harder* collisions, no degradation.

### 4. Multi-way collisions fail differently — and k does not rescue them

Hard tier only, `profile=full`, size 100:

| task group | R@1 | R@3 | R@5 | R@10 |
|---|---|---|---|---|
| base (pairwise traps) | 0.25 | 0.75 | 0.75 | 0.85 |
| extended (multi-way traps) | **0.45** | 0.60 | 0.60 | 0.75 |

The extended hard tasks score *higher* at k=1 but *lower* at k=3 and beyond. The
gold tool is either rank 1 or nowhere — competing tools from the other four
systems crowd it out.

This is the practically useful result. For pairwise collisions, "declare top-5
and let the model disambiguate" works: recall triples from k=1 to k=3. For
multi-way collisions it does not — raising k barely helps because the right
answer is not in the list at all. **Those two failure modes need different
fixes, and a blended recall number hides the distinction completely.**

### 5. BM25 almost never falls into the *designed* traps

1 of 40 errors at size 100. It fails on vocabulary mismatch — it does not know
"give someone access" means `github_add_collaborator` — while the traps were
built for *semantic* confusion. Prediction: the traps will bite the embedding
strategy and the LLM much harder than they bite BM25. Still untested, and the
most interesting thing to run next.

### Caveats

- Filler padding is lexically distant from core vocabulary, so BM25 rejects it
  easily. That is part of why finding 2 looks so clean. Padding with
  near-duplicates *of core tools* is the honest harder test.
- All hard traps live in the core, present at every size, so difficulty is
  constant by construction while `size` varies.
- Findings 1 and 4 are single-query and single-configuration respectively. The
  full agent sweep is what turns them into claims.

## Status

Working: 100-tool catalog over 10 domains, profiles, scaling to 400, 120-task
set, offline retrieval eval, all strategies, ADK integration, and the `adk web`
dev UI with one agent per strategy.

Not yet run: the full agent sweep over all 120 tasks.

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
catalog/      schema.py (ToolSpec, ADK StubTool) · domains.py (base 50)
              domains_ext.py (extended 50) · __init__.py (profiles + scaling)
tasks/        tasks.py (60) · tasks_ext.py (60) · __init__.py (profile-scoped)
strategies/   base.py (interface + ADK bridge) · lexical.py · embedding.py · hierarchical.py
harness/      runner.py (ADK execution + instrumentation) · metrics.py
agents/       one ADK agent package per strategy, for `adk web`
run_eval.py   the sweep — real numbers
compare_query.py  one query across every strategy — demo/intuition
results/      CSV output
```
