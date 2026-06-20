# Checkout Credential Boundary

status: completed

## Context

The exact evidence head still uses the checkout action's default credential
persistence. The docs-only sparse hosted job only needs read access to tracked
repository contents.

## Objectives

- Disable checkout credential persistence without adding runtime behavior.
- Enforce one workflow, one read-only permission block, one checkout action,
  and one correctly nested non-persisted credential declaration.
- Preserve the sparse tracked-file allowlist, immutable action pins, Python
  3.12, Ubuntu 24.04, timeout, concurrency, and `make check`.
- Correct documentation to match the exact workflow.

## Implementation Units

### Workflow And Checker

Files: `.github/workflows/check.yml` and `scripts/check-baseline.py`.

Add the checkout boundary, admit this plan to the sparse allowlist, and reject
duplicate workflows, permissions, checkout actions, write scopes, misplaced or
contradictory settings, and incomplete plan evidence.

### Documentation

Files: `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`, and this plan.

Record the shorter credential lifetime without weakening the docs-only
compatibility contract.

## Work Completed

- Added `persist-credentials: false` beneath the sole pinned checkout step.
- Added the plan to the sparse tracked-file allowlist and enforced exact
  workflow, permission, checkout, nesting, contradiction, and plan evidence.
- Updated hosted-validation documentation without adding runtime behavior,
  dependencies, endpoints, credential reads, or compatibility claims.

## Verification Completed

- `python3 scripts/check-baseline.py`
- `make lint`, `make test`, `make build`, and `make check`
- workflow YAML parse and `git diff --check`
- Hostile workflow and plan mutations

The local checks remain docs-only, dependency-free, and offline. Canonical
hosted push and pull-request checks remain required at the exact successor head
before owner merge.

## Boundaries

- Do not add application code, dependencies, endpoints, API calls, credential
  reads, request forwarding, compatibility claims, or live tests.
- Preserve every existing contract and policy document.
- Preserve the existing remediation PR and exact evidence.
