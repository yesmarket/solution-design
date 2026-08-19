# Integrations Table

Covers **Integrations**: the index of every data flow between systems in this design.

**Write mode:** append all rows the brain dump supports, in one pass. Draft the complete
set, show it as one table, approve once, write once.

**Input:** a brain dump, usually prose rather than a list, plus the diagram where the
page has one. Connectors on a Current or Target Solution diagram are integration
candidates, so read `../diagrams.md` when a diagram is available and reconcile against
it before drafting.

## This table is an index, not the detail

Integrations and the **Integration Interfaces** part of Infrastructure, Network, &
Integration describe the same flows at two different depths, and content routinely lands
in the wrong one.

| Belongs in Integrations | Belongs in Infrastructure, Network, & Integration |
|---|---|
| That the flow exists, and between which systems | Ports, protocols, subnets, peering |
| How it is delivered, at one word of resolution | Authentication method and credential location |
| Which components carry it | Payload structure, error and retry behaviour |

A reader should be able to scan Integrations and know how many integrations this design
has and what they connect, without reading a paragraph. Detail that does not survive
that test goes in the Infrastructure section, and this table stays one line per row.

## Schema

| Column | Format |
|---|---|
| Name | Noun phrase naming the flow. **5 words or fewer** |
| Delivery Mode | How the data moves. One value, plus a cadence in brackets where known |
| Source | Exact name of the system the data originates in |
| Destination | Exact name of the system the data lands in |
| Approach | Component chain, or one short clause. **One line** |

## Column rules

**Name** names the flow, not the systems either side of it: those already have their own
columns. "Nightly arrears extract", not "Snowflake to Katabat integration". A noun phrase
reads better than a verb phrase in a list of twelve, so prefer "Contact outcome return
file" over "Send contact outcomes". No trailing full stop. If two rows would take the
same name, the name is not specific enough yet.

**Delivery Mode** is how, and how often, the data moves. One value from the preferred
vocabulary:

| Value | Use for |
|---|---|
| Batch | Scheduled bulk transfer, file or query based, on a timetable |
| API | Synchronous request and response, on demand |
| Event | Published or streamed messages, emitted as things happen |
| Webhook | Callback the source posts to the destination when something changes |
| Message queue | Asynchronous point to point through a broker |
| Manual | A person moves it: an export, an upload, an emailed file |

Add the cadence or trigger in brackets where the brain dump gives one: `Batch (nightly)`,
`Batch (every 15 minutes)`, `API (on call arrival)`, `Manual (weekly)`. Leave the brackets
off rather than guessing a schedule.

**Match the page before the vocabulary.** If the table already uses other values, for
example `Real time` or `SFTP batch`, use what is there and stay consistent with it. Do not
restate existing rows into this list.

**Source and Destination** are the systems that own the data at each end, named exactly as
the rest of the page names them, and identically in every row: `Snowflake`, `Salesforce`,
`Genesys`, `Katabat`. Two rules do most of the work:

- **Middleware is never a Source or a Destination.** Azure Data Factory moving a file from
  Snowflake to Katabat is Source `Snowflake`, Destination `Katabat`, with ADF named in
  Approach. It carries the data, it does not own it. This is the most common error in this
  table and it makes the integration count look larger than it is.
- **Source is where the data originates, not who initiates the call.** A Genesys screen pop
  that pulls account context from Salesforce has Source `Salesforce` and Destination
  `Genesys`, even though Genesys makes the request. Note the initiator in Approach where it
  is not obvious.

Where a flow is genuinely bidirectional, **one row per direction** if the two directions
carry different payloads, run on different schedules, or use different modes, which is
usually the case. A single request and response exchange is one row.

Where the source is a file a person maintains rather than a system, name the artefact:
`Hardship tracker spreadsheet`, not `Ops team`. A team is not a source.

**Approach** is the component chain, written in the direction the data flows, using ASCII
arrows:

```
Snowflake -> ADF -> SFTP -> Katabat
```

Where a middleware component pulls from one side and pushes to the other, and that is the
clearer reading, the outward form is also fine:

```
Snowflake <- ADF -> Katabat
```

Pick one form and use it consistently down the whole table. Name the actual components in
the chain, not their categories: `MuleSoft`, not "the integration layer". Where the chain
alone leaves something material unsaid, add at most one short clause after it, for example
"Genesys initiates on call arrival". If it needs a second clause, it belongs in
Infrastructure, Network, & Integration.

> **Escape the arrows.** In Confluence storage format `<` must be written `&lt;` and `>`
> as `&gt;`, so `Snowflake <- ADF -> Katabat` goes on the wire as
> `Snowflake &lt;- ADF -&gt; Katabat`. An unescaped `<-` makes the body invalid XHTML and
> the write either fails or silently eats the rest of the row. No escaping is needed in
> ADF (`atlas_doc_format`), where cell text is a JSON string. If the page already uses
> `->` characters, match them rather than converting the table.

## Deriving rows from prose

The brain dump for this section is normally a paragraph describing what talks to what, not
a bare list, so the row count is yours to determine. **One distinct data flow is one row.**
Split when any of these differ: the pair of systems, the direction, the payload, or the
delivery mode. Do not split a single flow because it moves several files or tables.

Every row needs all five columns, and the brain dump will not supply all five. Derive
Delivery Mode and Approach from what is described, keep Source and Destination to names
that already appear on the page, and where a cadence or a component genuinely is not
stated, write `TBC` and list it as a gap in chat rather than inventing a schedule.

## Worked example

Brain dump supplied by the user:

> we push the arrears file to katabat nightly, it comes out of snowflake and adf picks it
> up and drops it on their sftp. katabat send us back a contact outcome file the same way
> each morning. also the collections agents in genesys need account context, that's a real
> time lookup from salesforce via mulesoft when the call lands. and the ops team manually
> uploads the hardship spreadsheet into salesforce each week for now.

One invocation, four rows, shown together and approved once:

| Name | Delivery Mode | Source | Destination | Approach |
|---|---|---|---|---|
| Nightly arrears extract | Batch (nightly) | Snowflake | Katabat | `Snowflake -> ADF -> SFTP -> Katabat` |
| Contact outcome return file | Batch (daily, morning) | Katabat | Snowflake | `Katabat -> SFTP -> ADF -> Snowflake` |
| Agent account context lookup | API (on call arrival) | Salesforce | Genesys | `Salesforce -> MuleSoft -> Genesys`, Genesys initiates |
| Weekly hardship upload | Manual (weekly) | Hardship tracker spreadsheet | Salesforce | Analyst uploads by hand, interim until automated |

Note what happened to the input:

- **ADF, SFTP and MuleSoft appear only in Approach.** None of them is a Source or a
  Destination. Four systems own data here, not seven.
- **Row 2 is its own row, not a note on row 1.** Different payload, different direction,
  different owner. Two integrations, and they will fail independently.
- **Row 3's Source is Salesforce** although Genesys makes the call. The account data
  originates in Salesforce. The initiator is a clause in Approach.
- **Row 4 is written down rather than skipped.** A manual step is an integration, and it is
  usually the one that breaks, so it earns a row and an honest `Manual` mode.
- The dump named no file format, no auth, and no failure handling. None of that belongs in
  this table, but Infrastructure, Network, & Integration will need it, so say so in chat.

## Before appending

- **Deduplicate.** The same Source and Destination pair carrying the same payload is the
  same integration however it is named. Flag it rather than appending a near duplicate.
  This skill does not edit existing rows, so tell the user what you would have changed.
- **Cross check Components Impacted.** Every system in Source or Destination should have a
  row there. Missing ones are candidates: list them in chat and offer
  `/component-impacted`. Do not write them, one section per invocation still holds.
- **Cross check the diagram.** Where the page carries a Current or Target Solution diagram,
  every labelled connector is a candidate row and every row should be traceable to
  something on it. Report both kinds of mismatch rather than silently picking one, per
  `../diagrams.md`.
- **Cross check the names.** A system called `Genesys` here and `Genesys Cloud` in
  Components Impacted reads as two systems to anyone scanning the page. Match the wording
  already in use.
