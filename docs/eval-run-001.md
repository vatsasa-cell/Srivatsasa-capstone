# Evaluation Run 001 — W5 Baseline

## 1. Evaluation Overview

This evaluation establishes the first quality baseline for the capstone using the W5 20-entry golden set.

- **Evaluation label:** `eval-run-001`
- **Golden set:** `data/golden_set.jsonl`
- **Number of entries:** 20
- **Candidate model:** `gpt-4o-mini`
- **Judge model:** `gpt-4o`
- **Candidate endpoint:** `/ask_batched`
- **Persistence:** `data/answers.db` → `eval_runs`
- **Wall-clock time:** 123.4 seconds

## 2. Aggregate Results

| Metric | Average Score |
|---|---:|
| Accuracy | **1.50 / 4** |
| Groundedness | **1.65 / 4** |
| Format | **2.40 / 4** |

### Accuracy Distribution

| Accuracy Score | Number of Entries |
|---:|---:|
| 4 | 0 |
| 3 | 0 |
| 2 | 10 |
| 1 | 10 |

## 3. Baseline Interpretation

The baseline shows weak accuracy and groundedness against the job-requirement golden set.

The current W4 candidate endpoint sends the user question directly to the LLM without supplying the job-requirement snippets as retrieval context. Consequently, the candidate frequently responds with generic hiring guidance or states that it does not have access to the specific job information.

This behavior provides a useful baseline for measuring future improvements rather than being treated as a system failure.

## 4. Five-Entry Judge Spot Check

Five randomly selected verdicts were manually reviewed.

### g011 — Soylent Engineering Manager

- Accuracy: 1
- Groundedness: 1
- Format: 2
- The candidate provided generic Engineering Manager qualifications and incorrectly suggested typical management experience of 5–10 years.
- The ideal answer specifies approximately three years of engineering-team leadership experience plus a solid IC background.

### g018 — Pied Piper Experience Exception

- Accuracy: 2
- Groundedness: 2
- Format: 2
- The candidate suggested that fewer than seven years would generally result in disqualification.
- The ideal answer explicitly states that exceptional candidates with less experience are welcome.

### g009 — Hooli Junior Frontend Developer

- Accuracy: 2
- Groundedness: 2
- Format: 3
- The candidate correctly mentioned JavaScript and React but added many unsupported technologies and requirements.
- The source specifically identifies JavaScript, React, and CSS fundamentals.

### g003 — Northwind Data Analyst

- Accuracy: 2
- Groundedness: 2
- Format: 3
- The candidate gave a generic 1–3 year experience range instead of the specific two-year minimum in the ideal answer.

### g010 — Pied Piper ML Engineer

- Accuracy: 1
- Groundedness: 1
- Format: 3
- The candidate incorrectly stated approximately five years of production ML experience.
- The ideal answer specifies 7+ years of production ML and distributed-systems experience.

## 5. Judge Quality Assessment

All five manually reviewed verdicts were consistent with the observed candidate responses.

The judge appropriately penalized:
- incorrect experience requirements;
- unsupported assumptions;
- generic responses that did not answer the specific question;
- failure to recognize important qualification exceptions.

The spot check did not identify an obvious judge-scoring problem.

## 6. Baseline Conclusion

`eval-run-001` establishes the initial W5 quality baseline:

- Accuracy: **1.50 / 4**
- Groundedness: **1.65 / 4**
- Format: **2.40 / 4**

Future prompt, retrieval, and system improvements can be compared against this baseline to determine whether they produce measurable quality gains.
