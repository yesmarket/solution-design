# Refining Existing Sections

How to improve a section that already has content on the page, rather than drafting one
from a brain dump. Read this whenever `-r` is passed, or when the user picks refine at the
replace gate.

## Contents

- [What refine is for](#what-refine-is-for)
- [The `-r` flag](#the--r-flag)
- [Prose sections only](#prose-sections-only)
- [The replace gate](#the-replace-gate)
- [Procedure](#procedure)
- [What refine may and may not change](#what-refine-may-and-may-not-change)
- [Showing the change](#showing-the-change)
- [Queueing a refine](#queueing-a-refine)
- [When to hand it to Rovo instead](#when-to-hand-it-to-rovo-instead)

## What refine is for

The page is the input, not the brain dump. Content already on the page may have been
written by this skill, edited by hand in Confluence, or produced by Rovo, and all three are
equally authoritative. Refine takes what is there, applies whatever new context the user
supplies, and writes it back improved.

Three situations it covers:

| Situation | What refine does |
|---|---|
| The section is fine but has drifted off house style | Normalise the style, leave the content alone |
| The user has extra context to fold in | Integrate it into what is already there |
| The user hand edited it and wants it tightened | Tighten, preserving everything they added |

Refine is **not** regeneration. Regeneration discards what is there and drafts fresh from a
brain dump; that is the replace path. If the user's new context contradicts most of the
section, say so and offer replace instead, because a refine that rewrites nine tenths of a
section is a replace pretending not to be.

## The `-r` flag

`-r` or `--refine` as the **first token** of the arguments selects refine mode. Everything
after it is additional context, and it is valid for the flag to stand alone.

```
/security -r
/security -r also mention that the signing key rotates quarterly
/background-context --refine tighten this, it runs long
```

- `-r` alone means refine against house style with no new input: fix style violations,
  tighten, change nothing factual. This is the most common use after a Rovo edit.
- `-r <context>` means fold that context into what is on the page.
- Strip the flag before treating the rest as context. Do not let `-r` leak into the drafted
  text.
- Anything that is not a leading `-r` or `--refine` is a brain dump, not a flag. Do not
  guess at other flags, and do not treat a stray hyphen mid text as one.

## Prose sections only

Refine applies to the sections whose write mode replaces a body:

Background & Context, Recommended Solution Overview, Current Solution, Target Solution,
Security, Regulatory Compliance and Privacy, Licensing & Cost, Telemetry, Data and
Information, and Infrastructure Network & Integration.

**Table sections do not refine.** They append rows, and an existing row is edited in
Confluence rather than through this skill. If `-r` arrives on a table section, say that
tables append rather than refine, and offer to append the content as new rows instead. Do
not silently rewrite a table.

For the three diagram led sections, refine the prose and callouts only. The diagram is
carried across untouched, exactly as in a normal replace. See `diagrams.md`.

## The replace gate

Refine also exists to stop a silent overwrite. **When a replace mode section already has
content and no `-r` was passed, ask before drafting**, using the interactive question tool:

| Option | Meaning |
|---|---|
| Refine what is there | Treat the page as the base, per this file |
| Replace it entirely | Discard the current content and draft fresh from the brain dump |
| Append to it | Keep the current body and add to it |
| Cancel | Leave it alone |

Show the current content, or a fair summary of it if it is long, **before** asking. The user
cannot judge whether replacing is safe without seeing what would be lost, and hand edits are
invisible to you: you cannot tell whether a paragraph came from this skill three days ago or
from the user this morning. Never assume content is yours to discard because it looks like
something you would have written.

Skip the gate only when the section is genuinely empty, or holds nothing but placeholder
text such as `TBC` or template boilerplate.

When the user chooses replace, **say plainly in the confirmation that the previous content
was discarded**, and note that page history holds it if they want it back.

## Procedure

1. **Fetch the page body**, as always. For refine this is not just context, it is the input.
2. **Extract the target section's current body** and read it properly, including anything
   that looks hand added.
3. **Identify what to change.** House style violations, the new context to fold in, and
   nothing else.
4. **Draft the revised body**, preserving everything covered under "may not change" below.
5. **Show a before and after**, per "Showing the change".
6. **Gate as normal**, with the queue option available.
7. **Write or queue**, following the ordinary write protocol in
   `confluence-mechanics.md`. A refine is spliced as a replace of the section body.

## What refine may and may not change

**May change:**

- House style violations: em dashes, hedging on settled decisions, filler, non Australian
  spelling, sentences where a fragment belongs, nested bullets in the two flat sections
- Structure, to match the shape the section reference specifies
- Wording, for clarity and for a mixed audience
- Acronym handling, per the page level first use rule
- Anything the user's new context explicitly changes
- Length, downward. Refine may cut. See below.

**May not change:**

- **Technical facts.** Service names, identifiers, hostnames, ports, versions, numbers,
  dates, owners, counts. If one looks wrong, say so in chat and leave it as it is.
- **Decisions.** A section asserting a decision is settled stays settled. Refine does not
  reopen or soften it.
- **Anything you cannot corroborate.** A fact you do not recognise is most likely something
  the user added by hand and you never saw. It is not noise. Carry it across verbatim.
- **Macros, images, inline comment markers, task lists, dates.** Per
  `confluence-mechanics.md`. Refine works around them, never through them.

The failure mode to design against is a hand added fact quietly disappearing because it was
absent from your context. That reads as an editing improvement and is data loss. If you
believe content should go, say so explicitly and let the user decide.

**Cutting is allowed and often the point**, but call it out. If the refine removes a
paragraph or a bullet, list what was removed in chat rather than leaving the user to spot
its absence in a diff.

## Showing the change

A refine is reviewed as a **change**, not as a draft. Show before and after, not just the
result: the user needs to see what moved.

- Short sections: show the current body, then the revised body.
- Longer sections: show a per paragraph or per bullet before and after for the parts that
  changed, then state plainly that everything else is unchanged.
- **Always list separately:** content removed, facts you left alone despite doubting them,
  and anything from the new context you could not place.

If nothing needs changing, say so and write nothing. A refine that produces a
cosmetically different section with the same meaning is a wasted write and a wasted review.

## Queueing a refine

Refines queue like anything else, with one difference in how conflicts resolve.

Set `writeMode` to `replace-prose` and add `"refinedFromPage": true` to the entry, since the
payload was derived from the page rather than from a brain dump.

**At flush, a conflicted refine has only one sane resolution: re-derive it.** For an append,
a changed target section can be overwritten, merged, or discarded; for a refine, the content
it was built from is gone, so its payload is not merely risky but obsolete. Do not offer
overwrite. Hold it back, tell the user the section changed after they queued the refine, and
offer to re-run the refine against the current content.

This is the case that protects a Confluence or Rovo edit made while a refine sat in the
queue, which is exactly the sequence to expect if the user is working in both places.

## When to hand it to Rovo instead

Refining in Confluence with Rovo is a reasonable choice and sometimes the better one. It
edits in place, iterates faster, and has no write protocol to get wrong.

Say so, once and without labouring it, when the user is clearly in a wordsmithing loop:
several refines of the same section in a row with no new facts.

The tradeoff worth naming, if it comes up: Rovo does not know this plugin's house rules, so
a Rovo edit can drift a section off template, and `-r` with no arguments is the cheapest way
to pull it back.
