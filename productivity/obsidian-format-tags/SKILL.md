---
name: obsidian-format-tags
description: "Refactor one raw Obsidian note into a clean, structured note with preserved meaning, frontmatter, and useful tags."
argument-hint: "<raw-note-markdown>"
user-invocable: true
allowed-tools: Read
---

Purpose: Turn one raw Obsidian note into a cleaner, structured note without changing its meaning.

Use when:
- one note is messy, overcaptured, or poorly tagged
- you want better structure, frontmatter, summary, actions, and tags

Do not use for:
- multi-note synthesis
- adding new facts, links, quotes, tasks, or decisions
- translating or changing the note's language

Inputs / Required Context:
- exactly one Obsidian Markdown note as plain text
- preserve existing frontmatter, tags, links, embeds, callouts, highlights, block refs, and code blocks

Outputs / Owned Artifacts:
- no file output; return only the transformed markdown of the same note
- preserve meaning and all useful content
- keep the raw capture in an appendix when the note is substantially reorganized

Modes or Arguments:
- `<raw-note-markdown>`: the full note body

Execution Rules:
1. Keep the note in the same language as the input.
2. Never invent facts, quotes, links, sources, tasks, or decisions; move uncertainty to `Открытые вопросы`.
3. Preserve Obsidian syntax exactly: `[[...]]`, `![[...]]`, callouts, `==...==`, block refs, tags, and fenced code blocks.
4. Ensure YAML frontmatter exists at the top; keep existing keys intact and ensure `type`, `status`, `summary`, and `tags`.
5. Merge frontmatter tags with meaningful inline hashtags into a deduplicated YAML list using kebab-case and no `#` prefix.
6. Detect the note type from the content: `log`, `meeting`, `research`, `project`, `idea`, `howto`, `reference`, or fallback `note`.
7. Rebuild the note in a top-down flow: TL;DR -> context -> organized body -> decisions -> next steps -> references -> appendix.
8. Use admonitions only when they improve clarity, keep them short, and do not nest them.
9. Keep logs and command output verbatim inside fenced code blocks.
10. Distill obvious noise, but do not delete useful information.

Failure / Stop Conditions:
- if the input is not a single note, ask for one note only
- if safe restructuring is impossible, preserve more raw text and state uncertainty instead of inventing structure

Return Format:
- output only final markdown
- no commentary, no explanations, no wrapper text

Example Invocation:
- `obsidian-format-tags <raw note markdown>`

Related Skills / Boundary:
- utility only; not part of the shared engineering or gamedev workflow chain
- do not use it as a general summarizer or research synthesizer

Transformation Rules:
- Frontmatter:
  - keep existing keys and values intact
  - ensure `type`, `status`, `summary`, and `tags`
  - `type`: `log | meeting | research | project | idea | howto | reference | note`
  - `status`: `inbox | draft | evergreen | reference`
  - `summary`: one plain-text sentence
  - `tags`: YAML list with 3-10 useful tags
- Admonitions:
  - use 0-6 admonitions max
  - always include a short `title`
  - do not put large logs inside admonitions
  - good defaults:
    - TL;DR -> `ad-summary` or `ad-note`
    - insight -> `ad-tip`
    - warning -> `ad-warning`
    - blocker -> `ad-danger`
    - unknowns -> `ad-question`
    - next actions -> `ad-todo`
- Structure:
  - generic order:
    - TL;DR admonition
    - `## Контекст`
    - `## Основное`
    - `## Решения`
    - `## Ссылки и материалы`
    - `## Приложение: сырьё`
  - use `##` for main sections and `###` for subsections
  - use checkboxes for action items
  - annotate external links with one short reason and keep them focused
  - keep the appendix collapsible when raw capture is preserved
- Type adjustments:
  - `meeting`: include participants, agenda, notes, decisions, action items
  - `research`: include question, evidence, short answer, what to verify next
  - `project`: include goal, scope, status, risks, plan or milestones
  - `howto`: include goal, steps, result check, pitfalls
- Quality bar:
  - valid YAML frontmatter
  - no hallucinated facts
  - logs remain verbatim
  - actions are concrete and small
  - final note reads cleanly top-down
