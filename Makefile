.PHONY: build check lint static-check test verify

PYTHON ?= python3
override REPO_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

check: verify

verify: static-check

lint test build: static-check

static-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) "$(REPO_ROOT)/scripts/check-baseline.py"
	cd "$(REPO_ROOT)" && PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest -v tests.test_repository_policy
