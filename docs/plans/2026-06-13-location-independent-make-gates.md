# Location-Independent Make Gates

status: planned

## Context

The standard Make aliases pass when invoked from the repository root, but a
caller using `make -f /path/to/openai-compat/Makefile check` from another
working directory resolves `scripts/check-baseline.py` relative to the caller
and fails before the sparse baseline can run. Shared automation should be able
to invoke the repository's Makefile without first changing directories.

## Requirements

- Resolve checker paths from the directory containing `Makefile`, independent
  of the caller's working directory.
- Keep `lint`, `test`, `build`, `verify`, and `check` on the same dependency-free
  sparse baseline.
- Preserve `PYTHON`, `PYTHONDONTWRITEBYTECODE`, and the existing tracked-file
  allowlist boundary.
- Statically reject a return to caller-relative checker execution.
- Document completed root and external-working-directory verification.

## Scope Boundaries

- Do not add dependencies, runtime code, endpoints, network access, or
  credential behavior.
- Do not change the compatibility, authentication, error, timeout, retry,
  observability, or request-resource policies.
- Do not weaken the sparse tracked-file allowlist or hosted validation.

## Implementation Units

1. Update `Makefile` to derive a stable repository root and invoke the checker
   through that root for every standard alias.
2. Extend `scripts/check-baseline.py` so the rooted Make contract, this plan,
   and completed verification evidence remain required.
3. Record the maintenance behavior in `README.md` and `CHANGES.md`.

## Verification Plan

- Run every standard Make alias from the repository root.
- Run every standard Make alias through the absolute Makefile path from an
  external working directory.
- Parse the pinned workflow YAML and run focused hostile mutations against the
  rooted Make and completed-plan contracts.
- Audit the intended diff for whitespace errors, generated artifacts, and
  secret-like material.
