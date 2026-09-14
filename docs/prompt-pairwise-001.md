# Prompt Pairwise Comparison

- Candidate model: `gpt-4o-mini`
- Judge model: `gpt-4o`
- Questions: `20`

## Aggregate Scores

| Strategy | Accuracy | Groundedness | Format | Overall |
|---|---:|---:|---:|---:|
| Prompt v1 | 3.60 | 3.65 | 3.85 | 3.70 |
| Prompt v2 | 3.60 | 3.75 | 3.70 | 3.68 |

## Per-Question Results

### g001: What role is Acme Corp hiring for, and how many years of backend development experience are required?

**Ideal:** Acme Corp is hiring a Senior Software Engineer. The role requires 5+ years of backend development experience.

**V1:** Acme Corp is hiring for a Senior Software Engineer, and the role requires 5+ years of backend development experience.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** Acme Corp is hiring for a Senior Software Engineer, and 5+ years of backend development experience are required.

V2 scores — Accuracy: 4, Groundedness: 4, Format: 4

### g002: What skills are expected for the Senior Software Engineer role at Acme Corp?

**Ideal:** The role expects strong skills in Python and distributed systems, along with backend development experience.

**V1:** The expected skills for the Senior Software Engineer role at Acme Corp include strong skills in Python and experience with distributed systems. Additionally, 5+ years of backend development experience is required.

V1 scores — Accuracy: 2, Groundedness: 2, Format: 3

**V2:** The expected skills for the Senior Software Engineer role at Acme Corp are strong skills in Python and distributed systems.

V2 scores — Accuracy: 3, Groundedness: 4, Format: 3

### g003: How much experience is required for the Data Analyst position at Northwind Ltd?

**Ideal:** Northwind Ltd is looking for a Data Analyst with 2 years of minimum experience. The role involves SQL, dashboards, and stakeholder requests.

**V1:** A minimum of 2 years of experience is preferred for the Data Analyst position at Northwind Ltd.

V1 scores — Accuracy: 3, Groundedness: 3, Format: 3

**V2:** The Data Analyst position at Northwind Ltd prefers a minimum of 2 years of experience.

V2 scores — Accuracy: 3, Groundedness: 3, Format: 4

### g004: What is the minimum product management experience required for the Globex International Product Manager - Growth role?

**Ideal:** Globex International is looking for someone with at least 4 years of product management experience in B2C contexts.

**V1:** The minimum product management experience required for the Globex International Product Manager - Growth role is 4 years.

V1 scores — Accuracy: 3, Groundedness: 3, Format: 4

**V2:** The minimum product management experience required for the Globex International Product Manager - Growth role is at least 4 years.

V2 scores — Accuracy: 3, Groundedness: 3, Format: 3

### g005: What role is Globex International hiring for and what area will the person own?

**Ideal:** Globex International is hiring a Product Manager - Growth. The person will own activation and onboarding metrics across the company's consumer apps.

**V1:** Globex International is hiring for a Product Manager - Growth, and the person will own activation and onboarding metrics across their consumer apps.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** Globex International is hiring for a Product Manager - Growth, and the person will own activation and onboarding metrics across their consumer apps.

V2 scores — Accuracy: 4, Groundedness: 4, Format: 4

### g006: How many years of infrastructure experience does Initech expect for its Lead DevOps Engineer role?

**Ideal:** Initech expects around 6 years of hands-on infrastructure work for the Lead DevOps Engineer role.

**V1:** Initech expects around 6 years of hands-on infrastructure experience for its Lead DevOps Engineer role.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** Initech expects around 6 years of hands-on infrastructure work for its Lead DevOps Engineer role.

V2 scores — Accuracy: 4, Groundedness: 4, Format: 4

### g007: Which technologies are preferred for the Initech Lead DevOps Engineer position?

**Ideal:** The position ideally requires experience with AWS, Terraform, and modern CI/CD.

**V1:** The preferred technologies for the Initech Lead DevOps Engineer position are AWS, Terraform, and modern CI/CD tools.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** The preferred technologies for the Initech Lead DevOps Engineer position are AWS, Terraform, and modern CI/CD.

V2 scores — Accuracy: 4, Groundedness: 4, Format: 4

### g008: Does the Hooli Junior Frontend Developer position require previous work experience?

**Ideal:** No. Hooli welcomes fresh graduates and states that no prior experience is required.

**V1:** No, the Hooli Junior Frontend Developer position does not require previous work experience. Fresh grads are welcome, and no prior experience is required.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** No prior experience is required for the Hooli Junior Frontend Developer position.

V2 scores — Accuracy: 3, Groundedness: 4, Format: 3

### g009: What technical skills are expected for the Hooli Junior Frontend Developer role?

**Ideal:** The role expects JavaScript, React, and CSS fundamentals.

**V1:** The technical skills expected for the Hooli Junior Frontend Developer role include JavaScript, React, and CSS fundamentals.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** The technical skills expected for the Hooli Junior Frontend Developer role are JavaScript, React, and CSS fundamentals.

V2 scores — Accuracy: 4, Groundedness: 4, Format: 4

### g010: How many years of production ML experience does Pied Piper typically look for?

**Ideal:** Pied Piper typically looks for 7+ years of experience in production ML and distributed systems.

**V1:** Pied Piper typically looks for 7+ years of production ML experience.

V1 scores — Accuracy: 3, Groundedness: 4, Format: 4

**V2:** Pied Piper typically looks for 7+ years in production ML experience.

V2 scores — Accuracy: 3, Groundedness: 4, Format: 3

### g011: What is the experience expectation for the Engineering Manager role at Soylent Industries?

**Ideal:** Soylent Industries expects about three years of experience leading engineering teams, along with a solid individual-contributor background.

**V1:** The experience expectation for the Engineering Manager role at Soylent Industries is about three years of leading engineering teams, along with a solid individual contributor background before that.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** The experience expectation for the Engineering Manager role at Soylent Industries is about three years leading engineering teams, plus a solid IC background before that.

V2 scores — Accuracy: 4, Groundedness: 4, Format: 4

### g012: What experience is required for the Senior UX Researcher role at Wonka Confectionery Ltd?

**Ideal:** Wonka Confectionery Ltd requires five years of UX research experience or an equivalent portfolio.

**V1:** The Senior UX Researcher role at Wonka Confectionery Ltd requires five years of UX research experience or an equivalent portfolio.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** Five years of UX research experience or an equivalent portfolio is required for the Senior UX Researcher role at Wonka Confectionery Ltd.

V2 scores — Accuracy: 4, Groundedness: 4, Format: 4

### g013: What experience range is specified for the Cybersecurity Analyst role at Stark Industries?

**Ideal:** Stark Industries specifies three to five years of experience in a SOC environment or equivalent.

**V1:** The experience range specified for the Cybersecurity Analyst role at Stark Industries is three to five years in a SOC environment or equivalent.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** The experience range specified for the Cybersecurity Analyst role at Stark Industries is three to five years in a SOC environment or equivalent.

V2 scores — Accuracy: 4, Groundedness: 4, Format: 4

### g014: Does Cyberdyne Systems specify a minimum number of years of experience for its AI/ML Research Scientist role?

**Ideal:** No. Cyberdyne Systems explicitly says it does not list a specific years requirement and hires based on demonstrated impact.

**V1:** No, Cyberdyne Systems does not specify a minimum number of years of experience for its AI/ML Research Scientist role. They hire based on demonstrated impact instead.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** No, Cyberdyne Systems does not specify a minimum number of years of experience for its AI/ML Research Scientist role.

V2 scores — Accuracy: 4, Groundedness: 4, Format: 4

### g015: Which roles in the job snippets accept candidates without a conventional fixed years-of-experience requirement?

**Ideal:** Hooli's Junior Frontend Developer role requires no prior experience and welcomes fresh graduates. Cyberdyne Systems' AI/ML Research Scientist role does not specify a years requirement and instead hires based on demonstrated impact. Pied Piper also says exceptional candidates with less than its typical 7+ years may be considered.

**V1:** The roles that accept candidates without a conventional fixed years-of-experience requirement are:

- [j05] Junior Frontend Developer at Hooli (no prior experience required).
- [j06] Senior ML Engineer at Pied Piper Inc. (exceptional candidates with less than 7 years are welcome).
- [j10] AI/ML Research Scientist at Cyberdyne Systems (no specific years requirement; hires based on demonstrated impact).

V1 scores — Accuracy: 3, Groundedness: 3, Format: 4

**V2:** The roles that accept candidates without a conventional fixed years-of-experience requirement are:

- Hooli: Junior Frontend Developer (no prior experience required)
- Cyberdyne Systems: AI/ML Research Scientist (no specific years requirement listed)

V2 scores — Accuracy: 3, Groundedness: 3, Format: 3

### g016: Compare the experience expectations for the Senior Software Engineer at Acme Corp, Lead DevOps Engineer at Initech, and Senior ML Engineer at Pied Piper.

**Ideal:** Acme Corp requires 5+ years of backend development experience. Initech expects around 6 years of hands-on infrastructure work. Pied Piper typically looks for 7+ years in production ML and distributed systems, while allowing exceptional candidates with less experience.

**V1:** - **Senior Software Engineer at Acme Corp**: Requires 5+ years of backend development experience.
- **Lead DevOps Engineer at Initech**: Expects around 6 years of hands-on infrastructure work.
- **Senior ML Engineer at Pied Piper**: Typically looks for 7+ years in production ML and distributed systems, but exceptional candidates with less experience may be considered.

In summary, the experience expectations are 5+ years for Acme Corp, around 6 years for Initech, and typically 7+ years for Pied Piper, with some flexibility for exceptional candidates.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** The experience expectations are as follows:

- **Senior Software Engineer at Acme Corp**: 5+ years of backend development experience.
- **Lead DevOps Engineer at Initech**: Around 6 years of hands-on infrastructure work expected.
- **Senior ML Engineer at Pied Piper**: Typically looks for 7+ years in production ML and distributed systems, but exceptional candidates with less are welcome. 

In summary, Acme Corp requires 5+ years, Initech expects around 6 years, and Pied Piper typically looks for 7+ years but is flexible for exceptional candidates.

V2 scores — Accuracy: 4, Groundedness: 4, Format: 4

### g017: Which job requirements mention an alternative to a traditional experience requirement?

**Ideal:** Wonka Confectionery Ltd accepts five years of UX research experience or an equivalent portfolio. Stark Industries accepts three to five years in a SOC environment or equivalent. Pied Piper says exceptional candidates with less than its typical 7+ years may be considered. Cyberdyne Systems does not specify years and hires based on demonstrated impact.

**V1:** The job requirements that mention an alternative to a traditional experience requirement are:

- [j06] Pied Piper Inc. for the Senior ML Engineer position, which states that exceptional candidates with less than 7+ years of experience are welcome.
- [j05] Hooli for the Junior Frontend Developer position, which welcomes fresh graduates with no prior experience required.

V1 scores — Accuracy: 2, Groundedness: 2, Format: 3

**V2:** The job requirements that mention an alternative to a traditional experience requirement are:

- [j06] Pied Piper Inc. has an opening for a Senior ML Engineer. They typically look for 7+ years in production ML and distributed systems, but exceptional candidates with less are welcome.
- [j05] Hooli is looking for a Junior Frontend Developer. Fresh grads welcome — no prior experience required.

V2 scores — Accuracy: 2, Groundedness: 2, Format: 3

### g018: If a candidate has fewer than 7 years of production ML experience, does the Pied Piper snippet automatically disqualify them?

**Ideal:** No. Pied Piper typically looks for 7+ years in production ML and distributed systems, but the snippet explicitly says exceptional candidates with less experience are welcome.

**V1:** No, the Pied Piper snippet states that exceptional candidates with less than 7 years of production ML experience are welcome to apply.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** No, the Pied Piper snippet states that exceptional candidates with less than 7 years of production ML experience are welcome.

V2 scores — Accuracy: 4, Groundedness: 4, Format: 4

### g019: What salary range is offered for the Senior Software Engineer position at Acme Corp?

**Ideal:** The provided job snippet does not specify a salary range, so the salary cannot be determined from the available information.

**V1:** The salary range for the Senior Software Engineer position at Acme Corp is not provided in the job requirement context. You may need to check the company's careers page or contact their HR department for specific salary information.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** The salary range for the Senior Software Engineer position at Acme Corp is not provided.

V2 scores — Accuracy: 4, Groundedness: 4, Format: 4

### g020: Does the Cyberdyne Systems AI/ML Research Scientist position guarantee that a candidate with a PhD will be hired?

**Ideal:** No. The snippet says a PhD is preferred but not required, and that Cyberdyne Systems hires based on demonstrated impact. It does not state that having a PhD guarantees hiring.

**V1:** No, having a PhD is preferred but not guaranteed to result in hiring; the focus is on demonstrated impact.

V1 scores — Accuracy: 4, Groundedness: 4, Format: 4

**V2:** No, the position does not guarantee that a candidate with a PhD will be hired. It states that a PhD is preferred but not required.

V2 scores — Accuracy: 4, Groundedness: 4, Format: 4

## Strategy Decision

**Selected strategy: Prompt v1**

Prompt v1 achieved the highest overall score in the pairwise evaluation (3.70 vs. 3.68 for Prompt v2). Accuracy was tied at 3.60, while Prompt v2 achieved better groundedness (3.75 vs. 3.65). Prompt v1 achieved better format scores (3.85 vs. 3.70), resulting in the highest overall average.

Prompt v2 showed a useful advantage on questions where unsupported details could be introduced. For example, g002 improved from 2/2/3 with v1 to 3/4/3 with v2. Therefore, the selected direction is to retain v1's concise answering behavior while carrying forward targeted grounding constraints from v2 where they improve factual support without unnecessarily restricting response quality.
