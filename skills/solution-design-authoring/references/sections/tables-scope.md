# Scope, Glossary and Reference Architecture Tables

Covers **Glossary**, **Scope - In Scope**, **Scope - Out of Scope**, and **Applicable
Reference Architectures**.

## Contents

- [Glossary](#glossary)
- [Scope - In Scope](#scope---in-scope)
- [Scope - Out of Scope](#scope---out-of-scope)
- [Applicable Reference Architectures](#applicable-reference-architectures)

---

## Glossary

**Write mode:** merge with dedupe, then sort alphabetically by term. Sorting is the one
case where rewriting the whole table is correct. Preserve existing descriptions
verbatim rather than regenerating them.

**Input:** derived. Scans the page and the session rather than taking a brain dump. Run
it late, once the narrative sections are populated.

### Schema

| Column | Format |
|---|---|
| Acronym/term | An acronym, word, or short phrase. 5 words or fewer |
| Description | What it is. **1 sentence only** |

### Procedure

1. Fetch the full page body.
2. Extract candidates from both the page content and the current session's brain dumps.
   The user may have introduced terms in conversation that are heading for the page.
3. Read the existing rows.
4. Filter using the rules below.
5. Present proposed additions as a table, with a count of candidates skipped and a
   separate list of terms found but not confidently definable.
6. On approval, merge, sort, and write.

### What to include

- **Acronyms and initialisms** used in the document: BYOC, OIDC, SHIR, CRN, TGW, DPIA.
- **Internal names an outsider would not know**: project codenames, entity names,
  subaccount names, environment names, portal names. Welcome/IQ, Humm Voice APAC.
- **Vendor product names where the product is non obvious** or easily confused: Genesys
  PureCloud BYOC, LexisNexis Bridger.
- **Terms this document uses in a specific narrow sense** that differs from the general
  one. These are the highest value entries and the easiest to miss.

### What to exclude

- Terms a peer architect certainly knows: API, HTTP, TLS, JSON, SQL, VPN, CI/CD, AWS,
  Azure.
- Terms appearing once in passing with no bearing on the design.
- Anything already present under any casing or formatting variant. Match loosely when
  deduping: SIT and sit are one entry, and so are "Genesys PureCloud" and "Genesys
  Cloud (PureCloud)". Prefer the existing wording.

The audience test: a peer architect, and a delivery lead who is not an engineer. If the
delivery lead would stall on it, include it.

### Description style

One sentence. Expansion first, then a clause of clarification only if the expansion is
not self explanatory.

> **BYOC** - Bring Your Own Carrier, the Genesys model where SIP trunking is provided
> by a third party carrier rather than by Genesys.

Do not define a term using another undefined acronym. If you must, add that one too.

**If you cannot define a term confidently, do not guess.** List it in chat as "found but
not defined, please supply". A wrong glossary entry propagates into every document that
copies the table.

---

## Scope - In Scope

**Write mode:** append one row. On a first invocation against an empty table, several
rows in one pass is acceptable if the brain dump clearly enumerates them; confirm the
full set with the user before writing.

### Schema

| Column | Format |
|---|---|
| Scope Item | 1 sentence to 1 paragraph |
| Product/Business Owner | Name |

### Rules

- **Each item must be independently testable as in or out.** "Improved security" is not
  a scope item. "MFA enforcement on the broker portal" is.
- **Name the boundary, not the ambition.** Scope items are deliverables and systems, not
  outcomes.
- In Scope permits a full paragraph where an item needs qualification. Use it when the
  item has a meaningful edge, for example which environments or which customer segments
  are covered. Do not pad short items to a paragraph.
- **Product/Business Owner is a person**, and a real one. `TBC` is acceptable. Do not
  guess, and do not put a team name in a column asking for a name without saying so.
- **Read the Out of Scope table before appending.** The two must not contradict. Flag
  any overlap rather than writing it.

---

## Scope - Out of Scope

**Write mode:** append one row.

### Schema

| Column | Format |
|---|---|
| Scope Item | 1 sentence |
| Rationale | 1 sentence |
| Product/Business Owner | Name |

### Rules

- One sentence only for the item here, unlike In Scope. If it needs a paragraph to
  explain, that belongs in Rationale.
- **Rationale prevents re litigation.** "Deferred to Phase 2", "covered by the separate
  Genesys migration design", "no business case at current volumes". A blank rationale
  guarantees the question comes back in every review.
- **This is the more valuable of the two tables.** When the brain dump is silent on
  exclusions, ask. Most scope disputes come from things nobody wrote down as excluded,
  and adjacent but excluded work is worth stating even when it feels obvious.
- If the brain dump for one scope table implies items for the other, note them in chat
  and offer. One section per invocation.

---

## Applicable Reference Architectures

**Write mode:** merge with dedupe.

**Input:** derived. Searches Confluence rather than taking a brain dump.

### Schema

| Column | Format |
|---|---|
| Link | Hyperlink to the RA page |
| Why this is relevant/applicable | 1 sentence |

The Link column is a proper Confluence page link, not a bare URL. See
`../confluence-mechanics.md` for the `<ac:link>` form.

### Procedure

1. Read the page's narrative sections to build a picture of the technology set: the
   platforms, services, patterns, and integrations in play.
2. Derive search terms from that set and search Confluence for reference architecture
   pages. Search iteratively rather than in one shot. A search for "Cognito" and a
   search for "observability reference architecture" return different useful sets.
3. Read enough of each candidate to judge relevance. **Never list an RA on a title match
   alone.** A title only match produces a table of plausible looking links that do not
   apply, which is worse than an empty section because reviewers assume it was checked.
4. Discard candidates that are superseded, draft, or archived unless nothing else covers
   the area. Note the status in the relevance sentence if you include one.
5. Present the proposed table, and separately list candidates you found and rejected
   with a one line reason so the user can overrule you.
6. On approval, merge and write.

### Relevance sentence

One sentence saying **why it applies and to which part of this design**. Not a
description of what the RA covers.

- Good: "Applies to the Cognito telemetry pipeline for the federated login flow."
- Bad: "Covers Cognito observability patterns on AWS."

Prefer 3 to 8 genuinely applicable RAs over an exhaustive list.

### Deviations

The two column schema has no status column, so alignment cannot be recorded in the
table. **Where the design deviates from an applicable RA, raise it in chat.** Deviations
are usually the most important thing surfaced by this exercise, and they belong in Key
Design Decisions or Risks rather than being lost. Flag them; do not write to those
tables from here.

If the Confluence search capability is unavailable, say so and ask the user for
candidate links. Do not write a speculative table from memory.
