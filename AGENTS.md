# AGENTS.md

## Repository purpose

`garethpaul/openai-compat` is a docs-only placeholder for a possible OpenAI compatibility project. It does not ship a runtime, proxy, API adapter, or SDK shim, and it does not currently make any compatibility guarantee.

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check`
- Combined verification: `make verify`
- Minimum runtime: Python 3.10; hosted validation covers Python 3.10 and 3.12.
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: no dominant source language detected.

## Testing guidance

- Test-related files detected: `docs/plans/2026-06-09-test-fixture-policy.md`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.
- Future compatibility work must keep API keys and request payloads out of logs, fixtures, and generated files unless explicit sanitized fixtures are reviewed.
- Generated Python bytecode is local tooling output and should not be committed or left behind after `make check`.
- The scan did not identify production authentication, payment, or secret-management code. Treat future additions in those areas as security-sensitive.
- Any future OpenAI-compatible proxy or SDK shim should define a compatibility contract and contract tests before claiming drop-in behavior.
- Non-goals must stay explicit until an endpoint contract and tests replace them with implemented behavior.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
