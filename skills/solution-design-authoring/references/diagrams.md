# Diagrams

Three sections are diagram led: **Current Solution**, **Target Solution**, and
**Infrastructure, Network, & Integration**. The first two carry a high level block
diagram aimed at a mixed technical and non technical audience. The third carries the
detailed technical diagram.

The diagram is the primary source for these sections. The brain dump supplements it.

## Obtaining the diagram

Try in this order and stop at the first that works.

**1. Already embedded on the page.** Fetch the page body and look inside the target
section for an embedded diagram. It will be one of:

- A Lucid macro: `<ac:structured-macro>` with a Lucid app name, carrying a document
  ID parameter. Extract the document ID and go to step 2 with it.
- An attached image: `<ac:image><ri:attachment ri:filename="..."/></ac:image>`.
  Retrieve and view the attachment if the tooling allows it.
- An external image URL: `<ac:image><ri:url ri:value="..."/></ac:image>`.

**2. Lucid MCP server.** If available, retrieve the structured representation using
the document ID from step 1, or one the user supplies. Prefer structured output over a
rendered image; see below.

**3. Ask the user.** If neither is available, ask them to paste an image of the diagram
or describe it. Say which of the two you would prefer and why. Do not proceed to draft
a topology without one of the three.

Never fabricate a topology. A section that says "the diagram was not available, here is
what the brain dump supports" is useful. An invented architecture diagram description
is actively dangerous, because it reads as authoritative and nobody re-checks it.

## Structured output versus rendered image

**Structured output** gives shape labels, shape types, container and grouping
relationships, connector endpoints, connector labels, and direction. Use all of it.
Container relationships are especially valuable, since a shape inside a VPC container
tells you placement that no label states.

**Rendered image** requires much more caution:

- Spatial adjacency is not a relationship. Two boxes side by side may be unrelated.
- Text may be too small or partially occluded. If you cannot read a label with
  confidence, say so rather than guessing at it.
- Legends and colour keys carry meaning. Read them before the diagram body.
- Never infer a protocol, port, or direction from an unlabelled connector.

State which source you used, at the point of drafting: "read from the Lucid structured
export" or "read from the embedded PNG". The user should know how much to trust it.

## Reading rules

Apply regardless of source.

- **A diagram shows intent, not deployed reality.** Attribute rather than assert: "per
  the target state diagram, traffic traverses the Transit Gateway". Only state it flatly
  if the brain dump corroborates.
- **Arrow direction is ambiguous.** It sometimes means data flow, sometimes dependency,
  sometimes nothing. Where direction matters, ask rather than assuming.
- **Unlabelled connectors mean nothing specific.** List them as undetermined.
- **Reconcile against the page.** Cross check component names against the other
  sections. Where the diagram and the text disagree, that discrepancy is a real finding.
  Report it and ask. Do not silently pick one.
- **Watch for staleness.** A diagram containing components absent from every other
  section may predate the current design. Ask before writing them in.
- **Report what the diagram does not say.** Diagrams routinely omit protocols, ports,
  directions, auth, and error paths. Listing those omissions tells the user what to add
  to the diagram, which is genuinely useful output.

## Never touch the diagram markup

For all three sections the write mode is: **keep the existing diagram element exactly
as it is, replace only the prose or callouts around it.**

The Lucid macro and `<ac:image>` elements carry attributes that reference server side
state. Reproducing them from scratch breaks the embed. Copy the element byte for byte
into the new section body, in its original position relative to the text.

If the section has no diagram and the design clearly needs one, say so in chat as a
gap. Do not attempt to generate or embed one.

## Audience calibration

**Current Solution and Target Solution diagrams are high level and read by non
technical stakeholders.** The callouts under them must match that register: no ARNs, no
port numbers, no class names. If the brain dump is full of implementation detail, that
detail belongs in Infrastructure, Network, & Integration. Note it and offer.

**The Infrastructure diagram is the detailed one.** Ports, protocols, subnets, and
peering belong there, and the prose can assume a network engineer as reader.
