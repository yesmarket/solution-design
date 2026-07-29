---
description: Search Confluence for applicable reference architectures and populate the table
---

Use the `solution-design-authoring` skill.

Section: **Applicable Reference Architectures**

Follow the skill's workflow: read the section reference file, fetch the current page
body, draft, then show the proposed content and put the approval gate to the user as
selectable options (`AskUserQuestion`), not a free text question, before writing
anything to Confluence.

On approval, **fetch the body again and splice onto that fresh copy**, never onto the
body you drafted from, and send the version explicitly. Another session may have saved
in the meantime and a stale body overwrites its work silently.

Context supplied by the user (may be empty for derived sections):

$ARGUMENTS
