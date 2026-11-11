---
name: restock
description: "When more of a seller's Amazon FBA stock must land and how much: Amazon's Restock and planning reports and what moves them, the Restock settings and limits only Seller Central shows, lead time and its stages, the bounds Amazon sets on a plan, and the forecast and cover methods sellers, tools and research use, each as a choice. For any question about reordering, days of supply, a recommended ship-in quantity or date, or how long until new stock is sellable."
---

Ids in brackets are positions in ../../research/README.md.

## Amazon's two recommendations

- The Restock report carries per-SKU days of supply, an `Alert`, a recommended quantity and ship date, in every store but India, on the Pricing or Amazon Fulfillment role (R1).
- The planning report carries a second advice, `Recommended ship-in quantity` and `Recommended ship-in date` (R7).
- Neither formula is published, and sellers report the two disagree (R3).
- Amazon names the inputs (a demand forecast, inventory, the seller's restock settings, shipment time) and calls the result "a guide only" (R4).
- No SP-API read gives Amazon's per-SKU demand forecast (R10, T3).
- A moderator said on 2025-02-24 the Restock report will be phased out, with no date; on 2026-11-10 it carried no deprecation label (R6).

## Only in Seller Central

- Lead time, minimum order quantity, replenishment frequency and case pack are keyed per SKU there, and no SP-API read returns them (R5).
- The maximum inventory level is on the Restock Inventory page, and a shipment restriction reaches the API only as an eligibility reason or plan error (R14).
- Capacity limits reach tools by scraping or hand entry (T4).

## Bounds and lead time

- Forward days of supply rests on a forecast, while historical days of supply and the low-inventory-level fee rest on shipped units (R9).
- Amazon states receiving as stages, longer at peak, not one total (R15).
- US AWD auto-replenishment refills below a level Amazon sets per seller-ASIN, in no API model (R12).

## Methods

- Amazon's cover measures count shipped units, not ordered units (R16).
- Paid tools share one shape, (lead time + target days) × daily sales − stock held and inbound, differing in every term (R18).
- Reorder point, service level, review period and intermittent-demand forecasts are each one choice among several (R29, R31, R32).

How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.

## References

- references/reports.md: both reports, columns, Minimum Inventory Level.
- references/bounds.md: settings, bounds, capacity, events, AWD.
- references/lead-time.md: receiving, transfer, transit, closures.
- references/methods.md: sales counts, tools, safety stock, models.
- ../stock-inbound/SKILL.md: inbound as a position.
- ../stock-cost/SKILL.md: the low-inventory-level fee, the 2027 US change.
