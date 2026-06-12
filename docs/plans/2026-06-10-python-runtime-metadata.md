# Python runtime metadata

status: completed

## Goal

Declare the Python runtime expected by repository verification without claiming
that the documentation-only compatibility surface is an implemented client.

## Changes

- Add PEP 621 project metadata with `requires-python = ">=3.10"`.
- Keep the package version at `0.0.0` while no implementation exists.
- Enforce the metadata through the dependency-free static baseline.

## Verification

Run `make check` and `git diff --check`.
