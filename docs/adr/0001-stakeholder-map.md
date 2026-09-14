# Stakeholder Map — M1_Gorthi

## 1. Primary User

**Primary user:** Recruiters and hiring managers who need quick answers
about job requirements while screening candidates or reviewing open roles.

The EKA is intended to answer routine questions about role names,
experience requirements, technologies, qualifications, and conditional
requirements from approved job-requirement content.

## 2. Secondary Stakeholders

- **HR / Talent Acquisition:** Uses the assistant to reduce repetitive
  requirement lookups and support candidate screening.
- **Hiring Managers:** Uses the assistant to clarify requirements for
  open positions.
- **HR Operations / Knowledge Owners:** Maintains the source job-requirement
  content and is responsible for keeping it current.
- **Security / Compliance:** Acts as a gatekeeper for appropriate use,
  data handling, access, and governance.
- **RPA / AI Engineering Team:** Builds, evaluates, monitors, and maintains
  the EKA solution.
- **Candidates / Employees:** May benefit indirectly from more consistent
  interpretation of published job requirements.

## 3. Before-AI Workflow

A recruiter or hiring manager identifies a question about a job requirement,
locates the relevant job description or requirement document, reads the
applicable section, and interprets the requirement manually.

For repeated questions, the same lookup and interpretation activity is
performed again. Ambiguous or missing information may require follow-up
with the hiring manager or HR/knowledge owner.

## 4. Desired After-State

The EKA accepts a natural-language question and returns a concise answer
grounded in the approved job-requirement context.

The assistant should preserve important role names, experience values,
technologies, and qualifications, avoid unsupported claims, and indicate
when requested information is not provided.

Questions that cannot be answered confidently from the approved context
should remain candidates for human review.

## 5. Top 3 Sponsor Metrics

The following metrics are proposed for M1 and should be validated with the
project sponsor before the ADR is locked:

1. **Answer Accuracy** — average LLM-judge accuracy score on the golden set,
   measured on a 1–4 scale. M1 baseline: **1.50**.
2. **Answer Groundedness** — average LLM-judge groundedness score on the
   golden set, measured on a 1–4 scale. M1 baseline: **1.65**.
3. **Answer Cost** — average generation cost per answer, with the W4/M1
   engineering target of **≤ $0.01 per answer on average**.

### M1 Measurement Baseline

| Sponsor Metric | M1 Baseline | Measurement |
|---|---:|---|
| Answer Accuracy | 1.50 / 4 | 20-question golden-set evaluation |
| Answer Groundedness | 1.65 / 4 | 20-question golden-set evaluation |
| Answer Cost | ≤ $0.01 target | Candidate-model generation cost |

### W12 Target

The final W12 targets for these sponsor metrics require sponsor
confirmation and should be updated here and in ADR-0001 once agreed.
