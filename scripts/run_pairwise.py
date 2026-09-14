import argparse
import json
from pathlib import Path

from openai import OpenAI

from src.eval.judge import judge_one


def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_prompt(path):
    return Path(path).read_text(encoding="utf-8").strip()


def build_context(snippets):
    return "\n\n".join(
        f"[{item['id']}] {item['snippet']}" for item in snippets
    )


def answer_question(client, model, prompt, question, context):
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": (
                    f"Job-requirement context:\n{context}\n\n"
                    f"User question:\n{question}"
                ),
            },
        ],
    )
    return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden-set", default="data/golden_set.jsonl")
    parser.add_argument("--snippets", default="data/job_snippets.jsonl")
    parser.add_argument("--prompt-v1", default="data/prompt-v1.txt")
    parser.add_argument("--prompt-v2", default="data/prompt-v2.txt")
    parser.add_argument("--candidate-model", default="gpt-4o-mini")
    parser.add_argument("--judge-model", default="gpt-4o")
    parser.add_argument("--output", default="docs/prompt-pairwise-001.md")
    args = parser.parse_args()

    client = OpenAI()

    golden = load_jsonl(args.golden_set)
    snippets = load_jsonl(args.snippets)
    prompt_v1 = load_prompt(args.prompt_v1)
    prompt_v2 = load_prompt(args.prompt_v2)
    context = build_context(snippets)

    results = []

    for i, item in enumerate(golden, start=1):
        question = item["question"]
        ideal = item["ideal_answer"]

        answer_v1 = answer_question(
            client, args.candidate_model, prompt_v1, question, context
        )
        answer_v2 = answer_question(
            client, args.candidate_model, prompt_v2, question, context
        )

        score_v1 = judge_one(
            question=question,
            candidate_answer=answer_v1,
            ideal_answer=ideal,
            judge_model=args.judge_model,
        )
        score_v2 = judge_one(
            question=question,
            candidate_answer=answer_v2,
            ideal_answer=ideal,
            judge_model=args.judge_model,
        )

        results.append(
            {
                "id": item["id"],
                "question": question,
                "ideal_answer": ideal,
                "v1": {
                    "answer": answer_v1,
                    "accuracy": score_v1.accuracy,
                    "groundedness": score_v1.groundedness,
                    "format": score_v1.format,
                    "reasoning": score_v1.reasoning,
                },
                "v2": {
                    "answer": answer_v2,
                    "accuracy": score_v2.accuracy,
                    "groundedness": score_v2.groundedness,
                    "format": score_v2.format,
                    "reasoning": score_v2.reasoning,
                },
            }
        )

        print(f"[{i}/{len(golden)}] {item['id']} complete")

    def avg(strategy, metric):
        return sum(r[strategy][metric] for r in results) / len(results)

    lines = [
        "# Prompt Pairwise Comparison",
        "",
        f"- Candidate model: `{args.candidate_model}`",
        f"- Judge model: `{args.judge_model}`",
        f"- Questions: `{len(results)}`",
        "",
        "## Aggregate Scores",
        "",
        "| Strategy | Accuracy | Groundedness | Format | Overall |",
        "|---|---:|---:|---:|---:|",
    ]

    for strategy, label in [("v1", "Prompt v1"), ("v2", "Prompt v2")]:
        accuracy = avg(strategy, "accuracy")
        groundedness = avg(strategy, "groundedness")
        fmt = avg(strategy, "format")
        overall = (accuracy + groundedness + fmt) / 3
        lines.append(
            f"| {label} | {accuracy:.2f} | {groundedness:.2f} | "
            f"{fmt:.2f} | {overall:.2f} |"
        )

    lines.extend(["", "## Per-Question Results", ""])

    for r in results:
        lines.extend(
            [
                f"### {r['id']}: {r['question']}",
                "",
                f"**Ideal:** {r['ideal_answer']}",
                "",
                f"**V1:** {r['v1']['answer']}",
                "",
                f"V1 scores — Accuracy: {r['v1']['accuracy']}, "
                f"Groundedness: {r['v1']['groundedness']}, "
                f"Format: {r['v1']['format']}",
                "",
                f"**V2:** {r['v2']['answer']}",
                "",
                f"V2 scores — Accuracy: {r['v2']['accuracy']}, "
                f"Groundedness: {r['v2']['groundedness']}, "
                f"Format: {r['v2']['format']}",
                "",
            ]
        )

    Path(args.output).write_text("\n".join(lines), encoding="utf-8")

    print("\nPairwise comparison complete.")
    print(f"Report: {args.output}")


if __name__ == "__main__":
    main()
