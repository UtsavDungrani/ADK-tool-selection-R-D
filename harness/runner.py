"""Run the selection eval through a real ADK agent.

MEASUREMENT NOTES -- the parts that make these numbers trustworthy.

Token cost is taken from `usage_metadata.prompt_token_count` on the actual
model response, not estimated by counting characters in the schemas. The
difference matters: declarations are serialised into a provider-specific wire
format whose token cost you cannot reliably guess from the Python objects.

Declared-tool capture happens in `before_model_callback`, which ADK invokes
with the fully assembled `LlmRequest`. Reading `llm_request.config.tools` there
gives the exact declarations going over the wire -- after ADK has expanded
toolsets and applied any of its own filtering. Reading the strategy's output
instead would miss anything the framework does in between.

Two accuracy numbers are recorded, and conflating them is the main way this
kind of study goes wrong:

  recall   Was the gold tool among those declared? A property of the selector.
  correct  Did the model then call the gold tool? A property of the pair.

recall=1, correct=0 means the retriever did its job and the model still chose
wrong -- more retrieval will not help; better descriptions or fewer
near-duplicates will. recall=0 forces correct=0 and is purely a retriever
failure. Reporting only `correct` hides which of the two you are looking at.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Optional

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from strategies.base import StrategyToolset
from tasks import Task

APP_NAME = "tool_selection_rnd"

INSTRUCTION = """You are a tool router.

Given the user's request, call exactly ONE tool that best fulfils it.

Rules:
- Always call a tool. Never answer in prose.
- Never ask a clarifying question.
- If an argument's value is not stated in the request, supply a reasonable
  placeholder. Argument values are not evaluated; choosing the right tool is.
"""


@dataclass
class TaskResult:
    task_id: str
    tier: str
    query: str
    gold: str
    trap: Optional[str]

    chosen: Optional[str] = None
    declared: list[str] = field(default_factory=list)
    declared_count: int = 0

    recall: bool = False       # gold was declared
    correct: bool = False      # model called gold
    trapped: bool = False      # model called the designed distractor
    no_call: bool = False      # model emitted no function call at all

    prompt_tokens: int = 0
    completion_tokens: int = 0
    cached_tokens: int = 0
    latency_ms: float = 0.0

    aux_llm_calls: int = 0
    aux_prompt_tokens: int = 0
    aux_completion_tokens: int = 0
    aux_embed_calls: int = 0
    aux_wall_ms: float = 0.0

    error: Optional[str] = None

    @property
    def total_prompt_tokens(self) -> int:
        """Main-call prompt tokens plus whatever the strategy spent itself."""
        return self.prompt_tokens + self.aux_prompt_tokens

    def as_row(self) -> dict[str, Any]:
        d = asdict(self)
        d["total_prompt_tokens"] = self.total_prompt_tokens
        return d


def _make_capture(sink: dict) -> Any:
    """before_model_callback that records the real declared tool surface."""

    def capture(callback_context, llm_request):  # noqa: ANN001 - ADK signature
        decls = []
        for tool in (getattr(llm_request.config, "tools", None) or []):
            decls.extend(getattr(tool, "function_declarations", None) or [])
        sink["declared"] = [d.name for d in decls]
        sink["declared_count"] = len(decls)

        cm = getattr(llm_request, "cache_metadata", None)
        if cm is not None:
            sink["cache_metadata"] = {
                "cached_tokens": getattr(cm, "cached_contents_token_count", None),
                "invocations": getattr(cm, "invocations_used", None),
            }
        return None  # never short-circuit the model call

    return capture


def _usage_from_event(event) -> tuple[int, int, int]:
    """(prompt, completion, cached) tokens from an ADK event, if present."""
    um = getattr(event, "usage_metadata", None)
    if um is None:
        return 0, 0, 0
    return (
        getattr(um, "prompt_token_count", 0) or 0,
        getattr(um, "candidates_token_count", 0) or 0,
        getattr(um, "cached_content_token_count", 0) or 0,
    )


async def run_task(
    task: Task,
    toolset: StrategyToolset,
    model: str,
    session_service: InMemorySessionService,
) -> TaskResult:
    """Run one task in a fresh session.

    A fresh session per task is deliberate. Carrying history would let an
    earlier task's declarations and answers leak into a later one, and the
    whole point is to measure selection for a single cold request.
    """
    res = TaskResult(
        task_id=task.id, tier=task.tier, query=task.query,
        gold=task.gold, trap=task.trap,
    )
    sink: dict = {}

    agent = LlmAgent(
        model=model,
        name="selector",
        instruction=INSTRUCTION,
        tools=[toolset],
        before_model_callback=_make_capture(sink),
    )
    runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

    user_id = "evaluator"
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=user_id, session_id=f"s-{task.id}-{uuid.uuid4().hex[:8]}"
    )
    message = types.Content(role="user", parts=[types.Part(text=task.query)])

    t0 = time.perf_counter()
    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session.id, new_message=message
        ):
            p, c, cached = _usage_from_event(event)
            res.prompt_tokens += p
            res.completion_tokens += c
            res.cached_tokens += cached

            calls = event.get_function_calls() if hasattr(event, "get_function_calls") else []
            if calls and res.chosen is None:
                # First tool call is the selection. Later calls would be the
                # model continuing after the stub response; not our concern.
                res.chosen = calls[0].name
    except Exception as exc:  # noqa: BLE001 - record and continue the sweep
        res.error = f"{type(exc).__name__}: {exc}"
    res.latency_ms = (time.perf_counter() - t0) * 1000.0

    res.declared = sink.get("declared", [])
    res.declared_count = sink.get("declared_count", 0)

    cost = toolset.last_cost
    res.aux_llm_calls = cost.llm_calls
    res.aux_prompt_tokens = cost.prompt_tokens
    res.aux_completion_tokens = cost.completion_tokens
    res.aux_embed_calls = cost.embed_calls
    res.aux_wall_ms = cost.wall_ms

    res.recall = task.gold in res.declared
    res.no_call = res.chosen is None and res.error is None
    res.correct = res.chosen == task.gold
    res.trapped = bool(task.trap) and res.chosen == task.trap
    return res
