.DEFAULT_GOAL := check

.PHONY: __repository-make-authority build check lint root-test static-check test verify
.SECONDEXPANSION:

override SHELL := /bin/sh
override .SHELLFLAGS := -c
ifneq ($(filter command line,$(origin MAKEFLAGS)),)
$(error MAKEFLAGS must not be overridden for repository verification)
endif
override REPOSITORY_MAKE_FIRST_FLAGS := $(firstword $(MAKEFLAGS))
ifneq ($(filter -%,$(REPOSITORY_MAKE_FIRST_FLAGS)),)
override REPOSITORY_MAKE_FIRST_FLAGS :=
endif
override REPOSITORY_MAKE_SHORT_FLAGS := $(REPOSITORY_MAKE_FIRST_FLAGS) $(filter-out --%,$(filter -%,$(MAKEFLAGS)))
ifneq ($(findstring n,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring t,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring q,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring i,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(filter --just-print --dry-run --recon --touch --question --ignore-errors,$(MAKEFLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must be empty; repository verification requires this Makefile to be loaded alone)
endif
override MAKEFILES :=
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override REPOSITORY_MAKEFILE := $(value MAKEFILE_LIST)
override EXPECTED_MAKEFILE_LIST := $(value MAKEFILE_LIST)
override CURRENT_MAKEFILE_LIST = $(value MAKEFILE_LIST)
export REPOSITORY_MAKEFILE EXPECTED_MAKEFILE_LIST CURRENT_MAKEFILE_LIST
override REPO_ROOT := $(shell path='$(subst ','"'"',$(REPOSITORY_MAKEFILE))'; path=$$(printf '%s' "$$path" | /usr/bin/sed 's/^ //'); /usr/bin/dirname -- "$$path")
export REPO_ROOT

build check lint root-test static-check test verify:: $$(if $$(filter file,$$(origin MAKEFILE_LIST)),,$$(error MAKEFILE_LIST must not be overridden))
build check lint root-test static-check test verify:: __repository-make-authority

__repository-make-authority::
	@if [ "$$CURRENT_MAKEFILE_LIST" != "$$EXPECTED_MAKEFILE_LIST" ]; then \
		printf '%s\n' 'multiple -f Makefiles are not supported' >&2; \
		exit 1; \
	fi

check:: verify

verify:: static-check root-test

lint test build:: static-check

static-check::
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) "$$REPO_ROOT/scripts/check-baseline.py"
	cd "$$REPO_ROOT" && PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest -v tests.test_repository_policy

root-test::
	cd "$$REPO_ROOT" && PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest -v tests.test_makefile_root

PYTHON ?= python3
