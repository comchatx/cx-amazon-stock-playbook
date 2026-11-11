# Capacity limits, Capacity Manager, the overage fee and IPI

- What only Seller Central shows, in full: ../stock-position/SKILL.md and its references.

## The limit

- FBA capacity is one monthly limit per storage type, in volume, since 2023-03-01 in the US and Europe, 2023-05-01 in Canada and 2024-10-01 in Japan (C24).
- Amazon announces it through the Capacity Monitor and an e-mail with estimates for the following months (C24).
- Amazon says the limit is influenced by IPI, sales forecasts, shipment lead time and fulfilment-centre capacity (C24).
- New professional accounts, under a tenure in FBA that Amazon states, have no limit (US) (C24).
- The limit and its estimates are in Seller Central's Capacity Monitor only; no operation, report or reachable page gives the current limit (C24, C36).
- Amazon's US texts disagree on the week of the month the limit is announced and on how many months of estimates follow, a 2023 announcement against a 2026 staff post and help page GAFNWEYTJUV2GBFC as the listing playbook's research read it on 2026-10-14 (Q2).
- 领星 and 积加 state that they scrape the limit from Seller Central (C36).

## Usage and the overage fee

- Capacity usage is on-hand stock plus shipments created and not yet arrived, and exceeding the limit on that sum blocks new shipments (C25).
- An open shipment that is never sent counts until it is cancelled, and a removal order counts within 24 hours of creation even while pending (C25).
- The overage fee is charged only when on-hand stock alone, "not including open shipments", exceeds the limit, against the highest estimated or confirmed limit for the period (US, Europe, Canada) (C25).
- `GET_FBA_OVERAGE_FEE_CHARGES_DATA` gives the limit and usage only for a charged month: `storage_limit_volume`, `storage_usage_volume`, `overage_volume`, `charge_rate` (C25).
- It is the only report that names a capacity limit; Amazon describes it as "Estimated" overage fees for inventory "that exceeds your storage limits", so a row presupposes an overage; Amazon Fulfillment opens it (C36, C39).
- The overage rate table is help page GV8JEETWV9Q33CMX, which this research could not read (C25).
- Japan abolished its storage overage fee on 2024-10-01; the US, Europe and Canada kept theirs (C27).

## Capacity Manager

- A Capacity Manager request is a bid: a maximum reservation fee per cubic foot, per cubic metre in Japan, granted "starting with the highest reservation fee" (US, Europe, Japan) (C26).
- Performance credits are designed to offset the reservation fee in part or in full from sales on the extra space; a 2024 forum reply put a dated figure on the credit (C26).
- The requests, bids and credits have no API read; they are in Seller Central's Capacity Manager only (C26).
- The charge after the fact is Finances v0 `CapacityReservationBillingEvent`, which Finance and Accounting opens, with no request, bid, volume or storage type on it (C26).
- Whether that amount is net of performance credits, and whether a credit posts as its own event, was read in Amazon's documents and not yet seen on a live store (C26).

## IPI

- Amazon published numeric IPI thresholds for the US from 2021-01-01 and 2022-01-01, and for the UK and EU from 2020, each tied to a measurement week (C28).
- Those thresholds belonged to the quarterly storage-limit system that ended on 2023-03-01; since then Amazon's text says the limit is "influenced by" the IPI score and states no threshold (C28).
- No operation, report or reachable page states a current IPI threshold, and the score itself is on the Seller Central dashboard only (C28, Q1).
