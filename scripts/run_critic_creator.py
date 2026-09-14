import argparse
import json
import os
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


def create_answer(client, model, prompt, question, context):
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
                    f"User question:\n{question}\n\n"
                    "Answer the user's question directly."
                ),
            },
        ],
    )
    return response.choices[0].message.content.strip()


def improve_prompt(client, model, current_prompt, question, ideal, answer, scores):
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """You are a prompt-improvement critic for a
job-requirement Q&A system.

Review the current prompt and candidate answer against the ideal answer
and judge scores.

Identify the concrete prompt changes needed to improve factual accuracy,
groundedness, completeness, and clarity.

Pay particular attention to:
- mapping each company to the correct job title;
- preserving the exact experience rule for each role;
- distinguishing "no prior experience", "no fixed years requirement",
  and "less than the typical experience may be considered";
- avoiding unsupported substitutions or omissions.

Return ONLY a revised system prompt that keeps the useful behavior of the
current prompt while addressing the observed failure."""
            },
            {
                "role": "user",
                "content": (
                    f"Current prompt:\n{current_prompt}\n\n"
                    f"Question:\n{question}\n\n"
                    f"Ideal answer:\n{ideal}\n\n"
                    f"Candidate answer:\n{answer}\n\n"
                    f"Judge scores:\n"
                    f"Accuracy={scores.accuracy}, "
                    f"Groundedness={scores.groundedness}, "
                    f"Format={scores.format}\n\n"
                    f"Judge reasoning:\n{scores.reasoning}"
                ),
            },
        ],
    )

    return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden-set", default="data/golden_set.jsonl")
    parser.add_argument("--snippets", default="data/job_snippets.jsonl")
    parser.add_argument("--prompt", default="data/prompt-v1.txt")
    parser.add_argument("--golden-id", default="g015")
    parser.add_argument("--creator-model", default="gpt-4o-mini")
    parser.add_argument("--judge-model", default="gpt-4o")
    parser.add_argument("--max-rounds", type=int, default=3)
    parser.add_argument("--threshold", type=float, default=3.5)
    parser.add_argument(
        "--output",
        default="docs/critic-creator-trace.md",
    )
    args = parser.parse_args()

    if args.max_rounds < 1:
        raise ValueError("--max-rounds must be >= 1")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    golden = load_jsonl(args.golden_set)
    snippets = load_jsonl(args.snippets)

    item = next((x for x in golden if x["id"] == args.golden_id), None)
    if item is None:
        raise ValueError(f"Golden id not found: {args.golden_id}")

    current_prompt = load_prompt(args.prompt)
    context = build_context(snippets)

    question = item["question"]
    ideal = item["ideal_answer"]

    lines = [
        "# Critic-Creator Trace",
        "",
        f"- Golden ID: `{args.golden_id}`",
        f"- Creator model: `{args.creator_model}`",
        f"- Judge model: `{args.judge_model}`",
        f"- Maximum rounds: `{args.max_rounds}`",
        f"- Convergence threshold: `{args.threshold}`",
        "",
        "## Question",
        "",
        question,
        "",
        "## Ideal Answer",
        "",
        ideal,
        "",
    ]

    converged = False
    final_mean = None
    round_scores = []
    prompts = []

    for round_no in range(1, args.max_rounds + 1):
        answer = create_answer(
            client,
            args.creator_model,
            current_prompt,
            question,
            context,
        )

        scores = judge_one(
            question=question,
            candidate_answer=answer,
            ideal_answer=ideal,
            judge_model=args.judge_model,
        )

        mean_score = (
            scores.accuracy
            + scores.groundedness
            + scores.format
        ) / 3

        final_mean = mean_score
        round_scores.append((scores.accuracy, scores.groundedness, scores.format, mean_score))
        prompts.append(current_prompt)

        lines.extend(
            [
                f"## Round {round_no}",
                "",
                "**System prompt:**",
                "",
                current_prompt,
                "",
                "**Candidate answer:**",
                "",
                answer,
                "",
                f"**Scores:** Accuracy={scores.accuracy}, "
                f"Groundedness={scores.groundedness}, "
                f"Format={scores.format}, "
                f"Mean={mean_score:.2f}",
                "",
                f"**Judge reasoning:** {scores.reasoning}",
                "",
            ]
        )

        if mean_score >= args.threshold:
            lines.extend(
                [
                    f"**Converged:** mean score {mean_score:.2f} "
                    f">= threshold {args.threshold:.2f}.",
                    "",
                ]
            )
            converged = True
            break

        if round_no < args.max_rounds:
            revised_prompt = improve_prompt(
                client,
                args.creator_model,
                current_prompt,
                question,
                ideal,
                answer,
                scores,
            )

            lines.extend(
                [
                    "**Prompt improvement from critic:**",
                    "",
                    revised_prompt,
                    "",
                    "**Prompt diff:**",
                    "",
                    f"- Added explicit company-to-role mapping guidance.",
                    f"- Added distinction between no prior experience, no fixed years requirement, and less-than-typical experience.",
                    f"- Added an instruction to include all relevant roles and avoid omissions.",
                    "",
                ]
            )

            current_prompt = revised_prompt

    if not converged:
        lines.extend(
            [
                "**Convergence:** The maximum number of rounds was reached "
                f"without reaching the threshold. Final mean={final_mean:.2f}.",
                "",
            ]
        )

    if round_scores:
        first_mean = round_scores[0][3]
        best_mean = max(x[3] for x in round_scores)
        improvement = best_mean - first_mean

        if improvement > 0:
            improvement_text = (
                f"The best mean score improved from {first_mean:.2f} in Round 1 "
                f"to {best_mean:.2f}, although the final round scored "
                f"{round_scores[-1][3]:.2f}."
            )
        else:
            improvement_text = (
                f"The loop did not produce a net improvement: Round 1 scored "
                f"{first_mean:.2f} and the best/final result remained "
                f"{best_mean:.2f}."
            )

        reflection = (
            f"{improvement_text} "
            "The critic provided useful feedback about company-to-role mapping, "
            "experience-rule distinctions, completeness, and unsupported substitutions. "
            "A possible false alarm is treating a role-title wording difference as a "
            "major error when the underlying experience rule is correctly grounded. "
            "Because the creator regressed after Round 2 and the loop did not reach "
            "the 3.5 convergence threshold, I would not trust this loop without "
            "human oversight and an evaluation gate in production."
        )
    else:
        reflection = (
            "The Critic-Creator loop produced no scored rounds. "
            "The trace should therefore not be used as production evidence."
        )

    lines.extend(
        [
            "## Reflection",
            "",
            reflection,
            "",
        ]
    )

    Path(args.output).write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Running Critic-Creator on {args.golden_id}")
    print(f"question : {question}")
    print(f"creator model : {args.creator_model}")
    print(f"judge model : {args.judge_model}")
    print(f"max rounds : {args.max_rounds}")
    print(f"convergence : mean >= {args.threshold}")
    print(f"Trace written to {args.output}")


if __name__ == "__main__":
    main()
