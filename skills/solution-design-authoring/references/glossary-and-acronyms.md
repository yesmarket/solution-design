# Glossary and Acronym Sweeps

Two whole document passes, run late, once several sections are populated. Both read
the entire page rather than one section, which makes them the exception to one section
per invocation. Neither invents content: one proposes Glossary rows, the other changes
how existing terms are written.

Read `sections/tables-scope.md` for the Glossary schema and the include/exclude rules
before running the first of these.

## Contents

- [Glossary scan](#glossary-scan)
- [Acronym sweep](#acronym-sweep)

---

## Glossary scan

**Command:** `/glossary-scan`. **Write mode:** merge, dedupe, sort. One write at the
end, not one per term.

Finds terms on the page that a reader would stall on, then walks them one at a time so
the user decides what earns a row. This is deliberately slower than the batch tables:
a wrong Glossary entry propagates into every document that copies the table, and the
user is the only one who can confirm a house definition.

### Procedure

1. Fetch the full page body, plus anything the user has said in this session that is
   heading for the page.
2. Extract candidates. Cast wider than acronyms:
   - **Acronyms and initialisms**, expanded or not: ADF, PEP, ECDD, SHIR, DWH, FIU
   - **Multi word domain terms** used as though they are settled: "enhanced customer
     due diligence", "suspicious matter reporting", "customer screening"
   - **Vendor and product names**, especially modular ones where the module matters:
     "Risk Narrative Compliance Lens", "LexisNexis Bridger", "WhereScape RED"
   - **Internal system and environment names**: Select, Instinct, Predator, DWHProd
   - **Terms this document uses in a narrower sense than the general one**
3. Read the existing Glossary rows and drop anything already present under any casing
   or formatting variant.
4. Apply the exclude rules in `sections/tables-scope.md`. The audience test is now the
   mixed audience in `SKILL.md`: if a delivery lead or a compliance reader would stall
   on it, it belongs in the Glossary, even when every engineer on the page knows it.
5. Present the full candidate list up front, so the user can see the size of the job
   before committing to it. Group it: acronyms, product names, domain terms, internal
   systems.
6. **Walk the candidates one at a time.** For each, propose the one sentence
   description and ask, using the interactive question tool, whether to add it. Offer:
   add as drafted, add with different wording, skip, and stop the walkthrough. Keep a
   running list of accepted rows.
7. If you cannot define a term confidently, say so instead of guessing, and offer to
   add it with the description left for the user to supply.
8. At the end, show the accepted rows as one table, merge them into the existing
   Glossary, sort the whole table alphabetically, and write **once**.

### Stopping early

If the user stops the walkthrough partway, write the rows accepted so far and list the
candidates not yet reviewed so the next run can pick them up. Do not discard them
silently.

---

## Acronym sweep

**Command:** `/acronym-sweep`. **Write mode:** replace, across multiple sections, in a
single write.

Enforces the acronym rule in `SKILL.md` across the whole document: an acronym is
expanded exactly once, at its first appearance in reading order, and written short
everywhere after.

This pass changes wording only. It must not add facts, reorder content, or touch any
table structure, macro, or embed.

### Procedure

1. Fetch the full page body.
2. Build the list of acronyms in play, in **document reading order**, including any
   already present in the Glossary.
3. For each acronym, find every occurrence and classify it:
   - **First occurrence expanded correctly** as `Expansion (ACRONYM)`: leave it
   - **First occurrence not expanded**: expand it
   - **First occurrence expanded without the bracketed short form**: add the brackets
   - **Later occurrence still expanded**: collapse it to the short form
   - **Later occurrence expanded again in brackets**: collapse it to the short form
4. Watch for reading order traps:
   - The page properties header table sits above every section and counts as document
     start. An acronym first appearing there is first used there.
   - A term first expanded in a section that was written later but sits **higher** on
     the page still counts as first use, because the reader meets it first.
   - Table cells count. An acronym whose first appearance is inside a Key Design
     Decisions cell is expanded there.
5. Never expand an acronym you cannot expand with confidence. List it instead and ask.
6. Present the changes as a before and after list grouped by acronym, with the section
   each change lands in, so the user can scan it without diffing the page.
7. On approval, apply every change in one write.

### What this pass does not do

- It does not add Glossary rows. Run `/glossary-scan` for that, and say so if the sweep
  surfaces acronyms with no Glossary entry.
- It does not rewrite sentences for style, even where the collapse leaves the sentence
  slightly awkward. Flag those individually and let the user decide.
- It does not touch acronyms inside a quoted statement attributed to a person, since
  changing quoted wording misrepresents the speaker.
