---
name: solution-design-authoring
description: Draft and write individual sections of a Solution Architecture Detailed Design page in Confluence, following the house template and formatting conventions. Use this whenever the user wants to fill in, draft, update, append to, or review any section of a detailed design or HLD, including Background & Context, Recommended Solution Overview, Glossary, Scope, Current/Target Solution, Key Design Decisions, Components Impacted, Security / Regulatory / Licensing / Telemetry / Data considerations, Infrastructure & Integration, Risks, Assumptions, Issues, Dependencies, Constraints, and Applicable Reference Architectures. Use it even when the user just pastes a brain dump of context and names a section, or says something like "add a design decision", "write up the scope", "populate the glossary", or "audit this design for gaps". Also use it when reviewing an existing design page for completeness, when scanning a design for terms that belong in the Glossary, or when normalising how acronyms are expanded across a page.
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
   say so at the end and offer. Do not write. For a table section this means one
   section, not one row: most table sections take every row the brain dump supports in
   a single pass, see the section index. The only exceptions to the one section rule
   are the two whole document sweeps, `/glossary-scan` and `/acronym-sweep`, which by
   definition read the entire page, and only one of which writes across sections. Queueing
   a section for a later batched write does not relax this: one invocation still drafts
   one section, the write is simply deferred.
3. **Always show the draft and ask whether to proceed before writing.** These are
   shared pages under active review and a bad write is expensive to unpick. Ask with
   the interactive question tool (`AskUserQuestion` in Claude Code) so the user picks
   an option instead of typing an approval word. See "Asking the user" below. Never
   silently wait for the user to volunteer approval.
4. **Never invent technical facts.** If the brain dump is thin, write what is
   supported and list the specific gaps. A short honest section beats a padded one.
5. **Never write a page body you fetched before the approval gate.** Confluence replaces
   the whole body on every write, so a stale body silently deletes whatever another
   session saved in the meantime. Fetch again immediately after approval, splice onto
   that, and send the version number explicitly. Full protocol in
   `references/confluence-mechanics.md`, "Concurrent sessions". This is the rule that
   stops parallel terminals from clobbering each other's sections.

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
| Interactive question (`AskUserQuestion`) | The approval gate, and any either/or question | Ask the same question as plain text in chat |
| Filesystem read and write | Persisting the pending write queue across invocations | Keep the queue in the conversation only, and say so once. See `references/pending-writes.md` |

Resolve exact tool names and parameter schemas at call time rather than relying on
memory of them. They differ between the claude.ai Atlassian connector and the Claude
Code Atlassian MCP server, and they change between versions.

Assume no code execution and no subagents. Everything this skill does must work from tool
calls and chat output alone. A filesystem is used for one thing only, persisting the
pending write queue, and the skill degrades to a conversation held queue without it.

## Workflow

1. **Resolve the target page.** If the user gave a URL, page ID, or title, use it. If
   a page was established earlier in the session, reuse it and state which page you
   are writing to. Otherwise ask once.
2. **Check for pending writes on that page** and read the section reference file for the
   requested section. Do both before drafting, not after. Pending entries are part of the
   page's effective state and several drafting checks depend on them. See
   `references/pending-writes.md`.
3. **Draft fetch: fetch the current page body.** Always. You need the existing content
   for context, the surrounding markup, and for table sections the actual column headers.
   **Record the version number and the target section's current markup**; you will
   compare against both before writing.
4. **For table sections, map to the columns that exist on the page**, not the columns
   in the reference file. See `references/confluence-mechanics.md`.
5. **Draft the content.**
6. **Show the user the proposed content and ask whether to proceed with the write.**
   Render as markdown in chat, with a one line note on what will be replaced versus
   appended and which version you drafted against, then put the approval gate to the user
   per "Asking the user" below. Do not just show the draft and wait; ask.
7. **If the user chose to queue rather than write, store the entry and stop here.** No
   fetch, no write. Confirm what is pending and that the page is unchanged. See
   `references/pending-writes.md`.
8. **On approval to write, write fetch: fetch the body again**, with nothing between that
   fetch and the write. Compare its version and its copy of your target section against
   what you recorded in step 3, splice the approved content onto **this** body, and write
   with the version set explicitly. See "Concurrent sessions" in
   `references/confluence-mechanics.md` for what to do when the version has moved.
9. **Confirm** with the page URL, the version you wrote, and a one line summary of what
   changed. Verify the heading set and the macro and image counts survived.

## Asking the user

Every question this skill puts to the user goes through the interactive question tool
(`AskUserQuestion` in Claude Code) when it is available, so the answer is a click
rather than typed text. That covers the approval gate, which page to target when it is
ambiguous, which column mapping to use when the page headers do not match the
reference file, and any either/or judgement call in a section reference.

The approval gate is always the same four options:

| Option | Meaning |
|---|---|
| Write it to the page | Splice and write exactly what was shown |
| Queue it and continue | Hold the draft as a pending write, change nothing on the page |
| Revise first | Do not write. Take the user's changes and show the draft again |
| Do not write | Leave the page untouched. Output the draft for manual copy-paste |

**Order them by the mode the user is in.** `Write it to the page` goes first for the first
section of a session; once anything is pending, `Queue it and continue` goes first,
because batching is evidently what the user is doing. Queueing exists so several sections
can be drafted and reviewed, then written in one operation, which is both faster and
safer than one write per section. Full protocol in `references/pending-writes.md`.

Keep option labels short enough to read at a glance and put the recommended one first.
The tool always offers a free text escape, so do not add an "other" option yourself,
and do not ask a question whose answer is already in the conversation.

Where the tool is unavailable, for example on claude.ai, fall back to a direct text
prompt such as "Shall I write this to the page?" and treat a plain "yes" or "go ahead"
as sufficient to proceed.

## Section index

| Section | Type | Write mode | Reference |
|---|---|---|---|
| Background & Context | Prose | Replace | `sections/narrative.md` |
| Recommended Solution Overview | Prose | Replace | `sections/narrative.md` |
| Current Solution | Diagram + callouts | Replace callouts, keep diagram | `sections/narrative.md` |
| Target Solution | Diagram + callouts | Replace callouts, keep diagram | `sections/narrative.md` |
| Glossary | Table | Merge, dedupe, sort | `sections/tables-scope.md` |
| Scope - In Scope | Table | Append rows, batch | `sections/tables-scope.md` |
| Scope - Out of Scope | Table | Append rows, batch | `sections/tables-scope.md` |
| Applicable Reference Architectures | Table | Merge, dedupe | `sections/tables-scope.md` |
| Key Design Decisions | Table | Append **one** row | `sections/tables-decisions.md` |
| Components Impacted | Table | Append rows, batch | `sections/tables-decisions.md` |
| Risks | Table | Append **one** row | `sections/tables-registers.md` |
| Assumptions | Table | Append rows, batch | `sections/tables-registers.md` |
| Issues | Table | Append rows, batch | `sections/tables-registers.md` |
| Dependencies | Table | Append rows, batch | `sections/tables-registers.md` |
| Constraints | Table | Append rows, batch | `sections/tables-registers.md` |
| Security Considerations | Prose | Replace | `sections/considerations.md` |
| Regulatory, Compliance, and Privacy Considerations | Prose | Replace | `sections/considerations.md` |
| Licensing & Cost Considerations | Prose | Replace | `sections/considerations.md` |
| Telemetry Considerations | Prose | Replace | `sections/considerations.md` |
| Data and Information Considerations | Prose | Replace | `sections/considerations.md` |
| Infrastructure, Network, & Integration | Diagram + prose | Replace prose, keep diagram | `sections/considerations.md` |

### Batch tables versus one at a time

**Batch** tables take every item the brain dump supports in a single invocation. Draft
the full set, show it as one table, approve once, write once. Splitting them across
invocations wastes a full page read and write per row for no benefit.

**Key Design Decisions and Risks are one row per invocation.** Both carry judgement the
user needs to weigh individually: a decision's rationale and implications, a risk's
Possibility/Impact pair. Batching them produces rows nobody actually reviewed. If a
brain dump clearly contains several, draft the first, write it, then offer the next.

### Bare lists for Assumptions, Issues, Dependencies, and Constraints

For these four the brain dump is normally a plain list: one item per line, bullet markers
present or absent, and no implications written out. Read it literally, one non-empty line
to one row, and **derive the Implication or Impact column yourself** rather than asking
the user for it. Where a line already carries its own consequence, use the user's wording
instead of your own. Deriving means inferring from the item and what is already on the
page, not inventing; thin lines get the bullets you can defend plus a gap noted in chat.
Full rules and a worked example in `sections/tables-registers.md`.

Cross cutting references, read as needed:

- `references/confluence-mechanics.md` - splice rules, heading matching, storage
  format. Read before any write.
- `references/pending-writes.md` - the queue: draft several sections, write once. Read
  when a section is queued, when the user asks what is pending, and before
  `/write-pending`.
- `references/confluence-macros.md` - decision macro, status macro, tick and cross.
  Read before writing Key Design Decisions, Components Impacted, or Assumptions.
- `references/diagrams.md` - how to obtain and read a diagram. Read before Current
  Solution, Target Solution, or Infrastructure.
- `references/glossary-and-acronyms.md` - the two whole document sweeps. Read before
  `/glossary-scan` or `/acronym-sweep`.

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
- **Write for a mixed audience.** These pages are read by architects and engineers, and
  also by delivery leads, product owners, and risk, compliance and financial crime
  people. Assume a reader who is capable but not necessarily technical. Use plain
  language and short sentences. Name components precisely, then say what they do in
  ordinary words. Never use a phrasing only an engineer can parse when a plainer one
  carries the same meaning. Depth is still welcome in Infrastructure, Network, &
  Integration and in the Considerations sections, where a technical reader is a fair
  assumption. Everything else should be legible to a non engineer on first read.
- **Prose sections: 2 to 5 short paragraphs.**
- **Table cells: fragments, not sentences.** No trailing full stops on bullet points
  inside cells. Where a schema says "1 sentence", a full stop is fine.
- **Name things exactly.** Real service names, repo names, account and environment
  names. `fabricapp-merchant-application-service`, not "the merchant service". If the
  brain dump is vague about an identifier, flag it rather than smoothing it over.
- **Expand every acronym on first use, then use the short form.** See "Acronyms and the
  Glossary" below, which makes this a page level rule rather than a section level one.
- **Australian English.** Prioritise, organisation, licence (noun) and license (verb).
- **No filler.** Delete "it is important to note that", "in order to", "leverage"
  where "use" works, and any sentence that survives deletion without loss.
- **Present tense for Current Solution, declarative for Target Solution.**
- **No hedging on decisions already made.** Uncertainty belongs in Risks, Issues, or
  Assumptions.

## Acronyms and the Glossary

First use is **first use in the whole document, not first use in your section.** You
have already fetched the page body, so check it before you draft. Where sections are
pending in the queue, first use means first use in the page **as it will exist after the
flush**, so check the pending entries too.

1. If the acronym has not yet appeared anywhere on the page, write the expansion with
   the acronym in brackets: `Azure Data Factory (ADF)`, `politically exposed person
   (PEP)`, `enhanced customer due diligence (ECDD)`.
2. Everywhere after that, in your section and in every later section, use the short
   form alone: `ADF`.
3. If the acronym is already expanded somewhere above your section, use the short form
   only. Do not expand it a second time.
4. If your section sits **above** the existing first expansion, move the expansion to
   your section and say so, because the reader meets your section first.

**Every acronym, product name, or internal term you introduce is a Glossary candidate.**
That includes multi word terms that are not acronyms at all, for example "enhanced
customer due diligence" or "Risk Narrative Compliance Lens". Do not write to the
Glossary from another section's invocation; that breaks one section per invocation.
Instead, list the candidates at the end of your chat response and offer
`/glossary-scan`.

`references/glossary-and-acronyms.md` carries the full procedure for both sweeps. Read
it when running `/glossary-scan` or `/acronym-sweep`.

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

If sections are pending in the write queue, **say so before the table and list them.** The
audit reports the page as it stands, so a section sitting in the queue reads as Missing
when it is actually drafted and waiting. Say explicitly that the findings do not account
for pending entries.
