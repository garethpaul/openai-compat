ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override REPO_ROOT := $(shell path='$(subst ','"'"',$(MAKEFILE_LIST))'; path=$$(printf '%s' "$$path" | /usr/bin/sed 's/^ //'); /usr/bin/dirname -- "$$path")
export REPO_ROOT

.PHONY: build check lint root-test static-check test verify

PYTHON ?= python3

check: verify

verify: static-check root-test

lint test build: static-check

static-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) "$$REPO_ROOT/scripts/check-baseline.py"
	cd "$$REPO_ROOT" && PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest -v tests.test_repository_policy

root-test:
	cd "$$REPO_ROOT" && PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest -v tests.test_makefile_root
