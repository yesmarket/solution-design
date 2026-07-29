# Confluence Mechanics

How to change one section of a page without damaging the rest. Read this before any
write.

## Contents

- [The core constraint](#the-core-constraint)
- [Concurrent sessions](#concurrent-sessions)
- [Locating a section](#locating-a-section)
- [Heading aliases](#heading-aliases)
- [Mapping table columns](#mapping-table-columns)
- [Splice rules by write mode](#splice-rules-by-write-mode)
- [Storage format reference](#storage-format-reference)
- [Things you must never touch](#things-you-must-never-touch)
- [Write and verify](#write-and-verify)
- [Failure modes](#failure-modes)

## The core constraint

**There is no section level update API.** The Confluence update operation replaces the
entire page body. Every section edit is therefore read, modify in memory, write the
whole body back. Consequences:

- You must fetch the current body first, every time. No exceptions.
- Anything you fail to carry across is deleted, silently.
- The version number must be the current version incremented by one. If someone else
  saved between your read and your write, the write either fails or clobbers them.

Because the whole body is the unit of write, **every write is a potential clobber of the
entire page**, not just of the section you are editing. The next section covers the
protocol that prevents it. It is not optional and it is not a best effort.

## Concurrent sessions

Assume you are not the only writer. Another terminal, another author in the Confluence
editor, or a Rovo agent may save between your read and your write. This has already
happened in practice and cost sections that had to be restored from page history.

### The two fetch rule

**Fetch the body twice. Draft from the first, write onto the second.**

1. **Draft fetch**, at the start of the invocation. Use it for context: existing content,
   table headers, acronym first use, the target section's current markup. **Record the
   version number and keep the target section's exact markup.**
2. **State the version in the draft you show the user**, for example "drafted against
   version 47". It costs one line and makes a clobber diagnosable afterwards.
3. **Approval gate.**
4. **Write fetch**, immediately after approval. This is the authoritative body. Nothing
   goes between this fetch and the write: no further questions, no further reads, no
   re drafting. If anything does intervene, fetch again.
5. Splice onto the **write fetch** body and send `version = write fetch version + 1`.

**Never send a body captured before the approval gate.** Your draft is content, a set of
rows or a section body, not a snapshot of the page. Splicing the approved content onto a
stale body is the exact mechanism by which another session's work disappears, and it
looks like a successful write from your side.

### Comparing the two fetches

| Draft version vs write version | Target section changed? | What to do |
|---|---|---|
| Same | n/a | Splice and write normally |
| Moved | No | Another session wrote a different section. Splice onto the new body, write, and tell the user you layered onto version N and what moved |
| Moved | **Yes** | **Stop. Do not write.** Another session wrote *your* section |

That last row is the case that loses work. Show the user what the section says now versus
what you drafted from, and ask whether to merge the two, replace what is there, or abandon
your draft. Never resolve it yourself: an overwrite here silently discards content someone
just approved in another terminal.

### Optimistic locking, and never blind retry

Send the version number explicitly, always. It is the only lock available, and its whole
purpose is to make a concurrent save fail loudly instead of quietly winning.

- **Never omit the version** and never use a force, overwrite, or minor edit option that
  bypasses the check.
- **A rejected write is information, not an obstacle.** Re fetch, re compare per the table
  above, re decide. Bumping the number and retrying is not a fix, it is the clobber.
- Do not retry more than once without telling the user what conflicted.

### Prove the diff before you write

Before sending, compare your outgoing body against the write fetch body. **The only
difference must be inside the target section.** If anything outside it differs, your
splice boundary is wrong. Stop and re splice rather than writing and checking after.

Cheap checks that catch a clobber, all worth running:

- **Heading census.** Same set of headings, same order, before and after.
- **Length sanity.** An append should make the body longer. A prose replace should be
  within a sane range of the old one. A body that shrank when you appended a row means
  you dropped something.
- **Macro and image census.** Same count of `<ac:structured-macro>`, `<ac:image>`, and
  `<ac:inline-comment-marker>` before and after.

### Working with several terminals

The skill cannot serialise sessions it cannot see, so some of this is on the author:

- **Safest is one session per page at a time.** Parallel terminals on one page are what
  produced the clobbering.
- **Queue rather than write, then flush once.** Fewer writes means fewer windows in which
  a concurrent save can be lost. The queue directory is shared per page, so two terminals
  queueing different sections of one page flush together correctly. See
  `pending-writes.md`.
- **Never two sessions on the same section**, even briefly. Two sessions on different
  sections of the same page is survivable because of the write fetch, but only if both
  follow it.
- **Approve promptly.** The exposure window is between the write fetch and the write,
  which the protocol keeps to a single call. A draft that sat unapproved for twenty
  minutes is fine, that is what the write fetch is for; a slow approval does not make the
  write unsafe, but a long gap does raise the chance the target section moved underneath
  it.
- **Parallel work is safer across pages than within one page.** If you are running four
  terminals, four pages is fine, four sections of one page is not.
- If the user is clearly running several sessions on one page, say so once and suggest
  splitting by page or running the sections in sequence.

### If a clobber has already happened

Say so immediately and plainly. Do not attempt to reconstruct the lost content from
memory: Confluence page history has it exactly. Give the user the version number to
restore, name the section that was lost, and let them revert. Reconstructing from your
own context produces something that looks right and is not.

## Locating a section

Sections are delimited by headings, not by any structural container. To find the
Background & Context section you find its heading element and take everything up to the
next heading at the same or higher level.

1. Determine the heading level the target section uses. Do not assume `h2`. Some designs
   use `h1` for top level sections and some `h2`, and the Scope tables usually sit one
   level below a `Scope` parent.
2. Match the heading text **fuzzily**: case insensitive, ignore leading numbering (`3.`,
   `3.1`, `A.`), ignore trailing colons, treat `&` and `and` as equivalent, treat
   hyphens and dashes in `Scope - In Scope` as interchangeable, ignore surrounding
   whitespace and formatting markup inside the heading.
3. The section body is everything from immediately after the heading until the next
   heading of the same or higher level, or the end of the page.
4. A heading nested deeper than the target belongs to the target's section. Do not stop
   at it.

If no heading matches, **stop and ask.** Do not append the section at the end of the
page and do not guess at a nearby heading. Report which headings you did find so the
user can point you at the right one.

## Heading aliases

The template drifts between designs. Accept these variants:

| Canonical | Also accept |
|---|---|
| Background & Context | Background, Context, Background and Context, Problem Statement |
| Recommended Solution Overview | Solution Overview, Recommended Solution, Proposed Solution, Solution Summary |
| Current Solution | Current State, As Is, As-Is Architecture, Existing Solution |
| Target Solution | Target State, To Be, To-Be Architecture, Proposed Architecture |
| Scope - In Scope | In Scope, In-Scope, Scope (In Scope) |
| Scope - Out of Scope | Out of Scope, Out-of-Scope, Not in Scope, Exclusions |
| Key Design Decisions | Design Decisions, Key Decisions, Architecture Decisions |
| Components Impacted | Impacted Components, Affected Components, Systems Impacted |
| Regulatory, Compliance, and Privacy Considerations | Compliance Considerations, Regulatory Considerations, Privacy Considerations, Compliance & Privacy |
| Licensing & Cost Considerations | Cost Considerations, Licensing Considerations, Commercial Considerations, Cost & Licensing |
| Telemetry Considerations | Observability Considerations, Monitoring & Logging, Telemetry & Observability |
| Infrastructure, Network, & Integration | Infrastructure & Integration, Network & Integration, Infrastructure, Integration Architecture |
| Data and Information Considerations | Data Considerations, Information Management, Data Architecture |
| Applicable Reference Architectures | Reference Architectures, Related Reference Architectures, Applicable RAs |

An alias match is still a match. **Write to the heading as it exists on the page. Do not
rename the user's heading to the canonical form.**

## Mapping table columns

Eleven sections are tables. The schemas in the section reference files are the default
for a table you are building fresh. **For a table that already exists, the page wins.**

1. Read the header row before drafting.
2. Map your content onto the columns that are there, in their order.
3. If the page has a column your schema does not, write `TBC` rather than leaving the
   cell empty or dropping the column.
4. If your schema has content the page has no column for, **do not add a column.** Tell
   the user what did not fit and ask.
5. Match column names fuzzily, the same way as headings. Known variants worth
   recognising:

| Table | Canonical column | Also seen |
|---|---|---|
| Risks | Mitigation | Migration (long standing typo in some template copies) |
| Risks | Residual Rating | Residual, Post Mitigation Rating |
| Glossary | Acronym/term | Term, Acronym, Item |
| Components Impacted | Impacts | Impact, Change, Description of Change |
| Scope | Product/Business Owner | Owner, Business Owner, Product Owner |
| Applicable Reference Architectures | Why this is relevant/applicable | Relevance, Rationale, Applicability |

Where a variant is a plain typo, still write to the heading as it exists. Mention it to
the user once so they can fix the template if they want, but do not correct it as a side
effect of an unrelated edit.

## Splice rules by write mode

**Replace prose** - discard the existing section body, insert the new body. Keep the
heading element byte identical. **If the section is not empty, do not choose this mode
unilaterally**: offer refine instead, per `refine.md`. Discarding content the user wrote by
hand or via Rovo is indistinguishable from discarding your own earlier draft, and only one
of those is safe.

**Refine prose** - the same splice as replace prose, but the new body is derived from the
existing one rather than from a brain dump. Mechanically identical, reviewed differently:
show a before and after. See `refine.md`.

**Replace callouts, keep diagram** - used by Current Solution, Target Solution, and
Infrastructure. Copy the diagram element verbatim into the new body in its original
position relative to the text, then replace only the prose or bullets. See
`diagrams.md`.

**Append one row** - locate the first table inside the section, append one `<tr>`
immediately before `</tbody>`. Do not rebuild the table. Do not reorder rows. Do not
touch the header row. If the section has no table, build one from the schema and say so
in your confirmation.

**Append rows, batch** - the same, with several `<tr>` appended in order immediately
before `</tbody>`. Still one write. Which sections batch and which do not is in the
section index in `SKILL.md`; Key Design Decisions and Risks are the two that do not.

**Merge and dedupe** - read existing rows, work out which candidates are genuinely new,
append only those. Report the count skipped. Match loosely when deduping. For Glossary
only, also sort the whole table alphabetically after merging, preserving existing
descriptions verbatim.

**Flush several sections** - used by `/write-pending`. Apply each queued entry's own write
mode from the list above, in document order, onto one freshly fetched body, then write
once. Each splice lands in a different section, so boundaries must not overlap: if two
entries resolve to the same heading, stop and ask rather than applying both. Full protocol
in `pending-writes.md`.

For every append mode, **check for a near duplicate before adding.** Re recording an
existing design decision with slightly different wording is worse than not recording it,
because reviewers cannot tell which is current. Where entries are pending in the queue,
dedupe against those too; they are rows that exist, just not yet on the page.

## Storage format reference

If the connector returns and accepts Confluence **storage format** (XHTML like), the
rules below apply. If it returns **ADF** (`atlas_doc_format`, a JSON document tree),
work in the JSON structure instead and preserve unknown node types verbatim. Detect
which you have from the fetched body. Do not assume, and note that the claude.ai
Atlassian connector and the Claude Code Atlassian MCP server may differ on this.

```html
<h2>Key Design Decisions</h2>
<table>
  <tbody>
    <tr>
      <th><p>Decision</p></th>
      <th><p>Rationale</p></th>
    </tr>
    <tr>
      <td><p>Mint portal session tokens via /login/federated</p></td>
      <td>
        <ul>
          <li><p>Avoids exposing Cognito tokens to the legacy portal</p></li>
          <li><p>Keeps token minting server side</p></li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>
```

Non obvious rules that cause most breakage:

- **Every cell's content must be wrapped in a block element**, `<p>` or `<ul>` or
  similar. Bare text in a `<td>` renders but corrupts on the next editor save.
- **List items wrap their text in `<p>`** inside table cells.
- Header cells are `<th>` and only in the first row. Column widths live in `<colgroup>`
  if present. Preserve it untouched.
- Self close void elements: `<br />`, not `<br>`. The parser is strict.
- Escape `&` as `&amp;` in text content, including inside headings you are matching
  against. `Licensing &amp; Cost Considerations` is what is actually in the markup.
- No `<div>` or `<span>` wrappers around your content. They survive the write and then
  get stripped unpredictably by the editor.
- Internal links are `<ac:link><ri:page ri:content-title="Page Title" /></ac:link>`, not
  `<a href>`. Use this for the Link column in Applicable Reference Architectures. To
  give the link different text, add
  `<ac:plain-text-link-body><![CDATA[Link text]]></ac:plain-text-link-body>` inside the
  `<ac:link>`.
- Macros in cells are covered in `confluence-macros.md`. Read it before writing Key
  Design Decisions, Components Impacted, or Assumptions.

## Things you must never touch

Copy these across verbatim wherever they appear. They are irreplaceable from your side
because their attributes reference server side state:

- `<ac:structured-macro>` blocks of any kind: table of contents, info and warning
  panels, status lozenges, Jira issue filters, expand blocks, code blocks, Lucid embeds.
- `<ac:image>` and `<ri:attachment>` elements, including the block diagrams in Current
  Solution, Target Solution, and Infrastructure.
- `<ac:task-list>`, since checkboxes carry completion state.
- `<ac:inline-comment-marker>`. These anchor reviewer comments. Destroying one orphans a
  review comment thread, which is both rude and invisible.
- `<time datetime="..." />` date elements.

If a macro sits inside a section you have been asked to replace, do not silently discard
it. Surface it: "this section contains an info panel and an embedded diagram, keep them
above the new text, below it, or remove?"

## Write and verify

1. **Write fetch.** Immediately after approval, with nothing between it and step 3.
   Compare its version against the version you drafted from and act per the table in
   "Concurrent sessions".
2. Splice the approved content onto **this** body. Diff the result against it and confirm
   the only change is inside the target section.
3. Write the full modified body with `version = write fetch version + 1`.
4. Provide a version comment naming the section, for example
   `Claude: appended Key Design Decision (token minting approach)`. **Always name the
   section**: when several sessions are writing one page, this is what makes history
   readable and tells the user which terminal did what.
5. Re fetch and confirm your content is present, the heading set is unchanged, and the
   macro and image counts match. Any shortfall means you ate something. Say so
   immediately rather than reporting success.

## Failure modes

| Symptom | Cause | Response |
|---|---|---|
| Version conflict on write | Someone saved concurrently | Re fetch and compare per "Concurrent sessions". Re splice onto the new body if your section is untouched; stop and ask if it is not. Never bump the version and retry |
| A section written earlier in the session has reverted or vanished | Another session wrote a stale body over it | Stop writing to this page. Give the user the history version to restore and say which section was lost. Do not reconstruct it |
| Content renders as escaped text | Body sent with the wrong representation flag | Check the representation parameter matches the format you produced |
| Table collapses on next editor save | Missing `<p>` wrappers in cells | Rewrite the affected rows properly |
| Status lozenge renders grey | Used `color` instead of `colour` | See `confluence-macros.md` |
| Headings disappeared after write | Splice boundary ran past the next heading | Restore from page history immediately and tell the user which version to revert to |
| Diagram gone after write | Diagram element not carried across | Restore from history. Never reconstruct an embed by hand |
| Section heading not found | Template variant | Consult the alias table, then ask. Never append blind |
