# DR #1 Summary — M1_Gorthi

## 1. What You Built

M1 evolved the capstone into an AI/RAG assistant focused on job-requirement question answering. The system accepts natural-language questions and is designed to provide concise answers while preserving important role names, experience requirements, technologies, qualifications, and unavailable-information cases.

W5 added a 20-question golden evaluation set over a 10-snippet job-requirement corpus, an LLM-as-a-judge evaluation framework, pairwise prompt comparison, and a Critic-Creator experiment. The existing FastAPI API contract was retained while the W5 work added evaluation and experimentation around the candidate system.

## 2. What You Measured

The W4 candidate was evaluated against all 20 golden questions. The baseline averages were 1.50 for accuracy, 1.65 for groundedness, and 2.40 for format on a 1–4 scale.

Two prompt strategies were then compared using the same context, candidate model, and judge model. Prompt v1 scored 3.60 accuracy, 3.65 groundedness, and 3.85 format, for an overall score of 3.70. Prompt v2 scored 3.60 accuracy, 3.75 groundedness, and 3.70 format, for an overall score of 3.68. Prompt v1 was therefore selected for M1.

The Critic-Creator experiment on g015 did not converge to the 3.5 threshold. Round 1 and Round 2 both scored 3.33 mean, while Round 3 regressed to 2.33. This shows that critic feedback did not guarantee monotonic improvement and supports retaining an evaluation gate and human oversight.

## 3. Top 3 Things to Discuss

1. **Retrieval strategy:** The baseline demonstrates the limitation of answering without retrieval context. The next phase should determine the appropriate retrieval and chunking approach for the job-requirement corpus.

2. **Evaluation gates:** The Critic-Creator regression shows why an iterative improvement loop should not be trusted without measurable evaluation thresholds and regression checks.

3. **Grounding and answer trust:** Prompt v2 improved groundedness even though Prompt v1 had the higher overall score. The design should continue exploring targeted grounding constraints without sacrificing answer quality and usability.

## 4. What I Will Defend If Asked

- **Why keep gpt-4o-mini?** It provides a cost-conscious candidate baseline while allowing quality to be measured systematically.

- **Why select Prompt v1?** It achieved the highest overall pairwise score, 3.70 versus 3.68 for Prompt v2, while Prompt v2's grounding improvements remain useful for future refinement.

- **Why is the Critic-Creator result acceptable?** The experiment is valuable precisely because it exposed a failure mode: the loop regressed from 3.33 to 2.33 instead of converging. The result supports human oversight, explicit evaluation gates, and regression testing before such a loop could be trusted in production.
