#!/usr/bin/env python3
"""Static baseline checks for the sparse openai-compat repository."""

from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_WORKFLOW = """name: Check

on:
  pull_request:
  push:
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: check-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  baseline_matrix:
    name: baseline (${{ matrix.python-version }})
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.12"]
    env:
      PYTHONDONTWRITEBYTECODE: "1"
    steps:
      - name: Check out repository
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10
        with:
          persist-credentials: false
      - name: Set up Python
        uses: actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405
        with:
          python-version: ${{ matrix.python-version }}
      - name: Validate compatibility contract
        run: make check

  baseline:
    name: baseline
    if: ${{ always() }}
    needs: baseline_matrix
    runs-on: ubuntu-24.04
    timeout-minutes: 5
    steps:
      - name: Verify every baseline matrix result succeeded
        env:
          MATRIX_RESULT: ${{ needs.baseline_matrix.result }}
        run: |
          if [ "$MATRIX_RESULT" != "success" ]; then
            echo "::error::baseline matrix result was $MATRIX_RESULT"
            exit 1
          fi
"""
PLAN = "docs/plans/2026-06-08-openai-compat-baseline.md"
NON_GOALS_PLAN = "docs/plans/2026-06-09-compat-non-goals.md"
VERSIONING_PLAN = "docs/plans/2026-06-09-compat-versioning-claims.md"
DOCUMENTATION_EVIDENCE_PLAN = "docs/plans/2026-06-09-documentation-evidence.md"
TEST_FIXTURE_POLICY_PLAN = "docs/plans/2026-06-09-test-fixture-policy.md"
RATE_LIMIT_RETRY_PLAN = "docs/plans/2026-06-09-rate-limit-retry-contract.md"
MODEL_MAPPING_PLAN = "docs/plans/2026-06-09-model-mapping-policy.md"
MAKE_GATE_PLAN = "docs/plans/2026-06-09-make-gate-aliases.md"
PYTHON_BYTECODE_PLAN = "docs/plans/2026-06-09-python-bytecode-guard.md"
ENV_CREDENTIAL_PLAN = "docs/plans/2026-06-10-environment-credential-policy.md"
PYTHON_METADATA_PLAN = "docs/plans/2026-06-10-python-runtime-metadata.md"
HOSTED_VALIDATION_PLAN = "docs/plans/2026-06-10-hosted-contract-validation.md"
OBSERVABILITY_PLAN = "docs/plans/2026-06-10-observability-retention-policy.md"
TIMEOUT_CANCELLATION_PLAN = "docs/plans/2026-06-12-timeout-cancellation-policy.md"
REQUIRED = [
    ".github/workflows/check.yml",
    ".gitignore",
    "AGENTS.md",
    "CHANGES.md",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "VISION.md",
    "docs/compatibility-contract.md",
    "docs/readme-overview.svg",
    PLAN,
    NON_GOALS_PLAN,
    VERSIONING_PLAN,
    DOCUMENTATION_EVIDENCE_PLAN,
    TEST_FIXTURE_POLICY_PLAN,
    RATE_LIMIT_RETRY_PLAN,
    MODEL_MAPPING_PLAN,
    MAKE_GATE_PLAN,
    PYTHON_BYTECODE_PLAN,
    ENV_CREDENTIAL_PLAN,
    PYTHON_METADATA_PLAN,
    "pyproject.toml",
    HOSTED_VALIDATION_PLAN,
    OBSERVABILITY_PLAN,
    TIMEOUT_CANCELLATION_PLAN,
    "scripts/check-baseline.py",
]
ALLOWED_TRACKED = set(REQUIRED)
EXPECTED_PYPROJECT = """[project]
name = "openai-compat-contract"
version = "0.0.0"
description = "Documentation-only OpenAI compatibility contract"
requires-python = ">=3.10"
classifiers = ["Private :: Do Not Upload"]
"""


def read(path):
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def tracked_files():
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return set(result.stdout.splitlines())


def main():
    failures = []
    if sys.version_info < (3, 10):
        failures.append("repository verification requires Python 3.10 or newer")
    for path in REQUIRED:
        if not (ROOT / path).is_file():
            failures.append(f"required file missing: {path}")

    unexpected = sorted(tracked_files() - ALLOWED_TRACKED)
    if unexpected:
        failures.append("sparse baseline must document new tracked surfaces: " + ", ".join(unexpected))

    gitignore = read(".gitignore")
    for expected in [".env", ".env.*", "*.log", "__pycache__/", "node_modules/", "tmp/"]:
        if expected not in gitignore:
            failures.append(f".gitignore must include {expected}")
    bytecode_paths = sorted(
        str(path.relative_to(ROOT))
        for pattern in ("__pycache__", "*.pyc")
        for path in ROOT.rglob(pattern)
    )
    if bytecode_paths:
        failures.append("generated Python bytecode must not remain after gates: " + ", ".join(bytecode_paths[:5]))

    makefile = read("Makefile")
    if read("pyproject.toml") != EXPECTED_PYPROJECT:
        failures.append("pyproject.toml must exactly declare the private documentation-only Python 3.10+ baseline")
    for phrase in [
        ".PHONY: build check lint static-check test verify",
        "check: verify",
        "verify: static-check",
        "lint test build: static-check",
        "PYTHONDONTWRITEBYTECODE=1 $(PYTHON) scripts/check-baseline.py",
    ]:
        if phrase not in makefile:
            failures.append(f"Makefile must include standard gate alias: {phrase}")

    docs = "\n".join(read(path) for path in ["README.md", "SECURITY.md", "VISION.md"])
    for phrase in [
        "make lint",
        "make test",
        "make build",
        "make check",
        "placeholder",
        "no implementation",
        "compatibility contract",
        "docs/compatibility-contract.md",
        "contract tests",
        "docs-only placeholder",
        "does not ship a runtime",
        "Do not infer compatibility",
        "no OpenAI proxy",
        "credential handling",
        "environment-variable credential policy",
        "credential source precedence",
        "request logging",
        "payload retention",
        "error propagation",
        "official OpenAI documentation",
        "documentation evidence",
        "test fixture policy",
        "sanitized fixtures",
        "no live API calls",
        "rate limits and retries",
        "idempotency-key",
        "model mapping policy",
        "model identifiers",
        "silent fallback",
        "non-goals",
        "versioning",
        "Python bytecode",
        "hosted Linux",
        "observability and data retention policy",
        "explicit opt-in",
        "retention periods",
        "timeout and cancellation policy",
        "client disconnect propagation",
    ]:
        if phrase.lower() not in docs.lower():
            failures.append(f"docs must mention {phrase}")
    changes = read("CHANGES.md")
    for phrase in ["make lint", "make test", "make build", "make check"]:
        if phrase not in changes:
            failures.append(f"CHANGES must mention {phrase}")

    forbidden_snippets = ["sk" + "-", "OPENAI_API" + "_KEY=", "BEGIN " + "PRIVATE KEY"]
    for path in ["README.md", "SECURITY.md", "VISION.md", "docs/compatibility-contract.md"]:
        content = read(path)
        for forbidden in forbidden_snippets:
            if forbidden in content:
                failures.append(f"{path} must not include credential-looking snippet: {forbidden}")

    contract = read("docs/compatibility-contract.md")
    for phrase in [
        "Status: no compatibility behavior is implemented",
        "Supported Endpoints",
        "Non-Goals Until Implemented",
        "drop-in API or SDK compatibility",
        "request or response retention",
        "streaming, file uploads, fine-tuning, batch jobs, or webhook behavior",
        "Authentication And Credential Handling",
        "Environment Variable Credential Policy",
        "No environment-variable credential behavior is implemented yet.",
        "credential source precedence",
        "whether process environment variables are read automatically",
        "tests that clear and restore credential-like environment variables",
        "Error Mapping",
        "Rate Limits And Retries",
        "No rate-limit or retry behavior is implemented yet.",
        "upstream 429 responses",
        "maximum retry count, backoff, and jitter behavior",
        "idempotency-key handling",
        "Model Mapping Policy",
        "No model mapping",
        "default-model behavior",
        "accepted model identifiers",
        "silent fallback",
        "Observability And Data Retention",
        "No logging, metrics, tracing, analytics, or data-retention behavior",
        "distributed tracing require explicit opt-in",
        "retention periods, storage locations, access controls, and deletion behavior",
        "sensitive payload fragments and credentials never",
        "Timeout And Cancellation Policy",
        "No timeout, deadline, client-disconnect propagation, or cancellation behavior",
        "connect, response-header, overall request, and streaming idle timeout budgets",
        "one overall deadline shared by the initial attempt and all retries",
        "caller cancellation and client disconnects propagate",
        "cleanup of response bodies, streams, tasks, sockets, and temporary resources",
        "deterministic tests using fake clocks",
        "Versioning And Compatibility Claims",
        "Documentation Evidence",
        "date reviewed",
        "official documentation URL",
        "Contract Tests",
        "Test Fixture Policy",
        "fixture provenance",
        "no live API calls",
        "Security Checklist",
    ]:
        if phrase not in contract:
            failures.append(f"compatibility contract must include {phrase}")

    plan = read(PLAN)
    if "status: completed" not in plan or "make check" not in plan:
        failures.append("plan must record completed status and verification")
    non_goals_plan = read(NON_GOALS_PLAN)
    if "status: completed" not in non_goals_plan or "Non-Goals Until Implemented" not in non_goals_plan:
        failures.append("non-goals plan must record completed status and verification")
    versioning_plan = read(VERSIONING_PLAN)
    if "status: completed" not in versioning_plan or "Versioning And Compatibility Claims" not in versioning_plan:
        failures.append("versioning plan must record completed status and verification")
    documentation_evidence_plan = read(DOCUMENTATION_EVIDENCE_PLAN)
    if "status: completed" not in documentation_evidence_plan or "Documentation Evidence" not in documentation_evidence_plan:
        failures.append("documentation evidence plan must record completed status and verification")
    test_fixture_policy_plan = read(TEST_FIXTURE_POLICY_PLAN)
    if "status: completed" not in test_fixture_policy_plan or "Test Fixture Policy" not in test_fixture_policy_plan:
        failures.append("test fixture policy plan must record completed status and verification")
    rate_limit_retry_plan = read(RATE_LIMIT_RETRY_PLAN)
    if "status: completed" not in rate_limit_retry_plan or "Rate Limits And Retries" not in rate_limit_retry_plan:
        failures.append("rate limit retry plan must record completed status and verification")
    model_mapping_plan = read(MODEL_MAPPING_PLAN)
    if "status: completed" not in model_mapping_plan or "Model Mapping Policy" not in model_mapping_plan:
        failures.append("model mapping plan must record completed status and verification")
    make_gate_plan_path = ROOT / MAKE_GATE_PLAN
    make_gate_plan = make_gate_plan_path.read_text(encoding="utf-8") if make_gate_plan_path.exists() else ""
    if "status: completed" not in make_gate_plan or "make lint" not in make_gate_plan or "make build" not in make_gate_plan:
        failures.append("make gate alias plan must record completed status and verification")
    python_bytecode_plan = read(PYTHON_BYTECODE_PLAN)
    if "status: completed" not in python_bytecode_plan or "Python bytecode" not in python_bytecode_plan:
        failures.append("Python bytecode plan must record completed status and verification")
    env_credential_plan = read(ENV_CREDENTIAL_PLAN)
    if "status: completed" not in env_credential_plan or "Environment Variable Credential Policy" not in env_credential_plan:
        failures.append("environment credential plan must record completed status and verification")
    python_metadata_plan = read(PYTHON_METADATA_PLAN)
    if "status: completed" not in python_metadata_plan or "requires-python" not in python_metadata_plan:
        failures.append("Python runtime metadata plan must record completed status and verification")
    hosted_validation_plan = read(HOSTED_VALIDATION_PLAN)
    workflow = read(".github/workflows/check.yml")
    if "status: completed" not in hosted_validation_plan or "make check" not in hosted_validation_plan:
        failures.append("hosted contract validation plan must record completed status and verification")
    observability_plan = read(OBSERVABILITY_PLAN)
    if "status: completed" not in observability_plan or "Observability And Data Retention" not in observability_plan:
        failures.append("observability retention plan must record completed status and verification")
    timeout_cancellation_plan = read(TIMEOUT_CANCELLATION_PLAN)
    if (
        "status: completed" not in timeout_cancellation_plan
        or "Timeout And Cancellation Policy" not in timeout_cancellation_plan
        or "make check" not in timeout_cancellation_plan
    ):
        failures.append("timeout cancellation plan must record completed status and verification")
    if workflow != EXPECTED_WORKFLOW:
        failures.append(
            "Check workflow must preserve the Python matrix and emit a fail-closed exact baseline aggregation check"
        )

    try:
        ET.parse(ROOT / "docs/readme-overview.svg")
    except ET.ParseError as error:
        failures.append(f"docs/readme-overview.svg must parse as XML: {error}")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("openai-compat sparse baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
