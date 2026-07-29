# Register Tables

Covers **Risks**, **Assumptions**, **Issues**, **Dependencies**, and **Constraints**.

**Write mode differs across the five:**

| Table | Write mode |
|---|---|
| Risks | Append **one** row per invocation |
| Assumptions, Issues, Dependencies, Constraints | Append **all** rows the brain dump supports, in one pass |

Risks stay one at a time because the Possibility/Impact pair is a judgement the user
has to weigh per row. The other four are usually enumerated in a single brain dump and
gain nothing from being split. For those, draft every row, show the complete table,
approve once, write once. Deduplicate within your own batch as well as against the
rows already on the page.

## Input convention: one line, one row

For Assumptions, Issues, Dependencies, and Constraints the user's brain dump is usually
a bare list. One item per line, with or without a leading `-` or `*`, no implications
written out. Expect that as the normal case and read it literally:

- **Each non-empty line is one row.** Do not merge two lines into a single row because
  they look related, and do not split one line into two rows unless it plainly carries
  two separate items, in which case split it and say you did.
- **Leading markers are noise.** `-`, `*`, `•`, numbering, and inconsistent indentation
  all mean the same thing. Never ask the user to reformat or re-punctuate the list.
- **A sub-bullet indented under a line belongs to that line**, as content for its second
  column. It is not a row of its own.
- **The second column is yours to author.** The user supplies the Assumption, Issue,
  Dependency, or Constraint text; you derive the Implication or Impact bullets. This is
  the default, not a fallback, so do not stop and ask what the implications are.
- **Unless the user wrote them.** If a line already carries its own consequence, after a
  colon, an `=>`, a "which means", a "so", or in an indented sub-bullet, that is the
  user's Implication or Impact. Use their words. Tighten the phrasing to house style but
  do not replace their reasoning with your own or quietly add to it.

**Deriving is inference, not invention.** An implication has to follow from the item
plus what is already on the page and in the session. Where a line is too thin to support
a confident consequence, write the bullets you can defend and list the rest as a gap in
chat, or write `TBC` in the cell. Do not manufacture a plausible sounding impact to fill
the column; a derived implication the user has not thought about is exactly the thing
that gets asserted in review as though they had.

Because the second column is inferred rather than supplied, it is the part of the draft
most likely to be wrong. The draft you show at the approval gate is the user's only
chance to catch it, so show every derived cell in full rather than summarising the table.

For Assumptions specifically, a bare line names no validator, so `Validated` defaults to
a cross and `By` to `TBC`. Do not read the absence of a validator as an invitation to
tick.

Classification still applies. A line that lands in the wrong table is worth flagging even
when the other nine are fine, per the test below.

## Shared rules

**Column mapping.** Read the existing header row and map onto the columns that are
actually there. The schemas below are the default when building a table fresh. If the
page has a column you have no content for, write `TBC` rather than leaving it empty.

Watch for the column heading `Migration` in the Risks table. That is a long standing
typo for `Mitigation` and appears in some copies of the template. Treat them as the
same column, and write to the heading as it exists on the page rather than silently
correcting it. Mention it to the user once.

**Deduplicate.** Check for an existing row on the same underlying concern before
appending. If one exists, ask whether to amend rather than adding a near duplicate.

**Cell style.** Fragments, no trailing full stops on bullets, bullets for multi part
content. Single sentence columns take a full stop.

**Classification.** These five tables are routinely confused. Use this test:

| It is a... | If... |
|---|---|
| Risk | It might happen in future and would be bad |
| Issue | It has already happened or is true now, and needs resolving |
| Dependency | Someone outside this design must deliver something |
| Assumption | You believe something is true but have not verified it |
| Constraint | Something is imposed on the design and will not change |

"We assume the API can handle 500 TPS" is an assumption. "The API is rate limited to
500 TPS" is a constraint. If the brain dump lands in the wrong table, say so and offer
to write it to the right one instead.

## Contents

- [Input convention: one line, one row](#input-convention-one-line-one-row)
- [Risks](#risks)
- [Assumptions](#assumptions)
- [Issues, Dependencies, Constraints](#issues-dependencies-constraints)

---

## Risks

### Schema

| Column | Format |
|---|---|
| Risk | Short description, 1 sentence |
| Rating | A Possibility/Impact pair, e.g. `Low/High`. DREAD sub-attributes as supporting bullets where the risk is security flavoured. See below |
| Impact | Short bullet points, 2 to 4 |
| Mitigation | Short bullet points, 2 to 4 |
| Residual Rating | Same format as Rating, after mitigations are applied |

### Rating methodology

**Confirmed against three real Humm designs** (Managed Instinct, SSO/Federation HLD,
NZ DC Migration; see `../../assets/examples/sources.md`): the headline Rating and
Residual Rating are always a **Possibility/Impact pair**, for example `Low/High`. None
of the three sampled pages derive a separate "Overall" value by averaging sub-scores.
This replaces the earlier placeholder rule (mean of DREAD sub-values, round up on a
tie), which did not match any of the three real pages.

Every sub value, where used, is one of **Very High**, **High**, **Medium**, **Low**.

**Use DREAD for security risks**: threats, vulnerabilities, and anything where an
adversary is part of the story. DREAD's five sub-attributes appear as **bulleted
supporting narrative underneath the Possibility/Impact headline**, explaining the
judgement call rather than feeding a formula that produces it:

```
Rating: Low / High
- Damage: High
- Reproducibility: Low
- Exploitability: Low
- Affected Users: High
- Discoverability: Low
```

(worked from the NZ DC Migration on-prem HSM risk: Possibility rated Low because
hardware failure is not attacker driven or easily reproducible, Impact rated High
because it is loss of card transaction processing capability, even though two of the
five DREAD sub-attributes are independently High. The pair is not the arithmetic mean
of the five sub-values, it is a separate judgement informed by them.)

**Use Possibility and Impact alone for everything else**: delivery slippage, cost
overrun, vendor behaviour, capacity, operational failure. No sub-attribute breakdown.

```
Rating: Medium / High
```

**Setting the Possibility/Impact pair is an authorial judgement.** Propose it directly
using the DREAD breakdown (where one exists) as supporting evidence in the cell. Do not
present a formula to the user as though it produces the pair; if the brain dump does
not support a confident Possibility or Impact value, propose one and mark it clearly
for the user to confirm rather than deriving it mechanically.

Do not mix methods within one document. If existing rows include a DREAD breakdown and
this new risk is not security flavoured, ask before omitting it rather than producing a
table where rows are not comparable.

If the brain dump does not support a rating, propose one and mark it clearly for the
user to confirm. Do not silently pick.

### Residual Rating

Same format, reflecting the position after the listed mitigations land.

- **Residual must be equal to or lower than Rating.** If your draft has it higher,
  something is wrong in the reasoning; stop and re-check.
- **If residual equals the original rating, the mitigations are not doing anything.**
  Say so to the user explicitly. Either the mitigations are weaker than claimed or the
  rating is not sensitive enough. This is the most useful signal in the whole table and
  it is routinely papered over.
- Residual assumes mitigations are **implemented**, not merely planned. If they are
  planned, note that in the Mitigation cell, because a residual rating that assumes
  unbuilt controls is how risk registers mislead.

### Column rules

**Risk** is one sentence. Prefer the cause and consequence form: "If federated login
volume exceeds Cognito default request rate limits, portal logins will fail at peak."
It forces the thinking and makes the Impact column easy to fill.

**Impact** is what happens if it materialises. Concrete and specific: which users,
which service, what degradation.

**Mitigation** entries are actions, not intentions. "Monitor closely" is not a
mitigation. "Request a Cognito quota increase before UAT" is. Each should be something
a person could be assigned. If the brain dump contains a fallback for after the risk
materialises, label it as contingency within the cell rather than mixing it in.

### Worked example

Brain dump: *"bit worried the portal session and cognito session getting out of sync
will cause weird half logged in states, hard to test for, we'd probably only find it in
prod. mitigation is to make the portal session strictly shorter than cognito's and add
a session validity check on each portal request."*

| Risk | Rating | Impact | Mitigation | Residual Rating |
|---|---|---|---|---|
| If portal and Cognito session lifetimes diverge, users may reach an inconsistent partially authenticated state. | Medium/High | <ul><li>Users see partial access to portal functions</li><li>Support load from unexplained login failures</li><li>Likely to surface first in production</li></ul> | <ul><li>Set portal session lifetime strictly shorter than Cognito session</li><li>Validate session state on each portal request</li><li>Add negative test cases at expiry boundaries</li></ul> | Low/High |

Possibility and Impact was used rather than DREAD, correctly: this is a correctness and
operability risk, not a threat. The third mitigation was added because the user said it
was hard to test for. Inferring that mitigation from the input is fair. Inventing an
owner would not be.

### Worked example: real DREAD row

From the NZ DC Migration exemplar (see `../../assets/examples/sources.md`), lightly
trimmed. This is a security flavoured risk, so the DREAD sub-attributes sit as
supporting bullets under the Possibility/Impact headline rather than replacing it:

| Risk | Rating | Impact | Mitigation | Residual Rating |
|---|---|---|---|---|
| Failure or irreversible degradation of on-prem payment HSM infrastructure could result in partial or total loss of card transaction processing capability, compounded by possible delay to the programme that plans to decommission these HSMs. | Low/High<ul><li>Damage: High</li><li>Reproducibility: Low</li><li>Exploitability: Low</li><li>Affected Users: High</li><li>Discoverability: Low</li></ul> | <ul><li>Loss of card transaction processing capability</li><li>Affects the entire cards portfolio</li></ul> | <ul><li>Maintain two production HSMs with workload separation</li><li>On single HSM failure, engage an external HSM provider as contingency</li><li>Retain a test HSM that can be repurposed for production with vendor assistance if required</li></ul> | Low/Medium |

Note what the DREAD breakdown is doing here: two of the five sub-attributes are
independently High (Damage, Affected Users), yet the headline stays Low/High rather
than shifting toward High/High. The breakdown is evidence for the judgement call, not
an input a formula averages. If your draft finds itself computing a mean to reach the
headline, stop, that is the placeholder rule this file no longer uses.

---

## Assumptions

### Schema

| Column | Format |
|---|---|
| Assumption | Short description, 1 sentence |
| Implication | Short bullet points, 2 to 4 |
| Validated | Tick or cross. See `../confluence-macros.md` |
| By | Who validated it, or blank |

### Column rules

**Assumption** is falsifiable and stated as a positive declarative. If it cannot turn
out to be wrong, it is a fact and belongs in a narrative section.

**Implication** is what follows if the assumption holds, and more usefully, what breaks
if it does not. At least one bullet should address the failure case. Derive it yourself
from the assumption unless the user wrote it, per the input convention above. An
assumption whose failure would break the design should also be raised as a candidate
risk; flag it, do not write to the Risks table.

**Validated** is a tick only when the brain dump names who validated it and how. A tick
is a claim that someone checked. Default to a cross. Never tick an assumption because it
seems obviously true.

**By** is a person's name. Blank or `TBC` when Validated is a cross. If Validated is a
tick, By must be populated: a validated assumption with no validator is not validated,
and you should ask rather than writing it.

### Worked example

| Assumption | Implication | Validated | By |
|---|---|---|---|
| The ANZ SFTP endpoint supports SSH key authentication. | <ul><li>No credential rotation tooling required</li><li>If false, password auth needs a vault backed rotation process</li><li>Adds roughly two weeks to delivery if false</li></ul> | *(cross)* | TBC |
| Existing Elastic entitlement covers serverless deployment at current ingest volumes. | <ul><li>No commercial approval needed for the upgrade</li><li>If false, procurement lead time blocks the target date</li></ul> | *(tick)* | J. Nguyen |

---

## Issues, Dependencies, Constraints

These three share an identical two column schema.

| Column | Format |
|---|---|
| Issue / Dependency / Constraint | Short description, 1 sentence |
| Impact | Short bullet points, 2 to 4 |

The first column is named for the table. Everything else is the same.

### Issues

Present tense, factual, currently true. "The DataComm mapping export does not include
subaccount attribution", not "may not include".

Impact says what it blocks or degrades. If it blocks nothing, question whether it is an
issue at all. Issues frequently start life as realised risks; if an existing risk row
describes this issue's cause, cross reference it in the Issue cell.

Where the brain dump contains a next step or owner and there is no column for them, say
so in chat. Do not silently discard it, and do not add a column without asking.

### Dependencies

Something outside this design's control that the design needs: another team's delivery,
a vendor action, an approval, an environment, a decision.

**Name the counterparty in the sentence.** A dependency without an owning party is a
note, not a tracked item. Be specific and completable: "Network team support" is not a
dependency; "Firewall rule permitting egress from the SIT subnet to the ANZ SFTP
endpoint on port 22, from the Network team" is.

Impact says what cannot proceed without it, and by when it is needed if the brain dump
says.

### Constraints

Something imposed that will not change: a platform limit, a policy, a contract, a date,
an architectural standard.

**Name the source in the sentence.** A constraint without a source is indistinguishable
from a preference and gets challenged in review. "All inter cloud traffic must traverse
the existing Site to Site VPN to the AWS Transit Gateway, per network standard NS-014."

Constraints are not requirements. "The solution must be highly available" is a
requirement. "Only two availability zones are provisioned in the target account" is a
constraint. A constraint that is actually negotiable should say so in the Impact cell:
that is often the most useful thing in the section.

### Worked example: bare list in, full table out

Brain dump for Constraints, exactly as pasted, no bullets, no implications:

```
all inter cloud traffic has to go over the existing site to site VPN
only 2 AZs in the target account
ANZ SFTP only supports SSH keys, no password auth
change freeze from 15 Dec to 5 Jan so cutover has to be before that
```

Four lines, four rows. The Impact column is derived in every row because the user wrote
none of it:

| Constraint | Impact |
|---|---|
| All inter cloud traffic must traverse the existing Site to Site Virtual Private Network (VPN) to the AWS Transit Gateway. | <ul><li>No direct public egress path available for the integration</li><li>Throughput bounded by the existing tunnel capacity</li><li>Network team change required for any new route</li></ul> |
| Only two Availability Zones are provisioned in the target account. | <ul><li>Quorum based components cannot be spread across three zones</li><li>Loss of one zone removes half of the deployed capacity</li></ul> |
| The ANZ Secure File Transfer Protocol (SFTP) endpoint supports SSH key authentication only. | <ul><li>No password or vault backed credential rotation path</li><li>Key lifecycle and custody process required before go live</li></ul> |
| A change freeze applies from 15 December to 5 January. | <ul><li>Cutover must complete before 15 December</li><li>No remediation window inside the freeze if cutover defects surface</li></ul> |

Note what the derivation did and did not do. Consequences follow from each line and from
what is already on the page: the Transit Gateway and the AWS account came from the
Infrastructure section, not from thin air. Nothing invented an owner, a date the user did
not give, or a mitigation. The third row is a constraint rather than an assumption
because the user stated it as fact about the endpoint; had they written "we assume the
endpoint supports SSH keys" it belongs in Assumptions, and the right move is to say so
rather than write it here.
