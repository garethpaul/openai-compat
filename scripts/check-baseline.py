#!/usr/bin/env python3
"""Static baseline checks for the sparse openai-compat repository."""

from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = "docs/plans/2026-06-08-openai-compat-baseline.md"
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

    makefile = read("Makefile")
    if "python3 scripts/check-baseline.py" not in makefile:
        failures.append("Makefile must expose the static checker")

    docs = "\n".join(read(path) for path in ["README.md", "SECURITY.md", "VISION.md"])
    for phrase in [
        "make check",
        "placeholder",
        "no implementation",
        "compatibility contract",
        "docs/compatibility-contract.md",
        "contract tests",
    ]:
        if phrase.lower() not in docs.lower():
            failures.append(f"docs must mention {phrase}")

    contract = read("docs/compatibility-contract.md")
    for phrase in [
        "Status: no compatibility behavior is implemented",
        "Supported Endpoints",
        "Authentication And Credential Handling",
        "Error Mapping",
        "Contract Tests",
        "Security Checklist",
    ]:
        if phrase not in contract:
            failures.append(f"compatibility contract must include {phrase}")

    plan = read(PLAN)
    if "status: completed" not in plan or "make check" not in plan:
        failures.append("plan must record completed status and verification")

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
