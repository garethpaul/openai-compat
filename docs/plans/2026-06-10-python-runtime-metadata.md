# Python runtime metadata

status: completed

## Goal

Declare the Python runtime expected by repository verification without claiming
that the documentation-only compatibility surface is an implemented client.

## Changes

- Add PEP 621 project metadata with `requires-python = ">=3.10"`.
- Keep the package version at `0.0.0` while no implementation exists.
- Mark the project `Private :: Do Not Upload` so metadata cannot become a
  public compatibility claim by accidental publication.
- Enforce the metadata through the dependency-free static baseline.
- Run the sparse gate on both Python 3.10 and Python 3.12 in hosted validation.

## Verification

Run `make check`, the Python 3.10/3.12 hosted matrix, and `git diff --check`.
