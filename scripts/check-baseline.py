#!/usr/bin/env python3
"""Static baseline checks for the sparse openai-compat repository."""

from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = "docs/plans/2026-06-08-openai-compat-baseline.md"
NON_GOALS_PLAN = "docs/plans/2026-06-09-compat-non-goals.md"
VERSIONING_PLAN = "docs/plans/2026-06-09-compat-versioning-claims.md"
DOCUMENTATION_EVIDENCE_PLAN = "docs/plans/2026-06-09-documentation-evidence.md"
TEST_FIXTURE_POLICY_PLAN = "docs/plans/2026-06-09-test-fixture-policy.md"
RATE_LIMIT_RETRY_PLAN = "docs/plans/2026-06-09-rate-limit-retry-contract.md"
MODEL_MAPPING_PLAN = "docs/plans/2026-06-09-model-mapping-policy.md"
MAKE_GATE_PLAN = "docs/plans/2026-06-09-make-gate-aliases.md"
PYTHON_BYTECODE_PLAN = "docs/plans/2026-06-09-python-bytecode-guard.md"
REQUIRED = [
    ".gitignore",
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
    "scripts/check-baseline.py",
]
ALLOWED_TRACKED = set(REQUIRED)


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
