---
name: solution-design-authoring
description: Draft and write individual sections of a Solution Architecture Detailed Design page in Confluence, following the house template and formatting conventions. Use this whenever the user wants to fill in, draft, update, append to, or review any section of a detailed design or HLD, including Background & Context, Recommended Solution Overview, Glossary, Scope, Current/Target Solution, Key Design Decisions, Components Impacted, Security / Regulatory / Licensing / Telemetry / Data considerations, Infrastructure & Integration, Risks, Assumptions, Issues, Dependencies, Constraints, and Applicable Reference Architectures. Use it even when the user just pastes a brain dump of context and names a section, or says something like "add a design decision", "write up the scope", "populate the glossary", or "audit this design for gaps". Also use it when reviewing an existing design page for completeness.
---

# Solution Design Authoring

Writes one section at a time into an existing Confluence Detailed Design page. The
user supplies an unstructured brain dump; this skill converts it into the house
format for that specific section and writes it back without disturbing the rest of
the page.

## Absolute rules

1. **Never use em dashes** in any content written to Confluence or shown to the user.
   Not in prose, not in table cells, not in bullet points. Use a comma, a colon,
   parentheses, or split the sentence. This applies to en dashes in ranges too: write
   "2 to 4 bullets", not "2 4 bullets" with a dash.
2. **One section per invocation.** Never opportunistically fill in neighbouring
   sections, even if the brain dump contains material that belongs there. If it does,
   say so at the end and offer. Do not write.
3. **Always show the draft and stop for approval before writing.** These are shared
   pages under active review and a bad write is expensive to unpick.
4. **Never invent technical facts.** If the brain dump is thin, write what is
   supported and list the specific gaps. A short honest section beats a padded one.

## Environment probe

This skill runs in both Claude Code and claude.ai, which expose different MCP servers
and different tool names for the same capability. **Dispatch on capability, never on a
remembered tool name.** At the start of an invocation, establish which of these you
have:

| Capability | Used for | If missing |
|---|---|---|
| Confluence read | Every section | Ask the user to paste the page content, then draft only |
| Confluence write | Every section | Draft and output copy-pasteable content, tell the user the write is blocked |
| Confluence search | Applicable Reference Architectures, Glossary cross-check | Ask the user for candidate RA links |
| Lucid / diagram | Current Solution, Target Solution, Infrastructure | Ask for an image paste or a written description |

Resolve exact tool names and parameter schemas at call time rather than relying on
memory of them. They differ between the claude.ai Atlassian connector and the Claude
Code Atlassian MCP server, and they change between versions.

Assume no filesystem, no code execution, and no subagents. Everything this skill does
must work from tool calls and chat output alone.

## Workflow

1. **Resolve the target page.** If the user gave a URL, page ID, or title, use it. If
   a page was established earlier in the session, reuse it and state which page you
   are writing to. Otherwise ask once.
2. **Read the section reference file** for the requested section. Do this before
   drafting, not after.
3. **Fetch the current page body.** Always. You need the existing content for context,
   the version number, the surrounding markup, and for table sections the actual
   column headers.
4. **For table sections, map to the columns that exist on the page**, not the columns
   in the reference file. See `references/confluence-mechanics.md`.
5. **Draft the content.**
6. **Show the user the proposed content and stop.** Render as markdown in chat, with a
   one line note on what will be replaced versus appended.
7. **On approval, splice and write.**
8. **Confirm** with the page URL and a one line summary of what changed.

## Section index

| Section | Type | Write mode | Reference |
|---|---|---|---|
| Background & Context | Prose | Replace | `sections/narrative.md` |
| Recommended Solution Overview | Prose | Replace | `sections/narrative.md` |
| Current Solution | Diagram + callouts | Replace callouts, keep diagram | `sections/narrative.md` |
| Target Solution | Diagram + callouts | Replace callouts, keep diagram | `sections/narrative.md` |
| Glossary | Table | Merge, dedupe, sort | `sections/tables-scope.md` |
| Scope - In Scope | Table | Append row | `sections/tables-scope.md` |
| Scope - Out of Scope | Table | Append row | `sections/tables-scope.md` |
| Applicable Reference Architectures | Table | Merge, dedupe | `sections/tables-scope.md` |
| Key Design Decisions | Table | Append one row | `sections/tables-decisions.md` |
| Components Impacted | Table | Append one row | `sections/tables-decisions.md` |
| Risks | Table | Append one row | `sections/tables-registers.md` |
| Assumptions | Table | Append one row | `sections/tables-registers.md` |
| Issues | Table | Append one row | `sections/tables-registers.md` |
| Dependencies | Table | Append one row | `sections/tables-registers.md` |
| Constraints | Table | Append one row | `sections/tables-registers.md` |
| Security Considerations | Prose | Replace | `sections/considerations.md` |
| Regulatory, Compliance, and Privacy Considerations | Prose | Replace | `sections/considerations.md` |
| Licensing & Cost Considerations | Prose | Replace | `sections/considerations.md` |
| Telemetry Considerations | Prose | Replace | `sections/considerations.md` |
| Data and Information Considerations | Prose | Replace | `sections/considerations.md` |
| Infrastructure, Network, & Integration | Diagram + prose | Replace prose, keep diagram | `sections/considerations.md` |

Cross cutting references, read as needed:

- `references/confluence-mechanics.md` - splice rules, heading matching, storage
  format. Read before any write.
- `references/confluence-macros.md` - decision macro, status macro, tick and cross.
  Read before writing Key Design Decisions, Components Impacted, or Assumptions.
- `references/diagrams.md` - how to obtain and read a diagram. Read before Current
  Solution, Target Solution, or Infrastructure.

## Right-sizing

A Detailed Design should be proportionate to the work it describes, not a fixed
template filled in regardless of scope. Both failure modes are real review problems,
not just style preferences:

- **Too big for the work** wastes a reviewer's time restating the obvious, and buries
  the few decisions that matter under sections that did not need to exist.
- **Too small for the work** gives false confidence that something complex has been
  thought through when it has not, most often visible as an empty Risks table on a
  design that clearly has risks, or a Key Design Decisions table missing a row for a
  choice the narrative already asserts as settled.

`assets/examples/sources.md` carries three house exemplars that calibrate the range:

| Size | Exemplar | Rough shape |
|---|---|---|
| Small | Managed Instinct | ~2,800 words, 6 decision rows. A single vendor migration. Risk table present but empty, correctly, the work did not surface one. |
| Medium | SSO/Federation HLD for Humm Loan | ~9,800 words. One capability built for reuse by future merchants, not just the first two. Deeper security and telemetry detail than Small because it introduces new attack surface. |
| Big | NZ DC Migration | ~19,000 words, 26 decisions, 9 DREAD-rated risks. A genuine multi-workstream programme (a data warehouse, microservices, a fraud platform, an RPA platform, HSMs, AD, office networking). One page, not split into child pages, and the length comes from distinct components and decisions rather than restating the same idea three times. |

The Big exemplar is close to a natural ceiling for a single Confluence page. If a
design grows past it, the right move is splitting out the largest table, Key Design
Decisions is usually the biggest, or a per-workstream appendix, rather than compressing
content that genuinely needs the space.

**Signals a design is bigger than its scope:**

- The same fact is restated in two or three sections instead of one section
  cross-referencing another
- A prose section runs past 5 paragraphs without introducing new information
- Components Impacted carries rows for systems with no deliverable change and no
  regression risk worth flagging (compare the legitimate "no deliberate change,
  regression test the login flow" pattern in `tables-decisions.md`, that earns a row,
  padding does not)

**Signals a design is smaller than its scope:**

- Risks, Assumptions, or Issues are empty and the conversation clearly contains
  candidates the user has not yet turned into a row
- Key Design Decisions has no row for a choice the narrative sections state as decided
- Components Impacted lists fewer systems than the Target Solution diagram shows

When drafting the first section of a new design, or in audit mode, form a view of
where the work sits on this spectrum and say so once. It recalibrates how much is
enough for every section that follows, and it is cheaper to correct at Background &
Context than after ten sections have been drafted to the wrong scale.

## House style

Applies to every section. Section references may tighten these but never relax them.

- **No em dashes.** See rule 1 above.
- **Write for a peer architect, not an executive.** Assume the reader knows what a VPC
  and an OIDC flow are. Do not explain fundamentals. The exception is Current Solution
  and Target Solution, which are read by delivery leads and business stakeholders.
- **Prose sections: 2 to 5 short paragraphs.**
- **Table cells: fragments, not sentences.** No trailing full stops on bullet points
  inside cells. Where a schema says "1 sentence", a full stop is fine.
- **Name things exactly.** Real service names, repo names, account and environment
  names. `fabricapp-merchant-application-service`, not "the merchant service". If the
  brain dump is vague about an identifier, flag it rather than smoothing it over.
- **Expand every acronym on first use**, then use the short form. If you introduce a
  new acronym, note that Glossary may need updating.
- **Australian English.** Prioritise, organisation, licence (noun) and license (verb).
- **No filler.** Delete "it is important to note that", "in order to", "leverage"
  where "use" works, and any sentence that survives deletion without loss.
- **Present tense for Current Solution, declarative for Target Solution.**
- **No hedging on decisions already made.** Uncertainty belongs in Risks, Issues, or
  Assumptions.

## Handling thin input

Do not pad. Draft what is supported, then list gaps in chat, not on the page:

> **Gaps to confirm before this section is review ready:**
> - Which Cognito user pool the federated flow targets in SIT
> - Whether the ANZ SFTP endpoint is in scope for this phase

## Audit mode

When asked to review or audit a design rather than write a section:

1. Fetch the page body.
2. Map present headings against the section index above.
3. Report per section: **Missing**, **Empty** (heading present, no content or
   placeholder text), **Thin** (present but under specified, for example Risks with no
   mitigations or Key Design Decisions with empty Other Options Considered), or **OK**.
4. Cross check for consistency: acronyms used but absent from Glossary; components
   named in Target Solution but missing from Components Impacted; decisions referenced
   in narrative but absent from Key Design Decisions; risks with no residual rating;
   assumptions marked validated with no validator named.
5. Check right-sizing against the scope of work, per the section above: sections
   restating the same fact more than once, prose running long without new information,
   or an empty Risks or Assumptions table on a design that clearly has candidates for
   one, are findings worth a line even when every section is technically present.
6. Output as a single table in chat. Write nothing to the page in audit mode.
