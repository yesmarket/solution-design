---
description: Read supplied Confluence links and populate the Related table
---

Use the `solution-design-authoring` skill.

Section: **Related**

Follow the skill's workflow: check for pending writes on the target page, read the section
reference file, fetch the current page body, draft, then show the proposed content and put
the approval gate to the user as selectable options (`AskUserQuestion`), not a free text
question, before writing anything to Confluence.

The gate offers **write now, queue it and continue, revise, or discard.** If the user
queues it, store a pending entry and write nothing, per `references/pending-writes.md`.

If the user writes now, **fetch the body again and splice onto that fresh copy**, never
onto the body you drafted from, and send the version explicitly. Another session may have
saved in the meantime and a stale body overwrites its work silently.

Each Confluence link supplied in context is one row. Use the Atlassian MCP server to read
every linked page and work out how it relates to this design. Any additional free-text
context supplied alongside a link should inform the relevance sentence.

Context supplied by the user (links, and optionally why each was shared):

$ARGUMENTS
