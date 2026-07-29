---
description: Write every queued section to the page in a single Confluence write
---

Use the `solution-design-authoring` skill.

Read `references/pending-writes.md` before starting, and
`references/confluence-mechanics.md` for the splice and version rules.

Flush the pending write queue for the target page:

1. List every pending entry with its section, write mode, and the content as it was
   approved. Show the content, not just the section names: this is the last review before
   the page changes.
2. Take **one** approval for the whole flush via `AskUserQuestion`, offering write all,
   drop specific entries, or cancel. Do not re ask per entry.
3. Fetch the body once, hold back any entry whose target section has changed since it was
   queued, splice the rest in document order, and write once with the version set
   explicitly and a version comment naming every section written.
4. Verify, then delete only the entry files that were written. Report precisely what
   landed and what is still pending.

A failed write leaves the whole queue intact. Never delete an entry that was not written.

Page reference, or specific sections to flush:

$ARGUMENTS
