# Rate Limit Retry Contract Plan

status: completed

## Context

`openai-compat` has no runtime behavior, but future proxy or SDK-shim work would
need to decide whether upstream throttling is passed through, translated, or
retried. Silent retry behavior can hide 429s, duplicate non-idempotent requests,
or make compatibility claims misleading.

## Objectives

- Add a `Rate Limits And Retries` section to the compatibility contract.
- Require future behavior to define upstream 429 handling and rate-limit header
  treatment.
- Require retryable methods, retry budgets, backoff, jitter, timeout budgets,
  and idempotency-key handling before request forwarding exists.
- Extend the sparse checker and docs so retry semantics stay visible.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
