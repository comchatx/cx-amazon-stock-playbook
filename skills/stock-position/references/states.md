# States: what each FBA quantity holds

## The five states

- Amazon names five states for FBA stock: fulfillable ("can be picked, packed, and shipped"), inbound, reserved, unfulfillable ("cannot be sold") and researching (W1).
- Reserved, inbound, researching and unfulfillable are separate fields beside the fulfillable quantity (W1).
- Amazon defines `fulfillableQuantity` as "The item quantity that can be picked, packed, and shipped" (W6).
- The API's only grain is the marketplace, where fulfillable is the stock that "could be fulfilled in the given marketplace", not the stock physically in that country (W6).

## Inbound

- Inbound working is units in a shipment "for which you have notified Amazon" (W7).
- Inbound shipped is units for which the seller has also "provided a tracking number" (W7).
- Inbound receiving is units not yet received in a shipment some of whose units have been (W7).
- The three are per SKU, not per shipment (W7).
- They appear as `afn-inbound-working-quantity`, `afn-inbound-shipped-quantity` and `afn-inbound-receiving-quantity` in the MYI report and as `Working`, `Shipped` and `Receiving` in the Restock report (W7).
- The Restock report's `Total Days of Supply` includes units from open shipments (W7).
- Amazon's notification schema counts WORKING shipments as Working, and SHIPPED, IN_TRANSIT, DELIVERED and CHECKED_IN shipments as Shipped (W8).
- In that schema Receiving begins only when units "are in progress to be received" (W8).
- 赛狐 groups DELIVERED and CHECKED_IN under receiving instead, by its own mapping (W8).
- Inbound shipments as a position: ../../stock-inbound/SKILL.md.

## Reserved

- In the API, reserved has three parts: `pendingCustomerOrderQuantity`, `pendingTransshipmentQuantity` and `fcProcessingQuantity` (W9).
- `pendingCustomerOrderQuantity` is reserved for customer orders, including orders placed but not yet authorised (W9).
- `pendingTransshipmentQuantity` is units moving between fulfilment centres (W9).
- `fcProcessingQuantity` is units sidelined for additional processing (W9).
- That `totalReservedQuantity` equals the sum of the three parts was read in Amazon's documents and not yet seen on a live store (W9).
- FC processing covers, in Amazon's words, "verification of item dimensions and weight, pending investigations, or pending removal orders" (W11).
- The API's reserved total includes units in FC transfer by definition (W12).
- 领星 and 积加 describe Seller Central's reserved figure as customer orders plus FC processing, with FC transfer outside it (W12).
- DataHawk reports that the planning report includes FC transfer in reserved only in the IN, SA, AE, BR and AU stores (W12).
- Amazon has not published which holds for which report; this was read in Amazon's documents and tools' pages and not yet seen on a live store (W12).
- SoStocked gives durations for FC transfer and FC processing as its own practitioners' figures; Amazon publishes no duration for either (W44).

## Whether FC-transfer units can be bought

- An Amazon moderator wrote on 2024-08-26 that FC-transfer units "are available for customers to buy", possibly with a future ship date (W10).
- That post cites the Reserved Inventory report help page G201723860, which this research could not read (W10).
- The *Inventory Buyability* help page GFC63UNUF6LMLK2R, as the listing seat read it on 2026-10-14, says customers cannot buy reserved units (W10).
- The buyable statement is one moderator's post, and neither side was read first-hand on 2026-11-10 (W10).
- The MYI reports carry `afn-fc-transfer-quantity` and `afn-onhand-buyable-quantity`, which Amazon's page does not define (W10).
- Which of these columns a store's MYI file carries today was read in Amazon's documents and not yet seen on a live store (W10, W13).

## Researching

- Researching is, in Amazon's words, "misplaced or warehouse damaged units that are actively being confirmed" (W14).
- The API ages researching units in three buckets of days in `researchingQuantityBreakdown`, whose names give each bucket's span (W14, W15).
- Amazon's texts give two different limits for how long research lasts (W15).
- One limit is in Amazon's 2021 launch text, as a seller quoted it on 2021-04-07, and in Amazon's Chinese column text as 领星 quotes it (W15).
- A longer limit is on the *Inventory Buyability* help page GFC63UNUF6LMLK2R, as the listing seat read it on 2026-10-14 (W15).
- No dated announcement of a change between the two was found, and the help page that states the limit is one this research could not read (W15).
- The 2021 text says that once researched units are reimbursed or the period ends, the adjustment moves to the Inventory Adjustment report, which the Inventory Ledger has since replaced (W15, W25).

## Unfulfillable

- Unfulfillable has six dispositions in the API, read with `details=true`: customer damaged, warehouse damaged, distributor damaged, carrier damaged, defective and expired (W16).
- Unsellable stock and every way out: ../../stuck-stock/SKILL.md.

## Sold ahead of receipt

- Units Amazon offers ahead of receipt through In-Stock Head Start are `FutureSupplyBuyable` (findable and buyable) and `PendingCustomerOrderInTransit` (already bought, in transit) in `FBA_INVENTORY_AVAILABILITY_CHANGES` (W17).
- In the MYI reports they are `afn-future-supply-buyable` and `afn-reserved-future-supply`; `getInventorySummaries` has no such field (W17).
- Units sold this way are still inside inbound, so inbound is not always unsold stock; this was read in Amazon's documents and not yet seen on a live store (W17).

## SKUs, commingling and deleted listings

- FBA stock is counted per seller SKU, and one ASIN can sit under several SKUs of one seller, each with its own quantity (W35).
- Amazon announced on 2025-12-08 that commingling ends for inventory shipped on or after 2026-03-31 (W36).
- Under that rule, Brand Registry brand owners with the Brand Representative role may use manufacturer barcodes without commingling or Amazon stickers (W36).
- Resellers must apply Amazon barcode stickers, and products without a manufacturer barcode need Amazon barcodes from everyone (W36).
- The announcement does not say what became of units commingled earlier (W36).
- The SP-API eligibility program is still named `COMMINGLING` in the models of 2026-10-29 (W36).
- Amazon's listing guide says a deleted listing "does not appear in any of the reports or API data" (W37).
- 积加 reports stock rows for deleted products that it cannot remove; whether such rows occur in the API or the MYI file was read in these sources and not yet seen on a live store (W37).

## What tools count as stock

- Nova and Improvado count available plus FC transfer as stock at Amazon (W43).
- 领星's 可售库存 is `afn-fulfillable-quantity` alone, its FBA库存 adds FC transfer and FC processing, and its restock stock counts fulfillable plus the two FC-transfer reserves (W43).
- 积加's 可售 is local plus remote fulfillable in Europe (W43).
- InventoryLab counts fulfillable only, and 优麦云 adds units under investigation (W43).
- Tools also count in-transit by different shipment statuses, and differ on whether AWD, overseas-warehouse and 3PL units enter a stock figure (W43).
- Each of these is the tool's own definition (W43).
