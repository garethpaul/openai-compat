# Request Validation And Resource Limits

status: planned

## Context

The compatibility contract requires request validation and payload size limits,
but it does not define which resource dimensions a future proxy must bound.
Checking only `Content-Length` or a raw compressed body can still allow chunked
overruns, decompression bombs, deeply nested JSON, oversized strings or arrays,
and unsupported media types to consume memory or parser time before forwarding.

## Priority

An OpenAI-compatible boundary would accept attacker-controlled structured and
potentially streamed input. Validation must fail before upstream forwarding,
credential use, persistence, or expensive parsing, with stable errors that do
not echo private request content.

## Prioritized Engineering Backlog

1. Require endpoint-specific request validation and resource limits before
   runtime work.
2. Add incremental parser and decompression fixtures with the first transport.
3. Add bounded metrics for rejection reason and observed size without recording
   request bodies or sensitive field values.

## Requirements

- R1. Define accepted HTTP methods, media types, character encodings, and
  content encodings for every endpoint.
- R2. Define separate wire-byte and decompressed-byte limits, including
  chunked or missing-length requests.
- R3. Require incremental reads that stop as soon as a limit is exceeded and
  clean up partially read bodies or temporary files.
- R4. Define JSON nesting, object, array, string, and field-count limits where
  structured input is accepted.
- R5. Define unknown-field, duplicate-key, malformed-body, and schema-mismatch
  behavior before forwarding.
- R6. Define stable sanitized `400`, `413`, and `415` responses that never echo
  credentials, prompts, files, tool arguments, or raw body fragments.
- R7. Require deterministic offline tests for exact boundaries, chunked
  overruns, decompression expansion, malformed encodings, and cleanup.
- R8. Enforce the policy language through the docs-only sparse baseline.

## Scope Boundaries

- Do not add a runtime, HTTP parser, decompressor, proxy, adapter, or SDK shim.
- Do not choose numeric limits before an endpoint, transport, and workload are
  defined.
- Do not change the existing timeout, retry, credential, or observability
  policies.
- Do not add dependencies.

## Verification

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
