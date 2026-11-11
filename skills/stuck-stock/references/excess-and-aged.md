# Excess and aged stock

- How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.

## Excess

- Amazon considers an item excess when its days of supply on Amazon's demand forecast pass a figure Amazon sets on the help page *Inventory performance* G202174810, as the listing playbook's seat quoted it on 2026-10-14; this research could not read the page first-hand (S9).
- The forecast behind the call is not exposed (S9).
- Per SKU, Amazon's call is `GET_FBA_INVENTORY_PLANNING_DATA` `estimated-excess-quantity` (S9).

## The planning report

- `GET_FBA_INVENTORY_PLANNING_DATA` is the single successor of the excess, inventory health and inventory age reports removed on 2022-06-27 (S10).
- It carries `estimated-excess-quantity`, `recommended-action`, `recommended-sales-price`, `recommended-sale-duration-days`, `recommended-removal-quantity` and `estimated-cost-savings-of-recommended-actions` (S10).
- Amazon's page defines no value set for `recommended-action` or `alert`; the values these take were read in Amazon's documents and not yet seen on a live store (S10).
- Whether `GET_FBA_RECOMMENDED_REMOVAL_DATA` still returns rows was not seen on a live store (S10).
- Where the report is unavailable, its columns by store and its dates: ../stock-position/SKILL.md (W23).

## Automated removal of aged sellable stock

- Under the Automated fulfillable settings Amazon returns, liquidates or disposes of sellable stock past an age threshold, and of ASINs unsold for a run of months that are past a second age (S11).
- An ASIN removed this way can be barred from inbound for a period; the ages and that period are in Amazon moderators' posts of 2024-03-07 and 2026-02-09 and on help page G200678710, which this research could not read (S11).
- The threshold Amazon stated has changed by store and year: one figure in a US moderator's post of 2024-03-07, a lower one in the UK from 2025-04-04 per an Amazon e-mail a seller posted, and the same lower one in the US from 2025-10-26 per an Amazon e-mail a seller quoted (S11).
- In a thread opened 2026-06-26, an Amazon moderator wrote that sellable stock past that lower age is removed even when the setting is "Disabled", with Amazon choosing the disposition (S11).
- Amazon's texts differ on whether the setting is on by default: moderators' posts of 2024-03-07 and 2026-02-09 describe it as something the seller enables, while a search summary quotes Amazon saying sellers are opted in by default (S11).
- The seller's own setting is in Seller Central only, with no API read (S11, S15).
- What Amazon did is in `GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA` (`order-type`, `order-source`); whether these columns tell an automated removal apart was read in Amazon's documents and not yet seen on a live store (S11).
- The rule is on help page G200678710, which this research could not read, and in the store's News posts (S11).

## Where Amazon contradicts itself on aged US stock

- Amazon's US aged-surcharge schedule effective 2026-01-16 prices sellable stock in bands that run past the age at which the moderator's statement in that 2026 thread says such stock is removed under Amazon's policy (S12).
- Both texts stand with their dates; the scope is the US (S12).
- How the two coexist on a US account, and whether the removal applies in Canada, was read in Amazon's documents and not yet seen on a live store (S12).
- The surcharge bands and where they are read: ../stock-cost/SKILL.md (C7).

## Outlet

- An Outlet deal needs, among other conditions, stock held in fulfilment centres past a minimum time, new condition and a minimum discount, both figures set per store (S25).
- An Outlet deal carries no extra fee (S25).
- The eligibility Amazon shows is on Seller Central's Outlet deal eligibility page only, with no API read (S25).

## Practitioners' triggers

- Practitioners' triggers are their own and earlier than Amazon's fee bands (S26).
- My Amazon Guy starts watching aged stock at day 90 and again at day 120, as their own practice (S26).
- 赛狐ERP watches at 90 days and plans by 150 (their practice) (S26).
- Titan Network flags over 12 weeks of cover (their practice) (S26).
- Seller Labs names a window before the aged surcharge's higher bands as the cheap one to clear stock in (their practice) (S26).
- Seller Labs, My Amazon Guy, Nova and SalesDuo each test a removal against a named resale channel and its full return cost (S27).
- The same four treat resale revenue as zero when no channel is named (their practice) (S27).
