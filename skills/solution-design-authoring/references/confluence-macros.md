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

Before emitting a macro for the first time on a given site:

1. Fetch a page that already uses it. A previously completed design is ideal. Any page
   with a status lozenge will do for the status macro.
2. Copy the exact markup, including parameter names, casing, and any `ac:macro-id` or
   `ac:schema-version` attributes.
3. Reuse that shape. **Drop any `ac:macro-id`**, since it should be unique per
   instance; Confluence regenerates it. Keep everything else.
4. Write the verified markup back into this file under the relevant section so the
   next invocation does not have to rediscover it.

If no example exists on the site, use the form below, write it to a scratch page
first, and confirm it renders before touching a real design.

If the connector returns ADF rather than storage format, these XHTML forms do not
apply. Macros in ADF appear as `extension` or `inlineExtension` nodes with their
parameters in an attrs object. Same procedure: find a real example, copy its shape.

## Status macro

Used in Components Impacted. Three permitted values with fixed colours.

| Value | Colour parameter |
|---|---|
| New | `Green` |
| Existing | `Yellow` |
| Decommission | `Red` |

Best known storage format:

```html
<ac:structured-macro ac:name="status">
  <ac:parameter ac:name="colour">Green</ac:parameter>
  <ac:parameter ac:name="title">New</ac:parameter>
</ac:structured-macro>
```

Notes:

- The parameter is `colour`, British spelling. `color` is silently ignored, which
  produces a grey lozenge and no error. If your status lozenges come out grey, this is
  why.
- Valid colours are Grey, Red, Yellow, Green, and Blue. Nothing else.
- The macro is inline. It still needs a `<p>` wrapper inside a table cell.
- Never use a fourth status value. If the brain dump describes a component as
  "modified" or "changed", that is `Existing`, and the nature of the change goes in the
  Impacts column.

<!-- VERIFIED MARKUP: paste the confirmed form from your site here once checked -->

## Decision macro

Used for the Decision column in Key Design Decisions.

Confluence exposes decisions through the decision blueprint, and the storage
representation has varied across versions. Candidate forms, in order of likelihood:

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

**Do not guess between these.** Follow the discovery procedure at the top of this file
against a real Humm design page that already uses the macro. This is the one to verify
first, because Key Design Decisions is the most frequently appended table and a broken
decision macro will be replicated across every row before anyone notices.

Fallback while unverified: write the decision as plain bold text in the cell and tell
the user explicitly that the macro was not applied and the cell needs manual
conversion. A plain text decision that renders is better than a broken macro that
does not.

<!-- VERIFIED MARKUP: paste the confirmed form from your site here once checked -->

## Tick and cross

Used for the Validated column in Assumptions.

Best known storage format:

```html
<ac:emoticon ac:name="tick"/>
<ac:emoticon ac:name="cross"/>
```

Notes:

- Inline element, needs a `<p>` wrapper in a table cell.
- Self closing, with the slash. The parser is strict.
- Newer Confluence may render these as emoji nodes instead. If a fetched page shows
  emoji rather than `ac:emoticon`, match what the page uses rather than mixing forms
  within one table.
- **Never write a tick unless the brain dump names who validated the assumption and
  how.** An unvalidated assumption gets a cross and a blank or `TBC` in the By column.
  Marking assumptions validated by default defeats the purpose of tracking them, and it
  is the kind of thing that gets discovered during an incident.

<!-- VERIFIED MARKUP: paste the confirmed form from your site here once checked -->

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
