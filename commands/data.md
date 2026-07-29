---
description: Draft the Data and Information Considerations section
---

Use the `solution-design-authoring` skill.

Section: **Data and Information Considerations**

If the arguments begin with **`-r`** or **`--refine`**, refine instead of drafting fresh:
the section's current content on the page is the input, anything after the flag is extra
context, and `-r` alone means normalise to house style without changing any facts. Strip the
flag before using the rest as context.

Otherwise, **if this section already has content, show it and ask** whether to refine,
replace entirely, append, or cancel, before drafting anything. Never overwrite existing
content without asking: a hand edited or Rovo edited paragraph is indistinguishable from one
you wrote. Read `references/refine.md` first in either case, and review a refine as a before
and after rather than as a fresh draft.

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
