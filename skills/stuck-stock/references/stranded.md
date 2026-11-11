# Stranded stock

- How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.

## What it is

- Amazon defines stranded inventory as FBA inventory in fulfilment centres with no associated active offer, needing either the listing reactivated or the units removed (S1).
- Amazon names closing or deleting a listing, changing it from FBA to seller-fulfilled, listing issues, infringement concerns and system errors as causes (S1).
- An Amazon moderator wrote on 2024-03-12 that stranding "is usually due to a listing or account health issue" (S1).
- Amazon's table of stranded reasons is on the help pages *Fix stranded inventory* and *Inventory Buyability*, as the listing playbook's seat quoted them on 2026-10-14; this research could not read them first-hand (S1).
- No text read names the reason code an account-health stranding carries (S1).

## Where it is read

- No field of `getInventorySummaries` and no MYI column counts stranded units (S2).
- `GET_STRANDED_INVENTORY_UI_DATA` (Pricing or Amazon Fulfillment, near real-time) is the read, with `stranded-reason`, `primary-action`, `date-stranded` and `Date-to-take-auto-removal`; these columns and their values were read in Amazon's documents and not yet seen on a live store (S2).
- The report has no `date-classified-as-unsellable`: since 2020-06-30 aged stranded stock is removed under the seller's settings instead of being reclassified as unsellable (S2).
- Whether stranded units sit inside `fulfillableQuantity` and the planning report's `available` was not seen on a live store (S2).

## Auto-removal

- Stranded stock that is not fixed is removed or disposed of automatically; the days depend on the stranded reason and the seller's setting, and with no setting the units are disposed of (S3).
- Stranded units with an active offer are not auto-removed, per the help page *Stranded inventory required removals* as the listing playbook's seat quoted it on 2026-10-14 (S3).
- Amazon's texts give different timings: an Amazon moderator wrote on 2024-03-12 that stock is removed a fixed number of days after Amazon's e-mail notice, and the help page as quoted on 2026-10-14 gives a maximum per stranded reason code (S3).
- The dated value for each SKU is the stranded report's `Date-to-take-auto-removal`, beside `stranded-reason` and `date-stranded`, read in Amazon's documents and not yet seen on a live store (S3).
- The rule itself is on the help page *Stranded inventory required removals*, which this research could not read (S3).

## Automatic relisting

- Since 2019-06-25 Amazon relists stock stranded as "Listing closed", "Listing closed and inventory error" or "Item discontinued" (S4).
- Since the same date Amazon switches "Merchant fulfilled" strandings back to FBA (S4).
- Both happen automatically unless the seller opted the listing out or set a future offer start date (S4).

## Inbound and Amazon-created SKUs

- Amazon refuses an inbound shipment that contains an ASIN with stranded units, per *Fix stranded inventory* as the listing playbook's seat quoted it on 2026-10-14 (S5).
- The same page says a fix can take 48 hours to show in the stranded view (S5).
- Units under the Amazon-created SKUs `Amazon.Found.B…` and `FBA….Missing#` are stranded until the seller creates a listing for them, and are otherwise removed under the auto-removal settings (S5).

## UK and EU

- In the UK and the EU the stranded settings, removal dates and quantities are separate between UK-stored and EU-stored stock (S6).

## Bulk fix

- The Bulk Fix Stranded Inventory report (`GET_STRANDED_INVENTORY_LOADER_DATA`, near real-time) tells the reader to submit it with `POST_FLAT_FILE_INVLOADER_DATA` (S7).
- The Feeds API's *Feed Type Values* page of 2026-11-05 no longer lists that feed type (S7).
- Amazon's deprecation notice for listings feeds exempts uploads made in Seller Central (S7).

## The listing side

- The listing side of a stranding is read from the Listings Items API: `status`, and an issue's enforcement action `LISTING_SUPPRESSED` or `CATALOG_ITEM_REMOVED` (S8).
- An enforcement action `SEARCH_SUPPRESSED` leaves the offer buyable (S8).
- `GET_MERCHANTS_LISTINGS_FYP_REPORT` is the report read of the same side (S8).
- Both need Product Listing and neither carries a quantity (S8).
- Every state and the inventory reads: ../stock-position/SKILL.md.
