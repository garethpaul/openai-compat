# Safe Make Root

## Problem

Whitespace-splitting Make functions and caller-controlled `MAKEFILE_LIST`
values could redirect sparse contract verification outside the checkout.

## Change

- Resolve the raw Makefile path with POSIX-compatible system tooling.
- Reject non-file origins for GNU Make's automatic `MAKEFILE_LIST` value.
- Add no-network regressions for every public target, spaces, a literal
  apostrophe, command-line and environment `REPO_ROOT`, and command-line and
  environment `MAKEFILE_LIST` injection.

## Validation

- Run the complete sparse contract and hostile repository policy suite.
- Run root-policy tests without API access or external dependencies.
- Confirm the Python 3.10/3.12 matrix and CodeQL pass at the exact pull-request
  head.
