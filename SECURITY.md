# Security Policy

## Supported Versions

The supported security scope for `openai-compat` is the current default branch, `main`. Older commits, tags, branches, forks, demos, and generated artifacts are not actively supported unless the repository explicitly marks them as maintained.

Project summary: No GitHub description is currently set.

## Reporting a Vulnerability

Please report suspected vulnerabilities through GitHub's private vulnerability reporting or by opening a draft GitHub Security Advisory for `garethpaul/openai-compat` when that option is available. If GitHub does not show a private reporting option for this repository, contact the repository owner through GitHub and avoid posting exploit details publicly until the issue can be assessed.

Do not open a public issue that includes exploit code, secrets, personal data, or detailed reproduction steps for an unpatched vulnerability.

## What to Include

Helpful reports include:

- the affected file, endpoint, permission, dependency, or workflow
- a concise impact statement explaining what an attacker could do
- reproduction steps using test data and accounts you control
- the branch, commit SHA, platform version, device, runtime, or dependency versions used
- logs, screenshots, or proof-of-concept snippets that demonstrate impact without exposing private data

## Project Security Posture

- This repository appears to be a public sample, documentation, or utility project. The active security scope is the code and documentation on the default branch.
- The repository scan did not identify production authentication, payment, or secret-management code. Treat the project as public sample code unless future changes add sensitive surfaces.
- No primary dependency manifest was detected in the repository root. If dependencies are added later, include a manifest and prefer reproducible installation instructions.
- This repository is currently a placeholder with no implementation. There is
  no OpenAI proxy, API adapter, SDK shim, runtime service, or credential
  handling code in the current baseline.
- Future compatibility code should start with a written compatibility contract
  and contract tests before introducing proxy, SDK shim, or credential-handling
  behavior. Use `docs/compatibility-contract.md` as the required security and
  behavior checklist before adding those surfaces.
- Future code that reads process environment credentials should define accepted
  variables, credential source precedence, redaction, and isolated tests before
  implementation.
- Keep non-goals explicit for unsupported forwarding, credential exchange,
  request retention, streaming, file, fine-tuning, batch, webhook, and model
  equivalence behavior until tests prove otherwise.


## Dependency and Supply Chain Security

Dependency updates should come from trusted package managers and should keep lockfiles in sync when lockfiles exist. Do not commit credentials, private keys, tokens, generated secrets, or machine-local configuration. If a vulnerability depends on a compromised package, typosquatting risk, insecure transitive dependency, or unsafe build step, include the package name, affected version, and the path through which it is used.

For future OpenAI-compatible surfaces, document credential handling, upstream
request logging, payload retention, response translation, error propagation,
token redaction, environment-variable credential policy, rate limits and
retries, timeout behavior, versioning, and documentation evidence before
claiming compatibility. Model mapping policy should define accepted model
identifiers, aliases, unsupported-model behavior, and silent fallback rules
before runtime behavior exists. Environment credential handling should define
credential source precedence before code reads process state. Future test
fixture policy should require sanitized fixtures, fixture provenance, and no
live API calls by default. Retry behavior should define upstream 429 handling,
backoff, retry budgets, and idempotency-key handling before request forwarding
exists.
Timeout and cancellation policy should define phase-specific deadlines, one
overall budget across retries, client disconnect propagation, resource cleanup,
sanitized errors, and deterministic tests before network behavior exists.
Observability and data retention policy should define permitted event fields,
explicit opt-in for tracing, sampling, retention periods, deletion behavior,
and tests proving credentials and sensitive payload fragments remain absent.
Run `make lint`, `make test`, `make build`, and `make check` before changing
the sparse baseline. Generated Python bytecode is local tooling output and
should not remain after verification.
Pinned, read-only hosted Linux validation enforces the same docs-only sparse
allowlist without API credentials, dependencies, or live OpenAI requests.

## Safe Research Guidelines

Good-faith research is welcome when it stays within these boundaries:

- use only accounts, devices, data, and infrastructure that you own or have explicit permission to test
- avoid destructive actions, persistence, spam, phishing, social engineering, or denial-of-service testing
- minimize access to personal data and stop testing immediately if private data is exposed
- do not exfiltrate secrets or third-party data; report the minimum evidence needed to verify impact
- keep vulnerability details confidential until the maintainer has assessed the report

## Maintainer Response

The maintainer will review complete reports as availability allows, prioritize issues by exploitability and impact, and coordinate a fix or mitigation when the affected code is still maintained. For sample, archived, or educational repositories, the likely remediation may be documentation, dependency updates, or clearly marking unsupported code rather than a production-style patch release.
