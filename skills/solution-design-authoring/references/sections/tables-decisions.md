# Decision Tables

Covers **Key Design Decisions** and **Components Impacted**. Both append exactly one
row per invocation. Both use macros: read `../confluence-macros.md` before writing.

Never batch multiple rows from one brain dump unless the user explicitly asks. If the
dump clearly contains two decisions, draft the first, write it, then offer the second.

## Contents

- [Key Design Decisions](#key-design-decisions)
- [Components Impacted](#components-impacted)

---

## Key Design Decisions

### Schema

| Column | Format | Length |
|---|---|---|
| Decision | Short sentence, declarative, active voice. **Decision macro.** | 1 sentence, 20 words or fewer |
| Rationale | Bullet points | 2 to 4 bullets, 12 words or fewer each |
| Implications | Bullet points | 2 to 4 bullets, 12 words or fewer each |
| Other Options Considered | Bullet points, names only | 2 to 4 bullets, **5 words or fewer each** |

### Column rules

**Decision** states what will be done, not what was discussed. Starts with a verb. No
"we decided to", no "it is recommended that". Names the specific mechanism, not the
category. Wrapped in the decision macro; if the macro form is unverified, see the
fallback in `../confluence-macros.md`.

**Rationale** is why this option won. Each bullet is an independent reason. If a bullet
only makes sense as a continuation of the previous one, merge them. Rationale is not a
description of the solution: if a bullet does not answer "why this rather than
something else", it belongs in Implications or in the narrative sections.

**Implications** are what this decision commits us to or costs us. Include the
uncomfortable ones: added latency, new operational burden, a dependency on another
team, a licence uplift. A row where Implications are all upside has not been thought
through. Push back on the user rather than writing it.

**Other Options Considered** are names only, 5 words or fewer, no evaluation. The
reader wants to know the option space was explored; the reasons live in Rationale. If
the brain dump gives a long description of a rejected option, compress it to a name and
drop the rest. Never write "N/A": if no alternatives were considered, ask what else was
on the table, because there is almost always "do nothing" or "keep the existing
approach".

### Worked example

Brain dump supplied by the user:

> for the legacy cards portal SSO we're not going to pass cognito tokens directly to
> the portal, we'll add a /login/federated endpoint on the API that takes the validated
> cognito identity and mints a session token the portal understands. means the portal
> doesn't need to understand jwt or cognito at all and we don't have cognito access
> tokens floating around in the browser for a legacy app we don't fully trust. downside
> is we own another token minting path and we have to keep the portal session lifetime
> in sync with the cognito session, plus it's another hop. we looked at just doing SAML
> into the portal directly but the portal's saml support is ancient, also considered
> putting a reverse proxy in front that injects headers, and briefly talked about just
> rewriting the portal auth which is way out of scope.

Correct output:

| Decision | Rationale | Implications | Other Options Considered |
|---|---|---|---|
| *(decision macro)* Mint legacy portal session tokens via a `/login/federated` API endpoint | <ul><li>Portal needs no JWT or Cognito awareness</li><li>No Cognito access tokens exposed in browser</li><li>Token minting stays server side and auditable</li></ul> | <ul><li>Humm owns an additional token minting path</li><li>Portal and Cognito session lifetimes must stay aligned</li><li>Adds a network hop to login</li></ul> | <ul><li>Direct SAML to portal</li><li>Header injecting reverse proxy</li><li>Rewrite portal auth</li></ul> |

Note what happened to the input:

- "we're not going to pass cognito tokens directly" is the rationale, not the decision.
  The decision is the positive statement of what is being built.
- "the portal's saml support is ancient" was dropped from Other Options Considered.
  Names only. If that reason matters, it goes in Rationale as "Portal SAML
  implementation is unsupported".
- "way out of scope" was dropped for the same reason, but is a candidate for the Out of
  Scope table. Mention it to the user; do not write it.
- Every Implications bullet is a real cost. None restate the benefit.

### Rejected output patterns

| Anti pattern | Example | Fix |
|---|---|---|
| Decision describes a discussion | "It was decided to consider federating the portal" | "Mint portal session tokens via `/login/federated`" |
| Decision names a category | "Use a federated authentication approach" | Name the endpoint, service, or protocol |
| Rationale restates the decision | "Because we are minting tokens server side" | Say what that buys: "No tokens exposed in browser" |
| Implications are all benefits | "Improved security posture" | Include the operational and delivery costs |
| Other Options padded with reasons | "Direct SAML, rejected because support is ancient" | "Direct SAML to portal" |
| Other Options says N/A | "N/A" | Ask what else was considered |
| Sentences in bullets | "This will require us to keep the sessions in sync." | "Session lifetimes must stay aligned" |

### Before appending

Scan existing rows for a decision covering the same question. If one exists and the new
input supersedes it, do not append: tell the user and ask whether to amend the existing
row. If it is a different question in the same area, append, and make the Decision
wording distinguish the two clearly.

---

## Components Impacted

### Schema

| Column | Format |
|---|---|
| Component | Exact system, service, or repository name |
| Status | One of New, Existing, Decommission. **Status macro**, green / yellow / red respectively |
| Impacts | Short bullet points, 2 to 4 |
| Owner | Name of owner, or `TBC` |
| SME | Name of SME, or `TBC` |

### Column rules

**Component** is the deployable or repository at the granularity the owning team would
recognise. `fabricapp-heroku-cognito-authentication-adapter`, not "the auth adapter".
`Twilio - Humm Voice APAC subaccount`, not "Twilio". If the brain dump is vague, ask. A
row that cannot be traced to a repo or resource is not actionable.

**Status** is exactly one of three values, rendered with the status macro at the colour
given in `../confluence-macros.md`. Pick one, do not hedge.

- `New` (green): does not exist today, will be created.
- `Existing` (yellow): exists today and is touched by this design, whether modified,
  reconfigured, or merely in the blast radius and requiring regression confirmation.
- `Decommission` (red): exists today and will be retired.

If a component is in scope only for regression testing, it is still `Existing` and it
still earns a row. Say so in Impacts. Those are the ones that break.

**Impacts** describe what changes in that component, from that team's point of view.
Not the overall solution. A platform team reading only their row should know what they
have to do. For an `Existing` component with no deliberate change, say what needs
verifying.

**Owner** and **SME** are people, not teams, where the brain dump names them. `TBC` is
acceptable and honest. Do not guess. If the user names one person and it is unclear
which column they belong in, ask rather than duplicating them across both.

### Worked example

Brain dump:

> the cognito auth adapter needs the new federated endpoint added, and the cards portal
> itself needs a small change to accept the minted session token on inbound redirect.
> we'll need a new secret in key vault for the signing key. the merchant application
> service isn't changing but it shares the same cognito pool so worth regression
> testing. dave owns the adapter, priya is the SME on the portal.

Four separate invocations, one row each:

| Component | Status | Impacts | Owner | SME |
|---|---|---|---|---|
| `fabricapp-heroku-cognito-authentication-adapter` | *(green)* Existing | <ul><li>Add `/login/federated` endpoint</li><li>Mint and sign portal session tokens</li></ul> | Dave | TBC |
| Legacy cards portal (Welcome/IQ) | *(yellow)* Existing | <ul><li>Accept minted session token on inbound redirect</li></ul> | TBC | Priya |
| Azure Key Vault | *(yellow)* Existing | <ul><li>New secret for session token signing key</li></ul> | TBC | TBC |
| `fabricapp-merchant-application-service` | *(yellow)* Existing | <ul><li>No deliberate change</li><li>Shares Cognito user pool, regression test login flows</li></ul> | Dave | TBC |

Note the fourth row: the user said it is not changing and it still earns a row, with
`Existing` status and an explicit "no deliberate change" impact.

Note also that Key Vault is `Existing`, not `New`. The vault exists; the secret is new.
Status describes the component, not the change.

### Before appending

Check whether the component already has a row. If it does and the status differs, flag
the conflict rather than adding a second row for the same component.
