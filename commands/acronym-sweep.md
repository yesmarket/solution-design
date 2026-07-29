---
description: Normalise acronyms across the page so only the first use is expanded
---

Use the `solution-design-authoring` skill.

Read `references/glossary-and-acronyms.md` before starting.

Sweep the **entire page** and enforce the acronym rule: an acronym is expanded exactly
once, at its first appearance in document reading order, written as
`Expansion (ACRONYM)`, and written as the short form everywhere after that. Expand
first uses that were missed, and collapse later uses that are still spelled out.

Change wording only. Do not add facts, reorder content, or touch table structure,
macros, or embeds. Present the changes as a before and after list grouped by acronym,
get approval, then apply them all in a single write.

This sweep rewrites text across every section, so it is the most destructive operation in
the skill if the body is stale. **Re fetch immediately after approval and re apply the
approved wording changes to that copy**, per "Concurrent sessions" in
`references/confluence-mechanics.md`. If the re fetch shows the page has moved, re run the
sweep against the new body rather than writing the old one. Do not run this while another
session is writing to the same page.

If sections are pending in the write queue, **flush them first** with `/write-pending`. A
sweep of a body that is missing queued sections is wrong the moment they land. Say so and
let the user decide rather than sweeping around them.

Page reference, or any acronyms to focus on:

$ARGUMENTS
