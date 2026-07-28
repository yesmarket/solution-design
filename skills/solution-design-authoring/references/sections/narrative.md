# Narrative Sections

Covers **Background & Context**, **Recommended Solution Overview**, **Current
Solution**, and **Target Solution**.

The first two are prose. The last two are **a diagram followed by key callouts**, and
require `../diagrams.md` before drafting.

These are the sections a reviewer reads end to end. Everything else in the document is
reference material; these carry the argument.

## Contents

- [Background & Context](#background--context)
- [Recommended Solution Overview](#recommended-solution-overview)
- [Current Solution and Target Solution](#current-solution-and-target-solution)

---

## Background & Context

**Purpose:** why this work exists. A reader who knows nothing about the initiative
should finish this section knowing what problem is being solved, who asked, and what
constrains the answer.

**Shape:** 2 to 4 paragraphs of prose.

1. The business or operational driver. Name the trigger: a compliance deadline, a
   vendor end of life, a capability gap, a specific incident, a programme of work.
2. The current state facts a reader needs in order to understand the problem. Not the
   full current architecture, which is Current Solution. Just enough context.
3. What this document covers and its relationship to anything upstream: programme,
   epic, prior design, the HLD this DD sits under. Link Jira epics and parent pages
   where the brain dump names them.

**Do not** include the solution here. If the brain dump leads with the answer, note
that the material belongs in Recommended Solution Overview and write Background from
what is left. If nothing is left, ask for the problem statement.

**Do not** editorialise about prior decisions. "The existing integration was built
without proper consideration of..." should be rewritten as a neutral fact.

---

## Recommended Solution Overview

**Purpose:** the executive readable summary of the answer. This is the section quoted
in a steering pack. It must stand alone.

**Shape:** 2 to 4 paragraphs, or 1 to 2 paragraphs followed by a short bulleted list of
the solution's constituent parts.

1. The recommendation, in one or two sentences, up front. No build up.
2. How it works, at the level of named components and the flow between them. A reader
   should be able to draw a box diagram from this paragraph.
3. Why this over the alternatives, in one or two sentences, pointing at Key Design
   Decisions for the detail rather than repeating it.
4. Delivery shape if the brain dump covers it: phasing, what lands first, what is
   deferred.

**Constraints:**

- No implementation detail. No config values, no ARNs, no method signatures.
- Do not duplicate Key Design Decisions. Reference the table.
- Avoid vendor marketing language even when the brain dump uses it. "Provides
  enterprise grade observability" should say what it actually does.

---

## Current Solution and Target Solution

Both follow the same shape: **a high level block diagram, followed by key callouts.**
The callouts are sometimes labelled "key points" on older pages; treat them as the same
thing and keep the existing heading.

### Audience

These diagrams are deliberately high level and are read by delivery leads, product
owners, and business stakeholders alongside engineers. **The callouts must match that
register.** No ARNs, no port numbers, no class names, no subnet CIDRs. If the brain
dump is full of implementation detail, that detail belongs in Infrastructure, Network,
& Integration. Note it and offer; do not write it here.

This is the one place where the "write for a peer architect" house rule is relaxed.

### Write mode

**Keep the diagram exactly as it is. Replace only the callouts beneath it.**

The Lucid macro or embedded image carries attributes referencing server side state and
cannot be reconstructed. Copy the element byte for byte into the new section body, in
its original position. See `../diagrams.md`.

If the section has no diagram, draft the callouts from the brain dump and flag the
missing diagram as a gap. Do not attempt to generate or embed one.

### Reading the diagram

Read `../diagrams.md` before drafting. In summary: prefer the embedded diagram on the
page, fall back to the Lucid MCP server, fall back to asking the user. Never fabricate
a topology. State which source you used.

Cross check the diagram against the brain dump. Where they disagree, that is a real
finding: report it and ask rather than silently picking one.

### Callout format

Flat bulleted list. 5 to 10 callouts. Each callout is one line, one idea, no trailing
full stop. Each should be legible to someone who has just looked at the diagram and
wants to know what they are seeing.

Good callouts explain something the diagram cannot show on its own:

```
- Customer identity is held in Cognito and is the single source of truth for portal access
- The cards portal has no direct connection to Salesforce, all traffic passes through the adapter
- Batch payment files are exchanged with ANZ once daily, there is no real time path
- The Genesys contact centre remains on its existing carrier trunks and is unchanged
```

Weak callouts restate box labels:

```
- There is a Cognito user pool
- The adapter connects to Salesforce
```

Prefer callouts that state: what is authoritative for what, what is synchronous versus
batch, what is unchanged, where a trust or organisational boundary sits, and what the
diagram deliberately omits.

### Current Solution specifics

Present tense throughout. "The adapter polls Salesforce every 15 minutes", not "polled".

Callouts should cover the components in play, how they integrate at a conceptual level,
where data lives, and the specific limitations that motivate the change. State
limitations as facts, not complaints: "No structured logging is emitted from the batch
job" is useful; "logging is inadequate" is not.

Describe only what is within the blast radius of this change. A full current state
inventory belongs in a reference architecture.

### Target Solution specifics

Declarative tense. "The adapter exposes", or "the endpoint will validate". Pick one and
hold it across the section.

**Mirror the order of the Current Solution callouts** where possible. A reviewer
diffing the two mentally should not have to re orient. Where a Current callout has no
Target equivalent because that thing is going away, say so explicitly.

Be explicit about what is not changing when it would otherwise be ambiguous. This is
the single most common review comment on target state sections.

Every component named in the callouts should have a row in Components Impacted. Note
any that do not, at the end of your chat response. Do not write to that table.

---

## Style calibration

<!-- TODO(Ryan): once you have dropped example designs into ../../assets/examples/,
     replace this block with verbatim extracts of a Background & Context section and a
     Target Solution callout list you consider exemplary. The callout register in
     particular is hard to specify in rules and easy to demonstrate. -->

Until house examples are present, calibrate to: dense, specific, no adjectives that
could be deleted without loss of meaning. Roughly the register of a well written AWS
reference architecture document, with the Current and Target callouts pitched a level
above that.
