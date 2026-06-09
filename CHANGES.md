# Changes

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
