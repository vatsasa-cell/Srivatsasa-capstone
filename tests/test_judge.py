import json

import pytest

from src.eval.judge import JudgeScore, RUBRIC_PROMPT


def test_judge_score_accepts_valid_scores():
    score = JudgeScore(
        accuracy=4,
        groundedness=3,
        format=4,
        reasoning="The answer is correct and grounded in the supplied job information.",
    )

    assert score.accuracy == 4
    assert score.groundedness == 3
    assert score.format == 4


@pytest.mark.parametrize(
    "field",
    ["accuracy", "groundedness", "format"],
)
def test_judge_score_rejects_zero(field):
    values = {
        "accuracy": 4,
        "groundedness": 4,
        "format": 4,
        "reasoning": "Test reasoning",
    }
    values[field] = 0

    with pytest.raises(Exception):
        JudgeScore(**values)


@pytest.mark.parametrize(
    "field",
    ["accuracy", "groundedness", "format"],
)
def test_judge_score_rejects_five(field):
    values = {
        "accuracy": 4,
        "groundedness": 4,
        "format": 4,
        "reasoning": "Test reasoning",
    }
    values[field] = 5

    with pytest.raises(Exception):
        JudgeScore(**values)


def test_judge_score_requires_reasoning():
    with pytest.raises(Exception):
        JudgeScore(
            accuracy=4,
            groundedness=4,
            format=4,
        )


def test_judge_score_serializes_to_json():
    score = JudgeScore(
        accuracy=4,
        groundedness=4,
        format=3,
        reasoning="The candidate answer is well grounded.",
    )

    payload = json.loads(score.model_dump_json())

    assert payload["accuracy"] == 4
    assert payload["groundedness"] == 4
    assert payload["format"] == 3
    assert "reasoning" in payload


def test_rubric_is_long_enough():
    assert len(RUBRIC_PROMPT.split()) > 150


def test_rubric_contains_required_dimensions():
    rubric = RUBRIC_PROMPT.lower()

    assert "accuracy" in rubric
    assert "groundedness" in rubric
    assert "format" in rubric


def test_rubric_requires_tool_call():
    assert "ALWAYS call the rate_answer tool" in RUBRIC_PROMPT
    assert "Never reply in plain text." in RUBRIC_PROMPT
