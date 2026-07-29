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
    "scope-in", "scope-out", "component-impacted",
    "assumption", "issue", "dependency", "constraint",
}

# Batch sections whose input is habitually a bare newline separated list with the
# consequence column left for us to derive. See the input convention in
# references/sections/tables-registers.md.
BARE_LIST = {"assumption", "issue", "dependency", "constraint"}

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

Follow the skill's workflow: read the section reference file, fetch the current page
body, draft, then show the proposed content and put the approval gate to the user as
selectable options (`AskUserQuestion`), not a free text question, before writing
anything to Confluence.

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

AUDIT = """\
---
description: Audit a detailed design page for missing, empty or thin sections
---

Use the `solution-design-authoring` skill in **audit mode**.

Do not write anything to Confluence. Report findings as a single table in chat.

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

Page reference, or any acronyms to focus on:

$ARGUMENTS
"""

STANDALONE = {
    "dd-audit": AUDIT,
    "glossary-scan": GLOSSARY_SCAN,
    "acronym-sweep": ACRONYM_SWEEP,
}


def mode_note(slug: str) -> str:
    if slug in SINGLE_ROW:
        return SINGLE_NOTE
    if slug in BATCH_ROWS:
        if slug in BARE_LIST:
            return f"{BATCH_NOTE}\n\n{BARE_LIST_NOTE}"
        return BATCH_NOTE
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
