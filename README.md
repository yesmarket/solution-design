# solution-design

Authors Solution Architecture Detailed Design sections into Confluence, one section at
a time. Runs in both Claude Code and claude.ai.

## Design

All substance lives in **one skill**. The commands name a section, state its write mode,
and hand off. They carry no schemas, no content rules, and no house style: the hard part is
Confluence's read modify write model and the formatting conventions, and duplicating that
across 25 command files would guarantee drift. Commands have grown past the original three
lines as write-protocol reminders were added, but the rule holds, if a change would add
substance to a command file it belongs in a reference file instead.

```
solution-design/
├── .claude-plugin/plugin.json
├── .mcp.json                        bundles the Atlassian and Lucid MCP servers
├── commands/                        25 thin aliases pointing at the skill
├── tools/generate_commands.py       regenerate the aliases from one table
└── skills/solution-design-authoring/
    ├── SKILL.md                     workflow, section index, house style, audit mode
    ├── references/
    │   ├── confluence-mechanics.md  splice rules, heading and column matching
    │   ├── confluence-macros.md     decision macro, status macro, tick and cross
    │   ├── diagrams.md              obtaining and reading diagrams
    │   ├── glossary-and-acronyms.md the two whole document sweeps
    │   ├── pending-writes.md        the queue: draft many sections, write once
    │   ├── refine.md                -r, the replace gate, what refine may not change
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

A representative sample. There is one command per section, 21 of them, plus 4 page level
commands; run `/help` or see `commands/` for the full list.

```
/background-context <brain dump>
/key-design-decision <brain dump>       appends one row
/risk <brain dump>                      appends one row, DREAD or Possibility/Impact
/assumption <brain dump>                appends every row the dump supports, one write
/component-impacted <brain dump>        appends every row the dump supports, one write
/glossary                               no input, scans page and session
/reference-architectures                no input, searches Confluence
/target-solution <brain dump>           reads the diagram, writes callouts
/security -r <extra context>            refines what is on the page, keeps your edits
/glossary-scan                          whole page, walks candidate terms one by one
/acronym-sweep                          whole page, normalises acronym expansion
/dd-audit <page url>                    read only completeness review
/write-pending                          writes every queued section in one write
```

**Refining content that is already there.** The ten prose sections take `-r` (or
`--refine`), which makes the section's current page content the input rather than drafting
over it. `-r` on its own normalises to house style and changes nothing factual, which is the
cheapest way to pull a section back on template after editing it in Confluence or with Rovo.
`-r <context>` folds new context into what is there. Without the flag, a section that already
has content prompts first: refine, replace entirely, append, or cancel, with the current
content shown so you can see what a replace would cost. Nothing gets silently overwritten,
because a hand edited paragraph is indistinguishable from a generated one.

Refine may fix style, structure and wording, and may cut, but it may not change technical
facts, settled decisions, or anything it cannot corroborate: a fact it does not recognise is
treated as something you added, not as noise. Refines queue like anything else, and a
conflicted refine is re-derived against the current content rather than overwriting the newer
edit. Table sections do not refine, they append; edit an existing row in Confluence.
`/dd-audit` reports off-template sections as **Drifted** so style drift is visible without
reading every section.

**Queue several sections, write once.** Every gate offers *queue it and continue* as well
as *write it now*, so you can run `/scope-in`, then `/scope-out`, then `/assumption`,
reviewing each draft as you go, and land all of them with a single `/write-pending`. One
Confluence write instead of three: faster, and fewer windows for a concurrent session to
lose work in. Risks and Key Design Decisions still gate one row at a time, so queueing
buys the write saving without giving up per-row review.

### Where the queue is stored

```
~/tmp/solution-design/pending/<pageId>/<nnn>-<section-slug>.json

~/tmp/solution-design/pending/4915523641/001-scope-in.json
~/tmp/solution-design/pending/4915523641/002-scope-out.json
```

One file per pending entry, append only so two terminals cannot clobber it, sequence
numbered so the apply order is fixed and two terminals cannot pick the same filename. The
page id keys the directory because titles change; the title is stored inside the entry so
listings stay readable. Nothing needs creating up front, the first write makes the
directories.

**Under your home directory, never under the repo.** This plugin gets used from many
different repositories and a scratch file inside one of them ends up in a `git add -A`.
The skill resolves your home directory at runtime rather than carrying a hardcoded path,
so it behaves the same on any machine, and it refuses to write the queue if the resolved
location would land inside the working directory. It also will not use a session scoped
scratch directory, since those are discarded between sessions and the queue exists
precisely to survive a restart.

Because it sits outside the project directory, Claude Code prompts on first use unless
these are allowed in `~/.claude/settings.json`:

```json
"Write(~/tmp/solution-design/**)",
"Read(~/tmp/solution-design/**)",
"Bash(rm -f ~/tmp/solution-design/pending/*)"
```

Home relative patterns keep the same settings file working across devices. If a
`~`-prefixed pattern does not match on your setup, use `//` for a path from the filesystem
root, for example `Write(//Users/you/tmp/solution-design/**)`, which is device specific and
so worth putting in that device's settings rather than a shared one.

The `rm` rule only clears entries after a successful flush and is scoped to that one
directory. Skip it if you would rather approve each cleanup: a flush that writes
successfully but cannot clear its entries reports that plainly, and the conflict check stops
those entries from being applied twice.

On claude.ai, which has no filesystem, the queue is held in the conversation instead and the
skill says so when you first queue something. Drafting checks that read the page also read
the queue: acronym first use, dedupe, the In Scope versus Out of Scope contradiction check,
and `/dd-audit`, which states what is pending rather than reporting a queued section as
missing.

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
work standalone and assumes no code execution and no subagents. It uses a filesystem for
exactly one thing, persisting the pending write queue, and falls back to a conversation held
queue where there is none. The commands are ergonomics for Claude Code only.

Every invocation drafts and **stops for approval** before writing. That rule lives in
the skill workflow, not the commands, so a malformed alias cannot bypass it. In Claude
Code the gate is a pick list via `AskUserQuestion` with four options (write it now, queue it
and continue, revise first, do not write); on claude.ai, which has no such tool, it falls
back to a plain text question.

**Running several sessions at once.** Confluence has no section level update API: every
write replaces the whole page body, so a session that writes a body it fetched before
its approval gate silently deletes whatever another session saved in between. The skill
fetches twice for this reason, once to draft from and once immediately after approval to
splice onto, compares the two versions, and refuses to write when the target section
itself moved. That makes parallel terminals on **different pages** safe, and parallel
terminals on different sections of **one page** survivable. Two sessions on the same
section of the same page is still not safe, and sequential is still the only guarantee.
If a section does get lost, restore it from Confluence page history rather than having
it rewritten from memory.

## Portability

The skill dispatches on **capability, not tool name**, because the claude.ai Atlassian
connector and the Claude Code Atlassian MCP server expose different tool names and may
differ on storage format versus ADF. Six capabilities are probed at the start of an
invocation: Confluence read, Confluence write, Confluence search, diagram access,
interactive questions, and filesystem read and write. Each has a documented degraded path,
so a missing Lucid server costs you inference quality on three sections rather than blocking
the plugin, and a missing filesystem costs the queue its durability rather than the feature.

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
7. **Exercise the queue end to end.** Queue two sections, then `/write-pending`. The
   specific case worth checking is **two queued sections that share an acronym**, since the
   flush is supposed to reconcile first use across the merged set and emit exactly one
   expansion. Also confirm entries are removed only after a successful write.
8. **Test `-r` against a section you have hand edited**, ideally one you edited in
   Confluence or with Rovo. What must survive the round trip is a fact you added that the
   skill has never seen. Confirm it is carried across verbatim rather than smoothed away.

Items 7 and 8 cover code paths added on 2026-07-29 and 2026-07-30 that have not yet run
against a real page.

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

Also add the slug to whichever generator sets apply, since they decide which notes get baked
into the command:

| Set | For |
|---|---|
| `SINGLE_ROW` | Tables appending one row per invocation |
| `BATCH_ROWS` | Tables taking every row in one pass |
| `BARE_LIST` | Batch tables whose input is a bare list with a derived consequence column |
| `REFINABLE` | Replace mode sections, which accept `-r` and gate before overwriting |

To add a command that is not a section, add it to `STANDALONE` in the generator.

Plugin layout and frontmatter conventions move between releases. Worth checking
https://docs.claude.com/en/docs/claude-code/overview before publishing to a marketplace.
