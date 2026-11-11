# Amazon's two recommendation reports

Ids in brackets are positions in ../../../research/README.md.

## The Restock report

- `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT` "Provides recommendations on products to restock, suggested order quantities, and reorder dates. Content updated in near real-time" (R1).
- It needs the Pricing or the Amazon Fulfillment role, and exists in every store except India (R1).
- It carries Amazon's per-SKU days of supply (at Amazon, and including open shipments), an `Alert`, a recommended quantity and a recommended ship date (R1).
- Amazon lists the report's columns by name and defines none (R2).
- Amazon gives no values for `Alert` or `Recommended action`; the values they take were read in Amazon's documents as undefined and not yet seen on a live store (R2).
- The column list has no snapshot-date column (R2).
- `Recommended action` is listed for the US store only, and `Unit storage size` for US, CA, UK, DE, FR, IT and ES (R2).
- Whether the European file returns every country in one request, and which columns are empty per store, was read in Amazon's documents and not yet seen on a live store (R1).
- On 2025-02-24 an Amazon moderator called the Restock report "your best source for restock recommendations" and said it "will be phased out after we add all critical metrics from this report to the FBA Inventory report" (R6).
- The moderator named as the destination a report described in the words of `GET_FBA_INVENTORY_PLANNING_DATA`, and gave no date (R6).
- As of 2026-11-10 the Restock report type carries no deprecation label on Amazon's report page (R6).

## The planning report

- `GET_FBA_INVENTORY_PLANNING_DATA` carries Amazon's restock advice as `Recommended ship-in quantity` and `Recommended ship-in date` (R7).
- It carries the floor as `fba-minimum-inventory-level` and `fba-inventory-level-health-status` (R7).
- Its cover measures are `days-of-supply`, `historical-days-of-supply`, short- and long-term historical days of supply, `Total Days of Supply`, `weeks-of-cover-t30`, `weeks-of-cover-t90` and `sell-through` (R7).
- Its seasonal columns are `is-seasonal-in-next-3-months`, `season-name`, `season-start-date` and `season-end-date` (R7).
- Per SKU it says whether the SKU is exempt from the low-inventory-level fee and whether the fee was applied in the current week (R7).
- `healthy-inventory-level` is marked deprecated, and Amazon's page defines none of the planning report's columns (R7).
- The values `fba-inventory-level-health-status` and the report's alert columns take were read in Amazon's documents and not yet seen on a live store (R7).

## Two advices, one formula unpublished

- Amazon publishes two recommended restock quantities and dates, one in each report, and does not publish how either is computed (R3).
- Sellers report the two disagree, in a Seller Central Europe forum thread of 2024-06-20 (R3).
- How old the planning report's `Recommended ship-in date` is against the Restock report's recommended ship date on the same day was read in Amazon's documents and not yet seen on a live store (R3).
- Amazon publishes the recommendation's inputs: a machine-learned demand forecast, current inventory, the seller's restock settings and shipment time (R4).
- Amazon publishes its aim, staying above the Minimum Inventory Level, and no formula (R4).
- Amazon calls the recommendations "a guide only" that "shouldn't be used as a substitute for your own judgement about demand for your products" (R4).
- Practitioners say Amazon's recommendation does not know whether stock ships from a factory or a nearer warehouse (R26).
- Tools show Amazon's figure beside their own rather than using it: RestockPro "cannot vouch for the accuracy", and sellerboard shows it "for reference" (R26).

## The Minimum Inventory Level

- Amazon defines the Minimum Inventory Level as "the minimum number of units per product that you should have on hand in our fulfillment centers" (R8).
- It is forward-looking, from "demand forecasts and replenishment settings" (R8).
- It counts on-hand sellable, FC-transfer and reserved units, and not inbound units (R8).
- Amazon stated on 2023-12-19 that sellers above it see a sales increase over a four-week period on average, "though actual results may vary", with no method, sample or period (R8).
- The Chinese version of that statement footnotes Amazon Accelerate 2023, and it is Amazon's one published sales effect of stock level (R8).
- The figure of that statement is in News_Amazon "Plan FBA inventory levels using a new metric" (R8).

## The forecast behind them

- No SP-API report, operation or Data Kiosk dataset gives a seller Amazon's per-SKU demand forecast (R10).
- The forecast report type that exists is for vendors (R10).
- `daysOfSupply` appears in no JSON model or Data Kiosk schema and reaches a caller only as a report column (R10).
- Amazon's published retail forecasters (MQ-RNN/CNN, MQTransformer, DeepAR) produce probabilistic or quantile forecasts across many related series (R34).
- No Amazon page read says which model drives a seller's Restock recommendation or Minimum Inventory Level (R34).

## Amazon's connector metrics

- Days of supply at the mean and at P90, P80 unit forecasts at 7, 30 and 60 days, a restock date and quantity, and inventory-health metrics exist as private-beta metrics behind Amazon's connector at `sellingpartner-ai.amazon.com` (T3).
- That host is not an SP-API host, and its data is "delayed ~2 days" (T3).
- The connector has no IPI or capacity metric, and "Not every metric in this catalog is exposed to every seller" (T3).
- No public JSON model carries days of supply (T3).
- Amazon's own stock-out skill and its cover rule: ../../stock-out/SKILL.md.
