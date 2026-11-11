---
name: stock-inbound
description: "A seller's FBA inbound read as stock: what is on its way and in what state, when it becomes sellable, what arrived short and where the claim line falls, what each Fulfillment Inbound write charges and which cannot be undone, and where peak arrival dates are read. For any question about units sent to Amazon and not yet sellable, or about a shipment's receipt."
---

## On its way

Inbound is three quantities per SKU, not per shipment: working, shipped and receiving (W7).
Units sold ahead of receipt through In-Stock Head Start are still inside inbound (W17).
A shipment's status runs `WORKING`, `SHIPPED`, `IN_TRANSIT`, `DELIVERED`, `CHECKED_IN`, `RECEIVING`, `CLOSED` (I7).
Amazon states receiving windows as stages, not one total, in Dominic_Amazon's *FBA Receiving Times* post of 2024-08-08, restated by no later post read (R15).

## Received or short

`CLOSED` is not proof of full receipt: Amazon also closes a shipment open past a set number of days, stated for the US on sell.amazon.com *How to track FBA shipments* (I8).
Only the v0 item reads give `QuantityReceived` per shipment; otherwise receipts are in the Inventory Ledger and the Inbound Performance report (I3, I14).
For US FBA, an Amazon moderator's 2026 post gives the claim window for units missing from an inbound shipment, not its start; where each part is read: references/shortages.md (I21).
Amazon reimburses at manufacturing cost and may refuse where labels did not tie units to the shipment; the claim itself is outside this pack (I22, I23).

## Writes

A write whose response carries an `operationId` is read with `getInboundOperationStatus`; four writes answer at once (I16).
`confirmPlacementOption` cannot be reversed, and its fee is a quote on the option (I15).
Confirming a partnered-carrier option agrees to its charge; `cancelInboundPlan` cancels every shipment of the plan (I16).
Abandoning one shipment of a multi-shipment plan brings an inbound defect fee and re-prices placement (I13).

## Peak

Amazon's peak dates are arrival dates, one per placement option since 2025, published each year in News_Amazon posts on the store's seller forum; no operation returns one (I24).
Late arrivals are received without a guarantee of Prime in time (I25).

## Roles

Every Fulfillment Inbound operation needs Amazon Fulfillment; AWD inbound needs Amazon Warehousing and Distribution, which the five do not open (I1, W38).
How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.

## References

[reads.md](references/reads.md): operations, identifiers, limits, reports, eligibility.
[arrival.md](references/arrival.md): statuses, closure, delivery windows, receiving.
[shortages.md](references/shortages.md): discrepancies, claims, reimbursement.
[writes.md](references/writes.md): writes, charges, what is permanent.
[peak.md](references/peak.md): peak arrival dates as rules.
[stock-position](../stock-position/SKILL.md): every state beside inbound.
