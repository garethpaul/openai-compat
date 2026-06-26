# Changes

## 2026-06-26 13:57:32 PDT - P1 - Make repository verification authoritative

### Summary

Closed a false-green verification boundary where a later `-f` Makefile could
replace public leaf recipes, or GNU Make execution modes could suppress or
ignore the repository-owned policy commands.

### Work completed

- Converted public targets to guarded double-colon rules with a repository
  authority prerequisite.
- Rejected later single-colon replacement, later double-colon append,
  preloaded Makefiles, caller `MAKEFLAGS`, and ten non-executing or
  error-ignoring modes.
- Replaced dry-run-only root assertions with live minimal-fixture executions.
- Extended the sparse baseline and hostile repository-policy regressions.

### Threads

- None; the focused Make authority work was completed directly.

### Files changed

- `Makefile` — own public target execution and reject unsafe invocation modes.
- `tests/test_makefile_root.py` and `tests/test_repository_policy.py` — cover
  replacement, append, mode, override, live path, and policy mutation behavior.
- `scripts/check-baseline.py` — freeze the reviewed authority boundary and its
  completed evidence.
- `README.md`, `SECURITY.md`, `VISION.md`, `AGENTS.md`, and
  `docs/plans/2026-06-26-make-invocation-authority.md` — document behavior and
  evidence.

### Validation

- Full sparse baseline, repository-policy, Make authority, external-directory,
  Python compilation, and diff checks — recorded in the completed plan.

### Bugs / findings

- Fixed P1 false-green verification through later Makefile recipe replacement.
- Fixed P1 false-green verification through dry-run, touch, question, and
  ignore-error modes.
- No runtime compatibility behavior, model mapping, API schema, credential
  handling, or network semantics changed.

### Blockers

- Codex review authentication is unavailable in this environment; attempt it
  once after the pull request is open, then rely on local and hosted gates.

### Next action

- Merge only the exact hosted-green pull-request head, then continue repository
  triage.

## 2026-06-21

- Made absolute Makefile verification safe for spaces and apostrophes,
  ignored caller-provided `REPO_ROOT` values, and rejected command-line or
  environment `MAKEFILE_LIST` injection before sparse contract checks run.
- Added root-policy regressions for every public Make target.

- Deep-reviewed and consolidated the sparse compatibility contract: added
  hostile repository-policy tests, required exact OpenAI-compatible route,
  error-envelope, and SSE termination definitions before implementation, and
  hardened file type, size, sparse-surface, workflow, and location-independent
  verification boundaries.

## 2026-06-13

- Made every standard Make gate resolve the sparse checker from the repository
  root, including absolute-Makefile invocations from external directories.
- Added a required authentication and error boundary covering ambiguous or
  duplicate credential inputs, separate authentication failure classes,
  header policy, stable error provenance and codes, redaction, correlation,
  and deterministic offline fixtures.

## 2026-06-12

- Disabled checkout credential persistence in the pinned, read-only hosted
  validation job and added structural checks for that boundary.
- Added a required timeout and cancellation policy covering phase-specific
  deadlines, one overall retry budget, client disconnect propagation, cleanup,
  sanitized errors, and deterministic offline tests.
- Extended the sparse baseline to prevent the policy or completed plan from
  being removed before runtime work begins.
- Added a required request validation and resource-limits policy covering media
  types, content encodings, wire and decompressed bounds, incremental reads,
  structural JSON limits, sanitized errors, cleanup, and offline tests.

## 2026-06-10

- Added Python 3.10+ PEP 621 runtime metadata for the documentation-only
  compatibility contract without claiming an implemented client, marked it
  `Private :: Do Not Upload`, and added hosted Python 3.10/3.12 verification.
- Added an environment-variable credential policy requirement before future
  compatibility code reads API-key-like process state.
- Added pinned, read-only hosted Linux validation for the docs-only sparse
  compatibility contract.
- Added an observability and data-retention policy requirement before future
  logging, metrics, tracing, analytics, or payload retention behavior.

## 2026-06-08

- Added a sparse placeholder baseline for `openai-compat`.
- Added `make check` static verification.
- Added local ignore rules for secrets, logs, generated outputs, dependency
  folders, and test caches.
- Documented that compatibility behavior requires a written contract and
  contract tests before implementation.
- Added `docs/compatibility-contract.md` as the required endpoint,
  authentication, error-mapping, testing, and security checklist for future
  compatibility behavior.
- Clarified that the current repository has no runtime, proxy, API adapter, SDK
  shim, credential-handling behavior, or compatibility guarantee.
- Added explicit compatibility non-goals for unimplemented forwarding,
  credential exchange, retention, streaming, file, fine-tuning, batch, webhook,
  and model-equivalence behavior.
- Tightened future guardrails for request logging, payload retention, error
  propagation, and official-doc-backed contract tests.
- Added versioning requirements before future compatibility claims can be made.
- Added documentation-evidence requirements before future endpoint behavior can
  be advertised.
- Added a test fixture policy requirement for sanitized fixtures and no live API
  calls by default.
- Added rate-limit and retry contract requirements before future request
  forwarding behavior.
- Added model mapping policy requirements before future model identifiers,
  aliases, or fallback behavior.
- Added `make lint`, `make test`, and `make build` aliases so the standard
  gate commands run the same SDK-free sparse baseline as `make check`.
- Added a Python bytecode guard so sparse verification catches leftover local
  `__pycache__` or `.pyc` output.
