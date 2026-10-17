# PII Stress-Test Findings — Week 8

## 1. Objective

Evaluate the default Presidio Analyzer against the adversarial corpus
at `W8_Gorthi/data/stress_test/pii_adversarial.md`.

## 2. Baseline execution

- Analyzer: Presidio AnalyzerEngine with default English configuration
- Input length: 1,619 characters
- Detection count: 43
- Anonymization: Not performed in this baseline script
- Corpus modified: No

## 3. Observations from the actual run

### Names
Several full names were detected as PERSON. Some mentions were
detected only as first names. The name `alice` was detected as PERSON,
but this did not identify its surrounding obfuscated email address.

### Email addresses
The obfuscated forms `alice [at] example [dot] com`,
`bob.smith ＠ example ．com`, and `y.tanaka(at)hospital(dot)org`
were not detected as complete email addresses.

### Phone numbers
`+81 (0) 3 1234 5678` was detected as PHONE_NUMBER with score 0.75.
`91-22-2570-1234 ext. 4501` and
`4 0 4 . 5 5 5 . 0 1 8 2` were detected with score 0.40.
The spelled-out phone number was not detected as a complete phone number.
The UK number was not detected in the recorded output.

### Employee identifiers
The output did not identify EMP-04827, Staff #4082,
RJP/2019/0451, or A.M.-2021-EUR-007 as complete employee identifiers.
CM18234 was classified as US_DRIVER_LICENSE with score 0.30,
which is a questionable classification for this corpus.

### Addresses
Some location and street fragments were detected, but complete
address coverage was inconsistent. A location detection alone does
not prove the full address was identified.

### Financial data
The IBAN was detected as IBAN_CODE with score 1.00.
The masked card number was not detected.
The project budget code was not detected as PII in this run.

### Questionable detections
The output included `European` as NRP, `Japanese` as NRP,
`0 4` as DATE_TIME, and `5698` as DATE_TIME. These should be reviewed
as potential false positives in this corpus.

## 4. Proposed improvements

1. Normalize common obfuscated email forms before detection, including
   bracketed words and full-width punctuation. Preserve an audit trail.
2. Add explicit recognizers for the employee ID formats used by the
   organization, with context-aware validation.
3. Normalize digit-spaced and spelled-out phone numbers before detection.
4. Add address-specific validation or a dedicated address-recognition
   strategy appropriate to the countries in scope.
5. Add a recognizer for masked payment-card patterns where appropriate.
6. Review false positives and tune thresholds only after measuring
   both missed detections and incorrect detections.

## 5. Limitations

This is one baseline run on one synthetic adversarial document.
The detection count is not a precision or recall score. Detection
does not prove successful anonymization, and missing output entries
do not prove that every unlisted value is safe to retain.

## 6. Next steps

Implement one targeted improvement, rerun the same corpus, and compare
the results against this baseline. Do not send this stress-test corpus
to the Week 8 Qdrant collection.
EOFmkdir -p docs/adr

cat > docs/adr/pii_stress_test_findings.md <<'EOF'
# PII Stress-Test Findings — Week 8

## 1. Objective

Evaluate the default Presidio Analyzer against the adversarial corpus
at `W8_Gorthi/data/stress_test/pii_adversarial.md`.

## 2. Baseline execution

- Analyzer: Presidio AnalyzerEngine with default English configuration
- Input length: 1,619 characters
- Detection count: 43
- Anonymization: Not performed in this baseline script
- Corpus modified: No

## 3. Observations from the actual run

### Names
Several full names were detected as PERSON. Some mentions were
detected only as first names. The name `alice` was detected as PERSON,
but this did not identify its surrounding obfuscated email address.

### Email addresses
The obfuscated forms `alice [at] example [dot] com`,
`bob.smith ＠ example ．com`, and `y.tanaka(at)hospital(dot)org`
were not detected as complete email addresses.

### Phone numbers
`+81 (0) 3 1234 5678` was detected as PHONE_NUMBER with score 0.75.
`91-22-2570-1234 ext. 4501` and
`4 0 4 . 5 5 5 . 0 1 8 2` were detected with score 0.40.
The spelled-out phone number was not detected as a complete phone number.
The UK number was not detected in the recorded output.

### Employee identifiers
The output did not identify EMP-04827, Staff #4082,
RJP/2019/0451, or A.M.-2021-EUR-007 as complete employee identifiers.
CM18234 was classified as US_DRIVER_LICENSE with score 0.30,
which is a questionable classification for this corpus.

### Addresses
Some location and street fragments were detected, but complete
address coverage was inconsistent. A location detection alone does
not prove the full address was identified.

### Financial data
The IBAN was detected as IBAN_CODE with score 1.00.
The masked card number was not detected.
The project budget code was not detected as PII in this run.

### Questionable detections
The output included `European` as NRP, `Japanese` as NRP,
`0 4` as DATE_TIME, and `5698` as DATE_TIME. These should be reviewed
as potential false positives in this corpus.

## 4. Proposed improvements

1. Normalize common obfuscated email forms before detection, including
   bracketed words and full-width punctuation. Preserve an audit trail.
2. Add explicit recognizers for the employee ID formats used by the
   organization, with context-aware validation.
3. Normalize digit-spaced and spelled-out phone numbers before detection.
4. Add address-specific validation or a dedicated address-recognition
   strategy appropriate to the countries in scope.
5. Add a recognizer for masked payment-card patterns where appropriate.
6. Review false positives and tune thresholds only after measuring
   both missed detections and incorrect detections.

## 5. Limitations

This is one baseline run on one synthetic adversarial document.
The detection count is not a precision or recall score. Detection
does not prove successful anonymization, and missing output entries
do not prove that every unlisted value is safe to retain.

## 6. Next steps

Implement one targeted improvement, rerun the same corpus, and compare
the results against this baseline. Do not send this stress-test corpus
to the Week 8 Qdrant collection.

## 7. Improvement experiment: obfuscated emails

### Method
Created `W8_Gorthi/src/normalize_obfuscated_emails.py` to normalize
bracketed/parenthesized "at" and "dot", full-width punctuation, and
whitespace around email punctuation before Presidio analysis.

### Actual result
The baseline produced no complete EMAIL_ADDRESS detections for the
three obfuscated email forms. After normalization, Presidio detected:

- alice@example.com — score 1.00
- bob.smith@example.com — score 1.00
- y.tanaka@hospital.org — score 1.00

Result: 3 of 3 test email forms were detected after normalization.

### Limitation
This result applies to these three synthetic examples only. The
normalization helper is not a complete email-obfuscation solution.
The source corpus was not modified, and the normalized text was tested
for detection, not anonymized or uploaded to Qdrant.

## 8. Improvement experiment: employee identifiers

### Method
Created `W8_Gorthi/src/test_employee_ids.py` to test five targeted
regular expressions, then `W8_Gorthi/src/test_employee_ids_presidio.py`
to register them as a custom Presidio PatternRecognizer with entity
type EMPLOYEE_ID.

### Actual result
Standalone regex test: 5 of 5 expected formats matched.
Presidio integration test: 5 of 5 expected formats detected,
each with score 0.90.

The detected values were EMP-04827, Staff #4082, RJP/2019/0451,
A.M.-2021-EUR-007, and Badge: CM18234.

### Limitation
These patterns are tailored to the five formats in this synthetic
corpus. They have not been validated against a representative
production dataset, and this detection test did not anonymize values.
The custom recognizer is currently registered only by the test script;
it has not been added to the main ingestion pipeline.

## 9. Employee-ID anonymization validation

### Actual result
The Presidio integration test detected five employee identifiers.
The anonymization test replaced all five values with `<EMPLOYEE_ID>`.
A post-anonymization check confirmed that each original identifier
was absent from the anonymized output.

Result: 5 of 5 identifiers detected and 5 of 5 removed in this test.

### Limitation
This validates the five sample formats only. Other identifiers,
unrecognized variants, and sensitive context surrounding an identifier
may remain. The test anonymizes the employee-ID matches only; it does
not demonstrate complete PII anonymization of the entire document.
