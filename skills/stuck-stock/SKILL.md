---
name: stuck-stock
description: "A seller's Amazon FBA stock that is not selling or cannot sell: stranded, excess, aged and unfulfillable units, where each is read, what Amazon removes, disposes of, liquidates or donates on its own, every way out with what is permanent, and where Amazon's notices contradict each other. For anything about stock stuck in Amazon's fulfilment centres and getting it sold, back or gone."
---

## Stranded

- Stranded stock is FBA stock in fulfilment centres with no active offer; Amazon calls it usually a listing or account health issue (S1).
- No `getInventorySummaries` field or MYI column counts it; `GET_STRANDED_INVENTORY_UI_DATA` is the read, its columns read in Amazon's documents and not yet seen on a live store (S2).
- Unfixed stranded stock is removed or disposed of automatically, the day per SKU in the report's `Date-to-take-auto-removal` (S3).
- Amazon refuses an inbound shipment holding an ASIN with stranded units (S5).

## Excess and aged

- Excess is Amazon's call on its unexposed demand forecast, per SKU in `GET_FBA_INVENTORY_PLANNING_DATA` `estimated-excess-quantity` (S9, S10).
- Amazon removes aged sellable stock under the Automated fulfillable settings, and a moderator wrote in a thread opened 2026-06-26 that it does so even with the setting disabled (S11).
- Amazon's US aged-surcharge schedule effective 2026-01-16 prices sellable stock at ages a moderator said in 2026 is removed; both stand (S12).

## Unfulfillable

- Unfulfillable stock with no return option set is disposed of at Amazon's discretion in the US, and after notice in the UK and EU, a disposal that cannot be cancelled (S14).

## Settings and ways out

- The automated settings and Liquidations and Donations enrolment are neither read nor changed through any SP-API operation, report or feed found (S15).
- An Amazon-created removal cannot be cancelled, and no API operation cancels one (S17).
- `POST_FLAT_FILE_FBA_CREATE_REMOVAL` is the SP-API's only way to create a removal order (S18).
- A liquidation order cannot be cancelled and stops storage and the aged surcharge at submission (S19, C2).
- Amazon's 2025-08-22 notice enrols unconfigured US and Canadian sellers in Liquidations from 2025-09-30, while a mirrored "corrected" text says US only (S21).

How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.

## References

- references/stranded.md: causes, the report, auto-removal, relisting, the listing side.
- references/excess-and-aged.md: the planning report, automated removal, Outlet, practitioners' triggers.
- references/unfulfillable.md: customer damaged, repackaging, disposal defaults.
- references/ways-out.md: removal, disposal, liquidation, donation, Grade and Resell, what is permanent.
- references/research.md: markdown and returns research.
- ../stock-cost/SKILL.md: storage, the aged surcharge and removal fees.
