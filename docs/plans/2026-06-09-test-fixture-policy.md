# Test Fixture Policy Plan

status: completed

## Context

`openai-compat` is still docs-only, but future compatibility behavior will need
fixtures for request, response, error, streaming, authentication, and timeout
cases. Without a fixture policy, compatibility tests could accidentally depend
on live API calls or commit sensitive payloads.

## Objectives

- Add a `Test Fixture Policy` section to the compatibility contract.
- Require sanitized request and response fixtures before implementation.
- Require fixture provenance and a refresh process.
- Require default contract tests to use local fakes with no live API calls.
- Extend the sparse checker and docs so the policy remains visible.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
