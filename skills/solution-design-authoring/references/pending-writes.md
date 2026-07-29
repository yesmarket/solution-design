# Pending Writes

How to draft several sections across several invocations and write them to Confluence in
a single operation. Read this whenever the user queues a section, asks what is pending,
or runs `/write-pending`.

## Contents

- [Why queue](#why-queue)
- [The four option gate](#the-four-option-gate)
- [The queue directory](#the-queue-directory)
- [Queueing a section](#queueing-a-section)
- [Reading the queue](#reading-the-queue)
- [Cross checks that must read the queue](#cross-checks-that-must-read-the-queue)
- [Flushing](#flushing)
- [Conflicts at flush](#conflicts-at-flush)
- [Discarding and editing pending entries](#discarding-and-editing-pending-entries)
- [Interaction with the whole page sweeps](#interaction-with-the-whole-page-sweeps)
- [When persistence is unavailable](#when-persistence-is-unavailable)

## Why queue

Writing six sections one at a time means six read modify write cycles against the whole
page body, and six windows in which another session can lose work. Queueing them and
writing once means one window. It is the same reasoning as
`confluence-mechanics.md`, "Concurrent sessions", applied at the level of the working
session rather than the individual write.

It also decouples review granularity from write granularity. Risks and Key Design
Decisions stay one row per invocation, so each row still gets its own gate and its own
judgement call, but three rows cost one write instead of three. Do not use queueing as a
reason to batch those two sections; the per row gate is the point.

**Queueing does not relax rule 2, one section per invocation.** Each invocation still
drafts exactly one section. The queue defers the write; it does not license drafting two
sections at once.

## The four option gate

When a queue is available, the approval gate offers four options rather than three:

| Option | Meaning |
|---|---|
| Write it to the page | Splice and write now, per the normal write protocol |
| Queue it and continue | Store the draft as a pending entry, write nothing |
| Revise first | Do not write, do not queue. Take changes and show the draft again |
| Do not write | Discard the draft entirely |

**Order the options by the mode the user is evidently in.** For the first section of a
session, `Write it to the page` goes first. **Once the queue holds at least one entry,
`Queue it and continue` goes first**, because the user has already told you they are
batching.

Every confirmation after a queue action must state plainly that **nothing has been
written to Confluence yet**, and how many entries are now pending. A user who thinks a
section is saved when it is not is the worst outcome this feature can produce.

## The queue directory

**Requires a filesystem, which exists in Claude Code and does not on claude.ai.** Probe
for it per the environment table in `SKILL.md`. Without it, see "When persistence is
unavailable" at the end of this file.

One directory per page, one file per pending entry:

```
<home>/tmp/solution-design/pending/<pageId>/<nnn>-<section-slug>.json
```

Worked example, a session with three sections queued against page `4915523641`, with
`<home>` standing in for whatever the home directory resolves to on this machine:

```
<home>/tmp/solution-design/pending/4915523641/001-scope-in.json
<home>/tmp/solution-design/pending/4915523641/002-scope-out.json
<home>/tmp/solution-design/pending/4915523641/003-assumption.json
```

The `<home>` placeholder is not a literal. Resolve it before writing, and never copy an
example path from this file into a tool call.

### Resolving the path

`<home>` is **the user's home directory, resolved at runtime.** Never hardcode one. Homes
differ by platform (`/home/name`, `/Users/name`, `C:\Users\name`) and this plugin runs on
more than one machine.

- If the file tool expands `~`, write to `~/tmp/solution-design/pending/...` directly.
- If it requires a fully absolute path, resolve the home directory once per session, for
  example by reading `$HOME`, and reuse the resolved value. Do it once, not per entry.

**Do not create the directory first.** The file write creates missing parents, so write the
entry file directly at its full path. No `mkdir`, nothing to test for existence. `tmp`
under home is a conventional scratch location; if it does not exist yet, writing the first
entry creates it.

### Never inside a repository

**The queue must never be written inside the working directory.** This plugin is used from
many different repositories, and a scratch file under one of them ends up in a
`git add -A`, in a diff, or in a commit. Design content in a code repository is a leak
waiting to happen.

Before writing the first entry of a session, confirm the resolved queue path is **outside**
the current working directory. If it is not, for example because the working directory is
itself under home in a way that makes the paths overlap, or because a user supplied
location resolves into the repo, **do not write it.** Say so and ask for a location outside
the repository.

Also never use a session scoped scratch directory, even when one is offered. Those are
discarded between sessions, which defeats the one property the queue exists for: surviving
a restart.

If the user names a different location, use theirs, apply the same two tests, and say once
where entries are going.

- `<pageId>` is the Confluence page id, not the title. Titles change and are not safe as
  keys. The page title lives inside the entry so listings stay readable.
- `<nnn>` is a zero padded sequence number, one higher than the highest already in the
  directory, starting at `001`. It fixes the order entries are applied in and keeps two
  terminals from choosing the same filename.
- `<section-slug>` is the command slug, for example `scope-in`, `key-design-decision`.
- The extension is always `.json`. Ignore any file in the directory that is not a `.json`
  entry rather than trying to parse it.

**One file per entry, written once and never rewritten.** This is deliberate: an
append only queue cannot be clobbered by a second terminal, which is the same failure
mode the two fetch rule exists to prevent. Never consolidate the directory into a single
JSON file, and never read modify write an existing entry file. To change an entry, delete
it and write a new one.

Because the key is the page id and the path is user level rather than session level, a
queue survives a terminal restart and is **visible to every terminal working on that
page**. Two sessions queueing different sections of one page therefore flush together
correctly, which is the intended behaviour.

### Entry format

```json
{
  "pageId": "123456789",
  "pageTitle": "Solution Design - Merchant Onboarding",
  "section": "Scope - In Scope",
  "sectionSlug": "scope-in",
  "headingOnPage": "In Scope",
  "writeMode": "append-rows",
  "draftedAgainstVersion": 47,
  "targetSectionMarkupAtDraft": "<...storage format of the section body as read...>",
  "payload": "<...storage format ready to splice...>",
  "payloadMarkdown": "| Scope Item | Owner |\n|---|---|\n| ... | ... |",
  "notes": "Two rows. Owner TBC on both, user to confirm."
}
```

- `payload` is **finished markup, ready to splice.** Flush applies queued work, it does
  not re draft it. If the payload would need re drafting at flush, the entry was queued
  too early.
- `payloadMarkdown` is what you showed the user at the gate. Keep it so the flush summary
  and any later listing can be rendered without reconstructing anything.
- `draftedAgainstVersion` and `targetSectionMarkupAtDraft` are what make the conflict
  check at flush possible. Both are mandatory.
- `writeMode` is one of `replace-prose`, `replace-keep-diagram`, `append-rows`,
  `merge-dedupe`, matching the splice modes in `confluence-mechanics.md`.
- `refinedFromPage` is `true` when the payload was derived from the section's existing
  content rather than from a brain dump. It changes how a conflict resolves at flush, see
  below. Omit it otherwise.

Do not invent a timestamp field. Use the file's modification time if you need to reason
about staleness.

## Queueing a section

1. Draft and show the section exactly as you would for an immediate write, including the
   version you drafted against.
2. At the gate, the user picks `Queue it and continue`.
3. Read the queue directory for this page to find the next sequence number.
4. Write one new entry file. Do not touch existing entries.
5. Confirm: the section queued, the count now pending, the list of pending sections, and
   an explicit statement that **nothing is on the page yet** plus the command to write
   them (`/write-pending`).

If the same section is already pending, say so and offer to replace the existing entry
(delete then write) or keep both, which for an append mode means both sets of rows land.
Never silently supersede.

## Reading the queue

Before drafting any section, **check for pending entries on the target page.** They are
part of the page's effective state even though they are not on it yet. Mention them once
at the start rather than per section.

If entries exist for a **different** page than the one being targeted now, say so once so
the user knows work is pending elsewhere, then leave them alone.

## Cross checks that must read the queue

These checks currently read the fetched body. Once a queue exists they must read the body
**plus every pending entry for that page**, in document order, or they produce wrong
output:

- **Acronym first use.** First use is first use in the page as it will exist after the
  flush. If `/scope-in` is pending with `Azure Data Factory (ADF)` expanded, a later
  `/scope-out` draft uses `ADF` alone. Otherwise the flush produces two expansions.
- **Deduplication.** A row queued but not written is still a row. Dedupe against pending
  entries as well as against the page, and against your own batch.
- **In Scope versus Out of Scope contradiction.** Read the other table's pending entries
  before drafting either one.
- **Glossary candidates.** Terms introduced by pending sections are candidates, and
  `/glossary-scan` must see them.
- **Right sizing and audit mode.** `/dd-audit` reports on the page as it stands. When
  entries are pending it must say so explicitly, list which sections they cover, and
  state that its findings do not account for them. An audit that silently reports a
  section as Missing when it is sitting in the queue is misleading.

## Flushing

Triggered by `/write-pending`, or by the user saying to write, flush, or push the pending
work.

1. **List the queue first.** Show every pending entry as a numbered summary with its
   section, write mode, and `payloadMarkdown`. This is the last review before the page
   changes, so show the content rather than only the section names.
2. **One approval for the whole flush**, through the interactive question tool. Offer
   write all, drop specific entries, or cancel. Do not re ask per entry; each entry was
   already approved at its own gate.
3. **Write fetch.** One fetch of the current body, per `confluence-mechanics.md`.
4. **Reconcile against the fresh body**, per "Conflicts at flush" below.
5. **Run the acronym pass across the merged set** in document reading order, so exactly
   one expansion survives per acronym. This is the one place where queued payloads may be
   adjusted, and the adjustment is wording only.
6. **Splice every entry onto the one body, in document order**, applying each entry's own
   write mode. Diff the result against the write fetch body and confirm the only changes
   are inside the target sections of queued entries.
7. **One write**, version explicitly set to the write fetch version plus one, with a
   version comment naming every section written, for example
   `Claude: wrote 4 pending sections (In Scope, Out of Scope, Assumptions, Constraints)`.
8. **Verify**, then **delete the entry files that were written.** Delete only on
   confirmed success.

**A failed write leaves the queue intact.** Never delete entries speculatively, never
delete an entry you dropped from the flush without saying so, and if the write fails
report which entries are still pending. A half consumed queue is worse than a failed
flush because the user cannot tell what landed.

**If the write succeeded but the cleanup did not**, because a delete was denied or errored,
say so prominently: the sections are on the page and their entries are still in the queue.
Name the files and ask the user to remove them. Do not report the flush as clean.

That case degrades safely rather than double writing, because of the conflict check: a
written but uncleaned entry now has a target section that differs from
`targetSectionMarkupAtDraft`, since your own write changed it. The next flush holds it back
automatically instead of appending its rows a second time. Rely on that as a backstop, not
as a reason to skip reporting the failure.

## Conflicts at flush

Per entry, compare `draftedAgainstVersion` and `targetSectionMarkupAtDraft` against the
freshly fetched body:

| Entry's target section | What to do |
|---|---|
| Unchanged since the entry was queued | Include in the flush normally |
| Changed since the entry was queued | **Hold it back.** Do not write it |

Write the clean entries, hold back the conflicted ones, and report exactly that: which
sections landed, which did not, and what the page now says in each conflicted section
versus what the entry holds. Then ask per conflicted entry whether to overwrite, merge,
or discard.

**A conflicted entry with `refinedFromPage` has only one sane resolution: re-derive it.**
Its payload was built from content that no longer exists, so overwriting would discard the
newer edit and merging two versions of the same prose is not meaningful. Do not offer
overwrite. Say the section changed after the refine was queued, and offer to re-run the
refine against the current content. This is the case that protects a Confluence or Rovo edit
made while a refine sat in the queue, which is exactly the sequence to expect when the user
is working in both places.

Holding back rather than cancelling the whole flush is deliberate. One stale entry should
not block five good ones, and partial success is safe here **only because it is reported
precisely.** Say which entries remain pending, every time.

## Discarding and editing pending entries

- **List** on request: read the directory, render the summaries.
**Write shell paths with `~/`, not an expanded home.** Where a step needs a shell command,
clearing flushed entries being the only one, write it as
`rm -f ~/tmp/solution-design/pending/<pageId>/<file>` rather than substituting the resolved
home directory. The shell expands the tilde, and a permission rule written against `~/` only
matches a command that literally contains `~/`, so an expanded path turns a pre approved
cleanup into a prompt. File tool paths are the opposite case: those need the resolved
absolute path.

- **Discard one**: delete its file, confirm which section is no longer pending.
- **Discard all**: delete the directory contents, and state the count so an accidental
  discard is visible immediately.
- **Edit**: never edit an entry file in place. Re draft the section, gate it again, delete
  the old entry, write a new one.

Deleting a pending entry destroys unwritten work with no page history to recover it from,
unlike a bad write. Confirm before any discard, and never discard as a side effect of an
unrelated action.

## Interaction with the whole page sweeps

`/glossary-scan` and `/acronym-sweep` read and rewrite the entire page. Running either
against a body that is missing queued sections produces a sweep that is wrong the moment
the queue lands.

- **`/acronym-sweep`: flush first.** Tell the user there are pending entries and that the
  sweep should run after them. Do not run it against a page with pending entries unless
  the user insists after being told.
- **`/glossary-scan`: include pending entries in the scan**, since its purpose is finding
  candidates, and candidates in the queue are still candidates. Say that it covered the
  page plus N pending sections.
- Both may themselves be queued, and follow the same entry format.

## When persistence is unavailable

On claude.ai, or anywhere the filesystem probe fails, the queue lives in the conversation
only. The feature still works, with two changes:

- **Say so once**, when the first section is queued: pending work exists only in this
  conversation and is lost if it ends.
- **Render the full payload for every queue action**, not a summary, so the content is
  recoverable by scrolling back.
- **Nudge toward flushing** once about three sections are pending, rather than letting the
  queue grow indefinitely.

Everything else, the four option gate, the cross checks, the single write, the conflict
handling, is identical.
