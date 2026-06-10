# Environment Variable Credential Policy

status: completed

## Context

`openai-compat` has no runtime behavior, but future proxy or SDK-shim work may
try to read credentials from process environment variables. Without a policy,
local developer state could silently affect contract tests or leak into logs,
fixtures, and error messages.

## Objectives

- Add an `Environment Variable Credential Policy` section to the compatibility
  contract.
- Require future work to define accepted credential variables and credential
  source precedence before reading process environment state.
- Require explicit automatic-read behavior, redaction rules, and isolated tests
  that clear and restore credential-like environment variables.
- Extend the sparse checker and docs so the credential policy stays visible.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
