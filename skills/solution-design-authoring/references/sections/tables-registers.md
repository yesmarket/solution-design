# Register Tables

Covers **Risks**, **Assumptions**, **Issues**, **Dependencies**, and **Constraints**.
All append one row per invocation.

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
if it does not. At least one bullet should address the failure case. An assumption whose
failure would break the design should also be raised as a candidate risk; flag it, do
not write to the Risks table.

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
