#!/usr/bin/env python3
"""Generate thin slash-command aliases that delegate to the skill.

Single source of truth for the command set. Edit SECTIONS and re-run:

    python3 tools/generate_commands.py

Every command is deliberately trivial: all content, schema and style rules live in
the skill. If you find yourself adding substance to a command file, it belongs in
skills/solution-design-authoring/references/ instead.
"""

import pathlib
import re

# Sections that append exactly one row per invocation. Every other table section takes
# all the rows the brain dump supports in a single pass. See the section index in
# SKILL.md; these two carry per-row judgement the user has to weigh individually.
SINGLE_ROW = {"key-design-decision", "risk"}

# Table sections that take every row in one pass. Glossary and Applicable Reference
# Architectures are absent deliberately: both are derived merge-and-dedupe sections
# that already write in a single pass, and neither takes a brain dump.
BATCH_ROWS = {
    "scope-in", "scope-out", "component-impacted", "integration",
    "assumption", "issue", "dependency", "constraint",
}

# Batch sections whose input is habitually a bare newline separated list with the
# consequence column left for us to derive. See the input convention in
# references/sections/tables-registers.md.
BARE_LIST = {"assumption", "issue", "dependency", "constraint"}

# Replace-mode sections. These accept -r to refine what is already on the page, and must
# ask before overwriting non-empty content. Table sections append and do neither. See
# references/refine.md.
REFINABLE = {
    "background-context", "solution-overview", "current-solution", "target-solution",
    "security", "compliance", "cost", "telemetry", "data", "infrastructure",
}

# (command slug, canonical section name, short description for the command palette)
SECTIONS = [
    ("background-context", "Background & Context",
     "Draft the Background & Context section"),
    ("solution-overview", "Recommended Solution Overview",
     "Draft the Recommended Solution Overview section"),
    ("current-solution", "Current Solution",
     "Draft the Current Solution (as-is) section"),
    ("target-solution", "Target Solution",
     "Draft the Target Solution (to-be) section"),
    ("scope-in", "Scope - In Scope",
     "Add all In Scope rows the brain dump supports, in one pass"),
    ("scope-out", "Scope - Out of Scope",
     "Add all Out of Scope rows the brain dump supports, in one pass"),
    ("key-design-decision", "Key Design Decisions",
     "Append one row to the Key Design Decisions table"),
    ("component-impacted", "Components Impacted",
     "Add all Components Impacted rows the brain dump supports, in one pass"),
    ("security", "Security Considerations",
     "Draft the Security Considerations section"),
    ("compliance", "Regulatory, Compliance, and Privacy Considerations",
     "Draft the Regulatory, Compliance, and Privacy Considerations section"),
    ("cost", "Licensing & Cost Considerations",
     "Draft the Licensing & Cost Considerations section"),
    ("telemetry", "Telemetry Considerations",
     "Draft the Telemetry Considerations section"),
    ("data", "Data and Information Considerations",
     "Draft the Data and Information Considerations section"),
    ("integration", "Integrations",
     "Add all Integrations rows the brain dump supports, in one pass"),
    ("infrastructure", "Infrastructure, Network, & Integration",
     "Draft Infrastructure, Network & Integration, inferring from the Lucid diagram"),
    ("risk", "Risks",
     "Append one row to the Risks register"),
    ("assumption", "Assumptions",
     "Add all Assumptions rows the brain dump supports, in one pass"),
    ("issue", "Issues",
     "Add all Issues rows the brain dump supports, in one pass"),
    ("dependency", "Dependencies",
     "Add all Dependencies rows the brain dump supports, in one pass"),
    ("constraint", "Constraints",
     "Add all Constraints rows the brain dump supports, in one pass"),
    ("glossary", "Glossary",
     "Scan the page and session for terms needing definition, then merge into Glossary"),
    ("reference-architectures", "Applicable Reference Architectures",
     "Search Confluence for applicable reference architectures and populate the table"),
]

TEMPLATE = """\
---
description: {description}
---

Use the `solution-design-authoring` skill.

Section: **{section}**

{mode}

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
"""

BATCH_NOTE = """\
Write mode: **all rows in one pass.** Draft every row the brain dump supports, show the
complete set as one table, approve once, write once. Do not split the rows across
invocations."""

SINGLE_NOTE = """\
Write mode: **one row only.** If the brain dump clearly contains more than one, draft
the first, write it, then offer the next."""

BARE_LIST_NOTE = """\
Input: expect a bare newline separated list, bullet markers optional. One non-empty line
is one row. **Derive the consequence column yourself**, do not ask the user for it, and
use the user's own wording where a line already states its consequence."""

REFINE_NOTE = """\
If the arguments begin with **`-r`** or **`--refine`**, refine instead of drafting fresh:
the section's current content on the page is the input, anything after the flag is extra
context, and `-r` alone means normalise to house style without changing any facts. Strip the
flag before using the rest as context.

Otherwise, **if this section already has content, show it and ask** whether to refine,
replace entirely, append, or cancel, before drafting anything. Never overwrite existing
content without asking: a hand edited or Rovo edited paragraph is indistinguishable from one
you wrote. Read `references/refine.md` first in either case, and review a refine as a before
and after rather than as a fresh draft."""

AUDIT = """\
---
description: Audit a detailed design page for missing, empty or thin sections
---

Use the `solution-design-authoring` skill in **audit mode**.

Do not write anything to Confluence. Report findings as a single table in chat.

If sections are pending in the write queue, list them before the table and state that the
findings reflect the page as it stands, not the pending work. A queued section otherwise
reads as Missing when it is drafted and waiting.

Page reference and any focus areas:

$ARGUMENTS
"""

GLOSSARY_SCAN = """\
---
description: Scan the whole page for terms, acronyms and systems that belong in the Glossary, then walk them one by one
---

Use the `solution-design-authoring` skill.

Read `references/glossary-and-acronyms.md` before starting, and
`references/sections/tables-scope.md` for the Glossary schema.

Scan the **entire page**, not one section, for candidates: acronyms, multi word domain
terms, vendor and product names, and internal system names. Examples of the kind of
thing that is easy to miss: "enhanced customer due diligence", "Risk Narrative
Compliance Lens", "suspicious matter reporting".

Show the full candidate list first so the size of the job is visible, then walk the
candidates **one at a time**, asking with `AskUserQuestion` whether to add each one.
Merge, sort, and write once at the end.

Walking the candidates takes a while, so the body you read at the start is stale by the
time you write. **Re fetch immediately before the single write and splice onto that
copy**, per "Concurrent sessions" in `references/confluence-mechanics.md`.

Include any sections pending in the write queue in the scan, since a candidate that is
queued but not yet written is still a candidate. Say how many pending sections you
covered.

Page reference, or any terms the user wants forced into the list:

$ARGUMENTS
"""

ACRONYM_SWEEP = """\
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
"""

WRITE_PENDING = """\
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
"""

STANDALONE = {
    "dd-audit": AUDIT,
    "glossary-scan": GLOSSARY_SCAN,
    "acronym-sweep": ACRONYM_SWEEP,
    "write-pending": WRITE_PENDING,
}


def mode_note(slug: str) -> str:
    if slug in SINGLE_ROW:
        return SINGLE_NOTE
    if slug in BATCH_ROWS:
        if slug in BARE_LIST:
            return f"{BATCH_NOTE}\n\n{BARE_LIST_NOTE}"
        return BATCH_NOTE
    if slug in REFINABLE:
        return REFINE_NOTE
    return ""


def main() -> None:
    out = pathlib.Path(__file__).resolve().parent.parent / "commands"
    out.mkdir(exist_ok=True)
    for slug, section, description in SECTIONS:
        body = TEMPLATE.format(
            section=section, description=description, mode=mode_note(slug)
        )
        # Collapse the blank line left behind when a section has no mode note.
        (out / f"{slug}.md").write_text(re.sub(r"\n{3,}", "\n\n", body))
    for slug, body in STANDALONE.items():
        (out / f"{slug}.md").write_text(body)
    total = len(SECTIONS) + len(STANDALONE)
    print(f"Wrote {total} command files to {out}")


if __name__ == "__main__":
    main()
