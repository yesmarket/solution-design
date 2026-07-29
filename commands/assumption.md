---
description: Add all Assumptions rows the brain dump supports, in one pass
---

Use the `solution-design-authoring` skill.

Section: **Assumptions**

Write mode: **all rows in one pass.** Draft every row the brain dump supports, show the
complete set as one table, approve once, write once. Do not split the rows across
invocations.

Input: expect a bare newline separated list, bullet markers optional. One non-empty line
is one row. **Derive the consequence column yourself**, do not ask the user for it, and
use the user's own wording where a line already states its consequence.

Follow the skill's workflow: read the section reference file, fetch the current page
body, draft, then show the proposed content and put the approval gate to the user as
selectable options (`AskUserQuestion`), not a free text question, before writing
anything to Confluence.

On approval, **fetch the body again and splice onto that fresh copy**, never onto the
body you drafted from, and send the version explicitly. Another session may have saved
in the meantime and a stale body overwrites its work silently.

Context supplied by the user (may be empty for derived sections):

$ARGUMENTS
