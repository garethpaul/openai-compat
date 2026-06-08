# OpenAI Compat Baseline Plan

status: completed

## Context

`openai-compat` is currently a sparse placeholder repository. It has project
docs and security metadata, but no implementation, package manifest, runtime
entry point, compatibility contract, or contract tests.

## Risks

- The repository name implies API compatibility behavior that is not
  implemented.
- Future code could introduce proxying, credential handling, request logging,
  or SDK shim behavior before the compatibility contract is documented.
- There was no local verification command for the sparse baseline.

## Work Completed

- Added `make check` and `scripts/check-baseline.py` to verify the current
  sparse repository shape.
- Added ignore rules for secrets, logs, generated build output, dependency
  directories, and test caches.
- Updated docs to state that there is no implementation yet and that future
  compatibility claims need contract tests.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
