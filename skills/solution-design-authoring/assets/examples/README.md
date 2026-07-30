# Exemplar Designs

**Three exemplars are already sourced**, one each for Small, Medium, and Big, as Confluence
page links in `sources.md` rather than as stored files. Their extracts are spliced into the
reference files, and the same three anchor the size calibration table in `SKILL.md`.

Add a fourth the same way if the range needs another point: a link and a size band in
`sources.md` first, then the extract. A pointer beats a stored PDF, since the page stays
current and the link stays traceable, but a PDF export is acceptable if a link is not
possible.

## Why they matter more than the rules

The reference files describe your conventions in prose. Prose rules get followed
approximately. Verbatim examples get matched closely. For formatting heavy output, the
density of a Key Design Decisions cell, how you group Security Considerations, how a
Target Solution callout list actually reads, an example is worth more than a page of
instructions.

## How to use them

Do not rely on the skill reading a whole PDF at draft time. It is slow, it will not work
identically in claude.ai and Claude Code, and it absorbs the example's subject matter
along with its style. Instead, pull short extracts into the reference files:

1. Pick a section from an exemplar you are happy with.
2. Copy it verbatim into the matching reference file, under an `### Exemplar` heading, next
   to any that are already there.
3. Two contrasting examples beat one: ideally a straightforward case and a messy one.
4. Add its Confluence link and size band to `sources.md` so the extract stays traceable.

### What has already been pulled in

The original `TODO(Ryan)` placeholder blocks are gone; these are the real extracts that
replaced them. Check here before adding a new one, so you extend rather than duplicate.

| File | Extracts present |
|---|---|
| `sections/narrative.md` | Background & Context, a straightforward case and a complex one. Target Solution callouts |
| `sections/considerations.md` | Security (Managed Instinct), Telemetry (SSO/Federation HLD) |
| `sections/tables-registers.md` | A real DREAD rated Risk row (NZ DC Migration), plus worked examples for Assumptions and bare list Constraints |
| `sections/tables-decisions.md` | Two worked examples, one real row that surfaces a rule tension, plus an anti pattern table |

**The risk rating rule is no longer a placeholder.** All three exemplars use a
Possibility/Impact pair for the headline Rating and Residual Rating, and DREAD
sub-attributes appear as supporting narrative rather than as inputs to a formula. That is
confirmed and documented in `tables-registers.md`; do not re-open it on the assumption it is
still guesswork.

Highest value additions from here, in order:

1. A **Current Solution** extract. `narrative.md` has Target Solution callouts but not the
   as-is counterpart, and the two read differently: present tense, describing something that
   already exists and is often messier than the target.
2. A **Cost or Compliance** extract. Both are now flat single level lists with no nested
   bullets, and neither has a real example, so the shape is specified in prose only.
3. A **real counter example**, per the section below. The anti pattern table in
   `tables-decisions.md` is illustrative rather than review sourced, so every entry is
   something someone thought to invent.

## Counter examples are useful too

If you have a design that came back from review with formatting or specificity
complaints, keep a redacted extract as a "do not do this" example. Anti patterns are
often more instructive than good ones. `tables-decisions.md` carries an anti pattern table
of invented examples; a real one from a review would be worth more, since reviewers object
to things nobody thinks to invent.

## Verified macro markup

**Largely done, confirmed 2026-07-28** against all three exemplars. The status, decision,
and tick macros are recorded in `../../references/confluence-macros.md` as the
`data-type="..."` HTML attributes the connector actually returns, not the `ac:*` storage XML
originally guessed at. The `ac:*` forms are kept there as a fallback for a connector that
returns storage format instead, and are **not** verified.

Two gaps remain, and an exemplar using either would close them:

- No `data-state` value other than `DECIDED` has been observed on the decision macro.
- No cross, meaning an unvalidated Assumption, appears anywhere in the sample. Only ticks.

If a new exemplar uses one of those, copy the markup out of the **page source** rather than
a PDF export, which will not show you the markup at all, and paste it into the matching
`VERIFIED MARKUP` slot with the page id and date.

## Note on content

These files sit in the skill directory and their content may be read into context.
Redact customer data, credentials, and anything you would not paste into a chat.
