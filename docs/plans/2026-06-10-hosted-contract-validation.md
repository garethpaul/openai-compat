# Hosted Contract Validation

status: completed

## Context

The repository deliberately contains a docs-only compatibility contract and a
sparse allowlist, but no hosted validation enforces that status. A future
tracked runtime file or weakened contract could otherwise land without running
the local baseline.

## Priorities

1. Run the canonical sparse contract gate for pushes and pull requests.
2. Pin workflow actions, Python, permissions, runner, timeout, and concurrency.
3. Keep validation dependency-free and free of API credentials or live calls.
4. Require the hosted workflow contract from `scripts/check-baseline.py`.
5. Preserve the explicit no-runtime and no-compatibility-claim baseline.

## Implementation Units

Files:

- `.github/workflows/check.yml`
- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`

Add a commit-pinned, read-only Python 3.10/3.12 matrix on `ubuntu-24.04` that
runs `make check` with credential persistence disabled. Extend the sparse
allowlist and checker so the workflow and this plan are required tracked
surfaces with an enforced configuration.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- workflow YAML parse
- `git diff --check`
- successful hosted Linux `Check` workflow for the pushed commit

## Boundaries

- Do not add runtime compatibility behavior.
- Do not add dependencies, API credentials, or live OpenAI requests.
- Do not claim endpoint, model, or SDK compatibility.
