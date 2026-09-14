"""Run the W5 golden-set evaluation against the W4 /ask_batched API."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import httpx

from src.eval.judge import judge_one
from src.pipeline.store import connect, write_eval_run


def load_golden(path: str) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def get_candidate_answer(
    client: httpx.Client,
    api_url: str,
    question: str,
) -> str:
    response = client.post(
        f"{api_url.rstrip('/')}/ask_batched",
        json={"question": question},
        timeout=120.0,
    )
    response.raise_for_status()

    payload = response.json()

    if "content" not in payload:
        raise ValueError(f"/ask_batched response missing 'content': {payload}")

    return payload["content"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden-set", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--api-url", required=True)
    parser.add_argument("--judge-model", default="gpt-4o")
    parser.add_argument("--candidate-model", default="gpt-4o-mini")
    parser.add_argument("--label", default="eval-run-001")
    args = parser.parse_args()

    golden = load_golden(args.golden_set)

    print("=" * 60)
    print(f"Golden entries: {len(golden)}")
    print(f"Candidate model: {args.candidate_model}")
    print(f"Judge model: {args.judge_model}")
    print(f"Label: {args.label}")
    print("=" * 60)

    con = connect(args.db)

    scores = []
    started = time.time()

    with httpx.Client() as client:
        for index, row in enumerate(golden, start=1):
            golden_id = row["id"]
            question = row["question"]
            ideal_answer = row["ideal_answer"]

            print(f"[{index}/{len(golden)}] {golden_id}: {question}")

            try:
                candidate_answer = get_candidate_answer(
                    client,
                    args.api_url,
                    question,
                )

                score = judge_one(
                    question=question,
                    candidate_answer=candidate_answer,
                    ideal_answer=ideal_answer,
                    judge_model=args.judge_model,
                )

                write_eval_run(
                    con=con,
                    golden_id=golden_id,
                    question=question,
                    candidate_answer=candidate_answer,
                    ideal_answer=ideal_answer,
                    candidate_model=args.candidate_model,
                    judge_model=args.judge_model,
                    accuracy=score.accuracy,
                    groundedness=score.groundedness,
                    format=score.format,
                    reasoning=score.reasoning,
                    eval_run_label=args.label,
                )

                scores.append(score)

                print(
                    f"    accuracy={score.accuracy} "
                    f"groundedness={score.groundedness} "
                    f"format={score.format}"
                )

            except Exception as exc:
                print(f"    ERROR: {type(exc).__name__}: {exc}")

    elapsed = time.time() - started

    print()
    print("=" * 60)
    print(f"Aggregate for label='{args.label}'")
    print("-" * 60)

    if not scores:
        print("No entries were successfully scored.")
        return

    avg_accuracy = sum(s.accuracy for s in scores) / len(scores)
    avg_groundedness = sum(s.groundedness for s in scores) / len(scores)
    avg_format = sum(s.format for s in scores) / len(scores)

    accuracy_counts = {
        n: sum(s.accuracy == n for s in scores)
        for n in (4, 3, 2, 1)
    }

    print(f"n entries scored : {len(scores)}")
    print(f"avg accuracy : {avg_accuracy:.2f}")
    print(f"avg groundedness : {avg_groundedness:.2f}")
    print(f"avg format : {avg_format:.2f}")
    print(
        "accuracy 4 / 3 / 2 / 1 : "
        f"{accuracy_counts[4]} / "
        f"{accuracy_counts[3]} / "
        f"{accuracy_counts[2]} / "
        f"{accuracy_counts[1]}"
    )
    print(f"wall-clock : {elapsed:.1f}s")
    print("=" * 60)

    con.close()


if __name__ == "__main__":
    main()
