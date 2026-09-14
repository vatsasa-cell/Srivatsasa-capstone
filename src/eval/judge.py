"""LLM-as-a-Judge for the W5 evaluation pipeline."""

from __future__ import annotations

import json
import os

from openai import OpenAI
from pydantic import BaseModel, Field


class JudgeScore(BaseModel):
    """Structured score returned by the evaluation judge."""

    accuracy: int = Field(ge=1, le=4)
    groundedness: int = Field(ge=1, le=4)
    format: int = Field(ge=1, le=4)
    reasoning: str


RUBRIC_PROMPT = """
You are a senior evaluator for a job-requirement question-answering assistant.
Evaluate the candidate answer against the user's question and the ideal answer.
Judge only what is supported by the supplied question, ideal answer, and candidate
answer. Do not reward plausible information that is not supported by the evidence.

Score three dimensions from 1 to 4.

ACCURACY:
1 = The answer is substantially incorrect, contradicts the ideal answer, or answers
the wrong question.
2 = The answer contains some correct information but has a significant omission,
misinterpretation, unsupported claim, or incorrect requirement.
3 = The answer is substantially correct and answers the question, but has a minor
omission, imprecise wording, or small unnecessary detail.
4 = The answer is fully correct, directly answers the question, preserves important
qualifiers such as minimums, ranges, exceptions, or alternatives, and contains no
material unsupported claims.

GROUNDEDNESS:
1 = The answer contains major claims that cannot be supported by the supplied
job information or directly contradicts the source.
2 = The answer is partly supported but includes one or more notable unsupported
claims, invented requirements, or unjustified inferences.
3 = Nearly all claims are grounded in the supplied information, with at most a
minor inference or wording issue that does not materially change the answer.
4 = Every material claim is directly supported by the supplied information and the
answer does not invent facts, requirements, benefits, salary, qualifications, or
guarantees. For missing information, a strong answer explicitly says that the
information is not provided rather than guessing.

FORMAT:
1 = The response is confusing, fails to answer in a usable form, or is substantially
unrelated to the requested information.
2 = The response is understandable but poorly focused, unnecessarily verbose, or
omits important information needed to make the answer useful.
3 = The response is clear, concise, professional, and directly addresses the
question, with only minor presentation issues.
4 = The response is concise, easy to understand, directly answers the question,
and clearly preserves important qualifiers such as "typically", "around",
"5+", ranges, alternatives, and exceptions.

For every score, give concise reasoning that identifies the specific strengths or
problems in the candidate answer. Treat "not stated in the source" as the correct
handling of missing information. Do not assume information merely because it would
normally be expected in a job posting.

ALWAYS call the rate_answer tool. Never reply in plain text.
""".strip()


RATE_ANSWER_TOOL = {
    "type": "function",
    "function": {
        "name": "rate_answer",
        "description": "Rate a candidate answer against the supplied ideal answer.",
        "parameters": {
            "type": "object",
            "properties": {
                "accuracy": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 4,
                },
                "groundedness": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 4,
                },
                "format": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 4,
                },
                "reasoning": {
                    "type": "string",
                },
            },
            "required": [
                "accuracy",
                "groundedness",
                "format",
                "reasoning",
            ],
            "additionalProperties": False,
        },
    },
}


def judge_one(
    question: str,
    candidate_answer: str,
    ideal_answer: str,
    judge_model: str = "gpt-4o",
) -> JudgeScore:
    """Score one candidate answer with the LLM judge."""

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    user_prompt = f"""
Question:
{question}

Ideal answer:
{ideal_answer}

Candidate answer:
{candidate_answer}
""".strip()

    resp = client.chat.completions.create(
        model=judge_model,
        messages=[
            {"role": "system", "content": RUBRIC_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        tools=[RATE_ANSWER_TOOL],
        tool_choice={
            "type": "function",
            "function": {"name": "rate_answer"},
        },
        temperature=0,
    )

    message = resp.choices[0].message

    if not message.tool_calls:
        raise ValueError("Judge did not return the required rate_answer tool call")

    tool_call = message.tool_calls[0]

    if tool_call.function.name != "rate_answer":
        raise ValueError(
            f"Unexpected judge tool: {tool_call.function.name}"
        )

    data = json.loads(tool_call.function.arguments)
    return JudgeScore.model_validate(data)
