# Exemplar Sources

Confluence page links for the three house exemplars, kept here instead of stored PDFs.
Fetch a page via the Atlassian MCP server (`getConfluencePage`, `contentFormat: "html"`)
when you need a fresh extract. The splices already pulled into the reference files are
a snapshot as of the date below; they do not update themselves if the source page is
edited later.

| Size | Design | Link | Word count | What it's good for |
|---|---|---|---|---|
| Small | Managed Instinct | [5074124823](https://humm-group.atlassian.net/wiki/spaces/ADVE/pages/5074124823/Managed+Instinct) | ~2,800 | Straightforward single integration, moving a fraud platform to a vendor managed PaaS. Concise Background & Context, well grouped Security Considerations (5 subheadings). Risk table exists but is empty, no worked risk row on this page. |
| Medium | SSO/Federation HLD for Humm Loan | [4798742565](https://humm-group.atlassian.net/wiki/spaces/ADVE/pages/4798742565/SSO+Federation+HLD+for+Humm+Loan) | ~9,800 | One capability built for reuse (federated auth and SCIM provisioning for future merchants, not just the first two). Dense Key Design Decisions row, well grouped Telemetry Considerations. Its Assumptions table has only 3 columns, no "By", a real instance of the "map to the page's own columns" rule. Risk table also empty. |
| Big | NZ DC Migration | [5249073739](https://humm-group.atlassian.net/wiki/spaces/ADVE/pages/5249073739/NZ+DC+Migration) | ~19,000 | Multi-workstream programme (data warehouse, microservices, a fraud platform, an RPA platform, HSMs, AD, office networking), one page, not split into child pages. The only one of the three with a populated, DREAD rated Risk row, and a 26 row Key Design Decisions table. Used to calibrate right-sizing (see `SKILL.md`) and to confirm the real Rating and Residual Rating format. |

Fetched and extracted 2026-07-28.

## What this settled

- **Macro markup** (`../confluence-macros.md` VERIFIED MARKUP slots). All three pages
  render the status, decision, and tick macros as `data-type="..."` HTML attributes
  (what the Atlassian MCP server returns for `contentFormat: "html"`), not the classic
  `ac:*` XML the file previously guessed at. Confirmed independently across three
  pages, so treat it as settled for this connector, not provisional. The old `ac:*`
  forms are kept as a fallback for a connector that returns storage XHTML instead, per
  `confluence-mechanics.md`.
- **Risk rating format** (`../sections/tables-registers.md`). All three pages use a
  `Rating (Possibility/Impact)` pair as the headline value, for example `Low/High`.
  None derive a separate "Overall" by averaging DREAD sub-values. Where DREAD applies,
  the five sub-attributes appear as bulleted supporting narrative underneath that
  judgement call, not as inputs to a formula that produces it. The former placeholder
  ("mean of sub values, round up on a tie") did not match any of the three real pages
  and has been replaced.

## What's still open

- None of the three sampled Assumptions tables has a populated cross (not validated)
  alongside a tick in the same table, only ticks. If a worked cross example matters,
  pull one from a fourth page.
- No page in this sample uses the expand macro for a dense risk cell. Still
  unverified in practice.
- The `data-state="DECIDED"` value was the only decision state observed across 45
  sampled decision items. Whether Confluence's decision macro supports an
  open/undecided state in this connector's HTML form is still unconfirmed.

## Redaction note

Extracts spliced into the reference files have customer names, addresses, and named
individuals replaced with bracketed placeholders (`[REDACTED-CUSTOMER]` and similar),
per the note in this directory's `README.md`. Internal product and system names (Humm,
Cognito, Predator, Instinct, and so on) are left intact since they carry no credential
risk and are load bearing for the structural exemplar.
