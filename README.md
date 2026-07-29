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
├── .mcp.json                        bundles the Atlassian and Lucid MCP servers
├── commands/                        24 thin aliases pointing at the skill
├── tools/generate_commands.py       regenerate the aliases from one table
└── skills/solution-design-authoring/
    ├── SKILL.md                     workflow, section index, house style, audit mode
    ├── references/
    │   ├── confluence-mechanics.md  splice rules, heading and column matching
    │   ├── confluence-macros.md     decision macro, status macro, tick and cross
    │   ├── diagrams.md              obtaining and reading diagrams
    │   ├── glossary-and-acronyms.md the two whole document sweeps
    │   └── sections/
    │       ├── narrative.md         Background, Overview, Current, Target
    │       ├── considerations.md    Security, Compliance, Cost, Telemetry, Data, Infra
    │       ├── tables-decisions.md  Key Design Decisions, Components Impacted
    │       ├── tables-registers.md  Risks, Assumptions, Issues, Dependencies, Constraints
    │       └── tables-scope.md      Glossary, Scope In, Scope Out, Reference Architectures
    └── assets/examples/
        ├── README.md                 how to use exemplars, why extracts beat whole PDFs
        └── sources.md                Confluence page links for the 3 house exemplars
```

The 21 sections group into five behaviours: prose, diagram plus callouts, append one
row, append all rows in one pass, and merge with dedupe. Sections are grouped into
reference files by behaviour rather than one file per section, so only one grouped file
loads per invocation.

## Usage

```
/background-context <brain dump>
/key-design-decision <brain dump>       appends one row
/risk <brain dump>                      appends one row, DREAD or Possibility/Impact
/assumption <brain dump>                appends every row the dump supports, one write
/component-impacted <brain dump>        appends every row the dump supports, one write
/glossary                               no input, scans page and session
/reference-architectures                no input, searches Confluence
/target-solution <brain dump>           reads the diagram, writes callouts
/glossary-scan                          whole page, walks candidate terms one by one
/acronym-sweep                          whole page, normalises acronym expansion
/dd-audit <page url>                    read only completeness review
```

**Batch versus one at a time.** Scope in and out, Components Impacted, Assumptions,
Issues, Dependencies, and Constraints take every row the brain dump supports in a
single pass, because each Confluence write costs a full page read and rewrite. Key
Design Decisions and Risks stay one row per invocation: both carry judgement the author
needs to weigh per row, and batching them produces rows nobody reviewed.

**Bare lists.** For Assumptions, Issues, Dependencies, and Constraints the expected
input is a plain newline separated list, bullet markers optional. One line becomes one
row and the Implication or Impact column is derived rather than asked for, so a dump of
ten one line items comes back as ten fully populated rows for review. Where a line
already states its own consequence, the author's wording is kept.

In claude.ai, where plugin slash commands are not available, the skill triggers from
plain language: *"fill in Key Design Decisions from this: ..."*. The skill is written to
work standalone and assumes no filesystem, no code execution, and no subagents. The
commands are ergonomics for Claude Code only.

Every invocation drafts and **stops for approval** before writing. That rule lives in
the skill workflow, not the commands, so a malformed alias cannot bypass it. In Claude
Code the gate is a pick list (write it / revise first / do not write) via
`AskUserQuestion`; on claude.ai, which has no such tool, it falls back to a plain text
question.

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

The plugin's `.mcp.json` declares the official remote servers for both (`mcp.atlassian.com`
and `mcp.lucid.app`), so installing the plugin in Claude Code offers to wire these up
automatically. Both are OAuth based: the first call opens a browser to authorise, per
user, per machine. This is a Claude Code CLI mechanism only; claude.ai does not read
plugin-declared MCP servers, so the skill's capability probe (see Portability, above)
still matters there. If your organisation already runs a different Atlassian or Lucid
MCP server (a self hosted `sooperset/mcp-atlassian`, for example), point `.mcp.json` at
that instead, the skill dispatches on capability, not on which server is behind it.

## Before first real use

1. ~~Verify the macro markup.~~ **Done 2026-07-28.** `references/confluence-macros.md`
   now carries markup verified against three real Humm pages fetched via this
   Atlassian MCP server: the status, decision, and tick macros all render as
   `data-type="..."` HTML attributes, not the classic `ac:*` storage XML originally
   guessed at. The `ac:*` forms are kept as a fallback for a connector that returns
   storage format instead; re-verify against a real page before trusting them there.
   Two things this pass did not resolve: no `data-state` value other than `DECIDED` was
   observed, and no cross (unvalidated) example exists in the sample, only ticks.
2. ~~Confirm the risk aggregation rule.~~ **Done 2026-07-28.** All three exemplars use
   a Possibility/Impact pair as the headline Rating and Residual Rating, never a
   separate averaged "Overall". `tables-registers.md` now reflects this; the DREAD
   sub-attributes, where used, are supporting narrative for that judgement call, not
   inputs to a formula. See `assets/examples/sources.md`.
3. **Keep `assets/examples/sources.md` current.** It points at Confluence page IDs
   rather than storing PDFs, so the extracts spliced into `narrative.md`,
   `considerations.md`, `tables-decisions.md`, `tables-registers.md`, and
   `confluence-macros.md` stay traceable to a real page instead of going stale. When you
   add a new exemplar, add its link and size band to `sources.md` first, then pull the
   extract. The same three pages also anchor the Right-sizing section in `SKILL.md`
   (Small/Medium/Big); add a fourth exemplar there too if the range needs another point.
4. **Verify the heading and column alias tables** in `confluence-mechanics.md` against
   real pages. This is what makes template drift survivable and the most likely thing
   to be wrong on day one.
5. **Test the splice on a scratch page.** Specifically test a section containing an info
   panel and an embedded Lucid diagram, since preserving macros and embeds is where a
   read modify write edit does real damage.
6. **Decide on the bullet length tension in `tables-decisions.md`.** The real Key
   Design Decisions row pulled from NZ DC Migration runs well past the "12 words or
   fewer" guideline. Flagged there as a `NOTE(Ryan)` rather than silently loosened,
   since it is a real, presumably endorsed row contradicting a prescriptive rule.

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
grouped reference file matches its behaviour. Three edits, no duplication. If the new
section is a table, also add its slug to `SINGLE_ROW` or `BATCH_ROWS` in the generator,
which decides the write mode note baked into the command.

To add a command that is not a section, add it to `STANDALONE` in the generator.

Plugin layout and frontmatter conventions move between releases. Worth checking
https://docs.claude.com/en/docs/claude-code/overview before publishing to a marketplace.
