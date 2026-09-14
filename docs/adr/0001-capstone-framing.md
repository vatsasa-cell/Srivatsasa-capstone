# ADR-0001: Capstone Framing — M1_Gorthi

- **Status:** Accepted — M1 Locked
- **Date:** 2026-09-14
- **Author:** Srivatsasa Gorthi

## 1. Context

The original W1 capstone framing proposed an HR Policy Assistant for
routine policy questions such as leave, benefits, and expense limits.
The original concept was a grounded Q&A assistant using an approved
knowledge source, with human escalation for ambiguous questions.

During M1, the capstone scope was refined to an Enterprise Knowledge
Assistant (EKA) focused on job-requirement question answering. The W5
evaluation corpus contains 10 job-requirement snippets and the evaluation
set contains 20 golden questions covering role names, experience,
technologies, qualifications, conditional requirements, comparisons,
and unavailable information.

The original W1 framing is preserved in:
`docs/adr/0001-capstone-framing-w1-original.md`

The detailed W5 evidence is maintained separately in:
`docs/w5-lab-notes.md`

## 2. Problem Statement

Recruiters and hiring managers need to answer recurring questions about
job requirements while screening candidates or reviewing open roles.
The current workflow requires manually locating the relevant job
description or requirement content and interpreting it.

The capstone aims to provide concise answers grounded in approved
job-requirement content while avoiding unsupported claims and escalating
questions that cannot be reliably answered from the available context.

## 3. Scope and Users

### Primary User

Recruiters and hiring managers who need quick answers about job
requirements while screening candidates or reviewing open roles.

### Secondary Stakeholders

- HR / Talent Acquisition
- Hiring Managers
- HR Operations / Knowledge Owners
- Security / Compliance
- RPA / AI Engineering Team
- Candidates / Employees as indirect beneficiaries

Security / Compliance is a governance gatekeeper. HR Operations /
Knowledge Owners maintain the source content. The RPA / AI Engineering
Team builds and maintains the solution.

### In Scope

- Natural-language questions about job requirements
- Role names
- Years of experience
- Technologies
- Qualifications
- Conditional experience requirements
- Comparison questions across job snippets
- Explicit handling of information that is not provided

### Out of Scope for M1

- Autonomous hiring decisions
- Candidate rejection or selection
- Actions in HR systems
- Persistent conversational memory
- Multilingual support
- Production retrieval infrastructure

## 4. Decisions Locked at M1

### 4.1 Solution Pattern

The capstone remains a Q&A assistant. It answers questions and does not
take autonomous business actions.

### 4.2 API Contract

The existing FastAPI service and W4 API contract are preserved.

The public `Answer` response contains:

- `content`
- `cost_usd`
- `retries`
- `confidence`
- `sources`
- `schema_version`

API contract details remain documented in:
`docs/adr/0002-api-contract.md`

### 4.3 Candidate Model

The candidate model is:

`gpt-4o-mini`

This model is used for answer generation and evaluation experiments.

### 4.4 Judge Model

The LLM-as-a-judge model is:

`gpt-4o`

The judge scores:

- Accuracy: 1–4
- Groundedness: 1–4
- Format: 1–4

The judge also returns reasoning.

### 4.5 Evaluation Set

M1 uses a 20-question golden set over a 10-snippet job-requirement
corpus.

The golden set is:

`data/golden_set.jsonl`

### 4.6 Prompt Strategy

Two prompt strategies were compared using the same questions, context,
candidate model, and judge model.

Prompt v1 achieved the higher overall score:

- Accuracy: 3.60
- Groundedness: 3.65
- Format: 3.85
- Overall: 3.70

Prompt v2 achieved:

- Accuracy: 3.60
- Groundedness: 3.75
- Format: 3.70
- Overall: 3.68

Therefore, **Prompt v1 is the selected M1 strategy**.

Targeted grounding constraints from Prompt v2 may be carried forward when
they improve factual support without unnecessarily restricting response
quality.

Detailed comparison:
`docs/prompt-pairwise-001.md`

### 4.7 Cost Target

The engineering target is:

**≤ $0.01 per answer on average**

Cost remains a tracked evaluation dimension for future iterations.

### 4.8 Retrieval Direction

Retrieval/context integration is identified as an important next step.
The W4 candidate baseline did not have access to the job-requirement
corpus as retrieval context.

Retrieval infrastructure is therefore deferred to a subsequent phase
rather than being treated as an M1 production capability.

## 5. Sponsor KPIs

The M1 stakeholder map identifies three sponsor metrics:

1. **Answer Accuracy**
2. **Answer Groundedness**
3. **Answer Cost**

### M1 Baseline

| KPI | M1 Measurement | Target |
|---|---:|---:|
| Answer Accuracy | 1.50 / 4 | W12 target — sponsor confirmation required |
| Answer Groundedness | 1.65 / 4 | W12 target — sponsor confirmation required |
| Answer Cost | Candidate-model generation cost; engineering target ≤ $0.01/answer | ≤ $0.01/answer average |

The M1 KPI definitions are documented in:
`docs/adr/0001-stakeholder-map.md`

W12 targets are not invented here because they have not yet been
confirmed by the sponsor.

## 6. Evaluation Baseline

The W4 candidate was evaluated against all 20 golden questions.

| Metric | M1 Baseline |
|---|---:|
| Entries scored | 20 |
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

The baseline shows that the W4 candidate performs poorly on the
job-requirement questions when the source corpus is not supplied as
retrieval context.

Detailed baseline:
`docs/eval-run-001.md`

## 7. Technology Approach

The M1 solution uses:

- Python
- FastAPI
- OpenAI API
- `gpt-4o-mini` for candidate generation
- `gpt-4o` for evaluation
- Pydantic models for structured API responses
- SQLite for evaluation/result persistence
- JSONL for the golden set and job-requirement corpus

The solution continues to use the existing W4 API contract while W5
adds evaluation and prompt experimentation around the candidate system.

## 8. Alternatives and Trade-offs

### Prompt v1 vs Prompt v2

Prompt v1 produced the highest overall aggregate score and was selected.
Prompt v2 produced higher groundedness but lower format and slightly
lower overall performance.

### Larger Candidate Model

A larger generation model could potentially improve answer quality, but
the M1 decision retains `gpt-4o-mini` to preserve the cost-conscious
engineering target and maintain a clear baseline.

### Retrieval in M1

Introducing full retrieval infrastructure during M1 could improve
groundedness, but it would also introduce additional architecture and
evaluation variables. M1 therefore establishes the evaluation baseline
first and defers retrieval integration.

### Human Review

The assistant should not make autonomous hiring decisions. Questions that
cannot be reliably answered from approved context remain candidates for
human review.

## 9. Open Questions

1. What retrieval strategy and chunking approach should be used when the
   job-requirement corpus is integrated?
2. What evaluation threshold should block or escalate an answer in a
   production workflow?
3. What are the sponsor-approved W12 targets for accuracy, groundedness,
   and cost?

## 10. DR #1 Defence

_To be completed during the live DR #1 discussion._

Key points to defend:

- The M1 baseline is intentionally measured before retrieval integration,
  providing a clear reference point for future improvements.
- Prompt v1 was selected from the pairwise experiment based on the highest
  overall score, while useful grounding constraints from v2 were retained
  as a potential improvement direction.
- The API contract remains stable while evaluation, prompting, and retrieval
  capabilities evolve around it.

## 11. Change Log

### W1 — Initial Framing

The capstone was initially framed as an HR Policy Assistant for routine
employee-policy questions using grounded Q&A over an employee handbook.

### W4 — Engineering Foundation

The FastAPI service, candidate model integration, structured `Answer`
schema, cost tracking, and schema-versioning approach were established.

### W5 — M1 Lock

The capstone scope was refined to the job-requirement EKA domain.

W5 established:

- a 20-question golden evaluation set
- an LLM-as-a-judge evaluation
- a measurable baseline
- pairwise prompt comparison
- Prompt v1 as the selected M1 strategy
- a Critic-Creator experiment
- explicit open questions for subsequent phases

The detailed W5 work is documented in:
`docs/w5-lab-notes.md`
