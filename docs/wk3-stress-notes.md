# W3 Stress Test Notes

## Finding 1 — Malformed JSON

I tested four invalid request bodies against the `/ask` endpoint. All four requests returned HTTP `422 Unprocessable Entity`. The first request with `{}` failed because the required `question` field was missing. The second request using `{"q": "What is the leave policy?"}` also returned `422` because the API expects the field name `question`. The third request using `{"question": 42}` returned `422` because `question` must be a string. The fourth request contained malformed JSON and returned `422` with a `json_invalid` error. None of these invalid requests reached the application endpoint handler; FastAPI/Pydantic validation rejected them before the `/ask` application code executed. The recorded responses confirm the first two validation failures and the malformed JSON failure. 

## Finding 2 — 5000-character question

I tested a long question generated to approximately 5,000 characters. The actual measured length was 5,200 characters. The `/ask` request completed successfully with a total wall time of approximately 2.09 seconds (`real 0m2.087s`). A response was streamed back to the client, demonstrating that streaming worked. No token-limit error was observed during this test. The response was a simulated answer, so this test verified the API streaming behavior rather than a real LLM token-limit boundary. :contentReference[oaicite:1]{index=1}

## Finding 3 — Disconnect mid-stream

I tested a client disconnect using `curl --max-time 1 -N` against `/ask`. The client received approximately 52 bytes before curl terminated with `curl: (28) Operation timed out after 1000 milliseconds`. This confirms that the client disconnected while the response was being streamed. I then checked the `/health` endpoint after the disconnect and the server remained available, indicating that the API process continued running. The server-side log output for the disconnect was not captured in the recorded terminal output, so no specific server log message is claimed here. :contentReference[oaicite:2]{index=2}

## Finding 4 — 50 parallel requests

I ran the stress test with 50 requests and up to 10 concurrent requests. The final successful run completed all `50 / 50` requests successfully. Total wall time was `8.51s`, with an effective throughput of `5.87 requests/second`. Successful-request latency was `p50 = 1.44s` and `p95 = 1.90s` (maximum `1.98s`). SQLite did not capture these 50 API requests: the `answers` table remained at 360 total rows, and the query for rows written during the previous five minutes returned `0`. The existing SQLite rows were from an earlier pipeline run, with the latest recorded timestamp being August 22, rather than the August 29 stress test. :contentReference[oaicite:3]{index=3} :contentReference[oaicite:4]{index=4}

## Known limits / follow-ups

The current W3 API successfully validates requests, streams responses, and handles concurrent requests, but the API `/ask` path does not currently persist each HTTP response into the SQLite `answers` table. SQLite persistence is currently performed by the batch pipeline execution rather than by the FastAPI `/ask` endpoint. Token-limit handling should be improved for production use, and SQLite write coverage should be added to the API path if request-level persistence is required. Cost tracking should also be verified and improved when moving from the simulated/fake pipeline behavior to the production LLM implementation.