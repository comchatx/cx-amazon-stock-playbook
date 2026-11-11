# Stock states: where every unit is, and what each of Amazon's states means

Read 2026-11-10 by the research seat. Verified 2026-11-10 by the verifier; the changes are listed in *Verification* at the end.

Tags: **[official]** is Amazon's own words (an SP-API documentation page, an SP-API model file, a post by an Amazon account on Amazon's seller forums, sell.amazon.com, supplychain.amazon.com), cited by page name and URL and read 2026-11-10 unless another date is given. **[official, via <who>]** is Amazon's text as a named third party reproduces it; the Amazon page itself was not read. **[snippet]** is a fact seen only in a search result's summary. **[opinion]** is a named practitioner, tool vendor or developer. **[research]** is a published paper. **[seat]** is this seat's own inference and enters no skill. Figures (day counts, refresh intervals, rate limits, column lists) are recorded with page and date so a reader knows what to look for; the live value is read at run time from the read named in *What cx must read at run time*.

How URLs were reached. SP-API documentation pages are cited at their public address `https://developer-docs.amazon.com/sp-api/docs/<slug>`; each was read by plain GET as markdown at `https://developer-docs.amazon/sp-api/docs/<slug>.md` (the site's own `llms.txt` lists the slugs; a wrong slug returns a 1,054,347-byte "Page Not Found" body). SP-API models were read in the local clone at commit `db2936aa` (2026-10-29) under `scratch/sp-api-plugins/models/`. Amazon seller-forum threads were read by plain GET; the posts sit in the page's `__NEXT_DATA__` JSON. Seller Central help pages return only a script shell to a plain GET on `sellercentral.amazon.com` and `sellercentral.amazon.co.uk` (tried with `?locale=en-US` on eight ids on 2026-11-10); by the lead's ruling of 2026-11-10 the help hub's content call was not used, so every help page is **unreachable** in this file and is listed in *Open questions*. `web.archive.org` answered 502 or timed out on every attempt on 2026-11-09 and 2026-11-10. Two facts are taken from the listing playbook's file `packages/cx-listing-playbook/research/angles/inventory-and-fulfillment.md` (that seat's read of 2026-10-14) and are marked as that seat's read, not re-read here.

## What this covers

- Every quantity state Amazon reports for FBA stock, with Amazon's own definition: fulfillable; inbound working, shipped and receiving; reserved and its parts; researching and its age buckets; unfulfillable and its dispositions; total quantity; the In-Stock Head Start pair (future supply buyable, reserved future supply).
- The same states as each report shows them, column by column, and where the columns do not tie: `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA`, `GET_FBA_MYI_ALL_INVENTORY_DATA`, `GET_AFN_INVENTORY_DATA`, `GET_AFN_INVENTORY_DATA_BY_COUNTRY`, `GET_RESERVED_INVENTORY_DATA`, the stock columns of `GET_FBA_INVENTORY_PLANNING_DATA` and `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`, the quantity column of `GET_MERCHANT_LISTINGS_ALL_DATA`, and the Inventory Ledger (summary and detail views), with the reports the ledger replaced and their dates.
- Identifiers and grain: SKU (MSKU), FNSKU, ASIN, condition; commingling and its end; one ASIN under several SKUs; marketplace, country and fulfilment-centre grain; what the API does under Pan-European FBA.
- Stock outside FBA that the FBA summaries do or do not show: Amazon Warehousing and Distribution (AWD) and Global Warehousing and Distribution (GWD).
- Time: freshness of each read, `startDateTime`, `details`, pagination, the 18-month reach, the ledger's daily cut and its reconciled and unreconciled quantities.
- Data pitfalls an operator meets.
- How English and Chinese tools name the states (在库, 在途, 预留, 可售) and how those names map to Amazon's.

Owned elsewhere and only cross-referenced:

- Storage, aged-inventory and capacity fees: `areas/holding-costs.md`.
- Stock-outs and their effect: `areas/running-out.md`.
- Restock arithmetic, days of supply as a planning figure, forecasting: `areas/restock-and-forecast.md`.
- The inbound flow (plans, shipments, placement, receiving disputes): `areas/inbound.md`.
- Stranded, excess and aged stock, removals: `areas/stuck-stock.md`.
- Seller-fulfilled quantity: `areas/fbm-and-outside-fba.md`.
- Pan-European FBA, EFN, Multi-Country Inventory, Remote Fulfillment, AWD and GWD as programs: `beyond/programs-and-regions.md`.
- The API surface table: `method/sp-api-stock-surface.md`. Pages with no API: `method/seller-central-only.md`.

## Amazon's own rules

### A. The five states, as Amazon words them

**A1. The API guide's wording.** [official] *FBA Inventory API*, https://developer-docs.amazon.com/sp-api/docs/fba-inventory-api (page `updatedAt` 2026-09-09), read 2026-11-10: the API lets a seller "retrieve information and track the real-time availability of your inventory in Amazon's fulfillment network at the marketplace level", and names five states:

> "**Fulfillable:** Inventory that can be picked, packed, and shipped. **Inbound:** Inventory that is on its way to Amazon's fulfillment network. **Reserved:** Inventory in Amazon's fulfillment network that is being picked, packed, and shipped; or is sidelined for measurement, sampling, or other internal processes. **Unfulfillable:** Inventory that cannot be sold. **Researching:** Inventory that is misplaced or warehouse damaged units that are actively being confirmed at an Amazon fulfillment center."

The same page: "This API is available in all marketplaces." It is a sellers' API. Its release notes record 2022-04-13 (global availability), 2024-06-19 (dynamic sandbox) and 2024-09-25 (the `stores` array).

**A2. The supply-chain site's wording, which differs on inbound and reserved.** [official] *Inbound and storage*, Amazon Supply Chain blog, https://supplychain.amazon.com/blog/inbound-and-storage (published 2021-05-14, modified 2026-05-04), read 2026-11-10:

> "Available: Products are in stock at the fulfillment center and ready to ship. Inbound: Products are en route to a fulfillment center but are available for fulfillment. However, shipping will be delayed until the inventory is received. Reserved: Products are tied to a customer order in the process of being shipped between fulfillment centers or set aside at a fulfillment center for additional processing. Unfulfillable: Products are not available for fulfillment, because they are damaged, defective, or otherwise. Researching: Products are misplaced or damaged and are actively being confirmed at the fulfillment center."

The two pages disagree on inbound: A1 says only "on its way"; A2 says inbound units "are available for fulfillment" with delayed shipping. A2's sentence matches In-Stock Head Start (section D), which applies to some inbound units, not all. The same page defines stranded as "a product in a fulfillment center that does not have an active offer on Amazon" (owned by `areas/stuck-stock.md`).

**A3. Buyability, as the listing playbook read it.** [official, read by the listing playbook's seat on 2026-10-14, not re-read] *Inventory Buyability*, Seller Central help GFC63UNUF6LMLK2R: "If units are stranded, reserved, being researched, or unfulfillable, customers won't be able to buy them." Reserved: "Usually, it's set aside to fulfill customer orders… In rare cases … for additional processing, verification, investigations, or pending removal orders"; "typically temporary". Researching: "Research may take up to 60 days but is typically completed much faster." Unfulfillable: "isn't in sellable condition". This page says reserved units cannot be bought; section C2 records Amazon saying the FC-transfer part can.

### B. The API's fields: `getInventorySummaries`

Source for all of B: [official] `models/fba-inventory-api-model/fbaInventory.json` in the local clone (commit `db2936aa`, 2026-10-29), read 2026-11-10; and *Get inventory summaries*, https://developer-docs.amazon.com/sp-api/docs/get-fba-inventory-summaries (`updatedAt` 2026-09-09). Role for `getInventorySummaries`: **Amazon Fulfillment; Product Listing** (regions NA, EU, FE), per *Role Mappings for SP-API Operations*, https://developer-docs.amazon.com/sp-api/docs/role-mappings (`updatedAt` 2026-10-28).

**B1. One row per seller SKU.** `InventorySummary` carries `asin`, `fnSku` ("Amazon's fulfillment network SKU identifier."), `sellerSku`, `condition` ("The condition of the item as described by the seller (for example, New Item)."), `lastUpdatedTime` ("The date and time that any quantity was last updated."), `productName`, `totalQuantity`, `stores` ("A list of seller-enrolled stores that apply to this seller SKU.", an array of strings with no enumeration) and, only when asked, `inventoryDetails`.

**B2. Total quantity includes inbound.** `totalQuantity`: "The total number of units in an inbound shipment or in Amazon fulfillment centers."

**B3. Details exist only when requested.** `details`: "true to return inventory summaries with additional summarized inventory details and quantities. Otherwise, returns inventory summaries only (default value)." `InventoryDetails`: "This object will not appear if the details parameter in the request is false."

**B4. Fulfillable and the three inbound stages.**

- `fulfillableQuantity`: "The item quantity that can be picked, packed, and shipped."
- `inboundWorkingQuantity`: "The number of units in an inbound shipment for which you have notified Amazon."
- `inboundShippedQuantity`: "The number of units in an inbound shipment that you have notified Amazon about and have provided a tracking number."
- `inboundReceivingQuantity`: "The number of units that have not yet been received at an Amazon fulfillment center for processing, but are part of an inbound shipment with some units that have already been received and processed."

So "receiving" counts the units of a partly received shipment that are still **not** received. A unit leaves `inboundReceivingQuantity` when it is received, not when the shipment closes.

**B5. Reserved and its three parts.** `ReservedQuantity`:

- `totalReservedQuantity`: "The total number of units in Amazon's fulfillment network that are currently being picked, packed, and shipped; or are sidelined for measurement, sampling, or other internal processes."
- `pendingCustomerOrderQuantity`: "The number of units reserved for customer orders."
- `pendingTransshipmentQuantity`: "The number of units being transferred from one fulfillment center to another."
- `fcProcessingQuantity`: "The number of units that have been sidelined at the fulfillment center for additional processing."

The model has no field for staging, for future supply, or for on-hand buyable. It does not state that the three parts sum to the total.

**B6. Researching and its age buckets.** The `ResearchingQuantity` object is "The number of misplaced or warehouse damaged units that are actively being confirmed at our fulfillment centers."; its `totalResearchingQuantity` is "The total number of units currently being researched in Amazon's fulfillment network." The breakdown names are `researchingQuantityInShortTerm` ("Short Term for 1-10 days."), `researchingQuantityInMidTerm` ("Mid Term for 11-20 days.") and `researchingQuantityInLongTerm` ("Long Term for 21 days or longer.").

**B7. Unfulfillable and its six dispositions.** `UnfulfillableQuantity.totalUnfulfillableQuantity`: "The total number of units in Amazon's fulfillment network in unsellable condition." The parts are `customerDamagedQuantity`, `warehouseDamagedQuantity`, `distributorDamagedQuantity`, `carrierDamagedQuantity`, `defectiveQuantity` and `expiredQuantity`, each "The number of units in <that> disposition."

**B8. Grain.** `granularityType` is required and its only enumerated value is `Marketplace`; `granularityId` and `marketplaceIds` (at most one) are required. `Granularity`: "For example, if you use Marketplace granularity, the fulfillable quantity will reflect inventory that could be fulfilled in the given marketplace." The quantity is what **could be fulfilled in** that marketplace, not what physically sits in that country. The API has no fulfilment-centre or country grain.

**B9. Three ways to ask, and what each ignores.** Operation description: "All inventory summaries with available details are returned when the startDateTime, sellerSkus and sellerSku parameters are omitted." "When startDateTime is provided, the operation returns inventory summaries that have had changes after the date and time specified. The sellerSkus and sellerSku parameters are ignored." When `sellerSkus` is given, `sellerSku` is ignored. `sellerSkus` takes at most 50 SKUs.

**B10. `startDateTime` reaches 18 months and is blind to inbound.** "You must specify a date and time that is no earlier than 18 months prior to the date and time when you call the API. Note: Changes in inboundWorkingQuantity, inboundShippedQuantity and inboundReceivingQuantity are not detected."

**B11. Paging.** "Important: To avoid errors, use both startDateTime and nextToken to get the next page of inventory summaries that have changed after the date and time specified." `nextToken` "will expire 30 seconds after being created". Default rate 2 requests per second, burst 2; the live limit is the `x-amzn-RateLimit-Limit` response header.

**B12. The model's write operations are sandbox-only.** The three operations that create, add to or delete an inventory item exist for the dynamic sandbox; production stock is not written through this API.

### C. Reserved: what each part is, and which part can be bought

**C1. Amazon's forum wording of the three parts.** [official] Topher_Amazon, Amazon seller forums, 2024-08-26, https://sellercentral.amazon.co.uk/seller-forums/discussions/t/c07904af-be04-432d-8c67-80ab0a46f601, read 2026-11-10 (read at the UK address; the post's own `marketplaceId` is the US store's, `ATVPDKIKX0DER`). The post ends "For more info, please reference the Reserved Inventory report help page", linked to help id G201723860 (anchor `#mnd_2jc_jcb`), so the wording is most likely that help page's own [seat]:

> "Customer order: These units are used to fulfill customer orders. FC transfer: These units are being transferred from one fulfillment center to another to help place the inventory closer to customers. Units in the FC transfer status are available for customers to buy. However, customers might be shown a future ship date if no other units are available in the fulfillment centers for immediate fulfillment. FC processing: These units have been sidelined at the fulfillment center for additional processing, such as verification of item dimensions and weight, pending investigations, or pending removal orders."

**C2. Two Amazon statements disagree on whether reserved units can be bought.** A3 (help page, read 2026-10-14 by the listing playbook) says customers cannot buy reserved units. C1 (Amazon moderator, 2024-08-26) says units in FC transfer "are available for customers to buy", possibly with a later ship date. Both are recorded. The reports' newer columns (E1) side with C1: they carry FC transfer as its own figure and an "on-hand buyable" figure. A third statement points the same way, at second hand: [official, via GitHub commenter `spiohq`, issue #5284, 2026-06-23] the planning report's help page GKT9YKCHXMSDVJKB "still documents it as 'Reserved FC Transfer', units moving between fulfillment centers, buyable but often with a delayed ship date" (the commenter's paraphrase, not Amazon's sentence). No Amazon page that uses the words "future supply" for FC-transfer stock was found; Amazon's "future supply" figures are the In-Stock Head Start pair (D), which concern inbound units, not units in transfer. A web search on 2026-11-10 for the moderator's sentence on an Amazon help page returned only third-party guides, most of which say transfer units are not available.

**C3. Reserved units are inside the ledger.** [official] TaylorR_Amazon, Amazon seller forums (read at the EU address; the post's `marketplaceId` is the US store's), 2023-12-05, https://sellercentral-europe.amazon.com/seller-forums/discussions/t/049699ca-8a05-4c03-9ea2-168705fbdfd0: "these reserved units should be included in your Inventory Ledger. Inventory may be reserved due to transfer, processing, or customer orders, and will show up in the ledger based on those categorizations."

**C4. The Chinese help text, via 领星.** [official, via 领星] https://www.lingxing.com/help/article/fbaInventory, read 2026-11-10, reproduces "亚马逊官方解释" (Amazon's official explanation) for each report column: `reserved_fc-transfers` "正在从一个运营中心转运至另一运营中心的商品数量" (units being moved from one fulfilment centre to another); `reserved_fc-processing` "搁置在运营中心等待进行其他处理的商品数量，包括与移除订单关联的商品" (units set aside at a fulfilment centre awaiting other processing, including units tied to removal orders); `reserved_customerorders` "为买家订单预留的商品数量" (units reserved for customer orders).

### D. In-Stock Head Start: future supply buyable and reserved future supply

**D1. What the two figures are.** [official] `schemas/notifications/FBAInventoryAvailabilityChangeNotification.json` (local clone), read 2026-11-10: `FutureSupplyBuyable` is "The number of units available for customers to find and buy while inventory is on its way to an Amazon fulfillment center through In-Stock Head Start." `PendingCustomerOrderInTransit` is "The number of units that customers have purchased while inventory is on its way to an Amazon fulfillment center through In-Stock Head Start". The MYI reports carry the same pair as `afn-future-supply-buyable` and `afn-reserved-future-supply` (E1).

**D2. The program's start.** [official] News_Amazon, 2019-07-25, "FBA Products in stock soon? Make them available now", https://sellercentral.amazon.com/seller-forums/discussions/t/e061bc46a55f2c54b0a71f8085b7e018: "With the new In-Stock Head Start pilot program, Fulfillment by Amazon (FBA) will make your temporarily out-of-stock products available for customers to find and buy when your shipment is on its way and we are confident about its arrival date." The post calls it a pilot; the date it opened to all sellers is not on the thread as served on 2026-11-10 (the research seat's "October 10, 2019" quotation from a seller could not be found there and was removed by the verifier).

**D3. The API summary does not carry the pair.** `getInventorySummaries` has no future-supply field (B5). The pair is read from the MYI report or from the notification.

### E. The reports: columns, roles, freshness

Source for all of E unless stated: [official] *Fulfillment by Amazon (FBA) Reports*, https://developer-docs.amazon.com/sp-api/docs/report-type-values-fba (`updatedAt` 2026-10-13), read 2026-11-10. Roles are from *Role Mappings for SP-API Types*, https://developer-docs.amazon.com/sp-api/docs/role-mappings-for-types (`updatedAt` 2026-09-09), which agrees with the report page on every type below. All these reports "can only be requested" (none is scheduled) and are tab-delimited flat files. The page gives column names and no column definitions.

**E0. How often content changes.** "A near real-time FBA report is generated no more than once every 30 minutes…" "A daily FBA report is generated no more than once every four hours." "These frequencies describe how often Amazon generates updated report content. They do not set how many report requests you can submit."

**E1. `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` and `GET_FBA_MYI_ALL_INVENTORY_DATA`** (roles: **Amazon Fulfillment; Pricing**). The first is "current details of active (not archived) inventory including condition, quantity, and volume. Content updated in near real-time."; the second covers "all (including archived) inventory". Columns as listed on 2026-11-10: `sku`, `fnsku`, `asin`, `product-name`, `condition`, `your-price`, `mfn-listing-exists`, `mfn-fulfillable-quantity`, `afn-listing-exists`, `afn-warehouse-quantity`, `afn-fulfillable-quantity`, `afn-unsellable-quantity`, `afn-reserved-quantity`, `afn-total-quantity`, `per-unit-volume`, `afn-inbound-working-quantity`, `afn-inbound-shipped-quantity`, `afn-inbound-receiving-quantity`, `afn-researching-quantity`, `afn-reserved-future-supply`, `afn-future-supply-buyable`, `afn-fc-transfer-quantity`, `afn-onhand-buyable-quantity`, `store`.

**E2. `GET_AFN_INVENTORY_DATA`** (role: **Amazon Fulfillment** only; near real-time): `seller-sku`, `fulfillment-channel-sku`, `asin`, `condition-type`, `Warehouse-Condition-code`, `Quantity Available`. It is the only report here that splits a SKU's rows by warehouse condition code.

**E3. `GET_RESERVED_INVENTORY_DATA`** (roles: **Amazon Fulfillment; Pricing**; near real-time; "Provides data about the number of reserved units in a seller's inventory."): `sku`, `fnsku`, `asin`, `product-name`, `reserved_qty`, `reserved_customerorders`, `reserved_fc-processing`, `reserved_staging` (stores US, CA, JP, UK, DE, FR, IT, ES), `program`. The page read 2026-11-10 lists **no** `reserved_fc-transfers` column. 领星's page (C4) and 积加's page (P5) still describe that column, and a developer reported on 2026-06-22 that it "disappeared" without notice (P8). That the column existed is corroborated by a seller's post of 2023-11-30 in the thread of C3, which lists the report's columns as `reserved_customerorders`, `reserved_fc-transfers` and `reserved_fc-processing`. When and whether it was removed in every store rests on the one developer's report; Amazon published no release note for it (the *SP-API Release Notes* page, `updatedAt` 2026-11-04, has none). Amazon's page gives no definition of `reserved_staging`.

**E4. `GET_AFN_INVENTORY_DATA_BY_COUNTRY`** (roles: **Amazon Fulfillment; Pricing**; "Amazon store availability: Europe (EU)"): "Contains quantity available for local fulfillment by country, helping Multi-Country Inventory sellers in Europe track their FBA inventory. Content updated in near real-time." Columns: `seller-sku`, `fulfillment-channel-sku`, `asin`, `condition-type`, `country`, `quantity-for-local-fulfillment`. It is the one requestable read of where European stock physically is by country, and it carries only the available quantity.

**E5. `GET_FBA_INVENTORY_PLANNING_DATA`, stock columns** (role: **Amazon Fulfillment** only; "Not available in the NL, PL, SE, or BE stores"; attributes vary by store and Brazil has a reduced set): `snapshot-date`, `sku`, `fnsku`, `asin`, `product-name`, `condition`, `available`, `fc-transfer`, `pending-removal-quantity`, the `inv-age-*` buckets, `inbound-quantity`, `inbound-working`, `inbound-shipped`, `inbound-received`, `Total Reserved Quantity`, `unfulfillable-quantity`, `Inventory age snapshot date`, `Inventory Supply at FBA`, `Reserved FC Processing`, `Reserved Customer Order`, `Reserved Staging`, `Total Days of Supply (including units from open shipments)`, `Fulfillment Service and Programs`, `marketplace`. The report has two dates: `snapshot-date` and `Inventory age snapshot date`. Its fee, age and recommendation columns are owned by `areas/holding-costs.md`, `areas/stuck-stock.md` and `areas/restock-and-forecast.md`.

**E6. `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`, stock columns** (roles: **Amazon Fulfillment; Pricing**; all stores except India; near real-time): `Total Units`, `Inbound`, `Available`, `FC transfer`, `FC Processing`, `Customer Order`, `Unfulfillable`, `Working`, `Shipped`, `Receiving`, `Fulfilled by`, `Total Days of Supply (including units from open shipments)`, `Days of Supply at Amazon Fulfillment Network`, `Alert`. This report shows FC transfer, FC processing and customer order as three separate columns.

**E7. `GET_MERCHANT_LISTINGS_ALL_DATA`** (roles: Inventory and Order Tracking; **Pricing**; Direct to Consumer Shipping (Restricted); **Product Listing**). [official] *Inventory Reports*, https://developer-docs.amazon.com/sp-api/docs/report-type-values-inventory (`updatedAt` 2026-10-28): one store per report (only the first `marketplaceId` is used); content is cached "between one and six hours depending on the number of entries"; the file starts with a UTF-8 byte-order mark. Columns include `seller-sku`, `quantity`, `pending-quantity`, `fulfillment-channel`, `status`, `asin1`, `item-condition`, `open-date`, `merchant-shipping-group`. What `quantity` holds on an Amazon-fulfilled row is not defined on the page (open question O6); seller-fulfilled quantity is owned by `areas/fbm-and-outside-fba.md`.

**E8. Reports that no longer exist.** [official] *SP-API Deprecation Schedule*, https://developer-docs.amazon.com/sp-api/docs/sp-api-deprecations (`updatedAt` 2026-09-09):

| Report type | Deprecated | Removed |
|---|---|---|
| `GET_EXCESS_INVENTORY_DATA`, `GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA`, `GET_FBA_INVENTORY_AGED_DATA` | 2022-03-31 | 2022-06-27 |
| `GET_FBA_FULFILLMENT_CURRENT_INVENTORY_DATA`, `GET_FBA_FULFILLMENT_INVENTORY_ADJUSTMENTS_DATA`, `GET_FBA_FULFILLMENT_INVENTORY_RECEIPTS_DATA`, `GET_FBA_FULFILLMENT_INVENTORY_SUMMARY_DATA`, `GET_FBA_FULFILLMENT_MONTHLY_INVENTORY_DATA`, `GET_FBA_RECONCILIATION_REPORT_DATA` | 2022-06-13 | 2023-01-31 |
| `GET_FBA_UNO_INVENTORY_DATA` | 2023-09-20 | 2024-03-27 |

`GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA` is therefore not live; the planning report (E5) carries its successor columns.

**E9. The Global FBA Inventory report.** [official] News_Amazon, 2024-12-09, "Global FBA Inventory report will be retired on December 27, 2024", https://sellercentral.amazon.com/seller-forums/discussions/t/9b51ac6d-2183-43ff-82b0-2b4b63034f0a: the information "will remain available in the FBA Inventory report" (Reports > Fulfillment > Manage FBA Inventory).

### F. The Inventory Ledger

Source: [official] *Fulfillment by Amazon (FBA) Reports* (as E). Role for both views: **Amazon Fulfillment** only.

**F1. What it is.** `GET_LEDGER_SUMMARY_VIEW_DATA`: "The Inventory Ledger Report is like a bank statement of your inventory. It provides end-to-end inventory reconciliation capability by showing starting inventory balance, received inventory, customer orders, customer returns, adjustments, removals and ending balance." `GET_LEDGER_DETAIL_VIEW_DATA`: "…including products that are sold, returned, removed/disposed, damaged, lost, and found. You can view all historical movements of your inventory for 18 months in this report."

**F2. Summary view: options and columns.** `reportOptions`: `aggregateByLocation` = `COUNTRY` (default) or `FC`; `aggregatedByTimePeriod` = `MONTHLY` (default), `WEEKLY` or `DAILY`; `FNSKU`, `MSKU` (returns "all active FNSKU mappings of that MSKU"), `ASIN`. A `DAILY` report is an end-of-day figure; `MONTHLY` needs the first and last day of a month, `WEEKLY` the start and end of a week; a date range that does not fit the period "can return empty data". Columns: `Date`, `FNSKU`, `ASIN`, `MSKU`, `Title`, `Disposition`, `Starting Warehouse Balance`, `In Transit Between Warehouses`, `Receipts`, `Customer Shipments`, `Customer Returns`, `Vendor Returns`, `Warehouse Transfer In/Out`, `Found`, `Lost`, `Damaged`, `Disposed`, `Other Events`, `Ending Warehouse Balance`, `Unknown Events`, `Location`, `Store`.

**F3. Detail view: options and columns.** `eventType` filter: `Adjustments`, `CustomerReturns`, `Receipts`, `Shipments`, `VendorReturns`, `WhseTransfers` (empty means all; the filter was added 2022-09-21 per *SP-API Release Notes*, `updatedAt` 2026-11-04). Columns: `Date`, `FNSKU`, `ASIN`, `MSKU`, `Title`, `Event Type`, `Reference ID`, `Quantity`, `Fulfillment Center`, `Disposition`, `Reason`, `Country`, `Reconciled Quantity`, `Unreconciled Quantity`, `Date and Time`, `Store`.

**F4. The ledger is the only requestable read with fulfilment-centre grain and disposition on every row,** and the summary view carries inbound in no column: its balance starts at receipt.

**F5. Column definitions.** [official, via Openbridge] (gists by `tspicer` reproducing Amazon's ledger help text: https://gist.github.com/tspicer/1743a3d2cd1085400bb393b68412e148 and https://gist.github.com/tspicer/afc2e79bca4c95c5f54f582f8236e933, read 2026-11-10):

- Starting warehouse balance: "Units that were available for this product in fulfillment centers at the start of the time period".
- Warehouse transfer in/out: "Aggregated number of units that have been transshipped into and out of fulfillment centers".
- In transit between warehouses: "Units that are in transit between fulfillment centers".
- Lost: units that "may be eligible for reimbursement or for which you have already been reimbursed".
- Unknown events: "Units for which the specific event type is not known. This is primarily caused by parts of an event occurring across different reporting time periods. Expanding the reporting time period can reduce the number of unknown event units."
- Reference ID: "Transaction ID, such as a shipment ID or adjustment ID".
- Reason: "The downloaded report displays codes, while the online report shows descriptions."
- Reconciled quantity: "Number of units that have been reconciled with other adjustment events"; unreconciled quantity: units that "have not been reconciled".

**F6. Adjustment reason codes.** [official, via Openbridge] https://gist.github.com/tspicer/006f51f798b9803bf0b0ef3fc93b4266, read 2026-11-10; the same table is at Reason Automation, https://help.reasonautomation.com/seller/inventory-ledger-details.

| Code | Sign | Amazon's label | Amazon's explanation as reproduced |
|---|---|---|---|
| 6 | − | Damaged at Amazon fulfillment center | decrease to carrier-damaged; "always followed by a P code increase to your fulfillment-center-damaged inventory level" |
| 7 | − | Damaged at Amazon fulfillment center | decrease to expired; followed by P |
| E | − | Damaged at Amazon fulfillment center | decrease to sellable; followed by P |
| H | − | Damaged at Amazon fulfillment center | decrease to customer-damaged; followed by P |
| K | − | Damaged at Amazon fulfillment center | decrease to defective; followed by P |
| U | − | Damaged at Amazon fulfillment center | decrease to distributor-damaged; followed by P |
| P | + | Inventory disposition change | "always follows a code 6, 7, E, H, K, U, or Q adjustment" |
| Q | − | Inventory disposition change | "always followed by a P code adjustment" |
| D | − | Inventory disposed of | |
| M | − | Inventory misplaced | "missing from a bin location in a fulfillment center" |
| 5 | − | Inventory misplaced | same |
| F | + | Inventory found | "missing inventory has been found" |
| N | + | Inventory found | "inventory that was incorrectly assigned has been transferred to your account or because you received an Amazon reimbursement" |
| O | − | Inventory correction | "transferred out of your account because they were incorrectly received into your inventory or because Amazon has reimbursed you for them" |
| 3 | + | Product redefinition transfer in | "Two products with separate identifiers (SKUs) are determined to be the same item. One SKU will be removed from your inventory (code 4) and added (code 3) as the other SKU." |
| 4 | − | Product redefinition transfer out | same |

A disposition change is therefore two rows (a decrease and a P increase), not one. Codes N and O move units for reasons that include reimbursement, so "found" and "correction" rows are not all physical finds.

**F7. Reconciliation reasons.** [official, via Openbridge] https://gist.github.com/tspicer/d62e47ef7fc24d62136936a5d48f1800: a "Damaged at Amazon fulfillment center" event reconciles as "Inspected and disposition corrected", "Reimbursed" or "Remaining misplaced or damaged inventory"; an "Inventory misplaced" event as "Inventory found", "Reimbursed", "Damaged inventory misplaced" or "Remaining…"; an "Inventory found" event as "Replacement inventory found", "Missing inventory found" or "Inventory ownership correction". An adjustment's unreconciled quantity is what none of these has yet closed. Reimbursement itself is owned by `areas/stuck-stock.md`.

**F8. When the ledger replaced the old reports: two dates.** [official] News_Amazon (EU forum), 2022-08-02, "New report simplifies FBA inventory information", https://sellercentral-europe.amazon.com/seller-forums/discussions/t/d02a7c4222e0c877da74bffe7812fa1d: "Inventory Ledger is updated daily and replaces these reports: [Daily Inventory History, Monthly Inventory History, Inventory Event Detail, Inventory Adjustments, Inventory Reconciliation, Received Inventory]. Note that these reports will be discontinued from September 30, 2022." [official] News_Amazon (US forum), 2022-10-24, "Switch to the new Inventory Ledger report now", https://sellercentral.amazon.com/seller-forums/discussions/t/bbf046a42a47d98c537cd0e74786a9c4: "On January 31, 2023, the Inventory Ledger report will replace the following six reports… As of January 31, you'll no longer have access to these reports." The second date matches the SP-API removal date (E8). The first post is the only Amazon statement read that says the ledger "is updated daily".

### G. The change notification

**G1. `FBA_INVENTORY_AVAILABILITY_CHANGES`** (role: **Amazon Fulfillment** only). [official] *SP-API Release Notes* entry 2022-10-19: it is "sent whenever there is a change in the FBA inventory quantities" and carries a "snapshot of the FBA inventory in all eligible Amazon stores in a particular region". [official] *Notification Type Values*, https://developer-docs.amazon.com/sp-api/docs/notification-type-values (`updatedAt` 2026-10-28): "Sellers can subscribe"; it supports `filterExpression`.

**G2. Its fields define the inbound stages by shipment status.** [official] `schemas/notifications/FBAInventoryAvailabilityChangeNotification.json`: per marketplace ("the destination where the affected inventory can be used to fulfill the order"), `InboundQuantityBreakdown.Working` is units "currently residing in a WORKING status shipment"; `Shipped` is units "currently residing in a SHIPPED, IN_TRANSIT, DELIVERED or CHECKED_IN status shipment"; `Receiving` is units that have "arrived and are in progress to be received in Amazon warehouses". `Fulfillable` is units that "can be used to fulfill orders in the given marketplace". `Researching` is units "currently being investigated upon adjustments". `ReservedQuantityBreakdown` has `WarehouseProcessing` ("temporarily sidelined for internal processing"), `WarehouseTransfer` ("in progress to be trans-shipped to another Amazon Warehouse location") and `PendingCustomerOrder` ("will soon be shipped out as customer order shipment"). A delivered or checked-in shipment is still "Shipped" until receiving starts.

**G3. `ITEM_INVENTORY_EVENT_CHANGE`** (role: **Brand Analytics**). [official] *Notification Type Values*: it "is sent five minutes after the beginning of each hour. This notification shares inventory data at an ASIN level, and includes data for the previous hour, as well as any delayed data from up to 24 hours earlier. ASINs are included if the number of units available for purchase by customers has changed." Its `highlyAvailableInventory` is "The number of units available to be sold on the website, based on units in Amazon fulfillment centers that are in sellable condition, minue units in customer shopping carts or otherwise bound for other orders (for example, subscribe-and-save orders)." [sic]. It is the one Amazon figure read that subtracts units in shopping carts. "Sellers and vendors can subscribe".

**G4. `LISTINGS_ITEM_MFN_QUANTITY_CHANGE`** (role: **Product Listing**) concerns seller-fulfilled quantity and is owned by `areas/fbm-and-outside-fba.md`.

### H. Identifiers, grain and commingling

**H1. Definitions.** [official] *Terminology*, SP-API documentation, read 2026-11-10: SKU, "A selling partner-supplied stock keeping unit (SKU) that identifies a listing."; ASIN, "A unique number that identifies an item in the Amazon catalog."; MFN, "Items that are sold on Amazon and fulfilled by the seller." The API's `fnSku` is "Amazon's fulfillment network SKU identifier." (B1). The reports call the same three things `sku`/`seller-sku`/`MSKU`, `fnsku`/`fulfillment-channel-sku`/`FNSKU` and `asin`.

**H2. Stock is counted per seller SKU, and the ledger per FNSKU.** The API returns one summary per `sellerSku` (B1). The ledger's `MSKU` option returns "all active FNSKU mappings of that MSKU" (F2), so one MSKU can map to more than one FNSKU over time. Reason codes 3 and 4 (F6) are Amazon merging two SKUs it judges to be the same item.

**H3. Commingling ended for stock shipped from 2026-03-31.** [official] News_Amazon, 2025-12-08, "Commingling practices will end effective March 31, 2026", https://sellercentral.amazon.com/seller-forums/discussions/t/106d0747-e5c6-44d8-86f3-7669f11238fe, read 2026-11-10:

> "In March, we'll end commingling practices across our supply chain and update eligibility criteria for using manufacturer barcodes. Commingling is when we fulfill customer orders using exact product matches from the closest available inventory in the Amazon fulfillment network, even if that inventory belonged to a different seller, to achieve faster delivery speeds. Now that most sellers maintain inventory levels that keep products close to customers, we can achieve fast delivery without commingling. The following requirements will go into effect for inventory shipped on or after March 31, 2026: **Brand owners** with the Brand Representative selling role in Amazon Brand Registry will no longer need to apply Amazon barcode stickers to prevent commingling for products that already have manufacturer barcodes (such as UPC, ISBN)… **Resellers** (not enrolled in Amazon Brand Registry as a Brand Representative selling role) will now be required to use Amazon barcode stickers for products even if they have a manufacturer barcode… For products that **do not have a manufacturer barcode**, both brand owners and resellers will need to use Amazon Barcode stickers."

The post is on the US forum and names no marketplace scope. It says nothing about units already commingled before that date; sellers asked in the thread and no Amazon answer was on the page read.

**H4. Under Pan-European FBA the API's marketplace rows are not separate stock.** Amazon's model says a marketplace's fulfillable quantity is what "could be fulfilled in the given marketplace" (B8). Developers report the consequence (P8): each EU marketplace returns the same EU-wide sum. `GET_AFN_INVENTORY_DATA_BY_COUNTRY` (E4) is Amazon's read of the per-country physical split. [snippet] An SP-API changelog entry, "Update to the FBA Quantity report for EU" (2022; the page now returns the changelog index), is summarised by search as adding `afn-fulfillable-quantity-local` and `afn-fulfillable-quantity-remote` to the Manage FBA Inventory reports for Spain, the UK, France, Germany and Italy, with the total the sum of the two; those two columns are not in the column list Amazon's report page showed on 2026-11-10 (E1).

**H5. A deleted listing leaves the listing reads.** [official, read by the listing playbook's seat on 2026-10-14; the sentence re-read 2026-11-10 in the downloaded page] *Understanding Amazon listing status and seller-fulfilled inventory management* (`updatedAt` 2026-09-09): "Deleting a listing completely removes it from the seller inventory. It does not appear in any of the reports or API data." The same page: "Inventory reports are not near real-time. The SLA for stock data freshness is 3 hours. For subsequent report calls from the same merchant account, data is 1 to 6 hours old, depending on inventory size." That page is about the listing reports; the FBA reports' own cadence is E0. Units that remain at Amazon under a deleted or closed listing are the stranded case, owned by `areas/stuck-stock.md`.

### I. Stock outside FBA: AWD and GWD

**I1. What AWD is.** [official] *Amazon Warehousing and Distribution*, https://sell.amazon.com/programs/warehousing, read 2026-11-10: "Amazon Warehousing and Distribution (AWD) is a bulk storage solution that distributes your inventory to the Amazon store and non-Amazon sales channels." "Visit the Amazon Warehousing and Distribution page in Seller Central to create and track shipments, view and move your AWD inventory, and track replenishments to the Amazon fulfillment network." "You can't move inventory from FBA to AWD because items are stored differently in our fulfillment and distribution centers."

**I2. AWD stock can count as buyable before it reaches FBA.** Same page: "If you leave auto-replenishment enabled, your products are considered in stock and buyable when they're received by AWD, and we manage your replenishments so you don't have to worry about Fulfillment by Amazon (FBA) capacity limits." Which FBA quantity field, if any, shows those units is not stated on any page read (open question O3).

**I3. The AWD API's quantity fields.** [official] `models/amazon-warehousing-and-distribution-model/awd_2024-05-09.json` (local clone); *Amazon Warehousing and Distribution API*, https://developer-docs.amazon.com/sp-api/docs/amazon-warehousing-and-distribution-api (`updatedAt` 2026-09-09): "This API is available in the Amazon US store." `listInventory` returns per `sku`: `totalOnhandQuantity` ("Total quantity that is present in AWD distribution centers."), `totalInboundQuantity` ("Total quantity that is in-transit from the seller and has not yet been received at an AWD Distribution Center"; added 2024-08-19) and, with `details=SHOW`, `availableDistributableQuantity` ("Quantity that is available for downstream channel replenishment."), `reservedDistributableQuantity` ("Quantity that is reserved for a downstream channel replenishment order that is being prepared for shipment.") and `replenishmentQuantity` ("Quantity that is in transit from AWD and has not yet been received at FBA."; added 2025-01-29), plus expiration details (added 2024-12-18). The role is **Amazon Warehousing and Distribution**, outside the door's five (see *Reads that need a role outside the five*). The guide adds: "Interoperability between API and Seller Central is currently limited…"

**I4. No FBA report read here has an AWD column.** The FBA report page (E) contains no mention of AWD. [official] News_Amazon, 2024-12-09 (E9): "the Amazon Warehousing and Distribution (AWD) Inventory report provides real-time data about your AWD and FBA inventory, such as how many units are available and how many are in transit. You can download all SKU-level inventory information in a single sheet." (AWD inventory > AWD reports > AWD Inventory report). That report is a Seller Central download; no SP-API report type for it is on the report pages read.

**I5. GWD.** [official] sell.amazon.com/programs/warehousing, read 2026-11-10: "Store inventory closer to your supplier with Global Warehousing and Distribution (GWD). GWD offers low-cost bulk storage in Shenzhen, Shanghai, and Ningbo, China, with replenishment capabilities to the US Amazon fulfillment network." "AWD is not currently available in China." GWD's help page (GW6YPQELDZLQ84CF) is unreachable; no API field for GWD stock was found in the models read. The program is owned by `beyond/programs-and-regions.md`.

### J. Gap fills by the verifier (gap fill 2026-11-10)

**J1. The researching limit: 30 days in Amazon's 2021 text, 60 days on the help page read in October 2026 (gap fill 2026-11-10).** [official, via a seller's post on Amazon's EU forum, 2021-04-07] https://sellercentral-europe.amazon.com/seller-forums/discussions/t/5b46fd45c5a27980040dbe30d9a84637, read 2026-11-10; the post is by a seller (`Seller_BS5lg2keRs2QO`, marked as the solution) and reproduces what reads as Amazon's help text under the heading "Why are my items being researched?":

> "You will notice a new inventory classification in the Manage Your Inventory page and report, called Researching. This represents the misplaced or warehouse damaged inventory that is actively being confirmed at our fulfilment centres. A timeline shows the duration of the research, which will never exceed 30 days. Once the inventory being researched has been reimbursed or has exceeded the 30-day duration, you will see the corresponding adjustment transition over to the Inventory Adjustment report. For inventory adjustments occurring after March 19, 2021, you do not have to wait 30 days to file a claim because we are handling the 30-day researching duration for you."

So the 30-day figure is the state's original 2021 definition, in English as well as in the Chinese text 领星 reproduces, and the "up to 60 days" sentence is the later one (the *Inventory Buyability* page, read 2026-10-14 by the listing playbook). No dated Amazon announcement of a change from 30 to 60 was found. The API's buckets (1–10, 11–20, 21 or longer) fit a 30-day limit and do not contradict a 60-day one. The Inventory Adjustment report the text names was replaced by the ledger (F8).

**J2. Negative quantities exist in the ledger (gap fill 2026-11-10).** The detail view's `Quantity` is signed: the reason-code table (F6) gives each code a sign, and sellers quote negative rows. [opinion] A seller, 2024-08-13, https://sellercentral-europe.amazon.com/seller-forums/discussions/t/2fcc4acb-0709-410e-8f8c-e2ffecba48a8: after a receipt of 37 at one fulfilment centre, rows of −1 and −14 against the same shipment reference at two other fulfilment centres. [official] TaylorR_Amazon, same thread, 2024-08-21: "those units might be in transfer to another warehouse. It's hard to say without looking at the reason code in the inventory ledger." [opinion] A seller, 2025-05-05, https://sellercentral.amazon.co.uk/seller-forums/discussions/t/3933f3a7-c04e-4b02-a3f4-92fcfa2c4f3d: "multiple negative entries in the 'Receipts' column (e.g., -40, -20)" of the summary view on shipments that came from AWD; KJ_Amazon (2025-05-07) asked for case details and gave no explanation. No source was found for negative values in `getInventorySummaries` or the MYI file, and none for rows of deleted listings beyond 积加's remark (P5).

**J3. Pan-European FBA and the API: nothing in Amazon's guide (gap fill 2026-11-10).** The *FBA Inventory API* guide, *Get inventory summaries*, the reference text in `fbaInventory.json` and the FBA report page were searched on 2026-11-10 for "Pan-EU" and "Pan-European": no hit. The only developer-docs page fetched that mentions the program is *Inventory Reports* (for `GET_PAN_EU_OFFER_STATUS`). The shared-sum behaviour therefore rests on the model's "could be fulfilled in the given marketplace" sentence (B8) plus the two developer reports (P8) and Improvado (P2).

**J4. Help-page ids found in Amazon's own posts (gap fill 2026-11-10).** None was read (script shell; content call off limits), but the ids are now known: *Reserved Inventory report help page* = G201723860, anchor `#mnd_2jc_jcb` (Topher_Amazon's link, C1), which is the same id 领星 links for the MYI column definitions; *Inventory Ledger report* = G4FKT5KQWFFJ7LDN and *Inventory Ledger report: How to get the information you need* = GCRWH2T93NYDHBXU (News_Amazon 2022-10-24, F8); *AWD inventory* help = GQ95WW7597USRF5P (News_Amazon 2024-12-09, E9).

**J5. No machine-readable definition of the FBA report columns exists in Amazon's models (gap fill 2026-11-10).** `models/schemas/reports/` in the local clone holds 22 schemas (Brand Analytics, vendor, coupon, promotion, account health and similar); none is for an FBA flat-file report or the ledger. No file under `schemas/data-kiosk/` contains an FBA quantity field (searched for `fulfillable` and `inboundShipped`). The report-type page lists column names only. The retired page *FBA Inventory reports attributes* has a Wayback capture (20231031221616, confirmed by the availability API on 2026-11-10) that again answered 502 or no response. So the ledger's reason codes and the report columns' definitions keep their third-party tags.

**J6. AWD units and FBA fields: still unstated by Amazon (gap fill 2026-11-10).** The AWD guide says only that the API returns "quantity information for units that are in transit to AWD or from AWD to a Fulfillment by Amazon (FBA) facility"; the release note of 2025-01-29 describes `replenishmentQuantity` as "units that are in transit from Amazon Warehousing and Distribution (AWD) to a Fulfillment by Amazon (FBA) facility". Neither says whether the same units are also in FBA's inbound quantities, nor which FBA field carries units "considered in stock and buyable" at AWD. The seller's 2025-05-05 post (J2) shows AWD transfers arriving in the FBA ledger as receipts against shipment references, which is consistent with Nova's statement (P1) and is not proof of it.

## What practitioners add

All [opinion], read 2026-11-10 unless stated. Thresholds named here are the named tool's own practice.

**P1. Novadata's glossary: "sellable" is available plus FC transfer, and the total at Amazon excludes inbound.** https://novadata.io/docs/inventory-and-catalogue/inventory-glossary.md ("Checked against Nova's code on 2026-10-29"). Sellable ("On-hand") = Available + FC transfer. Reserved = "Customer orders in process, FC processing, staging. Outside Sellable". Total at Amazon = Sellable + Reserved + Unfulfillable + Researching; "Inbound and FBM units are never in it", while "Amazon's report total and API total include inbound units". Working = "Working, Ready to ship"; Shipped = "Shipped, In transit, Delivered, Checked in" (agrees with Amazon's schema, G2). "AWD replenishment to FBA is not a separate line: Amazon lists it as an ordinary inbound shipment, already in Inbound units." Its days of supply at Amazon uses Sellable; "Reserved units stay out of the first because they are already in your sales"; it colours under 7 days red and under 14 yellow (Nova's thresholds). Researching "up to 60 days". It reads the FBA report and AWD every 8 hours.

**P2. Improvado on the MYI report.** https://improvado.io/product-updates/connectors/amazon-seller-central-manage-fba-inventory-report (updated 2026-10-15): "The columns Amazon added recently: FC Transfer Units … and On Hand Buyable (available units plus FC transfer units)." "For European marketplaces, available units split into local … and remote". "With Pan-European FBA, the same physical units can appear in the rows of several European marketplaces, so do not sum quantities across marketplaces". The report is a current snapshot with no history.

**P3. DataHawk: whether "reserved" includes FC transfer depends on the marketplace.** https://docs.datahawk.co/changelog/2026-06-01-fba-planning-reserved-quantity (2026-06-01): on the planning report, "for some marketplaces Amazon includes FC Transfer in the reserved_quantity column (Amazon-IN, Amazon-SA, Amazon-AE, Amazon-BR, Amazon-AU), while for all other marketplaces it does not." No Amazon page read confirms or denies this.

**P4. SoStocked (SPS Commerce) on reserved.** https://www.spscommerce.com/community/articles/amazon-reserved-inventory (updated 2026-03-06): FC transfer "usually takes 1-5 days but can take up to 30 days"; FC processing takes "two working days on average"; "inventory that is being processed in or out of a fulfillment center may be marked as both FC Transfer and FC Processing"; the article holds that FC transfer and FC processing count toward capacity use (capacity is owned by `areas/holding-costs.md`).

**P5. The Chinese tools' names, mapped to Amazon's columns.**

| Tool's term (gloss) | Amazon column the tool names | Who |
|---|---|---|
| 可售库存 (sellable) | `afn-fulfillable-quantity` | 领星 |
| 可售 (sellable) = 本地可售 + 远程可售 (local + remote) | `afn-fulfillable-quantity` + `afn-fulfillable-quantity-remote` ("欧洲地区特有字段", a field only Europe has) | 积加 |
| 待调仓 (awaiting transfer) / 运营中心转运 / 预留运转 | `reserved_fc-transfers`; 积加 now takes it from the planning report's "Reserved FC Transfer" / `fc-transfer` | 领星 / 积加 / 赛狐 |
| 调仓中 (in transfer; 领星's label for FC **processing**) / 预留-运营中心正在处理 / 预留处理中 | `reserved_fc-processing`; 积加 adds `reserved_staging` to it | 领星 / 积加 / 赛狐 |
| 待发货 (awaiting dispatch) / 预留-买家订单 / 预留订单 | `reserved_customerorders` | 领星 / 积加 / 赛狐 |
| 预留 (reserved) | `afn-reserved-quantity`; 领星: "对应后台的【预留=买家订单+运营中心处理中】" (matches Seller Central's reserved = customer orders + FC processing) | 领星; 积加 gives the same sum |
| 计划入库 / 货件处理中 / 入库处理中 (planned; shipment working) | `afn-inbound-working-quantity` | 领星 / 积加 / 赛狐 |
| 标发在途 / 货件已发货 / 入库已发货 (shipped, in transit) | `afn-inbound-shipped-quantity` | 领星 / 积加 / 赛狐 |
| 入库中 / 货件正在接收 / 入库正在接收 (receiving) | `afn-inbound-receiving-quantity` | 领星 / 积加 / 赛狐 |
| 货件在途量 (in-transit total) | sum of the three inbound columns | 积加 |
| 不可售 (unsellable) | `afn-unsellable-quantity` | 领星 |
| 调查中 (researching) | `afn-researching-quantity` | 领星 |
| 未来供应可购买数量 / 库存预售 (future supply buyable) | `afn-future-supply-buyable` | 积加 / 赛狐 |
| 未来供应预留数量 (reserved future supply) | `afn-reserved-future-supply` | 积加 |
| FBM可售 | `mfn-fulfillable-quantity` | 积加 |

Sources: 领星 Lingxing, https://www.lingxing.com/help/article/fbaInventory (undated); 积加 Jijia, https://help.jijiaerp.com/docs/v5Wl4W20 (最近修改 2026-09-29); 赛狐 Sellfox, https://www.sellfox.com/help/features.html?id=162.

Points where the tools add to or differ from Amazon:

- 领星 and 积加 both state reserved = customer orders + FC processing, with FC transfer outside it. Amazon's API definition (B5) puts `pendingTransshipmentQuantity` inside `reservedQuantity`.
- 领星 quotes Amazon's Chinese text for researching: "亚马逊运营中心正在调查的商品数量。商品处于调查状态的时间不得超过 30 天" (units Amazon's fulfilment centres are investigating; a unit may not stay in this state more than 30 days). [official, via 领星]. The English help page read on 2026-10-14 says "up to 60 days" (A3), and the API's last bucket is "21 days or longer" (B6). The 30-day figure also appears in English, in Amazon's 2021 launch text as a seller quoted it (J1).
- 领星: "FBM的listing也是会存在有FBA库存的情况" (a seller-fulfilled listing can still have FBA stock). 领星's 可用库存 (usable stock) is a figure the user configures, not an Amazon state.
- 积加 keeps deleted or obsolete products as rows marked 异常 (abnormal) because the source still returns them. It reads the reserved report hourly between 06:50 and 22:50 and takes Europe's per-country stock from 《多国家/地区库存报告》 (the multi-country inventory report); for North America it uses 《FBA北美远程配送Asin报告》 (the NA remote fulfilment ASIN report).
- 赛狐 maps 入库处理中 to WORKING/READY_TO_SHIP, 入库已发货 to SHIPPED/IN TRANSIT and 入库正在接收 to DELIVERED/CHECKED IN/RECEIVING. Amazon's schema puts DELIVERED and CHECKED_IN under Shipped (G2). 赛狐 drops shipments older than 180 days from 在途 (its practice), notes that BE, PL, SE and NL return no planning report and that TR and BR age fields are empty, and states "加拿大站点目前无法获取到亚马逊物流库存报告" (the Canada store currently cannot return the FBA inventory report).
- 赛狐 on AWD, https://www.sellfox.com/help/features/awd-amazon-warehouse-distribution-network: 在库量、在途量、可用量、预留量 (on hand, in transit, available, reserved); "目前AWD仅适用美国站" (AWD currently applies to the US store only); it shows AWD-to-FBA in transit and syncs at 00:00 and 12:00.
- The survey (`scratch/sp-api-plugins/03-tools-cn.md`, not re-read at the source) records 领星's formula "FBA库存=可售（afn fulfillable）+ 待调仓（reserved transfer）+ 调仓中（reserved processing）".

**P6. ConnectBooks.** https://help.connectbooks.com/en/articles/8955528-inventory-ledger-report-explained: the ledger "doesn't include inbound shipments to Amazon"; "It's only available once the day is over. You can't run it for the current day."; its Total is "The ending balance of sellable inventory in Amazon warehouses, plus the inventory moving between Amazon fulfillment centers." Its AWD report page (https://help.connectbooks.com/en/articles/12683512-awd-report-explained): Total = Available + Reserved in AWD, with inbound into AWD and outbound to FBA shown separately; US stores only.

**P7. Sellers on Amazon's forums.**

- A seller asked Amazon on 2025-01-09 whether "In Transit Between Warehouses" must be added to "Ending Warehouse Balance" to get the full stock at Amazon; Josh_Amazon answered on 2025-01-29 by pointing to Seller Support, with no rule (https://sellercentral.amazon.com/seller-forums/discussions/t/5106c5df-c87c-4d3d-9d7c-49d28eb98a09).
- 2018-02-13 thread (https://sellercentral.amazon.com/seller-forums/discussions/t/55cac1eccb7e8fb9f5f5fa80bd46d2fd): after a receipt, 5 available and 45 reserved was FC transfer; one seller reports units held reserved up to 20 days by orders whose payment failed.
- 2019-09-27 thread (https://sellercentral.amazon.com/seller-forums/discussions/t/ba94f57762f61763f636d21eca9cb6af): Manage Inventory offered the columns Available, Inbound, Reserved, Unfulfillable, Total, Future Supply Buyable, Reserved Future Supply; a seller saw a shipment in transit shown as both inbound and "Future Supply Buyable", while earlier shipments already received showed only under reserved, "as they have already gone into FC transfer mode".
- 2025-03-26 thread, EU forum (https://sellercentral-europe.amazon.com/seller-forums/discussions/t/bfac5e0c-f255-407d-8bbb-8436878cce35): a seller with no Pan-EU, EFN or remote fulfilment enrolment and no UK stock saw EU quantities with the UK selected in Manage Inventory.
- A developer on GitHub issue #5289 (PhilJeffcock, 2026-06-29) reports "substantial quantities of inventory stuck in the nIXD (cross dock) system for weeks on end", counted through the FC-transfer figure.

**P8. Developers on `amzn/selling-partner-api-models` (GitHub issues, read with `gh` 2026-11-10).**

- #5283 (2026-06-22): `reserved_fc-transfers` vanished from `GET_RESERVED_INVENTORY_DATA` without notice.
- #5284 (2026-06-22): the planning report's "Reserved FC Transfer" was deleted, `fc-transfer` added and the column order changed; on 2026-06-25 `Reserved_Staging` appeared; the help page GKT9YKCHXMSDVJKB still documented "Reserved FC Transfer"; the API has no staging field, and whether staging is inside `fcProcessingQuantity` is untested.
- #5289 (2026-06-26): `GET_FBA_MYI_ALL_INVENTORY_DATA` gained `afn-fc-transfer-quantity` and `afn-onhand-buyable-quantity` before `store`, and the reporter adds "(4 other columns added to it in early March 2026)" without naming them. A 2026-09-07 comment by another developer: "The format just changed again… 'afn-fc-transfer-quantity' and 'afn-onhand-buyable-quantity' are now gone". Amazon's page of 2026-10-13 lists both (E1). The two sources disagree; the file's header row at run time decides.
- #452 (2023-09-22) and #360 (2024-04-11): with Pan-European FBA, `getInventorySummaries` "returns the same values for each EU marketplace - a sum of inventory quantities from all the EU marketplaces"; #452 adds "(except the UK and other marketplaces, which technically fall under the 'EU' definition, but aren't part of the Pan-EU FBA programme)". These are two developers' reports. Amazon staff answered both (2024-06-03, pointing to developer support; 2024-04-24, suggesting the `sellerSkus` filter) and neither reply confirms or disputes the behaviour. No Amazon page read mentions Pan-European FBA in connection with this API (J3).
- #1983: Amazon support, as quoted by the reporter: "include that filter to the initial request and all the subsequent requests as well along with the next token… It is an expected behavior where the API would return empty array of 'InventorySummaries' but still return a 'NextToken'."
- #2447 and #4946: `nextToken` must be URL-encoded (an Amazon staff reply, 2025-09-03); `details` is sent as the text `true`; one developer observed pages of at most 50 summaries, sorted by SKU (#2447, 2022; the model states no page size).
- #2167: `lastUpdatedTime` more than a week old on some SKUs; #2275: empty `lastUpdatedTime`; #421: a SKU that contains a comma breaks `sellerSkus`.
- #5044 (2025-11-19): the planning report at times omits SKUs (about 30% of an inventory in one case) while the MYI report stays complete.
- #5414 (2026-10-16): `getInventorySummaries` returned zero for every quantity; unanswered.
- #4523: "One ASIN can be represented by many Listings/MSKUs on a single Seller account… The FBA Inventory Item is tied directly to the Listing, not the ASIN/Catalog item."

**P9. Other tools.** m19 (https://help.m19.com/what-is-the-inventory) uses Available, Inbound, Reserved and Unfulfillable and notifies at under 7 units with no inbound (m19's threshold). Reason Automation states for its ledger-detail table "Updated: Daily; Backfill: 1 year" (its pipeline, not Amazon's limit).

## Published research

No published study of Amazon's FBA quantity states, of the accuracy of Amazon's inventory records, or of reserved or researching durations was found.

One general study bears on how far a recorded quantity can be trusted. [research] DeHoratius and Raman, "Inventory Record Inaccuracy: An Empirical Analysis", *Management Science* 54(4), 2008, pp. 627–641; abstract read 2026-11-10 at https://econpapers.repec.org/RePEc:inm:ormnsc:v:54:y:2008:i:4:p:627-641: "Examining nearly 370,000 inventory records from 37 stores of one retailer, we find 65% to be inaccurate." The retailer is a store chain, not Amazon, and the paper predates FBA's present systems; it is context, not evidence about Amazon.

## Stable enough for a skill

- The five states and Amazon's wording of each (A1), and that `totalQuantity` includes inbound (B2).
- The three inbound stages by definition (B4) and by shipment status (G2); "receiving" counts units not yet received.
- Reserved has three parts in the API (B5, C1); FC transfer is described by Amazon as buyable with a possibly later ship date (C1), against the help page's general statement (A3).
- Researching and its three age buckets (B6); unfulfillable and its six dispositions (B7).
- Future supply buyable and reserved future supply are In-Stock Head Start figures, present in the MYI report and the notification and absent from the API summary (D).
- The API's grain is seller SKU by marketplace, where a marketplace's quantity is what could be fulfilled there (B8); the ledger adds country or fulfilment-centre grain and disposition (F2, F3); the by-country report is Europe's physical split (E4).
- `startDateTime` reaches 18 months, misses inbound changes and travels with every `nextToken` (B10, B11).
- The ledger's event types, reason codes and reconciliation reasons (F3, F6, F7), tagged as reproduced by a third party until the help page is read first-hand.
- The report types removed in 2022, 2023 and 2024 (E8).
- Commingling's end for stock shipped from 2026-03-31 (H3).
- Report columns are not stable: developers reported reserved and FC-transfer columns added, renamed and removed in 2026 with no release note (E3, P8; developer reports, not Amazon's statement). What is stable is that a file's header row states its columns.
- AWD quantities live in a separate API under a separate role (I3).

## What cx must read at run time

Requests go through the door (`cx raw amazon-sp-api …`); the token steps and the report lifecycle are the door's. Roles are from *Role Mappings for SP-API Operations* (`updatedAt` 2026-10-28) and *Role Mappings for SP-API Types* (`updatedAt` 2026-09-09).

### R1. Current quantity per SKU: `getInventorySummaries`

- Operation: FBA Inventory API v1 `getInventorySummaries`. **Role: Amazon Fulfillment; Product Listing.**
- Fields: `sellerSku`, `fnSku`, `asin`, `condition`, `totalQuantity`, `lastUpdatedTime`, `stores`; with `details=true`: `fulfillableQuantity`, the three inbound quantities, `reservedQuantity.*`, `researchingQuantity.*`, `unfulfillableQuantity.*`.
- Freshness: Amazon calls it "real-time availability" (A1) and states no interval. Rate 2 per second, burst 2; live limit in `x-amzn-RateLimit-Limit`.
- Pitfalls: `details` defaults to false (B3). `totalQuantity` includes inbound (B2). `nextToken` expires 30 seconds after creation and must be URL-encoded (B11, P8). With `startDateTime`, every page repeats it, an empty page can still carry a `nextToken`, and inbound changes are not detected (B10, P8). The SKU filters are ignored when `startDateTime` is present (B9). No future-supply, staging, on-hand-buyable, country or fulfilment-centre field (B5, B8). Under Pan-European FBA the EU marketplaces return one shared sum (P8). `lastUpdatedTime` has been reported stale or empty (P8). An all-zero response has been reported (P8, #5414).

### R2. The MYI snapshot: `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` / `GET_FBA_MYI_ALL_INVENTORY_DATA`

- **Role: Amazon Fulfillment; Pricing.** Request-only; content regenerated at most every 30 minutes (E0).
- Columns: E1. The only requestable read of `afn-reserved-future-supply`, `afn-future-supply-buyable`, `afn-fc-transfer-quantity`, `afn-onhand-buyable-quantity`, `afn-warehouse-quantity`, `per-unit-volume` and `mfn-fulfillable-quantity` beside the FBA figures.
- Pitfalls: Amazon's page defines no column. The FC-transfer and on-hand-buyable columns were reported added in June 2026 and gone on 2026-09-07, while Amazon's page of 2026-10-13 lists them (P8); the header row is the truth for that file. European files may carry local and remote fulfillable columns that Amazon's page does not list (H4, P2, P5). Whether `afn-reserved-quantity` includes FC transfer is not stated by Amazon (P3, P5). `_ALL_` includes archived listings; `_UNSUPPRESSED_` does not. A snapshot only; no history (P2). 赛狐 reports the Canada store not returning it (P5).

### R3. Reserved breakdown: `GET_RESERVED_INVENTORY_DATA`

- **Role: Amazon Fulfillment; Pricing.** Near real-time.
- Columns: `reserved_qty`, `reserved_customerorders`, `reserved_fc-processing`, `reserved_staging` (eight stores), `program` (E3).
- Pitfalls: no FC-transfer column on Amazon's page as of 2026-11-10, though tools and older files have `reserved_fc-transfers` (E3, P8); `reserved_staging` is undefined by Amazon; the API has no staging field (B5).

### R4. Sellable by warehouse condition: `GET_AFN_INVENTORY_DATA`

- **Role: Amazon Fulfillment** only. Near real-time. Columns: E2.

### R5. Europe by country: `GET_AFN_INVENTORY_DATA_BY_COUNTRY`

- **Role: Amazon Fulfillment; Pricing.** Europe only; near real-time. Columns: E4. Available-for-local-fulfilment only; no reserved, inbound or unfulfillable by country.

### R6. Planning and restock stock columns

- `GET_FBA_INVENTORY_PLANNING_DATA`. **Role: Amazon Fulfillment** only. Columns: E5. Not available in NL, PL, SE, BE; reduced in BR. Pitfalls: two snapshot dates; columns renamed in June 2026 (P8); SKUs reported missing at random (P8, #5044); FC transfer inside or outside the reserved total reported to vary by marketplace (P3).
- `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`. **Role: Amazon Fulfillment; Pricing.** Columns: E6. All stores except India.

### R7. Movement and balance history: the Inventory Ledger

- `GET_LEDGER_SUMMARY_VIEW_DATA` and `GET_LEDGER_DETAIL_VIEW_DATA`. **Role: Amazon Fulfillment** only.
- Columns and options: F2, F3. Reach: 18 months (F1).
- Freshness: a daily report (regenerated at most every four hours, E0); Amazon's 2022 post says "updated daily" (F8); a tool reports the current day cannot be run (P6).
- Pitfalls: date range must fit the period or the file can be empty (F2). Inbound is not in it. "In Transit Between Warehouses" is a separate column from the ending balance, and Amazon gave no rule on adding them (P7). "Unknown Events" grows with short periods (F5). The file shows reason codes, the page shows descriptions (F5). A disposition change is a pair of rows (F6). Found and correction codes N and O include reimbursement and ownership moves (F6). The `MSKU` option returns only active FNSKU mappings (F2).

### R8. Change feed: `FBA_INVENTORY_AVAILABILITY_CHANGES`

- Notification. **Role: Amazon Fulfillment** only. Fields: G2, D1. Sent on any quantity change, as a region-wide snapshot per SKU with one entry per marketplace. It is the one read that carries the In-Stock Head Start pair without a report request.

### R9. Buyable units per ASIN, hourly: `ITEM_INVENTORY_EVENT_CHANGE`

- Notification. **Role: Brand Analytics.** Field: `highlyAvailableInventory` (G3). ASIN grain, sent hourly with data delayed up to 24 hours. Whether a third-party seller's own stock, as opposed to Amazon's total for the ASIN, is what it reports is not stated on the page (open question O8).

### R10. The listing's quantity column: `GET_MERCHANT_LISTINGS_ALL_DATA`

- **Role: Product Listing or Pricing** (also Inventory and Order Tracking; Direct to Consumer Shipping (Restricted)). Columns: E7. One store per report; cached one to six hours; starts with a byte-order mark. The meaning of `quantity` on an Amazon-fulfilled row is undefined on Amazon's page (O6). `getListingsItem` (**Inventory and Order Tracking; Product Listing**) returns `fulfillmentAvailability`, per the listing playbook's read (not re-read).

### R11. Pan-European enrolment per ASIN: `GET_PAN_EU_OFFER_STATUS`

- **Role: Amazon Fulfillment; Pricing; Product Listing** (also Inventory and Order Tracking; Direct to Consumer Shipping (Restricted)). Spain, UK, France, Germany and Italy stores. It says which listings are enrolled, which decides whether R1's EU rows are one shared pool. Owned by `beyond/programs-and-regions.md`.

## Reads that need a role outside the five

- **AWD `listInventory`** — role **Amazon Warehousing and Distribution** (region NA). Would open `totalOnhandQuantity`, `totalInboundQuantity`, `availableDistributableQuantity`, `reservedDistributableQuantity`, `replenishmentQuantity` and expiration details per SKU (I3). US store only. `details` defaults to `HIDE`; `maxResults` up to 200; "this operation can return empty pages".
- **AWD `listInboundShipments`, `getInboundShipment`, `getInbound`** — same role. Would open shipment status (`CREATED`, `SHIPPED`, `IN_TRANSIT`, `RECEIVING`, `DELIVERED`, `CLOSED`, `CANCELLED`) and expected against received quantity per SKU.
- **AWD replenishment-order reads** (`listReplenishmentOrders`, `getReplenishmentOrder`) are in the model but are not on the Role Mappings page read 2026-11-10, so their role is unstated.

Without the AWD role, the only API trace of AWD stock is whatever reaches FBA's inbound quantities. Nova states an AWD replenishment shows as an ordinary FBA inbound shipment (P1); Amazon's pages do not say. If both the AWD `replenishmentQuantity` and FBA inbound were read and added, the same units could be counted twice [seat].

## Only in Seller Central

Established by finding no operation, report type or notification for it on the SP-API pages and models read on 2026-11-10; the full table is `method/seller-central-only.md`'s.

- The **AWD Inventory report** (AWD and FBA quantities in one sheet), named in Amazon's 2024-12-09 post (I4). No report type found.
- **GWD** stock in China (I5). No field found.
- The **online ledger's reason descriptions** and reconciliation view (the file carries codes; F5).
- **Column definitions** for the MYI, reserved and planning reports: they exist only on help pages (unreachable here), not on the SP-API report page.
- The Manage Inventory page's own columns and country selector (P7).

## The seller's choices

- **What counts as stock on hand.** Fulfillable alone; fulfillable plus FC transfer (Nova, Improvado's reading of "on-hand buyable", 领星's FBA库存 which also adds FC processing); or everything at Amazon. Each changes days of cover and every figure built on it.
- **Whether reserved counts in cover.** Customer-order units are already sold; FC-transfer units are buyable with a later date; FC-processing units may return to sellable or may be on a removal order. Counting all, none or part moves cover by the reserved share, which is largest just after a receipt.
- **Whether inbound counts, and from which stage.** Working is a plan the seller can still cancel; shipped includes delivered-but-unopened; receiving is a partly received shipment's remainder.
- **Whether future-supply-buyable units count as available.** They can be bought, and they are also inside inbound.
- **Whether AWD and GWD stock count**, and at which stage (on hand at AWD, in transit to FBA).
- **Which read is the book of record.** The API (per SKU, per marketplace, now), the MYI report (more columns, snapshot), or the ledger (daily, by disposition and location, reconcilable, no inbound). They answer different questions and do not tie to the unit.
- **How Europe is counted.** One pooled figure per SKU, or the by-country split.
- **Grain of the seller's own records.** By SKU, FNSKU or ASIN; a seller with several SKUs on one ASIN chooses whether to sum them.

## Open questions

For a first run on a real account:

- **O1.** Does `totalReservedQuantity` equal the sum of its three parts, and does `afn-reserved-quantity` in the same hour equal `totalReservedQuantity` or that figure less `pendingTransshipmentQuantity`? Does the answer differ in IN, SA, AE, BR and AU (P3)?
- **O2.** Which columns does the MYI file carry today in each store: `afn-fc-transfer-quantity`, `afn-onhand-buyable-quantity`, the local and remote fulfillable columns (E1, H4, P8)? Does the reserved report carry `reserved_fc-transfers` anywhere?
- **O3.** With AWD auto-replenishment on, which FBA field shows the AWD units Amazon calls "in stock and buyable" (I2): future supply buyable, fulfillable, or none? Does an AWD replenishment appear in FBA inbound shipped (P1)?
- **O4.** Is `reserved_staging` inside `fcProcessingQuantity` in the API (P8)?
- **O5.** Does the ledger's ending balance plus "In Transit Between Warehouses" equal fulfillable + reserved + unfulfillable + researching from the API at the same cut (P7)? How many days behind is the latest ledger day?
- **O6.** What does `quantity` hold on an Amazon-fulfilled row of `GET_MERCHANT_LISTINGS_ALL_DATA` (E7)?
- **O7.** Under Pan-European FBA, do the per-marketplace entries of `FBA_INVENTORY_AVAILABILITY_CHANGES` repeat the EU sum as the API does (H4)? Does North America's remote fulfilment behave the same for CA and MX rows?
- **O8.** Does `ITEM_INVENTORY_EVENT_CHANGE` report a third-party seller's own FBA units (G3)?
- **O9.** Do negative quantities, or rows for SKUs whose listing was deleted, occur in the API or the MYI file? 积加 reports rows it cannot remove (P5); Amazon's listing page says a deleted listing leaves the reports (H5). No source read documents negative values.
- **O10.** The ledger's `Disposition` values as the file writes them (for example the spelling of sellable and of each damaged class) were not read from an Amazon page.

For the office:

- **O11.** What happened to units commingled before 2026-03-31 (H3), and does the rule apply outside the US?
- **O12.** Amazon gives 60 days (English help page, read 2026-10-14), 30 days (its 2021 launch text as a seller quoted it, J1, and the Chinese text via 领星) and a "21 days or longer" bucket for researching. The 60-day sentence is the later read; no dated announcement of the change was found, and whether the Chinese page is simply stale is unresolved.
- **O13.** Whether the pack should name the AWD role as one a seller may add, since without it AWD stock is invisible to cx.

Help pages not read first-hand (script shell to a plain GET on .com and .co.uk; content call off limits by the lead's ruling):

| Id | What it is, as far as known | Why it matters here |
|---|---|---|
| GFC63UNUF6LMLK2R | *Inventory Buyability* (listing playbook's read, 2026-10-14) | definitions of reserved, researching, unfulfillable; the 60-day figure |
| G200740930 | linked by 领星 as a source of its Amazon column definitions; title not established | definitions of report columns |
| 201723860 (G201723860) | linked by 领星 as a source of its Amazon column definitions, and by Topher_Amazon as the "Reserved Inventory report help page" (anchor `#mnd_2jc_jcb`; C1, J4) | definitions of the MYI and reserved columns, including FC transfer's buyability and staging |
| G4FKT5KQWFFJ7LDN | *Inventory Ledger report* (linked from News_Amazon 2022-10-24; J4) | the ledger's columns, reason codes, reconciliation; F5–F7 rest on a third party's copy |
| GCRWH2T93NYDHBXU | *Inventory Ledger report: How to get the information you need* (same post) | how Amazon says the ledger ties to other figures |
| GQ95WW7597USRF5P | *AWD inventory* (linked from News_Amazon 2024-12-09) | AWD states in Seller Central's words; the AWD Inventory report |
| GKT9YKCHXMSDVJKB | planning-report help page, per GitHub issue #5284 | definitions of `fc-transfer`, `Reserved Staging`, on-hand buyable |
| G201711700 | *Amazon Fulfillment Reports* (title from a search result) | index of FBA report help, including the ledger |
| GGU374R3WCTMFK8L | *How to switch to manufacturer barcodes* (linked from the commingling post) | barcode rule after 2026-03-31 |
| GEFKUGES6NSE7CBP | *FBA barcode choice and labeling FAQ* (linked from the commingling post) | same |
| GW6YPQELDZLQ84CF | *Get started with Global Warehousing and Distribution* (linked from sell.amazon.com) | GWD stock states |

Also unreachable: the retired SP-API page *FBA Inventory reports attributes* (`/sp-api/docs/fba-inventory-reports-attributes`), which held column definitions and now redirects to the report-type page; its 2023-10-31 archive capture returned 502 on every attempt. The SP-API changelog entry "Update to the FBA Quantity report for EU" now resolves to the changelog index.

## Positions

Marketplace scope is worldwide unless the position states otherwise.

**P-stock-states-1.** Amazon names five states for FBA stock: fulfillable ("can be picked, packed, and shipped"), inbound ("on its way to Amazon's fulfillment network"), reserved, unfulfillable ("cannot be sold") and researching. [official] *FBA Inventory API* guide (2026-09-09). §A1.

**P-stock-states-2.** `getInventorySummaries` returns one summary per seller SKU for one marketplace, and its `totalQuantity` is "the total number of units in an inbound shipment or in Amazon fulfillment centers", so it includes inbound. [official] `fbaInventory.json`. §B1, §B2.

**P-stock-states-3.** The quantity breakdown (`inventoryDetails`) is returned only when the request sets `details` to true; the default is false. [official] `fbaInventory.json`; *Get inventory summaries*. §B3.

**P-stock-states-4.** Amazon defines inbound working as units in a shipment "for which you have notified Amazon", inbound shipped as units for which the seller has also "provided a tracking number", and inbound receiving as units "that have not yet been received … but are part of an inbound shipment with some units that have already been received and processed". [official] `fbaInventory.json`. §B4.

**P-stock-states-5.** By shipment status, Amazon's notification schema counts WORKING shipments as Working, and SHIPPED, IN_TRANSIT, DELIVERED and CHECKED_IN shipments as Shipped; Receiving begins only when units "are in progress to be received". 赛狐 instead groups DELIVERED and CHECKED IN under receiving (its mapping). [official] `FBAInventoryAvailabilityChangeNotification.json`; [opinion] 赛狐. §G2, §P5.

**P-stock-states-6.** In the API, reserved has three parts: `pendingCustomerOrderQuantity` (reserved for customer orders), `pendingTransshipmentQuantity` (moving between fulfilment centres) and `fcProcessingQuantity` (sidelined for additional processing). [official] `fbaInventory.json`. §B5.

**P-stock-states-7.** An Amazon forum moderator stated on 2024-08-26 that units in FC transfer "are available for customers to buy", possibly with a future ship date, citing the Reserved Inventory report help page (G201723860, not read), while Amazon's *Inventory Buyability* help page (read 2026-10-14 by the listing playbook) says customers cannot buy reserved units. Both stand as Amazon's words; the buyable statement is one moderator's post, not a help page read first-hand. [official] Topher_Amazon, Amazon seller forums; *Inventory Buyability* GFC63UNUF6LMLK2R (not re-read). §C1, §C2, §A3.

**P-stock-states-8.** FC processing covers, in Amazon's words, "verification of item dimensions and weight, pending investigations, or pending removal orders". [official] Topher_Amazon, UK forum, 2024-08-26; [official, via 领星] Amazon's Chinese column text. §C1, §C4.

**P-stock-states-9.** The API's reserved total includes units in FC transfer by definition, while 领星 and 积加 describe Seller Central's reserved figure as customer orders plus FC processing with FC transfer outside it, and DataHawk reports that the planning report includes FC transfer in reserved only in the IN, SA, AE, BR and AU stores. Amazon has not published which holds per report. [official] `fbaInventory.json`; [opinion] 领星, 积加, DataHawk (2026-06-01). §B5, §P3, §P5.

**P-stock-states-10.** Amazon's report page as read on 2026-11-10 lists no FC-transfer column on `GET_RESERVED_INVENTORY_DATA`; its reserved columns are `reserved_qty`, `reserved_customerorders`, `reserved_fc-processing` and `reserved_staging` (US, CA, JP, UK, DE, FR, IT, ES). A developer reported the `reserved_fc-transfers` column removed without notice on 2026-06-22. [official] *FBA Reports* (2026-10-13); [opinion] GitHub issue #5283. §E3, §P8.

**P-stock-states-11.** Developers reported that the stock columns of the reserved, planning and MYI reports changed between June and September 2026 (FC-transfer and staging columns removed, renamed or added) and Amazon's release notes record none of it; on one point the developers' report (the MYI FC-transfer and on-hand-buyable columns gone on 2026-09-07) and Amazon's column list of 2026-10-13 (which has both) disagree. The dated changes are the developers' word, not Amazon's; a file's own header row states what that file contains. [official] *FBA Reports* (2026-10-13); [opinion] GitHub issues #5283, #5284, #5289. §E1, §E3, §P8.

**P-stock-states-12.** Researching is, in Amazon's definition, "misplaced or warehouse damaged units that are actively being confirmed", and the API ages it in three buckets: 1–10 days, 11–20 days, and 21 days or longer. [official] `fbaInventory.json`. §B6.

**P-stock-states-13.** Amazon's sources give two different limits for the researching state: its 2021 launch text, as a seller quoted it on Amazon's forum, says the research "will never exceed 30 days", and the Chinese text 领星 reproduces says the same; the English *Inventory Buyability* help page (read 2026-10-14 by the listing playbook) says "up to 60 days". Neither was read first-hand on Amazon's help pages on 2026-11-10. [official] *Inventory Buyability* (not re-read); [official, via a seller's forum post, 2021-04-07]; [official, via 领星]. §A3, §J1, §P5.

**P-stock-states-14.** Unfulfillable has six dispositions in the API: customer damaged, warehouse damaged, distributor damaged, carrier damaged, defective and expired. [official] `fbaInventory.json`. §B7.

**P-stock-states-15.** Future supply buyable is the number of inbound units customers can find and buy through In-Stock Head Start, and reserved future supply is the number already bought while in transit; both are in the MYI reports and in `FBA_INVENTORY_AVAILABILITY_CHANGES` and neither is in `getInventorySummaries`. [official] `FBAInventoryAvailabilityChangeNotification.json`; *FBA Reports*; `fbaInventory.json`. §D.

**P-stock-states-16.** Units sold through In-Stock Head Start are still inside inbound, so "inbound" is not always unsold stock. [official] `FBAInventoryAvailabilityChangeNotification.json`; News_Amazon 2019-07-25. §D1, §D2.

**P-stock-states-17.** The API's only granularity is the marketplace, and a marketplace's fulfillable quantity is the stock that "could be fulfilled in the given marketplace", not the stock physically in that country. [official] `fbaInventory.json`. §B8.

**P-stock-states-18.** Two developers report (2023-09-22, 2024-04-11) that under Pan-European FBA `getInventorySummaries` returns the same sum for each participating EU marketplace (the UK excluded), so adding those marketplaces multiplies the stock. Amazon's guide does not mention it; Amazon's model says only that a marketplace's quantity is what "could be fulfilled in the given marketplace". Scope: EU stores. [official] `fbaInventory.json` (the granularity definition); [opinion] GitHub issues #452, #360; Improvado. §H4, §J3, §P2, §P8.

**P-stock-states-19.** `GET_AFN_INVENTORY_DATA_BY_COUNTRY` gives the quantity available for local fulfilment per country and is offered for Europe only; it carries no reserved, inbound or unfulfillable figure. Scope: Europe. [official] *FBA Reports*. §E4.

**P-stock-states-20.** A request with `startDateTime` returns the summaries changed since then, reaches back at most 18 months, ignores the SKU filters, and does not detect changes in the three inbound quantities. [official] `fbaInventory.json`. §B9, §B10.

**P-stock-states-21.** A `nextToken` from `getInventorySummaries` expires 30 seconds after it is created, and a `startDateTime` request must repeat `startDateTime` with every token; Amazon support has said an empty page that still carries a token is expected. [official] `fbaInventory.json`; [opinion] GitHub issue #1983 (quoting Amazon support). §B11, §P8.

**P-stock-states-22.** Amazon states that a near real-time FBA report's content is regenerated at most once every 30 minutes and a daily FBA report's at most once every four hours, and that these intervals do not limit how often a report may be requested. [official] *FBA Reports* (2026-10-13). §E0.

**P-stock-states-23.** `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` covers active listings and `GET_FBA_MYI_ALL_INVENTORY_DATA` adds archived ones; both are current snapshots with no history, and Amazon's SP-API page defines none of their columns. [official] *FBA Reports*; [opinion] Improvado. §E1, §P2.

**P-stock-states-24.** `GET_AFN_INVENTORY_DATA` is the report that splits a SKU's available quantity by warehouse condition code, and it requires the Amazon Fulfillment role alone. [official] *FBA Reports*; *Role Mappings for SP-API Types*. §E2.

**P-stock-states-25.** `GET_FBA_INVENTORY_PLANNING_DATA` is not available in the NL, PL, SE and BE stores, has a reduced column set in Brazil, and carries two dates (`snapshot-date` and `Inventory age snapshot date`). [official] *FBA Reports*. §E5.

**P-stock-states-26.** Developers have reported the planning report omitting part of an account's SKUs on some runs while the MYI report stayed complete. [opinion] GitHub issue #5044 (2025-11-19). §P8.

**P-stock-states-27.** `GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA`, `GET_EXCESS_INVENTORY_DATA` and `GET_FBA_INVENTORY_AGED_DATA` were removed on 2022-06-27; six inventory history, adjustment, receipt and reconciliation report types were removed on 2023-01-31; `GET_FBA_UNO_INVENTORY_DATA` was removed on 2024-03-27. [official] *SP-API Deprecation Schedule*. §E8.

**P-stock-states-28.** The Inventory Ledger replaced six reports (Daily Inventory History, Monthly Inventory History, Inventory Event Detail, Inventory Adjustments, Inventory Reconciliation, Received Inventory); Amazon first announced their end for 2022-09-30 and later for 2023-01-31. [official] News_Amazon 2022-08-02 (EU forum); News_Amazon 2022-10-24 (US forum). §F8.

**P-stock-states-29.** The ledger's summary view balances a period as starting balance, receipts, customer shipments, customer returns, vendor returns, transfers, found, lost, damaged, disposed, other and unknown events, and ending balance, per FNSKU and disposition, by country (default) or fulfilment centre and by month (default), week or day. [official] *FBA Reports*. §F1, §F2.

**P-stock-states-30.** The ledger's detail view lists each movement for 18 months with event type (Adjustments, CustomerReturns, Receipts, Shipments, VendorReturns, WhseTransfers), fulfilment centre, disposition, reason, and reconciled and unreconciled quantity. [official] *FBA Reports*. §F1, §F3.

**P-stock-states-31.** The ledger carries no inbound quantity, and it keeps units moving between fulfilment centres in a column ("In Transit Between Warehouses") separate from the ending warehouse balance; Amazon, asked on its forum whether to add the two, gave no rule. [official] *FBA Reports*; Josh_Amazon 2025-01-29; [opinion] ConnectBooks. §F2, §F4, §P6, §P7.

**P-stock-states-32.** A ledger summary request whose dates do not match the chosen period (whole month, whole week) "can return empty data". [official] *FBA Reports*. §F2.

**P-stock-states-33.** The ledger's "Unknown Events" are units whose event type is not known, mainly because parts of one event fall in different reporting periods; a longer period reduces them. [official, via Openbridge]. §F5.

**P-stock-states-34.** In the downloaded ledger, an adjustment's reason is a code; a change of disposition appears as two rows, a decrease (6, 7, E, H, K, U or Q) followed by a P increase. [official, via Openbridge; Reason Automation]. §F5, §F6.

**P-stock-states-35.** Ledger codes M and 5 are units misplaced and F is units found; codes N (found) and O (correction) also cover ownership transfers and units Amazon has reimbursed, so they are not all physical events; codes 3 and 4 are Amazon merging two SKUs it judges to be the same item. [official, via Openbridge]. §F6.

**P-stock-states-36.** A ledger adjustment's unreconciled quantity is the part not yet matched by a later event; Amazon's reconciliation reasons include "Inventory found", "Reimbursed", "Inspected and disposition corrected" and "Inventory ownership correction". [official, via Openbridge]. §F5, §F7.

**P-stock-states-37.** An Amazon moderator stated on 2023-12-05 that reserved units are included in the Inventory Ledger. [official] TaylorR_Amazon, EU forum. §C3.

**P-stock-states-38.** `FBA_INVENTORY_AVAILABILITY_CHANGES` is sent on any change in FBA quantities and carries a snapshot for every eligible store in the region, with inbound and reserved breakdowns. [official] *SP-API Release Notes* 2022-10-19; notification schema. §G1, §G2.

**P-stock-states-39.** `ITEM_INVENTORY_EVENT_CHANGE` is sent hourly at ASIN grain with data delayed up to 24 hours, and its `highlyAvailableInventory` subtracts units in customer shopping carts or bound for other orders. [official] *Notification Type Values* (2026-10-28). §G3.

**P-stock-states-40.** FBA stock is counted per seller SKU; one ASIN can sit under several SKUs of one seller, each with its own quantity. [official] `fbaInventory.json`; *Terminology*; [opinion] GitHub issue #4523. §H1, §H2, §P8.

**P-stock-states-41.** Amazon ended commingling for inventory shipped on or after 2026-03-31: Brand Representative brand owners may use manufacturer barcodes without commingling, resellers must apply Amazon barcode stickers, and products without a manufacturer barcode need Amazon barcodes from everyone. The announcement was read on the US forum and does not say what became of units commingled earlier. [official] News_Amazon 2025-12-08. §H3.

**P-stock-states-42.** Amazon's listing guide says a deleted listing "does not appear in any of the reports or API data"; 积加 reports stock rows for deleted products that it cannot remove. [official] *Understanding Amazon listing status and seller-fulfilled inventory management* (2026-09-09); [opinion] 积加. §H5, §P5.

**P-stock-states-43.** AWD quantities (on hand, inbound to AWD, available to distribute, reserved for a replenishment order, in transit from AWD to FBA) are read from the AWD API's `listInventory`, which needs the Amazon Warehousing and Distribution role and exists for the US store only. Scope: US. [official] `awd_2024-05-09.json`; *Amazon Warehousing and Distribution API*; *Role Mappings for SP-API Operations*. §I3.

**P-stock-states-44.** No FBA report type on Amazon's SP-API report page has an AWD column; Amazon's AWD Inventory report, which shows AWD and FBA stock together, is a Seller Central download. Scope: US. [official] *FBA Reports*; News_Amazon 2024-12-09. §I4.

**P-stock-states-45.** Amazon states that with AWD auto-replenishment enabled a product is "considered in stock and buyable" when AWD receives it. Scope: US. [official] sell.amazon.com/programs/warehousing. §I2.

**P-stock-states-46.** Amazon states that a seller "can't move inventory from FBA to AWD because items are stored differently in our fulfillment and distribution centers". Scope: US. [official] sell.amazon.com/programs/warehousing. §I1.

**P-stock-states-47.** GWD stores stock in Shenzhen, Shanghai and Ningbo for replenishment into the US fulfilment network; no SP-API field for GWD stock was found. Scope: US-bound stock. [official] sell.amazon.com/programs/warehousing. §I5.

**P-stock-states-48.** Tools differ on "sellable": Nova and Improvado count available plus FC transfer; 领星's 可售库存 is `afn-fulfillable-quantity` alone and its FBA库存 adds FC transfer and FC processing; 积加's 可售 is local plus remote fulfillable in Europe. These are the tools' definitions. [opinion] Novadata; Improvado; 领星; 积加. §P1, §P2, §P5.

**P-stock-states-49.** Practitioners give durations for reserved states that Amazon does not publish: SoStocked says FC transfer "usually takes 1-5 days but can take up to 30 days" and FC processing two working days on average. [opinion] SoStocked (SPS Commerce), 2026-03-06. §P4.

**P-stock-states-50.** The roles Amazon names for the stock reads are: Amazon Fulfillment or Product Listing for `getInventorySummaries`; Amazon Fulfillment or Pricing for the MYI, reserved, by-country and restock reports; Amazon Fulfillment alone for `GET_AFN_INVENTORY_DATA`, the planning report, both ledger views and `FBA_INVENTORY_AVAILABILITY_CHANGES`; Brand Analytics for `ITEM_INVENTORY_EVENT_CHANGE`. [official] *Role Mappings for SP-API Operations* (2026-10-28); *Role Mappings for SP-API Types* (2026-09-09). §E, §G, §R1–R9.

**P-stock-states-51.** (added by the verifier) Amazon's 2021 text on researching, as a seller quoted it, says that once researched units are reimbursed or the research period ends, the adjustment moves to the Inventory Adjustment report, a report the Inventory Ledger has since replaced. [official, via a seller's forum post, 2021-04-07]; News_Amazon 2022-10-24. §J1, §F8.

**P-stock-states-52.** (added by the verifier) Ledger quantities are signed: sellers quote negative `Quantity` rows in the detail view and negative `Receipts` in the summary view, and an Amazon moderator said of one such case that the units "might be in transfer to another warehouse" and that the reason code decides. No source documents negative values in `getInventorySummaries` or the MYI file. [official] TaylorR_Amazon 2024-08-21; [opinion] sellers on Amazon's forums (2024-08-13, 2025-05-05); [official, via Openbridge] the reason-code signs. §J2, §F6.

The seat's own (no source; enters no skill):

- Adding AWD `replenishmentQuantity` to FBA inbound may count the same units twice, if Nova is right that a replenishment is also an FBA inbound shipment.
- The supply-chain blog's sentence that inbound units "are available for fulfillment" reads as a description of In-Stock Head Start generalised to all inbound.
- The June–September 2026 column changes look like one migration: FC transfer moving out of "reserved" and into an "on-hand buyable" figure in the reports, while the API keeps the old grouping.
- The 60-day and 30-day researching limits may be two versions of one help page: 30 days at launch in 2021, 60 days later, with the Chinese page not updated (J1).
- Topher_Amazon's wording of the three reserved parts is probably the text of help page G201723860, which the post links.
- An all-zero API response or a planning file missing SKUs is more likely a fault of the read than a real stock-out; a second read of a different kind would tell them apart.

## Pages read

All read 2026-11-10 by plain GET unless stated. "dd" = read as markdown at `developer-docs.amazon/sp-api/docs/<slug>.md`.

| Page name | URL | Date read | Tag | Reached how / unreachable |
|---|---|---|---|---|
| FBA Inventory API (guide) | https://developer-docs.amazon.com/sp-api/docs/fba-inventory-api | 2026-11-10 | official | dd |
| Get inventory summaries (FBA) | https://developer-docs.amazon.com/sp-api/docs/get-fba-inventory-summaries | 2026-11-10 | official | dd |
| Fulfillment by Amazon (FBA) Reports | https://developer-docs.amazon.com/sp-api/docs/report-type-values-fba | 2026-11-10 | official | dd |
| Inventory Reports | https://developer-docs.amazon.com/sp-api/docs/report-type-values-inventory | 2026-11-10 | official | dd |
| Role Mappings for SP-API Operations | https://developer-docs.amazon.com/sp-api/docs/role-mappings | 2026-11-10 | official | dd |
| Role Mappings for SP-API Types | https://developer-docs.amazon.com/sp-api/docs/role-mappings-for-types | 2026-11-10 | official | dd |
| SP-API Deprecation Schedule | https://developer-docs.amazon.com/sp-api/docs/sp-api-deprecations | 2026-11-10 | official | dd |
| SP-API Release Notes | https://developer-docs.amazon.com/sp-api/docs/sp-api-release-notes | 2026-11-10 | official | dd |
| Notification Type Values | https://developer-docs.amazon.com/sp-api/docs/notification-type-values | 2026-11-10 | official | dd |
| Amazon Warehousing and Distribution API (guide) | https://developer-docs.amazon.com/sp-api/docs/amazon-warehousing-and-distribution-api | 2026-11-10 | official | dd |
| Get inventory summaries (AWD) | https://developer-docs.amazon.com/sp-api/docs/get-inventory-summaries | 2026-11-10 | official | dd |
| Terminology | https://developer-docs.amazon.com/sp-api/docs/terminology | 2026-11-10 | official | dd |
| Understanding Amazon listing status and seller-fulfilled inventory management | https://developer-docs.amazon.com/sp-api/docs/understanding-amazon-listing-status-and-seller-fulfilled-inventory-management | 2026-11-10 | official | dd (two quoted lines re-read; rest is the listing playbook's read) |
| FBA Inventory reports attributes | https://developer-docs.amazon.com/sp-api/docs/fba-inventory-reports-attributes | 2026-11-10 | official | **unreachable**: redirects to the report-type page; web.archive.org capture 20231031221616 returned 502/timeout on repeated tries |
| Update to the FBA Quantity report for EU (changelog) | https://developer-docs.amazon.com/sp-api/changelog/update-to-the-fba-quantity-report-for-eu | 2026-11-10 | snippet | **unreachable**: `.md` gives Page Not Found, HTML resolves to the changelog index; search summary only |
| `fbaInventory.json` | local: `scratch/sp-api-plugins/models/models/fba-inventory-api-model/fbaInventory.json` | 2026-11-10 | official | local clone, commit db2936aa |
| `awd_2024-05-09.json` | local: `…/models/amazon-warehousing-and-distribution-model/awd_2024-05-09.json` | 2026-11-10 | official | local clone |
| `FBAInventoryAvailabilityChangeNotification.json` | local: `…/schemas/notifications/FBAInventoryAvailabilityChangeNotification.json` | 2026-11-10 | official | local clone |
| Inbound and storage (Amazon Supply Chain blog) | https://supplychain.amazon.com/blog/inbound-and-storage | 2026-11-10 | official | GET |
| Amazon Warehousing and Distribution (program page) | https://sell.amazon.com/programs/warehousing | 2026-11-10 | official | GET |
| Global Warehousing and Distribution (guessed program page) | https://sell.amazon.com/programs/global-warehousing-and-distribution | 2026-11-10 | official | **unreachable**: 404 |
| Seller University module on GWD | https://sellercentral.amazon.com/learn/learning-module/c80eefc0-946e-4941-a11e-3dc815ffcce9 | 2026-11-10 | official | **unreachable**: script shell |
| News_Amazon, "Commingling practices will end effective March 31, 2026" (2025-12-08) | https://sellercentral.amazon.com/seller-forums/discussions/t/106d0747-e5c6-44d8-86f3-7669f11238fe | 2026-11-10 | official | GET, `__NEXT_DATA__` |
| News_Amazon, "Switch to the new Inventory Ledger report now" (2022-10-24) | https://sellercentral.amazon.com/seller-forums/discussions/t/bbf046a42a47d98c537cd0e74786a9c4 | 2026-11-10 | official | GET, `__NEXT_DATA__` |
| News_Amazon, "New report simplifies FBA inventory information" (2022-08-02) | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/d02a7c4222e0c877da74bffe7812fa1d | 2026-11-10 | official | GET, `__NEXT_DATA__` |
| News_Amazon, "Global FBA Inventory report will be retired on December 27, 2024" (2024-12-09) | https://sellercentral.amazon.com/seller-forums/discussions/t/9b51ac6d-2183-43ff-82b0-2b4b63034f0a | 2026-11-10 | official | GET, `__NEXT_DATA__` |
| News_Amazon, "FBA Products in stock soon? Make them available now" (2019-07-25) | https://sellercentral.amazon.com/seller-forums/discussions/t/e061bc46a55f2c54b0a71f8085b7e018 | 2026-11-10 | official | GET, `__NEXT_DATA__` |
| "Researching - FBA Inv" (seller's quotation of Amazon's text, 2021-04-07) | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/5b46fd45c5a27980040dbe30d9a84637 | 2026-11-10 (verifier) | official, via a seller | GET, `__NEXT_DATA__` |
| "What does it mean when Quantity in Inventory Ledger has a -14" (2024-08-13; TaylorR_Amazon 2024-08-21) | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/2fcc4acb-0709-410e-8f8c-e2ffecba48a8 | 2026-11-10 (verifier) | opinion; official (Amazon reply) | GET, `__NEXT_DATA__` |
| "Inquiry Regarding Missing Inventory from AWD to FBA Transfers" (2025-05-05; KJ_Amazon 2025-05-07) | https://sellercentral.amazon.co.uk/seller-forums/discussions/t/3933f3a7-c04e-4b02-a3f4-92fcfa2c4f3d | 2026-11-10 (verifier) | opinion; official (Amazon reply, no rule) | GET, `__NEXT_DATA__` |
| Wayback availability API for *FBA Inventory reports attributes* | https://archive.org/wayback/available?url=developer-docs.amazon.com/sp-api/docs/fba-inventory-reports-attributes | 2026-11-10 (verifier) | — | capture 20231031221616 exists; the capture itself **unreachable** (502, then no response) |
| Topher_Amazon reply on reserved inventory (2024-08-26) | https://sellercentral.amazon.co.uk/seller-forums/discussions/t/c07904af-be04-432d-8c67-80ab0a46f601 | 2026-11-10 | official | GET, `__NEXT_DATA__` |
| TaylorR_Amazon reply on reserved units and the ledger (2023-12-05) | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/049699ca-8a05-4c03-9ea2-168705fbdfd0 | 2026-11-10 | official | GET, `__NEXT_DATA__` |
| "Ending FBA Inventory Balance" thread (2025-01-09; Josh_Amazon 2025-01-29) | https://sellercentral.amazon.com/seller-forums/discussions/t/5106c5df-c87c-4d3d-9d7c-49d28eb98a09 | 2026-11-10 | opinion; official (Amazon reply) | GET, `__NEXT_DATA__` |
| Seller thread on reserved after receipt (2018-02-13) | https://sellercentral.amazon.com/seller-forums/discussions/t/55cac1eccb7e8fb9f5f5fa80bd46d2fd | 2026-11-10 | opinion | GET, `__NEXT_DATA__` |
| Seller thread on Future Supply Buyable (2019-09-27) | https://sellercentral.amazon.com/seller-forums/discussions/t/ba94f57762f61763f636d21eca9cb6af | 2026-11-10 | opinion | GET, `__NEXT_DATA__` |
| "EU FBA inventory shows when UK country is selected" (2025-03-26) | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/bfac5e0c-f255-407d-8bbb-8436878cce35 | 2026-11-10 | opinion | GET, `__NEXT_DATA__` |
| Seller Central help GFC63UNUF6LMLK2R, G200740930, G201723860, GKT9YKCHXMSDVJKB, G201711700, GGU374R3WCTMFK8L, GEFKUGES6NSE7CBP, GW6YPQELDZLQ84CF | https://sellercentral.amazon.com/help/hub/reference/external/<ID> | 2026-11-10 | official | **unreachable**: script shell on .com and .co.uk with `?locale=en-US`; content call off limits |
| Openbridge gists (ledger reason codes; reconciliation reasons; summary and detail column definitions) | https://gist.github.com/tspicer/006f51f798b9803bf0b0ef3fc93b4266 ; /d62e47ef7fc24d62136936a5d48f1800 ; /1743a3d2cd1085400bb393b68412e148 ; /afc2e79bca4c95c5f54f582f8236e933 | 2026-11-10 | official, via Openbridge | GET |
| Reason Automation, Inventory Ledger Details | https://help.reasonautomation.com/seller/inventory-ledger-details | 2026-11-10 | official, via Reason Automation; opinion | GET |
| Novadata, Inventory glossary | https://novadata.io/docs/inventory-and-catalogue/inventory-glossary.md | 2026-11-10 | opinion | GET |
| Improvado, Manage FBA Inventory report | https://improvado.io/product-updates/connectors/amazon-seller-central-manage-fba-inventory-report | 2026-11-10 | opinion | GET |
| DataHawk changelog 2026-06-01 | https://docs.datahawk.co/changelog/2026-06-01-fba-planning-reserved-quantity | 2026-11-10 | opinion | GET |
| SoStocked / SPS Commerce, Amazon reserved inventory | https://www.spscommerce.com/community/articles/amazon-reserved-inventory | 2026-11-10 | opinion | GET |
| m19, What is the inventory | https://help.m19.com/what-is-the-inventory | 2026-11-10 | opinion | GET |
| ConnectBooks, Inventory Ledger Report Explained | https://help.connectbooks.com/en/articles/8955528-inventory-ledger-report-explained | 2026-11-10 | opinion | GET |
| ConnectBooks, AWD Report Explained | https://help.connectbooks.com/en/articles/12683512-awd-report-explained | 2026-11-10 | opinion | GET |
| 领星 Lingxing, FBA库存 help | https://www.lingxing.com/help/article/fbaInventory | 2026-11-10 | opinion; official, via 领星 | GET |
| 积加 Jijia, FBA inventory help | https://help.jijiaerp.com/docs/v5Wl4W20 | 2026-11-10 | opinion | GET |
| 赛狐 Sellfox, FBA库存 help | https://www.sellfox.com/help/features.html?id=162 | 2026-11-10 | opinion | GET |
| 赛狐 Sellfox, AWD help | https://www.sellfox.com/help/features/awd-amazon-warehouse-distribution-network | 2026-11-10 | opinion | GET |
| GitHub issues #5283, #5284, #5289, #5414, #5044, #4946, #4523, #2447, #2275, #2167, #1983, #452, #421, #360 | https://github.com/amzn/selling-partner-api-models/issues/<N> | 2026-11-10 | opinion (Amazon staff replies noted) | `gh` read-only |
| DeHoratius and Raman 2008 (abstract) | https://econpapers.repec.org/RePEc:inm:ormnsc:v:54:y:2008:i:4:p:627-641 | 2026-11-10 | research | GET |
| EcomCrew, Amazon GWD vs AWD (updated 2026-05-04); My Amazon Guy, GWD in Shenzhen | https://www.ecomcrew.com/amazon-global-warehousing-distribution/ ; https://myamazonguy.com/news/new-amazon-gwd-in-shenzhen-china/ | 2026-11-10 | opinion | GET; skimmed, nothing built on them |
| SoStocked ledger article; Feedvisor help | (sostocked.com ledger URL; feedvisor zendesk) | 2026-11-10 | opinion | **unreachable**: 404; 403 |
| Survey notes `03-job-stock.md`, `03-tools-cn.md` | local: `scratch/sp-api-plugins/` | 2026-11-10 | seat's starting material | local; claims used only where marked "not re-read" |
| Listing playbook, `inventory-and-fulfillment.md` | local: `packages/cx-listing-playbook/research/angles/` | 2026-11-10 | that seat's read of 2026-10-14 | local; quotations marked as not re-read |
| Door, `references/door.md` | local: `packages/cx-amazon-sp-api-305/skills/amazon-sp-api/` | 2026-11-10 | local | the five roles |

## Verification

Verified 2026-11-10 by the verifier (not the research seat). Fresh copies of every page re-opened are under `scratch/stock-playbook/stock-states/verify/`.

**What was checked.** All 50 positions, and about 150 other claims: every quoted sentence and field name in A–I against a page fetched again today or the local file; every column list in E and F; every role; every date in E8, F8 and the release-note citations; every practitioner quotation in P1–P9; the research abstract.

**Re-opened and found as stated.** `fbaInventory.json` (all field descriptions, the `startDateTime` note "Changes in inboundWorkingQuantity, inboundShippedQuantity and inboundReceivingQuantity are not detected", the 18-month reach, the 30-second token, 50 SKUs, rate 2/2, the three sandbox-only operations); the notification schema; `awd_2024-05-09.json`; the *FBA Inventory API* guide and *Get inventory summaries*; the FBA report page (`updatedAt` 2026-10-13; every column list in E1–E6, F2, F3 matches, including no `reserved_fc-transfers` and the presence of `afn-fc-transfer-quantity` and `afn-onhand-buyable-quantity`); *Inventory Reports*; the deprecation schedule; release notes (2022-09-21, 2022-10-19, 2024-08-19, 2024-12-18, 2025-01-29); *Notification Type Values*; *Terminology*; the listing-status guide; the AWD guide; the supply-chain blog (published 2021-05-14, modified 2026-05-04); sell.amazon.com/programs/warehousing; the News_Amazon posts of 2019-07-25, 2022-08-02, 2022-10-24, 2024-12-09 and 2025-12-08 (commingling: "inventory shipped on or after March 31, 2026", verbatim); the Topher_Amazon, TaylorR_Amazon and Josh_Amazon replies; GitHub issues #5283, #5284, #5289, #452, #360, #1983, #2447, #4946, #2167, #2275, #421, #5044, #5414, #4523; the four Openbridge gists; Reason Automation; Novadata; Improvado; DataHawk; SPS Commerce; ConnectBooks (both); m19; 领星; 积加; 赛狐 (both); the RePEc abstract; three seller threads of P7.

**Roles.** Checked against *Role Mappings for SP-API Operations* (2026-10-28), *Role Mappings for SP-API Types* (2026-09-09) and the report page's own Roles lines: every role in the file is right. `getInventorySummaries` = Amazon Fulfillment or Product Listing; MYI (both), reserved, by-country, restock = Amazon Fulfillment or Pricing; `GET_AFN_INVENTORY_DATA`, planning, both ledger views, `FBA_INVENTORY_AVAILABILITY_CHANGES` = Amazon Fulfillment; `ITEM_INVENTORY_EVENT_CHANGE` = Brand Analytics; `GET_MERCHANT_LISTINGS_ALL_DATA` and `GET_PAN_EU_OFFER_STATUS` as stated; AWD reads = Amazon Warehousing and Distribution, outside the five, and no position rests on them (P-43 states the role as a fact). `listReplenishmentOrders` and `getReplenishmentOrder` are absent from the operations page, as the file says. One note: the *Get inventory summaries* tutorial names only the Product Listing role as its prerequisite; the role-mappings page and the API guide name both.

**Changes.**

| Where | What it said | What the source says | What was done |
|---|---|---|---|
| B6 | quoted "misplaced or warehouse damaged units…" as `totalResearchingQuantity` | that sentence describes the `ResearchingQuantity` object; the field is "The total number of units currently being researched in Amazon's fulfillment network." | corrected; P-12 stands |
| C1, C3, P-7 | "Amazon UK seller forums" / "EU forums" | the posts' `marketplaceId` is the US store's; the address is only where they were read | reworded |
| C1, Open questions table | the moderator names the Reserved Inventory report help page "without an id"; G200740930 guessed [seat] | the post links G201723860 `#mnd_2jc_jcb` | corrected; guess removed |
| C2, P-7 | reports' columns "(E3)" side with the buyable statement | the columns are in E1; a second-hand paraphrase of help page GKT9YKCHXMSDVJKB (issue #5284) also says buyable with delay; no Amazon page uses "future supply" for FC transfer | reference fixed; paraphrase added with its tag; P-7 now says the buyable statement is one moderator's post |
| D2 | a seller's quotation that In-Stock Head Start opened to all "Beginning on October 10, 2019" | not on the thread as served today | removed |
| E3, P-11, *Stable enough* | "Amazon changed … without a release note" stated as fact with an [official] tag | the dated changes are developers' reports (#5283, #5284, #5289); Amazon's page shows only today's lists | reworded as developers' reports; added a 2023-11-30 seller post that corroborates the old `reserved_fc-transfers` column |
| P7 | cross-dock remark placed on issue #5284 | it is on #5289 (2026-06-29) | corrected |
| P7 | "future-supply-buyable units drop to zero on receipt and reappear as FC transfer" | the seller says in-transit units showed as inbound and future supply buyable while received shipments showed under reserved | reworded |
| P8 | #452/#360 as plain fact of the API; "pages hold at most 50" | two developers' reports; Amazon's replies neither confirm nor deny; UK excluded; the page size is one developer's observation | qualified; P-18 reworded |
| P-13, O12, P5 | 60 days (English) against 30 days (Chinese, via 领星) | the 30-day limit is also Amazon's 2021 English launch text, as a seller quoted it | J1 added; P-13 reworded; tags kept below plain [official] |
| P-46 | "Amazon cannot move stock from FBA to AWD" | "You can't move inventory from FBA to AWD because…" | reworded as Amazon's statement |
| Open questions table | ledger and AWD help ids "not found" | ids are in Amazon's posts | filled (J4) |

Positions: 50 checked; 5 corrected (7, 11, 13, 18, 46); 0 removed; 2 added (51, 52). No position was found to be an instruction to cx.

**The six claims the lead named.** (1) Reserved in the API includes transshipment by the model's definition (confirmed); the report page today has no FC-transfer column on the reserved report (confirmed); FC-transfer buyability rests on one moderator post plus a second-hand paraphrase, against the help page's general sentence, and no Amazon "future supply" statement about FC transfer exists; the June–September 2026 column changes are developer reports and are now tagged so. (2) Pan-EU shared sum: two developer reports found and read; nothing in Amazon's guide; stays [opinion]. (3) `startDateTime` blind to inbound: confirmed verbatim in the model. (4) Researching limit: both figures are Amazon's, 30 days (2021) and 60 days (help page read 2026-10-14); neither read first-hand today. (5) Commingling: confirmed verbatim from News_Amazon 2025-12-08; "for inventory shipped on or after March 31, 2026"; no marketplace scope and no word on earlier units. (6) Ledger reason codes: no better source found (no report schema, no developer-docs definitions, help page G4FKT5KQWFFJ7LDN unread); the Openbridge tag stays.

**Could not be re-opened.** Every Seller Central help page (script shell; content call off limits): GFC63UNUF6LMLK2R, G201723860, G200740930, GKT9YKCHXMSDVJKB, G4FKT5KQWFFJ7LDN, GCRWH2T93NYDHBXU, GQ95WW7597USRF5P, G201711700, GGU374R3WCTMFK8L, GEFKUGES6NSE7CBP, GW6YPQELDZLQ84CF. The Wayback capture of *FBA Inventory reports attributes* (exists; 502). The changelog entry on EU local/remote columns (still [snippet]). The listing playbook's 2026-10-14 quotations in A3 (kept as that seat's read). The survey's 领星 formula in P5 (kept as "not re-read").

**Gaps filled.** J1 researching limit; J2 negative ledger quantities; J3 Pan-EU absent from Amazon's guide; J4 help-page ids; J5 no report schema or Data Kiosk dataset for FBA quantities; J6 AWD and FBA fields (what Amazon does and does not say).

**Gaps left.** Amazon's definitions of the MYI, reserved and planning columns (help pages unread). Whether the three reserved parts sum to the total and tie to `afn-reserved-quantity` (O1). Which MYI columns a file carries today per store, and the four columns a developer says were added in March 2026 (O2). Where AWD-buyable units show in FBA fields and whether AWD replenishment double-counts with FBA inbound (O3; J6). Whether staging sits inside `fcProcessingQuantity` (O4). The ledger's lag in days (O5; only "updated daily", 2022). Negative values and deleted-listing rows in the API and MYI file (O9). The ledger's `Disposition` spellings (O10). What an old hand would also look for and the file lacks: a first-hand statement of how long units may sit in FC transfer or FC processing (only SoStocked's figures); how reserved behaves around Prime Day and Q4 receipts; what the `program` column of the reserved report and the `stores`/`store` fields contain; the values of `Warehouse-Condition-code`; how removal orders in progress show across the API, the reserved report and `pending-removal-quantity`; North American remote fulfilment's effect on CA and MX rows (O7). Published research on FBA states: none found, confirmed by search.
