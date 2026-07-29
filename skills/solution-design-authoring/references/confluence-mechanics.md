# Confluence Mechanics

How to change one section of a page without damaging the rest. Read this before any
write.

## Contents

- [The core constraint](#the-core-constraint)
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
  saved between your read and your write, the write either fails or clobbers them. Keep
  the gap between read and write short: fetch immediately before writing, not at the
  start of a long drafting conversation.

If drafting took a while, **re fetch the body before writing** and confirm the version
has not moved.

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
heading element byte identical.

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

For every append mode, **check for a near duplicate before adding.** Re recording an
existing design decision with slightly different wording is worse than not recording it,
because reviewers cannot tell which is current.

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

1. Re fetch the body. Confirm the version number matches what you read earlier.
2. Write the full modified body with `version = current + 1`.
3. Provide a version comment describing the change, for example
   `Claude: appended Key Design Decision (token minting approach)`. This makes page
   history readable and lets a reviewer diff exactly what changed.
4. Re fetch and confirm your content is present and the page still has the same set of
   headings it had before. A heading count that dropped means you ate a section. Say so
   immediately rather than reporting success.

## Failure modes

| Symptom | Cause | Response |
|---|---|---|
| Version conflict on write | Someone saved concurrently | Re fetch, re splice onto the new body, warn the user their edit is layering on someone else's |
| Content renders as escaped text | Body sent with the wrong representation flag | Check the representation parameter matches the format you produced |
| Table collapses on next editor save | Missing `<p>` wrappers in cells | Rewrite the affected rows properly |
| Status lozenge renders grey | Used `color` instead of `colour` | See `confluence-macros.md` |
| Headings disappeared after write | Splice boundary ran past the next heading | Restore from page history immediately and tell the user which version to revert to |
| Diagram gone after write | Diagram element not carried across | Restore from history. Never reconstruct an embed by hand |
| Section heading not found | Template variant | Consult the alias table, then ask. Never append blind |
