#!/usr/bin/env python3
"""Generate thin slash-command aliases that delegate to the skill.

Single source of truth for the command set. Edit SECTIONS and re-run:

    python3 tools/generate_commands.py

Every command is deliberately trivial: all content, schema and style rules live in
the skill. If you find yourself adding substance to a command file, it belongs in
skills/solution-design-authoring/references/ instead.
"""

import pathlib
import textwrap

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
     "Append a row to the In Scope table"),
    ("scope-out", "Scope - Out of Scope",
     "Append a row to the Out of Scope table"),
    ("key-design-decision", "Key Design Decisions",
     "Append one row to the Key Design Decisions table"),
    ("component-impacted", "Components Impacted",
     "Append one row to the Components Impacted table"),
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
     "Append one row to the Assumptions table"),
    ("issue", "Issues",
     "Append one row to the Issues register"),
    ("dependency", "Dependencies",
     "Append one row to the Dependencies register"),
    ("constraint", "Constraints",
     "Append one row to the Constraints table"),
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

Follow the skill's workflow: read the section reference file, fetch the current page
body, draft, then show the proposed content for approval before writing anything to
Confluence.

Context supplied by the user (may be empty for derived sections):

$ARGUMENTS
"""

AUDIT = """\
---
description: Audit a detailed design page for missing, empty or thin sections
---

Use the `solution-design-authoring` skill in **audit mode**.

Do not write anything to Confluence. Report findings as a single table in chat.

Page reference and any focus areas:

$ARGUMENTS
"""


def main() -> None:
    out = pathlib.Path(__file__).resolve().parent.parent / "commands"
    out.mkdir(exist_ok=True)
    for slug, section, description in SECTIONS:
        body = TEMPLATE.format(section=section, description=description)
        (out / f"{slug}.md").write_text(body)
    (out / "dd-audit.md").write_text(AUDIT)
    print(f"Wrote {len(SECTIONS) + 1} command files to {out}")


if __name__ == "__main__":
    main()
