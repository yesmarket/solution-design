---
description: Add all Technical Debt rows the brain dump supports, in one pass
---

Use the `solution-design-authoring` skill.

Section: **Technical Debt**

Write mode: **all rows in one pass.** Draft every row the brain dump supports, show the
complete set as one table, approve once, write once. Do not split the rows across
invocations.

Input: expect a bare newline separated list, bullet markers optional. One non-empty line
is one row. **Derive the Justification column yourself** where the user has not stated
it, do not ask, and use the user's own wording where a line already states why the
trade-off is being made. **Propose the Severity** (small / medium / large) as a status
label per `references/confluence-macros.md`; mark it clearly for the user to confirm
rather than silently picking. **Owner** is a name; write `TBC` if the brain dump does
not name one, never invent one.

Follow the skill's workflow: check for pending writes on the target page, read the section
reference file, fetch the current page body, draft, then show the proposed content and put
the approval gate to the user as selectable options (`AskUserQuestion`), not a free text
question, before writing anything to Confluence.

The gate offers **write now, queue it and continue, revise, or discard.** If the user
queues it, store a pending entry and write nothing, per `references/pending-writes.md`.

If the user writes now, **fetch the body again and splice onto that fresh copy**, never
onto the body you drafted from, and send the version explicitly. Another session may have
saved in the meantime and a stale body overwrites its work silently.

Context supplied by the user (may be empty for derived sections):

$ARGUMENTS
