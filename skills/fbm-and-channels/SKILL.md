---
name: fbm-and-channels
description: "A seller's stock outside FBA's own counts: the seller-fulfilled (FBM) quantity Amazon holds and how a quantity write lands, one ASIN carrying both an FBA and a seller-fulfilled offer, Multi-Channel Fulfillment orders drawing on FBA stock, and stock held in the seller's own or a partner's locations. For reading or changing an FBM quantity, or for FBA stock that also serves other channels."
---

## Seller-fulfilled quantity

- Listings Items holds a seller-fulfilled quantity twice: `fulfillment_availability` is the seller's last submission, and the `fulfillmentAvailability` data set is the live quantity, Amazon's source of truth; Product Listing reaches both (F1).
- Amazon lowers it when an order is placed, changes it on cancellation and takes no orders at zero, as read in Amazon's documents and not yet seen on a live store (F2).
- It holds one record per `fulfillment_channel_code`: `DEFAULT` is seller-fulfilled, `AMAZON_*` is FBA, and `quantity` is supported on `DEFAULT` only (F3).
- A `merge` patch changes one channel's `quantity` and keeps its other fields; a `replace` submits the whole array (F4).
- `ACCEPTED` means taken for processing; `getListingsItem` reflects a write sooner than listing notifications (F6).
- The legacy inventory feeds are gone, so a quantity write is a Listings Items patch or `JSON_LISTINGS_FEED` (F8).

## One ASIN, both offers

- Amazon's developer documentation says one listing can carry both records, FBA inventory used first and seller-fulfilled after it is depleted, with limited or no Seller Central support; read in Amazon's documents and not yet seen on a live store (F18).
- Practitioners run a backup as a second SKU on the ASIN or flip one SKU by software (F19).

## Multi-Channel Fulfillment

- An MCF order ships from the same FBA inventory that serves Amazon orders (F20).
- `getOrderPreview` creates nothing and returns fulfillability and estimated fees; `createOrder`, `updateOrder` and `cancelOrder` move FBA units at MCF fees (F22, F23).
- Fulfillment Outbound runs as v2026-07-04 and legacy v2020-07-01; Amazon's role pages for them disagree (F21).

## Outside the five roles

- Multi-Location Inventory's Supply Sources API needs Selling Partner Insights, and the External Fulfillment Inventory API Direct-to-Consumer Shipping; the five roles open neither (F16, F29).
- Order handling capacity and Amazon's minimum for it are in Seller Central only (F14).

How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.
FBA's own stock states: ../stock-position/SKILL.md.

## References

- references/quantity.md: the record, writes, reports, notifications.
- references/seller-fulfilled.md: orders, capacity, vacation, other locations.
- references/both-offers.md: both offers, backups, buffers, research.
- references/mcf.md: MCF drawing on FBA stock.
