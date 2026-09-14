# W5 Lab Notes — M1_Gorthi

## 1. Purpose

Week 5 evaluates and improves the Enterprise Knowledge Assistant (EKA)
using a job-requirement question-answering domain.

The W5 work focuses on establishing a measurable evaluation baseline,
comparing prompt strategies, and using a Critic-Creator loop to improve
answers on difficult questions.

## 2. Evaluation Dataset

The evaluation set contains 20 golden questions covering job requirements
such as role names, years of experience, technologies, qualifications,
conditional requirements, comparisons, and unavailable information.

The source corpus contains 10 job-requirement snippets.

## 3. LLM-as-a-Judge

The evaluation uses an LLM judge with three scoring dimensions:

- Accuracy: 1–4
- Groundedness: 1–4
- Format: 1–4

The judge also provides reasoning for each score.

Judge model: `gpt-4o`

Candidate model: `gpt-4o-mini`

Detailed implementation:
- `src/eval/judge.py`
- `tests/test_judge.py`

## 4. Baseline Evaluation — eval-run-001

The W4 candidate was evaluated against all 20 golden questions.

Results:

| Metric | Baseline |
|---|---:|
| Number of entries | 20 |
| Average accuracy | 1.50 |
| Average groundedness | 1.65 |
| Average format | 2.40 |

Accuracy distribution:

| Accuracy | Count |
|---|---:|
| 4 | 0 |
| 3 | 0 |
| 2 | 10 |
| 1 | 10 |

The baseline demonstrates that the W4 candidate does not have access to
the job-requirement corpus as retrieval context. The low accuracy and
groundedness scores therefore provide a useful baseline for subsequent
W5 improvements.

Detailed results:
`docs/eval-run-001.md`



## 5. Pairwise Prompt Comparison

Two prompt strategies were compared using the same 20 questions,
the same job-requirement context, candidate model, and judge model.

### Prompt v1

```text
Answer the user's question directly and concisely.
```

### Prompt v2

```text
Answer the user's question using only the provided job-requirement context.

Rules:
1. Treat the supplied context as the only source of truth.
2. Answer the question directly and concisely.
3. Do not invent or assume information that is not stated in the context.
4. If the context does not provide the requested information, say that it is not provided.
5. Preserve important numbers, role names, technologies, and qualifications exactly as supported by the context.
```

Results:

| Strategy | Accuracy | Groundedness | Format | Overall |
|---|---:|---:|---:|---:|
| Prompt v1 | 3.60 | 3.65 | 3.85 | 3.70 |
| Prompt v2 | 3.60 | 3.75 | 3.70 | 3.68 |

Prompt v1 was selected because it achieved the highest overall score.

Prompt v2 showed better groundedness and is useful as a source of targeted grounding constraints.

Detailed results:
`docs/prompt-pairwise-001.md`
## 6. Critic-Creator Experiment

The Critic-Creator experiment evaluates iterative improvement on a difficult golden-set question.

The creator generates an answer, the answer is evaluated by the judge, and critic feedback is used to improve the subsequent answer.

The experiment uses:

- Golden question: `g015`
- Creator model: `gpt-4o-mini`
- Judge model: `gpt-4o`
- Maximum rounds: `3`
- Convergence threshold: mean score >= `3.5`

The trace records the candidate answer, judge scores, judge reasoning, and critic feedback for each round.

The purpose of the loop is to determine whether targeted critic feedback can produce a materially better answer on a difficult question while maintaining factual accuracy and groundedness.

Detailed trace:
`docs/critic-creator-trace.md`
## 7. W5 Conclusions

W5 established a measurable evaluation baseline and demonstrated that prompt strategy affects answer quality.

The pairwise experiment selected Prompt v1 based on the aggregate score, while identifying grounding constraints from Prompt v2 as useful improvements to carry forward.

The baseline also confirms that retrieval and context integration is an important next step because the W4 candidate answers questions without the job-requirement corpus.

## 8. Related Artifacts

- `data/golden_set.jsonl`
- `data/job_snippets.jsonl`
- `data/prompt-v1.txt`
- `data/prompt-v2.txt`
- `src/eval/judge.py`
- `scripts/run_eval.py`
- `scripts/run_pairwise.py`
- `scripts/run_critic_creator.py`
- `docs/eval-run-001.md`
- `docs/prompt-pairwise-001.md`
- `docs/critic-creator-trace.md`
- `docs/adr/0001-capstone-framing.md`
- `docs/adr/0002-api-contract.md`

**Observed result:** The experiment did not converge. Round 1 and Round 2 both achieved a mean score of 3.33, while Round 3 regressed to 2.33. The result indicates that critic feedback alone was not sufficient to guarantee monotonic improvement.
