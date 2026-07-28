# Exemplar Designs

Drop 2 or 3 detailed designs here that you would hold up as good. PDF exports are fine.

## Why they matter more than the rules

The reference files describe your conventions in prose. Prose rules get followed
approximately. Verbatim examples get matched closely. For formatting heavy output, the
density of a Key Design Decisions cell, how you group Security Considerations, how a
Target Solution callout list actually reads, an example is worth more than a page of
instructions.

## How to use them

Do not rely on the skill reading a whole PDF at draft time. It is slow, it will not work
identically in claude.ai and Claude Code, and it absorbs the example's subject matter
along with its style. Instead, pull short extracts into the reference files:

1. Pick a section from an exemplar you are happy with.
2. Copy it verbatim into the `TODO(Ryan)` block in the matching reference file, under an
   `### Exemplar` heading.
3. Two contrasting examples beat one: ideally a straightforward case and a messy one.

Priority order, by how much variance an example removes:

1. `sections/narrative.md`, the Current and Target Solution callouts. The register is
   hard to specify in rules and easy to demonstrate, and it is the only place the
   audience shifts to non technical readers.
2. `sections/considerations.md`, Security and Telemetry. Grouping conventions vary most
   here.
3. `sections/tables-registers.md`, a Risk row with a real DREAD rating. The aggregation
   rule in that file is a placeholder until you confirm Humm's framework.
4. `sections/tables-decisions.md` already has a worked example. Add one of yours if your
   Rationale and Implications split differs from the one there.

## Counter examples are useful too

If you have a design that came back from review with formatting or specificity
complaints, keep a redacted extract as a "do not do this" example. Anti patterns are
often more instructive than good ones, and `tables-decisions.md` already has a slot for
that shape of content.

## Verified macro markup

If an exemplar uses the decision macro, the status macro, or tick and cross, that is
your source for the real storage format. Copy the markup out of the page source rather
than the PDF export and paste it into the `VERIFIED MARKUP` slots in
`../../references/confluence-macros.md`. A PDF export will not show you the markup.

## Note on content

These files sit in the skill directory and their content may be read into context.
Redact customer data, credentials, and anything you would not paste into a chat.
