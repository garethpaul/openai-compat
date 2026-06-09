# Compatibility Versioning Claims Plan

status: completed

## Context

The compatibility contract required endpoint, authentication, error, testing,
and security details, but it did not require versioning rules before future
compatibility claims.

## Objectives

- Add `Versioning And Compatibility Claims` to the contract template.
- Require future compatibility claims to name the implemented version and
  upstream reference.
- Extend the static checker and docs so versioning remains visible.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
