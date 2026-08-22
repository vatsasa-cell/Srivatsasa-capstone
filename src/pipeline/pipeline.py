"""Async batch pipeline — STARTER file for Week 2.

You will complete this file across sub-steps 2b → 2e. Each stub maps to one
sub-step:
  - ask_llm                — 2b
  - ask_llm_with_retry      — 2c
  - run_batch               — 2d
  - JSON-logging block      — 2e

After Step 2a, you renamed this file to `src/pipeline/pipeline.py` and changed
the `from fake_llm import ...` import below to `from .fake_llm import ...`.

The completed reference is at <cohort-repo>/week2/reference/pipeline_reference.py.
"""
from __future__ import annotations
import asyncio
import json
import logging
import sys
import time

from .fake_llm import Question, Answer, fake_ask_llm, FakeLLMError


# ─────────────────────────────────────────────────────────────────────────────
# Step 5 (sub-step 2e) — structured (JSON) logging
#
# TODO 2e: Replace this commented block with:
#   - A `JsonFormatter(logging.Formatter)` class whose `format(record)` returns
#     `json.dumps({"ts": ..., "level": ..., "msg": ...})`
#   - A module-level `log = logging.getLogger("pipeline")` + setLevel(INFO)
#   - A StreamHandler attached to that logger, using JsonFormatter()
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# 2b — single LLM call
# ─────────────────────────────────────────────────────────────────────────────
async def ask_llm(q: Question, fail_rate: float = 0.0) -> Answer:
    """One LLM call. Branches on Settings.use_fake."""
    if _settings_for_import.use_fake:
        ans = await fake_ask_llm(q, fail_rate=fail_rate)
    else:
        resp = await _client.chat.completions.create(
            model=_settings_for_import.model,
            messages=[{"role": "user", "content": q.text}],
        )
        ans = Answer(
            question=q.text,
            text=resp.choices[0].message.content,
            cost_usd=0.0001,                  # real cost-from-usage lands in W25
        )
    log.info(f"asked: {q.text[:40]}")
    return ans


# ─────────────────────────────────────────────────────────────────────────────
# 2c — retry wrapper
# ─────────────────────────────────────────────────────────────────────────────
async def ask_llm_with_retry(
    q: Question, tries: int = 3, fail_rate: float = 0.0
) -> Answer:
    """Retry up to `tries` times. Wait 1 s, 2 s, 4 s between attempts.

    Re-raises the last exception if all attempts fail (no silent failures).
    """
    for attempt in range(tries):
        try:
            ans = await ask_llm(q, fail_rate=fail_rate)
            ans.retries = attempt
            return ans
        except Exception as exc:
            if attempt == tries - 1:
                raise
            log.warning(f"retry {attempt + 1} for: {q.text[:40]} ({exc})")
            await asyncio.sleep(2 ** attempt)
    raise RuntimeError("unreachable") 


# ─────────────────────────────────────────────────────────────────────────────
# 2d — batch runner
# ─────────────────────────────────────────────────────────────────────────────
async def run_batch(
    questions: list[Question], fail_rate: float = 0.0
) -> list[Answer]:
    """Fire every question in parallel via one big asyncio.gather (no batching)."""
    tasks = [ask_llm_with_retry(q, fail_rate=fail_rate) for q in questions]
    return await asyncio.gather(*tasks)

async def run_in_batches(
    questions: list[Question],
    batch_size: int = 5,
    fail_rate: float = 0.0,
) -> list[Answer]:
    """Fire questions in chunks of `batch_size`, with a 100 ms pause between batches."""
    out: list[Answer] = []
    for i in range(0, len(questions), batch_size):
        chunk = questions[i : i + batch_size]
        log.info(f"batch {i // batch_size + 1}: {len(chunk)} questions")
        batch_answers = await asyncio.gather(
            *(ask_llm_with_retry(q, fail_rate=fail_rate) for q in chunk)
        )
        out.extend(batch_answers)
        await asyncio.sleep(0.1)              # gentle pace between batches
    return out

# ─────────────────────────────────────────────────────────────────────────────
# Entrypoint — replaced in Step 3a (Settings) and again in Step 3c (CSV + batched)
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    fail_rate = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0

    sample = [
        Question(text="What is RAG in one sentence?"),
        Question(text="Name three uses of vector databases."),
        Question(text="Why might an LLM hallucinate?"),
    ]
    answers = asyncio.run(run_batch(sample, fail_rate=fail_rate))
    for a in answers:
        print(f"- {a.text[:80]}")
