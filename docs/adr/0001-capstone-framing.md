# ADR-0001: Capstone Framing — HR Policy Assistant
- **Status:** Draft v1 
- **Date:** 2026-08-21
- **Author:** Srivatsasa Gorthi
## Context
 Our HR team fields ~40 routine policy questions per week — leave, benefits,
expense limits — most of which are already documented in the employee handbook. A
grounded Q&A assistant could deflect ~70% of these while keeping the human in the
loop for the ambiguous 30%.
## Decision — Solution Framing Canvas
| Box | Your answer |
|-----|-------------|
| **Inputs** |  a natural-language question (1‒2 sentences), e.g. "How many sick days do I get in my first year?"|
| **Outputs** |  a 2‒4-sentence answer in plain English plus citation links pointing back to the source paragraph in the handbook. |
| **Tools** |gpt-4o-mini for generation, a vector store (W7 will introduce) for retrieval over the chunked handbook|
| **Memory** | What does it remember? Example: nothing across sessions in v1 (every question is fresh); we'll revisit in W14 if multi-turn conversations land.|
| **Autonomy level** | Where on the spectrum? Example: Q&A app — it answers, it doesn't act. No tool calls beyond retrieval. (Slide 9 of Day 1, between Chatbot and Workflow.) |
| **Decision boundaries** |  What's it allowed to decide vs. escalate? Example: it may answer any question whose retrieval confidence exceeds a threshold (TBD in W12); otherwise it returns "I'm not sure — please contact HR at hr@…"|
## Consequences 
- **Positive:** what this design unlocks. Example: deflects ~70% of routine traffic; gives an honest "I don't know" rather than guessing; citations build trust>
- **Negative / risks:**  what's harder / costlier / riskier. Example: requires a maintained, up-to-date handbook; one bad citation could erode trust faster than ten good answers; no memory means context across questions is lost.>
- **Things we'll re-visit:**  specific later-week revisits. Example: confidence-threshold tuning in W12; multi-turn memory in W14; multilingual support in W19. we'll come back to in later ADRs