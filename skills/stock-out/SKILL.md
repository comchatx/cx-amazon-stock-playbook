---
name: stock-out
description: "When a seller's Amazon offer runs out of stock: what out of stock is in Amazon's fields and reports, what Amazon says it stops, what practitioners and research measured about the weeks after, how a sales average taken over stock-out days understates demand and how tools correct it, and what Amazon's own stock-out agent skill computes. For reading, explaining or looking back on a stock-out, or a risk of one."
---

## In the data

- Zero fulfillable units can sit beside units in transfer, in processing, held for orders or inbound, each its own field (O1).
- Inactive in the listings report does not by itself mean out of stock (O5).
- No report counts days out of stock; the ledger's daily ending balance lets zero days be counted, read in Amazon's documents and not yet seen on a live store (O17).
- Amazon's in-stock rate and estimated lost sales sit in no SP-API model, report or Data Kiosk schema (O11, O12).
- The Replenishment API's Subscribe & Save metrics are the only seller-side SP-API figure found for revenue lost to a stock-out (O14).

## What Amazon says stops

- An out-of-stock offer cannot be featured, and its ad does not display (O8).
- An ASIN with no buyable offer from any seller is unsearchable (O6).
- Deals, coupons, Subscribe & Save and variation children each carry their own rule (O13, O15, O16).
- No Amazon page read states any further ranking effect or a grace period (O20).

## What is measured after

- No published study measures a marketplace seller's search position or rank after restocking (O21, T5).
- Practitioners' measurements disagree, and most pages give recovery figures without data (O23, O24).

## Demand that was not seen

- Sales observed while a SKU could not be bought are a lower bound on demand (O18).
- Tools divide by in-stock days, impute, scale, or do nothing, and define an out-of-stock day four ways (O19).

## Amazon's agent skill and "14 days"

- Amazon's open `stockout-prevention` skill counts fulfillable units only and bands cover at 7 and 21 days (T2).
- "14 days" on Amazon's pages is an FBM Restock eligibility criterion and a low-inventory-level fee band, not an FBA stock-out rule (T1).

How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.

## References

- [references/data.md](references/data.md): fields, reports, lost-sales figures, Subscribe & Save metrics.
- [references/consequences.md](references/consequences.md): Featured Offer, ads, search, deals, coupons, variations.
- [references/after.md](references/after.md): research and practitioners on recovery.
- [references/demand-and-tools.md](references/demand-and-tools.md): censored demand, tools, Amazon's skill, "14 days", practitioners' choices.
