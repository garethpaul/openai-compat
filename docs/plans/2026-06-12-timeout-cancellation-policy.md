# Timeout And Cancellation Policy

status: completed

## Context

The compatibility contract mentions timeout budgets under retries and requires
timeouts for network calls, but it does not define cancellation propagation,
streaming idle deadlines, cleanup, or which timeout phases future runtime code
must specify. That leaves room for an implementation to retry within a nominal
budget while still holding disconnected or stalled requests open.

## Priority

An OpenAI-compatible adapter would sit on a network boundary and may handle
long-lived streams. Explicit timeout and cancellation behavior is required
before implementation to prevent resource exhaustion, abandoned upstream work,
and inconsistent client-visible failures.

## Prioritized Engineering Backlog

1. Require a complete timeout and cancellation policy before runtime work.
2. Add deterministic cancellation and stalled-stream fixtures with the first
   transport implementation.
3. Add runtime metrics for timeout phase and cancellation source without
   recording prompts, credentials, or response bodies.

## Requirements

- R1. Define connect, response-header, overall request, and streaming idle
  timeout budgets.
- R2. Require retries to consume one overall deadline rather than resetting the
  timeout for each attempt.
- R3. Propagate client disconnects and cancellations to upstream work.
- R4. Define cleanup for response bodies, streams, tasks, sockets, and temporary
  resources after timeout or cancellation.
- R5. Define stable, sanitized client-visible timeout and cancellation errors.
- R6. Require deterministic tests with fake clocks or local fixtures and no live
  API calls.
- R7. Enforce the policy language through the docs-only sparse baseline.

## Scope Boundaries

- Do not add a runtime, HTTP client, proxy, adapter, or SDK shim.
- Do not define numeric timeout defaults before a transport and workload exist.
- Do not change the existing retry, credential, or observability policies.
- Do not add dependencies.

## Verification

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`

## Work Completed

- Added a dedicated timeout and cancellation section to the compatibility
  contract.
- Required phase-specific budgets, one deadline across retries, disconnect and
  cancellation propagation, resource cleanup, sanitized errors, and offline
  deterministic tests.
- Updated README, security guidance, vision, and change history.
- Extended the sparse baseline to require the policy language and completed
  plan before any runtime surface is added.
