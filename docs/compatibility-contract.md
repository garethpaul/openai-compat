# Compatibility Contract

Status: no compatibility behavior is implemented.

This document is the required starting point for any future OpenAI-compatible
proxy, SDK shim, adapter, or test fixture. A change must update this contract
before it claims compatibility with any endpoint, request shape, response
shape, model behavior, error behavior, or authentication flow.

## Supported Endpoints

No endpoints are supported yet.

Before implementation, define each endpoint with:

- upstream endpoint or SDK method being emulated
- supported request fields and intentionally unsupported fields
- response fields returned unchanged, translated, or omitted
- streaming behavior, including chunk shape and termination behavior
- timeout, retry, and rate-limit behavior
- compatibility tests that prove the behavior

## Non-Goals Until Implemented

Until a specific endpoint contract and tests exist, this repository does not
claim support for:

- drop-in API or SDK compatibility
- live upstream request forwarding
- credential exchange, persistence, or proxy-managed API keys
- request or response retention, analytics, tracing, or replay
- streaming, file uploads, fine-tuning, batch jobs, or webhook behavior
- model equivalence, pricing equivalence, latency equivalence, or quota
  equivalence

## Authentication And Credential Handling

No credential handling is implemented yet.

Before implementation, define:

- accepted credential sources, such as headers or local environment variables
- whether credentials are passed through, transformed, or exchanged
- redaction rules for logs, errors, fixtures, and test output
- whether credentials are ever persisted
- behavior for missing, malformed, revoked, or unauthorized credentials

## Request And Response Handling

No request forwarding, request storage, response translation, or response
caching is implemented yet.

Before implementation, define:

- how request bodies are validated before forwarding or translation
- payload size limits
- whether prompts, messages, files, or metadata are stored
- response normalization rules
- behavior for partial upstream failures and retries

## Error Mapping

No error mapping is implemented yet.

Before implementation, define:

- upstream errors that pass through unchanged
- errors translated into compatibility-layer responses
- HTTP status codes or SDK exceptions used for each class of failure
- retryable versus non-retryable failures
- redaction behavior for error bodies

## Versioning And Compatibility Claims

No versioned compatibility target is declared yet.

Before implementation, define:

- package, API, or service version that introduces each compatibility claim
- upstream API or SDK version, date, and official documentation reference used
  for the contract
- compatibility matrix for supported endpoints and intentionally unsupported
  fields
- deprecation policy for changed request shapes, response shapes, or error
  mappings
- release notes that distinguish docs-only placeholders from implemented
  behavior

## Documentation Evidence

No official-documentation evidence is recorded yet.

Before implementation, record:

- official documentation URL or SDK reference used for each endpoint contract
- date reviewed and upstream API or SDK version target
- unsupported fields observed in the upstream docs
- local fixture or contract test that proves each documented behavior
- owner responsible for refreshing the evidence when upstream docs change

## Contract Tests

No compatibility behavior may be added without tests that cover:

- one success path for every supported endpoint
- unsupported field rejection or pass-through behavior
- authentication failure behavior
- upstream error mapping
- timeout or retry behavior when implemented
- redaction of credentials and sensitive payload fragments

Tests should use sanitized fixtures or local fakes. They should not call a live
API by default.

## Security Checklist

Before merging compatibility behavior, verify:

- API keys and bearer tokens are never committed, logged, or captured in
  fixtures
- request payloads are not persisted unless the contract explicitly says so
- logs redact credentials and sensitive payload fragments
- generated caches, traces, and recordings are ignored by git
- timeouts exist for all network calls
- compatibility claims in README and package metadata match tested behavior
