# Confluence Macros

Three table columns require macros rather than plain text:

| Section | Column | Macro |
|---|---|---|
| Key Design Decisions | Decision | Decision macro |
| Components Impacted | Status | Status macro (coloured) |
| Assumptions | Validated | Tick or cross |

## Discover before you emit

**Macro markup is the single most likely thing in this skill to be wrong**, because
macro names and parameters differ between Confluence versions, between storage format
and ADF, and between Cloud and Data Center. The forms below are starting points, not
gospel.

**For Claude Code against this Atlassian MCP server, this is now settled.** All three
verified forms below were confirmed 2026-07-28 against three real Humm design pages,
see `../assets/examples/sources.md`. They came back as Confluence's newer ADF-derived
HTML (`data-type` attributes on plain tags), not the classic `ac:*` storage XML this
file originally assumed. Use the verified form first.

Still verify from scratch when any of these differ from what got you here:

- A different environment: claude.ai's Atlassian connector, a self hosted Atlassian
  MCP server, or Confluence Data Center. These may return storage XHTML or raw ADF
  JSON instead of this HTML form.
- `getConfluencePage` called with a different `contentFormat` (`markdown` or `adf`
  rather than `html`).
- A macro type not covered below (the expand macro, at the end of this file, is still
  unverified in practice either way).

Procedure when you do need to re-verify:

1. Fetch a page that already uses it. A previously completed design is ideal. Any page
   with a status lozenge will do for the status macro.
2. Copy the exact markup, including attribute or parameter names, casing, and any
   `ac:macro-id`, `ac:schema-version`, or `data-local-id` attributes.
3. Reuse that shape. **Drop any per-instance ID attribute** (`ac:macro-id`,
   `data-local-id`), since it should be unique per instance and Confluence regenerates
   it. Keep everything else.
4. Write the verified markup back into this file under the relevant section, with the
   date and the page(s) it came from, so the next invocation does not have to
   rediscover it.

If no example exists on the site, use the classic fallback form given under each macro
below, write it to a scratch page first, and confirm it renders before touching a real
design.

## Status macro

Used in Components Impacted. Three permitted values with fixed colours.

| Value | Colour parameter |
|---|---|
| New | `Green` |
| Existing | `Yellow` |
| Decommission | `Red` |

<!-- VERIFIED MARKUP: confirmed 2026-07-28 against Managed Instinct (5074124823),
     SSO/Federation HLD for Humm Loan (4798742565), and NZ DC Migration (5249073739),
     all fetched via mcp__atlassian__getConfluencePage with contentFormat: "html". See
     ../assets/examples/sources.md. -->

Verified form, a plain `<span>`, no `ac:structured-macro` wrapper at all:

```html
<span data-type="status" data-color="green" data-status-style="bold">new</span>
<span data-type="status" data-color="yellow" data-status-style="bold">existing</span>
<span data-type="status" data-color="red" data-status-style="bold">decommission</span>
```

Notes:

- The attribute is `data-color`, American spelling, the opposite of the classic
  storage macro's British `colour` parameter in the fallback below. Do not mix the two
  spellings within one write.
- Real pages also reuse this same element in other columns for other purposes: `AWS`
  (yellow), `Azure` (blue), `phase #2` (purple), a plain descriptive tag like
  `detailed design` (neutral, no fixed meaning). Colour is contextual to the column it
  sits in, not a single global mapping beyond the three Components Impacted values.
  Do not infer a fourth Components Impacted status from a colour used elsewhere on the
  page.
- The macro is inline. It still needs a `<p>` wrapper inside a table cell.
- Never use a fourth status value in Components Impacted specifically. If the brain
  dump describes a component as "modified" or "changed", that is `Existing`, and the
  nature of the change goes in the Impacts column.
- `ac:structured-macro` was not found on any of the three pages sampled. If your
  connector returns storage format instead (see `confluence-mechanics.md`), use the
  classic fallback below and re-verify against a real page on that connector first.

### Classic storage format fallback

Unverified on this connector, kept for Data Center or a different Cloud connector:

```html
<ac:structured-macro ac:name="status">
  <ac:parameter ac:name="colour">Green</ac:parameter>
  <ac:parameter ac:name="title">New</ac:parameter>
</ac:structured-macro>
```

- The parameter is `colour`, British spelling. `color` is silently ignored, which
  produces a grey lozenge and no error. If your status lozenges come out grey, this is
  why.
- Valid colours are Grey, Red, Yellow, Green, and Blue. Nothing else.

## Decision macro

Used for the Decision column in Key Design Decisions.

<!-- VERIFIED MARKUP: confirmed 2026-07-28 against Managed Instinct (5074124823),
     SSO/Federation HLD for Humm Loan (4798742565), and NZ DC Migration (5249073739).
     45 decision items sampled across the three pages (6 + 14 + 25), all identical in
     shape. See ../assets/examples/sources.md. -->

Verified form, a decision list with exactly one item per Decision cell:

```html
<ul data-type="decision-list">
  <li data-type="decision-item" data-state="DECIDED">
    Mint portal session tokens via /login/federated
  </li>
</ul>
```

Notes:

- `data-state` was `DECIDED` on all 45 instances sampled. No other state (an open or
  proposed decision, for example) was observed in this sample, so that part of the
  value set is still unconfirmed. Ask before writing anything other than `DECIDED`.
- One `<ul data-type="decision-list">` per cell, wrapping exactly one
  `<li data-type="decision-item">`. Not a running log of multiple decisions.
- Drop `data-local-id`, the same rule as any per-instance ID: Confluence regenerates
  it.
- Neither `ac:structured-macro ac:name="decision"` nor `ac:task-list` (the two
  candidate forms this file previously guessed at) were found on any of the three
  pages sampled. Keep them below only as a fallback for a connector that returns
  storage format.

### Classic storage format fallback

Unverified on this connector, kept for Data Center or a different Cloud connector.
Confluence exposes decisions through the decision blueprint and the storage
representation has varied across versions, so if you land here, verify against a real
page before trusting either form:

```html
<!-- Form A: structured macro -->
<ac:structured-macro ac:name="decision">
  <ac:parameter ac:name="title">Mint portal session tokens via /login/federated</ac:parameter>
</ac:structured-macro>
```

```html
<!-- Form B: task-list style decision list -->
<ac:task-list>
  <ac:task>
    <ac:task-status>complete</ac:task-status>
    <ac:task-body>Mint portal session tokens via /login/federated</ac:task-body>
  </ac:task>
</ac:task-list>
```

Fallback while unverified: write the decision as plain bold text in the cell and tell
the user explicitly that the macro was not applied and the cell needs manual
conversion. A plain text decision that renders is better than a broken macro that
does not.

## Tick and cross

Used for the Validated column in Assumptions.

<!-- VERIFIED MARKUP: confirmed 2026-07-28 for the tick only, against Managed Instinct
     (5074124823, 4 instances) and SSO/Federation HLD for Humm Loan (4798742565,
     several instances). Cross unverified, see note below. -->

Verified form, an emoji node, not `ac:emoticon`:

```html
<span data-type="emoji" data-shortname=":check_mark:" data-emoji-id="atlassian-check_mark" data-emoji-text=":check_mark:">:check_mark:</span>
```

Notes:

- **No cross example was found on any of the three pages sampled.** Every Validated
  cell seen was a tick. In practice, an unvalidated assumption is represented by a
  blank cell or `TBC`, not by a rendered cross. If you need to emit an explicit cross,
  the parallel emoji shortname `:cross_mark:` is a reasonable guess but is
  **unverified**, confirm it renders on a real page before relying on it.
- Inline element, needs a `<p>` wrapper in a table cell.
- **Never write a tick unless the brain dump names who validated the assumption and
  how.** An unvalidated assumption gets a blank or `TBC` in the Validated and By
  columns. Marking assumptions validated by default defeats the purpose of tracking
  them, and it is the kind of thing that gets discovered during an incident.
- `ac:emoticon` was not found on any of the three pages sampled. Keep it below only as
  a fallback for a connector that returns storage format.

### Classic storage format fallback

Unverified on this connector, kept for Data Center or a different Cloud connector:

```html
<ac:emoticon ac:name="tick"/>
<ac:emoticon ac:name="cross"/>
```

Self closing, with the slash. The parser is strict.

## Optional: expand macro for dense cells

Risk rating cells carrying a full DREAD breakdown plus a residual rating get tall
enough to distort the table. If that becomes a problem, the overall rating can sit in
the cell with the breakdown inside an expand macro:

```html
<ac:structured-macro ac:name="expand">
  <ac:parameter ac:name="title">DREAD breakdown</ac:parameter>
  <ac:rich-text-body>
    <ul><li><p>Damage: High</p></li></ul>
  </ac:rich-text-body>
</ac:structured-macro>
```

Do not adopt this unilaterally. Ask the user once, then keep it consistent within a
document.
