# solution-design

Authors Solution Architecture Detailed Design sections into Confluence, one section at
a time. Runs in both Claude Code and claude.ai.

## Design

All substance lives in **one skill**. The commands are three line aliases that name a
section and hand off. This is deliberate: the hard part is Confluence's
read modify write model and the house formatting conventions, and duplicating that
across 22 command files would guarantee drift.

```
solution-design/
├── .claude-plugin/plugin.json
├── commands/                        22 thin aliases pointing at the skill
├── tools/generate_commands.py       regenerate the aliases from one table
└── skills/solution-design-authoring/
    ├── SKILL.md                     workflow, section index, house style, audit mode
    ├── references/
    │   ├── confluence-mechanics.md  splice rules, heading and column matching
    │   ├── confluence-macros.md     decision macro, status macro, tick and cross
    │   ├── diagrams.md              obtaining and reading diagrams
    │   └── sections/
    │       ├── narrative.md         Background, Overview, Current, Target
    │       ├── considerations.md    Security, Compliance, Cost, Telemetry, Data, Infra
    │       ├── tables-decisions.md  Key Design Decisions, Components Impacted
    │       ├── tables-registers.md  Risks, Assumptions, Issues, Dependencies, Constraints
    │       └── tables-scope.md      Glossary, Scope In, Scope Out, Reference Architectures
    └── assets/examples/             drop your exemplar designs here
```

The 21 sections group into four behaviours: prose, diagram plus callouts, append one
row, and merge with dedupe. Sections are grouped into reference files by behaviour
rather than one file per section, so only one grouped file loads per invocation.

## Usage

```
/background-context <brain dump>
/key-design-decision <brain dump>       appends one row
/risk <brain dump>                      appends one row, DREAD or Possibility/Impact
/glossary                               no input, scans page and session
/reference-architectures                no input, searches Confluence
/target-solution <brain dump>           reads the diagram, writes callouts
/dd-audit <page url>                    read only completeness review
```

In claude.ai, where plugin slash commands are not available, the skill triggers from
plain language: *"fill in Key Design Decisions from this: ..."*. The skill is written to
work standalone and assumes no filesystem, no code execution, and no subagents. The
commands are ergonomics for Claude Code only.

Every invocation drafts and **stops for approval** before writing. That rule lives in
the skill workflow, not the commands, so a malformed alias cannot bypass it.

## Portability

The skill dispatches on **capability, not tool name**, because the claude.ai Atlassian
connector and the Claude Code Atlassian MCP server expose different tool names and may
differ on storage format versus ADF. Four capabilities are probed at the start of an
invocation: Confluence read, Confluence write, Confluence search, and diagram access.
Each has a documented degraded path, so a missing Lucid server costs you inference
quality on three sections rather than blocking the plugin.

## Requirements

- Confluence read and write, via whichever Atlassian integration the environment has
- Confluence search, for Applicable Reference Architectures
- A Lucid MCP server, for Current Solution, Target Solution, and Infrastructure

## Before first real use

1. **Verify the macro markup.** `references/confluence-macros.md` carries best known
   forms for the decision macro, the status macro, and tick and cross, but macro
   storage format varies by Confluence version. Fetch a real Humm design that already
   uses them, copy the exact markup, and paste it into the `VERIFIED MARKUP` slots in
   that file. Do the decision macro first, since Key Design Decisions is the most
   frequently appended table and a broken macro will replicate across every row.
2. **Confirm the risk aggregation rule.** `tables-registers.md` defaults to a mean of
   the DREAD sub values for the overall rating. That is a placeholder. Replace it with
   whatever Humm's risk framework actually prescribes.
3. **Drop 2 or 3 exemplar designs into `assets/examples/`** and fill the `TODO(Ryan)`
   blocks in `narrative.md` and `considerations.md` with verbatim extracts.
4. **Verify the heading and column alias tables** in `confluence-mechanics.md` against
   real pages. This is what makes template drift survivable and the most likely thing
   to be wrong on day one.
5. **Test the splice on a scratch page.** Specifically test a section containing an info
   panel and an embedded Lucid diagram, since preserving macros and embeds is where a
   read modify write edit does real damage.

## Conventions

**No em dashes anywhere.** This is rule 1 in the skill and is enforced in content
written to Confluence. Keep it true of the reference files too, since the model
calibrates its output style on them. To check:

```
grep -rP '\x{2014}|\x{2013}' .
```

## Extending

To add a section: append a tuple to `SECTIONS` in `tools/generate_commands.py`, rerun
it, add a row to the section index in `SKILL.md`, and add the schema to whichever
grouped reference file matches its behaviour. Three edits, no duplication.

Plugin layout and frontmatter conventions move between releases. Worth checking
https://docs.claude.com/en/docs/claude-code/overview before publishing to a marketplace.
