# Compatibility Non-Goals

status: completed

## Context

`openai-compat` is a docs-only placeholder. The compatibility contract already
defines sections that future implementation work must fill in, but it did not
explicitly list behaviors that are unsupported until an endpoint contract and
tests exist.

## Objectives

- Add a `Non-Goals Until Implemented` section to the compatibility contract.
- Clarify that API or SDK compatibility, forwarding, credential exchange,
  retention, streaming, file uploads, fine-tuning, batch jobs, webhooks, and
  model-equivalence behavior are not supported by implication.
- Extend the sparse checker and docs so non-goals remain visible.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
