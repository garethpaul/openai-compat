# Model Mapping Policy

status: completed

## Context

`openai-compat` has no runtime behavior, but future compatibility work could
accidentally accept model names, aliases, or defaults without documenting what
they mean. Silent model fallback would make compatibility claims hard to audit.

## Objectives

- Add a `Model Mapping Policy` section to the compatibility contract.
- Require future work to define accepted model identifiers and aliases.
- Require unsupported-model behavior and silent fallback rules before runtime
  behavior exists.
- Extend the sparse checker and docs so model mapping stays visible.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
