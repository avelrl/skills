---
name: localize
description: "Scan, extract, validate, or summarize localization state for a game project."
argument-hint: "[scan|extract|validate|status]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash
---

Purpose: Scan, extract, validate, or summarize a game's localization state without silent translation churn.

Use when:
- the project needs localization coverage, extraction, or validation work
- you need a fast picture of locale health before release or content updates

Do not use for:
- machine translation generation
- silent bulk rewrites of translation tables
- general asset auditing outside localization scope

Inputs / Required Context:
- required: one mode from `scan|extract|validate|status`
- read project conventions first from `docs/technical-preferences.md` and `gamedev/standards/data-files.md`
- default to `assets/data/` for localization tables and `en` as source locale unless the project says otherwise

Outputs / Owned Artifacts:
- `scan`, `validate`, and `status` return inline reports only
- `extract` returns a proposed diff or explicit candidate changes, never a silent rewrite
- all modes use the report spine `Summary -> Findings -> Risks -> Recommended Next Step`

Modes or Arguments:
- `scan`: find hardcoded player-facing strings and localization risks in source content
- `extract`: find new strings or keys and compare them with current tables
- `validate`: check locale coverage, placeholders, orphaned keys, and obvious length-limit issues
- `status`: summarize locale coverage and main open issues

Execution Rules:
1. Validate the mode and load project-specific conventions when they exist.
2. Use fallback assumptions only when project rules are missing, and state those assumptions explicitly.
3. For `scan`, include file paths and line numbers for findings.
4. For `extract`, output a proposed diff or explicit changes for review.
5. For `validate` and `status`, group issues by locale and severity.
6. If no problems are found, return an explicit zero-findings summary.

Failure / Stop Conditions:
- stop if the mode is unsupported
- for `extract`, `validate`, or `status`, return a setup gap if no localization tables exist instead of inventing a structure
- do not guess missing translator context; report it as an open content issue

Return Format:
- `scan`: report plus path and line findings
- `extract`: report plus proposed diff
- `validate`: grouped validation report
- `status`: compact locale coverage report

Example Invocation:
- `/localize validate`

Related Skills / Boundary:
- use `asset-audit` for non-localization asset checks
- do not turn this skill into an automated translation writer
