# Considerations Sections

Covers **Security**, **Regulatory, Compliance, and Privacy**, **Licensing & Cost**,
**Telemetry**, **Data and Information**, and **Infrastructure, Network, & Integration**.
All are prose and all replace the section body.

Infrastructure is diagram led and has its own rules at the end of this file. Read
`../diagrams.md` before drafting it.

## Shared shape

A short prose lead in of one or two sentences framing what is relevant for this design,
followed by grouped bullets under bold labels or subheadings. Not a wall of prose, and
not an ungrouped bullet dump.

```
The federated login path introduces a new server side token minting capability
and a new signing key. Existing Cognito controls are unchanged.

**Authentication & Authorisation**
- Cognito remains the sole identity provider, the portal never issues credentials
- ...

**Secrets & Key Management**
- Session signing key stored in Azure Key Vault, rotated quarterly
- ...
```

## Shared constraints

- **Design specific only.** No generic control catalogues. "Data is encrypted in transit
  using TLS 1.2 or above" is only worth a line if there is something notable about it in
  this design. If a category genuinely does not apply, write one line saying so and why.
  Silence reads as an oversight in review.
- **Never assert a control is in place unless the brain dump says so.** Where a control
  is expected but unconfirmed, write it as an open item and list it as a gap. Fabricated
  compliance statements are the worst failure mode in these sections, because they get
  read as assurance by people who will not verify them.
- **Point at the owning artefact** rather than restating it: an existing security
  standard page, a threat model, a reference architecture, a DPIA.
- Anything unresolved belongs in Risks or Issues too. Flag it in chat; do not write to
  those tables from here.
- These sections assume a peer architect as reader. Unlike Current and Target Solution,
  technical depth is appropriate.

## Contents

- [Security Considerations](#security-considerations)
- [Regulatory, Compliance, and Privacy Considerations](#regulatory-compliance-and-privacy-considerations)
- [Licensing & Cost Considerations](#licensing--cost-considerations)
- [Telemetry Considerations](#telemetry-considerations)
- [Data and Information Considerations](#data-and-information-considerations)
- [Infrastructure, Network, & Integration](#infrastructure-network--integration)

---

## Security Considerations

Groupings, used only where relevant:

- **Authentication & Authorisation** - identity providers, token types and lifetimes,
  service to service auth, privilege model
- **Network Exposure** - public versus private endpoints, ingress and egress paths, WAF,
  allowlists, VPN and TGW peering
- **Secrets & Key Management** - where secrets live, rotation, who can read them
- **Data Protection** - encryption at rest and in transit where non default,
  tokenisation, masking
- **Vulnerability & Supply Chain** - scanning coverage such as Snyk and SonarQube, base
  image provenance, dependency policy
- **Detection & Response** - what security telemetry reaches the SIEM or XDR platform,
  and what does not
- **Open Items** - controls not yet designed or confirmed

Call out anything that weakens an existing control or creates an exception to a
standard, explicitly and prominently. Those are what security review exists to find, and
burying one is worse than not writing the section.

Where a risk emerges that warrants DREAD scoring, note it for the Risks table rather
than rating it here.

---

## Regulatory, Compliance, and Privacy Considerations

Groupings:

- **Applicable Obligations** - name the specific regime and, where supported, the clause
  or control. Regulated lender obligations, AML/CTF, PCI DSS, APRA CPS 234 and CPS 230,
  Privacy Act and the APPs, GDPR where relevant.
- **Personal Information** - what PI is involved, collected, or newly disclosed, how it
  flows, retention
- **Data Residency & Cross Border** - where data is stored and processed, any offshore
  disclosure
- **Consent & Notification** - where consent is relied on and whether it exists
- **Records & Audit** - what must be retained, for how long, and where
- **Assessments Required** - PIA or DPIA, security assessment, vendor due diligence,
  change advisory
- **Open Items**

Do not interpret law. State the obligation as understood and route the judgement to the
accountable function: Privacy, Legal, Risk, or Compliance, naming who needs to confirm.
If the brain dump asserts a legal conclusion, attribute it ("Legal has advised that...")
rather than stating it flatly.

---

## Licensing & Cost Considerations

Groupings:

- **Licensing Impact** - products involved, licence model (per seat, per node,
  consumption, resource units), whether existing entitlement covers this
- **Run Cost** - new or changed recurring cost, with the driver and the units it scales
  on
- **Build Cost** - one off costs: professional services, migration, uplift
- **Cost Attribution** - cost centre, tagging, which entity is billed
- **Optimisation Levers** - reserved or committed pricing, tiering, retention reduction
- **Assumptions & Open Items**

**Show the shape of the maths and show the assumptions.** A cost figure without the
volume assumption behind it is a number someone will quote in a business case and be
wrong about. Give ranges, mark them clearly as estimates, and state the basis. If the
brain dump has no numbers, say what needs to be priced rather than estimating.

Currency is AUD unless stated otherwise. Note GST treatment if the input mentions it.

Any material cost assumption should also go to the Assumptions table. Flag it.

---

## Telemetry Considerations

Groupings:

- **Signals Emitted** - logs, metrics, traces, events, per component. Be specific about
  what is instrumented and what is not.
- **Collection Path** - agent, shipper, integration, or SDK, and how signals reach the
  platform
- **Retention & Tiering** - hot, warm, cold, frozen, and retention per signal type
- **Dashboards & Views** - what is built, for whom
- **Alerting** - conditions, thresholds, destination, on call routing
- **SLIs and SLOs** - where they exist or are proposed
- **Coverage Gaps**

Prefer alignment with an existing observability reference architecture over
re specifying from scratch. Link it and state the deltas.

Be honest about instrumentation that will not exist at go live. A telemetry section
describing an aspiration is how systems reach production unmonitored.

---

## Data and Information Considerations

Groupings:

- **Data Domains & Entities** - what data the design touches
- **Classification** - sensitivity per domain, using the organisation's scheme
- **Data Flows** - source, transform, destination per interface, sync or async, volumes
  and frequency
- **Storage** - datastore, format, schema ownership
- **Quality & Validation** - validation rules, reconciliation, error handling for bad
  records
- **Lineage & Ownership** - data owner and steward
- **Retention & Disposal** - retention period and deletion mechanism
- **Migration** - one off data movement, cutover, backfill, rollback

Where a flow crosses a trust or entity boundary, name the boundary. Where the design
introduces a new copy of existing data, say so explicitly. Duplicated sources of truth
are a recurring review finding.

---

## Infrastructure, Network, & Integration

**Diagram led.** Read `../diagrams.md` first. This section carries the detailed
technical diagram, as distinct from the high level block diagrams in Current and Target
Solution.

**Write mode:** keep the diagram exactly as it is, replace the prose around it.

**Audience:** a network or platform engineer. Ports, protocols, subnets, and peering
belong here. This is where the implementation detail that was excluded from Current and
Target Solution lands.

### Structure

**Hosting & Placement** - cloud, account or subscription, region, VPC or VNET, subnet
tier, cluster or service. Short paragraph or a table.

**Network Paths** - a table works best:

| Source | Destination | Protocol / Port | Direction | Path |
|---|---|---|---|---|
| SIT EKS worker subnet | ANZ SFTP endpoint | SFTP / 22 | Outbound | NAT Gateway, Site to Site VPN |

**Integration Interfaces** - per interface: the two endpoints, protocol and pattern
(REST, SFTP batch, event, message queue), synchronous or asynchronous, authentication
method, frequency or trigger, payload summary, error and retry behaviour.

**DNS & Certificates** - hostnames, zones, certificate issuer and rotation, where
covered.

**Ingress & Egress Controls** - load balancers, WAF, firewall rules, allowlists, private
endpoints.

### Rules

- Attribute anything read from the diagram rather than asserting it: "per the target
  state diagram". Only state flatly what the brain dump corroborates.
- **List what the diagram does not specify.** Protocols, ports, directions, auth, and
  error paths are routinely omitted. Naming the omissions tells the user what to add to
  the diagram, which is useful output in itself.
- Where this section and the Target Solution callouts describe the same flow
  differently, report the discrepancy and ask.
