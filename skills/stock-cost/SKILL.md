---
name: stock-cost
description: "What a seller's Amazon stock costs to hold: monthly storage, the utilization and aged surcharges, the low-inventory-level fee, capacity limits and overage, placement, removal, liquidation and AWD charges, each with its rule, its dated history, its differences by store and the report column or page where the seller's own rate is read, and the 2027 US and Canadian change. For anything about storage or inventory fees and what drives them."
---

## Storage

- Monthly storage is charged on the daily average volume units occupy in a month, by size class and season, and charged the month after (C1).
- `GET_FBA_STORAGE_FEE_CHARGES_DATA` carries the rate applied per FNSKU per fulfilment centre; no operation returns a rate card (C1, C41).
- The utilization surcharge rides on the seller's ratio of volume stored to volume shipped, per size class, never per SKU (C3, C5).
- The aged surcharge is assessed monthly on age counted first-in-first-out, its start age differing by store (C6, C8, C9).
- Rates, seasons, bands and thresholds are read on the report rows, the Europe rate card or the store's pricing page; the US tables are help pages this research could not read (C1, C5, C9).

## The low-inventory-level fee

- It surcharges the fulfilment fee of units shipped when historical days of supply fall below the store's threshold, never stock held (C11, C12, C17).
- The planning report flags per SKU whether it applied or is exempt; no report carries its amount (C11, C16).

## Capacity

- One monthly limit per storage type, seen only in Seller Central's Capacity Monitor; the overage report names it only for a month already charged (C24, C25, C36).

## The 2027 change

- Announced 2026-11-05, from 2027-02-01: the US and Canada drop the utilization surcharge, fold the aged surcharge into one age-based storage rate, and test the low-inventory fee on shipments both before and after the assessment date (C14, C21).
- Its rates sit behind sign-in, readable in no Amazon text found (C22).

## Roles

- Storage and removal reports need Pricing or Amazon Fulfillment; planning and overage reports Amazon Fulfillment; Finances reads Finance and Accounting (C39).
- Amazon's pages disagree on Data Kiosk Economics: its guide (2026-10-20) names Brand Analytics, its correction (2024-07-02) Selling Partner Insights, which the five roles do not open (C40).

## References

- references/storage.md: monthly storage, units, Europe, utilization and aged surcharges.
- references/low-inventory.md: the low-inventory-level fee, its grain and exemptions.
- references/capacity.md: capacity limits, overage, Capacity Manager, IPI.
- references/other-charges.md: placement, removal, liquidation, AWD, peak fee.
- references/2027.md: the 2027 US and Canadian change.
- references/reads.md: rates on rows, roles, Finances, estimates, Economics.
- references/calendar.md: the dated fee calendar.
