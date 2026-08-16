"""run_four_prompts.py — Instructor convenience script for W1 activity.

Runs the same question through all four W1 system prompts and writes
docs/runs/week1-activity.md with the side-by-side comparison.

Usage:
    python run_four_prompts.py "Explain quantum entanglement in two sentences."

Produces:
    docs/runs/week1-activity.md (with prompts A through D + headings)
"""
import sys
from pathlib import Path

from openai import OpenAI


client = OpenAI()


PROMPTS = {
    "A": ("You are concise.", "Default — terse academic"),
    "B": (
        "You are a kindergarten teacher. Explain like the listener is five years old.",
        "Kindergarten teacher — simple words, playful analogy",
    ),
    "C": (
        "You are a Shakespearean poet. Reply in iambic verse where possible.",
        "Shakespearean poet — iambic verse",
    ),
    "D": (
        "You are a brilliant but impatient physicist. You explain accurately "
        "but you don't have time for niceties.",
        "Grumpy expert — accurate but dismissive",
    ),
}


def ask_with_system_prompt(question: str, system_prompt: str,
                            model: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content


def main():
    if len(sys.argv) < 2:
        question = "Explain quantum entanglement in two sentences."
        print(f"(no question given — using default: {question!r})\n")
    else:
        question = sys.argv[1]

    output_lines = [
        "# Week 1 Activity — Voice Reshape",
        "",
        f"**Question (held constant across all four runs):** *{question}*",
        "",
        "---",
        "",
    ]

    for letter, (system_prompt, label) in PROMPTS.items():
        print(f"Running Prompt {letter} — {label}...")
        answer = ask_with_system_prompt(question, system_prompt)
        output_lines.extend([
            f"## Prompt {letter} — {label}",
            "",
            f"**System prompt:** {system_prompt!r}",
            "",
            "**Answer:**",
            "",
            f"> {answer}",
            "",
            "---",
            "",
        ])

    output_lines.extend([
        "## What changed?",
        "",
        "_(Fill in your 2-3 sentence observation here. Notice what stayed the "
        "same across all four answers, and what changed the most.)_",
        "",
    ])

    output_path = Path("docs/runs/week1-activity.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(output_lines))
    print(f"\nWrote {output_path}")


if __name__ == "__main__":
    main()
