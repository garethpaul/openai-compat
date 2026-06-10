## OpenAI Compat Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

OpenAI Compat is currently a sparse repository with security metadata but no
documented implementation. It is a docs-only placeholder, not a runtime,
adapter, SDK shim, or proxy.

The repository should be treated as a placeholder or archive until its intended
compatibility target, runtime surface, and tests are documented. The first
useful contribution is clarity.

The goal is to prevent accidental assumptions about API behavior while leaving a
clear path to turn the repository into a maintained compatibility project if
that becomes useful.

Current baseline: `make lint`, `make test`, `make build`, and `make check`
verify that the repository remains a sparse placeholder with no implementation
files until a compatibility contract and contract tests are added. The required
contract template lives at
[`docs/compatibility-contract.md`](docs/compatibility-contract.md).

The current focus is:

Priority:

- Preserve the repository and security-reporting metadata
- Document the intended compatibility scope before adding code
- Avoid naming specific API guarantees that are not implemented
- Keep the default branch clean and easy to inspect
- Keep placeholder verification available through `make check`
- Keep `make lint`, `make test`, `make build`, and `make check` on the
  SDK-free sparse baseline
- Link future API behavior claims to official OpenAI documentation and local
  contract tests.
- Keep compatibility non-goals explicit until tests prove implemented behavior
- Keep versioning requirements explicit before compatibility claims are made
- Keep documentation evidence explicit before endpoint behavior is advertised
- Keep test fixture policy explicit before compatibility tests are added
- Keep rate limits and retries explicit before request forwarding exists
- Keep model mapping policy explicit before model identifiers or aliases are
  accepted
- Keep environment-variable credential policy explicit before code reads
  process environment credentials
- Keep verification workspaces free of generated Python bytecode
- Keep the docs-only compatibility contract enforced in pinned, read-only
  hosted Linux CI

Next priorities:

- Add a README that defines the compatibility target and non-goals
- Fill in `docs/compatibility-contract.md` with a concrete endpoint contract
- Choose a language, package shape, and test strategy
- Add contract tests before any adapter implementation
- Define the compatibility contract before introducing request forwarding
- Document supported authentication and error-handling behavior
- Record official documentation evidence and review dates before implementation
- Define sanitized fixture provenance before implementation
- Define rate-limit, retry, timeout, and idempotency-key behavior before
  forwarding requests
- Define model mapping, aliasing, unsupported-model behavior, and silent
  fallback rules before accepting model identifiers
- Define accepted credential variables, credential source precedence, and
  environment isolation tests before reading process environment credentials
- Convert non-goals into tested contracts only when implementation exists

Contribution rules:

- One PR = one focused documentation, contract, or implementation change.
- Start with tests for any compatibility promise.
- Keep `make lint`, `make test`, `make build`, and `make check` passing while
  the repository remains docs-only.
- Keep examples free of secrets.
- Document unsupported behavior explicitly.
- Document rate limits and retries before adding proxy behavior.
- Document environment-variable credential behavior before reading API-key-like
  values from process state.
- Preserve the Python bytecode guard when changing sparse verification.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Compatibility layers can accidentally leak credentials, proxy sensitive
payloads, or mask API errors. Any future implementation should make request
paths, logging, and credential handling explicit.

## What We Will Not Merge (For Now)

- Unspecified proxy behavior
- Credential logging or opaque request forwarding
- Broad SDK shims without contract tests
- Claims of drop-in compatibility before behavior is documented

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
