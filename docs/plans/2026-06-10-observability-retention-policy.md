# Observability And Data Retention Policy

status: completed

## Context

The compatibility contract covers request forwarding, credentials, errors,
fixtures, models, and retries, but does not define what a future runtime may
emit or retain for operations. A proxy can leak sensitive payloads through
logs, metrics, traces, or analytics even when request handling itself is sound.

## Objectives

- Add an `Observability And Data Retention` contract section.
- Require an allowlist of event fields and explicit sensitive-data exclusions.
- Require explicit opt-in for debug logging and distributed tracing.
- Require sampling, retention period, storage, access, and deletion rules.
- Require contract tests proving credentials and payload fragments stay out of
  observability output.
- Extend active docs and the sparse baseline for this policy.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
