# Reports and the Inventory Ledger

How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.
The role each report needs: references/reads-and-roles.md.

## Inventory reports

- `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` covers active listings and `GET_FBA_MYI_ALL_INVENTORY_DATA` adds archived ones (W21).
- Both MYI reports are current snapshots with no history, and Amazon's SP-API page defines none of their columns (W21).
- `GET_AFN_INVENTORY_DATA` splits a SKU's available quantity by warehouse condition code (W22).
- Amazon's page lists the reserved report's (`GET_RESERVED_INVENTORY_DATA`) columns as `reserved_qty`, `reserved_customerorders`, `reserved_fc-processing` and `reserved_staging`, for US, CA, JP, UK, DE, FR, IT and ES, with no FC-transfer column (W13).
- Developers report that the reserved, planning and MYI stock columns changed between 2026-06 and 2026-09 with no release note (W13).
- Developers report the MYI FC-transfer and on-hand-buyable columns gone on 2026-09-07, while Amazon's list of 2026-10-13 still carries them; the dated changes are developers' word (W13).
- Which columns a store's file carries today was read in Amazon's documents and developers' reports and not yet seen on a live store (W13).
- A file's own header row states what it contains (W13).
- Amazon retains deprecated report columns to keep column order, and adds columns without notice (A3).
- `GET_FBA_INVENTORY_PLANNING_DATA` (the page's heading: "FBA Manage Inventory Health Report") is not available in the NL, PL, SE and BE stores and has a reduced column set in Brazil (W23).
- Developers have reported the planning report omitting part of an account's SKUs on some runs while the MYI report stayed complete (W24).
- A seller states the planning report omits out-of-stock listings, and Amazon did not dispute it in that thread (W24).
- `GET_AFN_INVENTORY_DATA_BY_COUNTRY` gives the quantity available for local fulfilment per country, is offered for Europe only, and carries no reserved, inbound or unfulfillable figure (W19).
- Movement between European countries is read from the Inventory Ledger; Seller Central's "Cross-Border Inventory Movement report" has no documented SP-API report type (W19).

## Report types that no longer exist

- `GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA`, `GET_EXCESS_INVENTORY_DATA` and `GET_FBA_INVENTORY_AGED_DATA` were removed on 2022-06-27 (W25).
- Six inventory history, adjustment, receipt and reconciliation report types were removed on 2023-01-31, and the Inventory Ledger replaced them (W25).
- Amazon first announced the end of those six for 2022-09-30, then for 2023-01-31 (W25).
- `GET_FBA_UNO_INVENTORY_DATA` was removed on 2024-03-27 (W25).
- No stock API, report, feed or notification has a removal date in 2027 on Amazon's deprecation schedule as read on 2026-11-10 (A5).

## The Inventory Ledger

- The ledger summary balances a period as starting balance, receipts, customer shipments, customer returns, vendor returns, transfers, found, lost, damaged, disposed, other and unknown events, and ending balance (W26).
- The summary is per FNSKU and disposition, by country (default) or by fulfilment centre (`aggregateByLocation`), and by month (default), week or day (`aggregatedByTimePeriod`) (W26).
- A summary request whose dates do not match the period (a whole month, a whole week) "can return empty data" (W26).
- The ledger detail lists each movement for 18 months with event type, fulfilment centre, date, disposition, reason, and reconciled and unreconciled quantity, filterable by `eventType` (W27).
- The detail's event types are Adjustments, CustomerReturns, Receipts, Shipments, VendorReturns and WhseTransfers; receipts per fulfilment centre and date sit under `Receipts` (W27).
- "Unknown Events" are units whose event type is not known, mainly because parts of one event fall in different reporting periods, and a longer period reduces them (W29).
- In the downloaded ledger an adjustment's reason is a code (W30).
- A change of disposition is two rows: a decrease (6, 7, E, H, K, U or Q), then a P increase (W30).
- Codes M and 5 are misplaced and F is found (W30).
- N (found) and O (correction) also cover ownership transfers and units Amazon has reimbursed, so they are not all physical events (W30).
- Codes 3 and 4 are Amazon merging two SKUs it judges to be the same item (W30).
- An adjustment's unreconciled quantity is the part not yet matched by a later event (W31).
- Amazon's reconciliation reasons include "Inventory found", "Reimbursed", "Inspected and disposition corrected" and "Inventory ownership correction" (W31).

## Where the reads do not tie

- `getInventorySummaries`' `totalQuantity` includes inbound units, and the ledger carries no inbound quantity (W2, W28).
- The ledger keeps units moving between fulfilment centres in a column ("In Transit Between Warehouses") separate from the ending warehouse balance (W28).
- Asked on its forum whether to add the two, Amazon gave no rule (W28).
- An Amazon moderator stated on 2023-12-05 that reserved units are included in the ledger (W28).
- That the ledger's ending balance plus units in transit between warehouses equals fulfillable, reserved, unfulfillable and researching at the same cut was read in Amazon's documents and not yet seen on a live store (W28).
- Ledger quantities are signed: sellers quote negative `Quantity` rows in the detail view and negative `Receipts` in the summary (W32).
- An Amazon moderator said of one such case that the units "might be in transfer to another warehouse" and that the reason code decides (W32).
- No source documents negative values in `getInventorySummaries` or the MYI file; that they do not occur there was read in Amazon's documents and not yet seen on a live store (W32).
- The API's reserved total includes FC transfer by definition, while tools describe Seller Central's reserved figure without it (W12).
- A planning file missing SKUs and a complete MYI file have been reported on the same account (W24).
- Under Pan-European FBA, developers report that each participating EU marketplace returns the same sum (W18).
- Per-centre on-hand quantity is not in the FBA Inventory API; it is reached through the ledger summary by fulfilment centre, the storage-fee report and the shipment reports (W45).

## Freshness

- Amazon states that a near real-time FBA report is regenerated at most once every 30 minutes and a daily one at most once every four hours (W20).
- A request inside that window returns the copy already made, and the intervals do not limit how often a report may be requested (W20).
- The planning report states no update frequency and carries three dates on one row (`snapshot-date`, `Inventory age snapshot date`, `Last updated date for Historical Days of Supply`), so its figures are not all of one day (W23).
- A `getInventorySummaries` request with `startDateTime` returns summaries changed since then, reaching back at most 18 months, and does not detect changes in the three inbound quantities (W4).
- `ITEM_INVENTORY_EVENT_CHANGE` carries data delayed up to 24 hours (W34).
- Amazon's pages state no time zone and no character encoding for any FBA report (A2).
- A developer reported in 2025 that an API-requested listings report arrived in cp-1252 with characters replaced, and the issue is open (A2).
