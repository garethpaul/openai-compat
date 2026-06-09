# Documentation Evidence Guard

status: completed

## Context

`openai-compat` can only make useful compatibility claims if each claim is tied
to a specific upstream documentation source, review date, and local contract
test. The existing contract required official-document-backed tests, but it did
not spell out the evidence future contributors need to record before adding
runtime behavior.

## Objectives

- Add a `Documentation Evidence` section to the compatibility contract.
- Require future endpoint work to record official documentation sources, review
  dates, upstream version targets, unsupported fields, local fixtures, and an
  evidence owner.
- Extend the static baseline so the evidence requirement remains visible while
  the repository stays docs-only.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
