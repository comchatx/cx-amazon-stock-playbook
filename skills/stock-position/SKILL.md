---
name: stock-position
description: "Where a seller's Amazon FBA stock is: every state Amazon names and which units can be bought now, `getInventorySummaries`, the inventory reports and the Inventory Ledger and where they do not tie, pooled stores (Pan-EU, Remote Fulfillment) and other programs and regions, AWD stock the door's five roles cannot read, and how fresh each read is. For any question about how many units a seller holds, where, and in what state."
---

## States

Amazon names five FBA states: fulfillable ("can be picked, packed, and shipped"), inbound, reserved, unfulfillable ("cannot be sold") and researching (W1).
`getInventorySummaries` returns one summary per seller SKU and marketplace; its `totalQuantity` includes inbound (W2, W35).
`fulfillableQuantity` is what could be fulfilled in that marketplace, not what sits in that country (W6).
Reserved is customer orders, transfers between centres and FC processing (W9).
On FC-transfer units, a moderator's post of 2024-08-26 says buyable; the *Inventory Buyability* help page, as the listing seat read it on 2026-10-14, says reserved units are not (W10).
Units sold ahead of receipt through In-Stock Head Start sit inside inbound (W17).
Each tool's "sellable" is its own definition (W43).

## Reports and the ledger

The MYI reports are current snapshots; the Inventory Ledger holds 18 months of signed movements (W21, W27, W32).
The ledger carries no inbound and keeps units between centres apart from the ending balance; its tie to the API's states was read in Amazon's documents and not yet seen on a live store (W28).
The API's reserved total includes FC transfer; tools describe Seller Central's without it (W12).
A file's header row states its columns, which change without notice (W13, A3).

## Pooled stores

Under Pan-European FBA, developers report each marketplace returning the same EU sum, read in developers' reports and not yet seen on a live store (W18).
Remote Fulfillment with FBA sells US stock in Canada, Mexico and Brazil (G8).

## AWD

AWD quantities need the Amazon Warehousing and Distribution role, which the five roles do not include; no FBA report has an AWD column (W38, W39).

## Freshness

A near real-time FBA report is remade at most every 30 minutes, a daily one every four hours (W20).
The planning report states no update frequency and carries three dates per row (W23).

How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.

## References

[states.md](references/states.md): states, reserved, researching, SKUs, tools.
[reports-and-ledger.md](references/reports-and-ledger.md): reports, ledger, ties, freshness.
[programs-and-regions.md](references/programs-and-regions.md): programs, regions, AWD.
[reads-and-roles.md](references/reads-and-roles.md): reads, roles, notifications.
[seller-central-only.md](references/seller-central-only.md): what no API returns.
