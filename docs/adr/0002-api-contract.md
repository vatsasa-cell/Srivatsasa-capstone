# ADR 0002 — /ask API Contract

**Status:** Locked from Week 3.

**Defended at:** Design Review #1 (Week 5).

**Owners:** *Srivatsasa Gorthi*

**Date:** *2026-08-29*

## Context

By end of W3 the capstone has a FastAPI service for an Enterprise Knowledge
Assistant. The API provides a stable interface for submitting questions and
receiving generated answers, while the underlying W2 pipeline can evolve in
later weeks with different models, retrieval, reranking, and agent capabilities.

The service's HTTP surface needs to remain stable so that the Streamlit UI,
evaluation harness, and future consumers do not need to change when the
answer-generation internals change.

This ADR locks the v1 API contract for `/ask`, `/ask_batched`, and `/health`.

## Decision

### Endpoint: `POST /ask`

**Request body (`Question`):**

| Field    | Type | Required | Notes              |
|----------|------|:--------:|--------------------|
| question | str  | Yes      | Free-text question. |

**Response:** streamed `text/plain`. The W3 API obtains the complete answer
from the underlying pipeline and then streams the answer word-by-word to the
client. The complete response, if every chunk is concatenated, is the full
answer.

### Endpoint: `POST /ask_batched`

Same input contract as `/ask`. Returns the full `Answer` body (JSON) without
streaming. Used for testing and for callers that cannot consume streams.

**Response body (`Answer`):**

| Field     | Type  | Required | Notes |
|-----------|-------|:--------:|-------|
| content   | str   | Yes      | The generated answer. |
| cost_usd  | float | Yes      | Cost of this call. Placeholder in W3; real in W4. |
| retries   | int   | Yes      | Number of retries that fired in this call. |

**Internal note:** The W2 pipeline uses `text` as the field name for both the
internal `Question` and `Answer` models. The `/ask` and `/ask_batched` handlers
translate the public `question` field into the internal `Question(text=...)`
model and translate the internal answer back to the public `Answer` contract.
This separation allows the internal pipeline to change without breaking the
public API contract.

### Endpoint: `GET /health`

Returns `{"status": "ok"}` with HTTP 200 when the service is alive.

### Error responses

- `422 Unprocessable Entity` — request fails Pydantic validation. Body follows
  FastAPI's default `{"detail": [...]}` shape.

- `5xx` — upstream LLM provider errors after retry budget is exhausted. Body is
  a JSON `{"detail": "..."}` with a short error message.

## Versioning Rule

- `/ask` is locked from Week 3.

- **Don't bump** for additive changes:
  - New optional fields on Answer
  - Internal model swaps
  - Logging / observability changes
  - Retry-policy tweaks
  - Internal prompt edits

- **Do bump to `/v2/ask`** for breaking changes:
  - Field removal or rename on the public shape (Question, Answer)
  - Type change on a public field
  - Required ↔ optional change
  - Semantic change to a field's meaning
  - Change to the error-response shape

- When `/v2/ask` ships, `/ask` runs in parallel for **at least 2 weeks**
  before retirement; consumers get an `X-Deprecation` warning header.

- Schema versioning on the response body lands in W4 (`schema_version` field
  added to `Answer`). The endpoint contract is separate from the body schema.

## Consequences

- **Positive.** The Streamlit UI, the W5 eval harness, and any later consumer
  integrate once. W4 → W30 internal changes happen behind the contract.

- **Negative.** We commit to maintaining `/ask` even when its internals become
  legacy. Acceptable cost.

- **Open.** Authentication is out of scope for v1. When we layer it in W28/W29
  it will require an `Authorization` header but won't change the request or
  response shape itself.

## Tests securing this contract

- `tests/test_api.py::test_ask_rejects_missing_question` — validation contract.

- `tests/test_api.py::test_health_returns_ok` — /health contract.

- *_(In W4)_* `tests/test_contract.py` — snapshot-test the `/openapi.json` to
  detect accidental contract breakage in CI.