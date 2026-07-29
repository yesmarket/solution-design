---
description: Add all In Scope rows the brain dump supports, in one pass
---

Use the `solution-design-authoring` skill.

Section: **Scope - In Scope**

Write mode: **all rows in one pass.** Draft every row the brain dump supports, show the
complete set as one table, approve once, write once. Do not split the rows across
invocations.

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
