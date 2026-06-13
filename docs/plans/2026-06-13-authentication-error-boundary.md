# Authentication And Error Boundary

status: planned

## Context

The sparse compatibility contract says that credential handling and error
mapping are not implemented, but its current checklist does not require a
future endpoint to resolve ambiguous credential sources, duplicate
authorization values, sanitized authentication failures, stable error codes,
or upstream error-body boundaries before implementation begins.

## Priorities

1. Require endpoint-specific authentication inputs and precedence before code
   accepts credentials.
2. Define stable client-visible failure classes without copying sensitive
   upstream details.
3. Require deterministic credential-free tests before any runtime surface is
   introduced.

## Requirements

- R1. Define accepted credential locations and reject ambiguous or duplicate
  authorization inputs before forwarding.
- R2. Define missing, malformed, revoked, expired, and insufficient-scope
  behavior separately, including stable status and machine-readable codes.
- R3. Define whether authentication challenge and rate-limit headers are
  generated, translated, passed through, or omitted.
- R4. Prevent credentials, raw authorization values, prompts, files, tool
  arguments, upstream bodies, stack traces, and internal transport details
  from entering client-visible errors or test output.
- R5. Preserve error provenance across client validation, compatibility-layer
  policy, upstream authentication, upstream rate limiting, timeout,
  cancellation, and internal failure classes without exposing sensitive data.
- R6. Define request-correlation behavior and ensure identifiers cannot be
  confused with authentication credentials.
- R7. Require deterministic offline fixtures for duplicate credentials,
  malformed schemes, redaction, stable error codes, and header policy.
- R8. Enforce the policy language and completed evidence through the docs-only
  sparse checker.

## Scope Boundaries

- Do not add a runtime, endpoint, HTTP parser, proxy, adapter, or SDK shim.
- Do not choose a credential scheme, status code, error schema, or header
  behavior for an endpoint that has not been defined.
- Do not add dependencies, live requests, API credentials, or secret fixtures.
- Do not weaken existing request-limit, timeout, retry, observability, model,
  or environment-variable policies.

## Verification Plan

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- run the checker from an external working directory
- parse workflow YAML
- run focused hostile mutations against the authentication/error contract
- `git diff --check`
- scan the intended diff for secrets and generated artifacts
