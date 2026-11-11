# The SP-API surface a stock job touches

Read 2026-11-10 by the research seat. Verified 2026-11-10 by a second seat (see *Verification* at the end).

Tags: **[official]** is Amazon's own words (a developer-docs page, the release notes, the deprecation schedule, or a
model file); **[opinion]** is a named developer or tool; **[seat]** is this seat's inference and enters no skill.
A model is cited as `<file>` in the local clone of `amzn/selling-partner-api-models` at commit
`db2936aa19f4b48185173c385c51ab115166f221` (2026-10-29 12:21 -0700), under
a local clone of `amzn/selling-partner-api-models`. On 2026-11-10 GitHub's commit list for that
repository since 2026-10-29 returned that one commit and no later one ("SPAPI October Release Finance API Rollback"),
so the clone is the head and no later commit touches a stock model.

How pages were reached: every developer-docs page was fetched with a plain GET of
`https://developer-docs.amazon.com/sp-api/docs/<slug>.md` (the page's markdown twin; its front matter carries
`updatedAt`, quoted below as "updated"). The index of slugs is `https://developer-docs.amazon.com/sp-api/llms.txt`.
No Amazon API host was called. No Seller Central help page was read (they serve a script shell; see *Open questions*).

Role abbreviations: PL Product Listing, PR Pricing, BA Brand Analytics, FA Finance and Accounting, AF Amazon
Fulfillment (the door's five); IOT Inventory and Order Tracking, SPI Selling Partner Insights, DTC Direct-to-Consumer
Shipping (Restricted), AWD Amazon Warehousing and Distribution (outside the five). "Reach: yes" means at least one of
the five roles is named for the read.

## What this covers

- Every operation, report type, Data Kiosk dataset, feed and notification a stock job can touch, with method and path,
  role, rate and burst, and whether the door's five roles reach it.
- Full column lists of the 21 main stock reports, as Amazon's report-type pages print them.
- Limits and lags in one place: rates, history windows, retention, missing regions, time zones, page-against-model
  disagreements, the 2025–2026 release notes and deprecations that touch stock, and 2027 announcements.
- What the door's own skill already states, what it lacks for a stock job, and whether cx can write each call itself.

Owned elsewhere and only cross-referenced: what each quantity state, fee and program means (`areas/` and `beyond/`
files); the compiled list of what no API carries (`method/seller-central-only.md`; this file lists the absences it
establishes); token steps, the report lifecycle and document URLs (the door:
`packages/cx-amazon-sp-api-305/skills/amazon-sp-api/references/door.md`).

## Amazon's own rules

### A. The two role pages and how far they can be trusted

- *Role Mappings for SP-API Operations* (`role-mappings`, updated 2026-10-28) lists 350 operations. [official]
- *Role Mappings for SP-API Types* (`role-mappings-for-types`, updated 2026-09-09) lists 181 feed, notification and
  report types. [official]
- *Roles in the Selling Partner API* (`roles-in-the-selling-partner-api`, updated 2026-11-03): "The Amazon Fulfillment
  role provides access to Amazon fulfillment operations and shipping services such as Fulfillment by Amazon (FBA) and
  Amazon Fulfillment Network (AFN)." IOT and Pricing are "available to vendors? No"; AF, PL, BA, FA are available to
  both. [official]
- Compared on 2026-11-10 by the verifier across all 16 report-type pages and 6 feed-type pages in `llms.txt`, 125
  report and feed types carry a Roles line on their own type page. Amazon Fulfillment is named on both sources for
  every unrestricted report on the FBA page. The two sources disagree on which other roles also reach: 
  `GET_AFN_INVENTORY_DATA_BY_COUNTRY` (type page PR, AF; types page AF only);
  `GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL` (type page PR, AF, IOT; types page AF only);
  `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL` (FBA page PR, AF, IOT, DTC, PL; order page PL, AF, IOT, DTC
  without PR; types page all five); `JSON_LISTINGS_FEED` (type page PL; types page IOT, PL);
  `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE` (type page adds IOT); `GET_CSV_MFN_PRIME_RETURNS_REPORT` (type page DTC,
  IOT, PR; types page DTC). On a type page and absent from the types page: `GET_XML_RETURNS_DATA_BY_RETURN_DATE`,
  `GET_DATE_RANGE_FINANCIAL_HOLDS_DATA`, `SC_VAT_TAX_REPORT`. `GET_PENDING_ORDERS_DATA` has no Roles line on the
  order page (the PL line there belongs to `GET_CONVERGED_FLAT_FILE_PENDING_ORDERS_DATA`); the types page gives IOT.
  [official, both pages]
- The types page still lists types the deprecation schedule has removed: `GET_FBA_SNS_FORECAST_DATA` and
  `GET_FBA_SNS_PERFORMANCE_DATA` (removed 2025-12-11), `ORDER_STATUS_CHANGE` (removed 2026-07-29),
  `POST_SHIPPING_OVERRIDE_DATA` (removed 2025-12-03). It lists `GET_FBA_FULFILLMENT_INVENTORY_EXPIRATION_DATE_DATA`
  (AF), which the FBA report-type page does not describe. [official]
- The operations page has no row for Fulfillment Outbound v2026-07-04 and none for AWD's outbound and
  replenishment-order operations; the Fulfillment Outbound guide itself (updated 2026-09-09) gives AF, NA/EU/FE for
  each v2026-07-04 operation. [official]

### B. FBA Inventory v1

Guide `fba-inventory-api` (updated 2026-09-09): the API lets a seller "retrieve information and track the real-time
availability of your inventory in Amazon's fulfillment network at the marketplace level"; "This API is available in all
marketplaces."; sellers only. The guide prints no marketplace list any more. Model `fba-inventory-api-model/fbaInventory.json`. [official]

| Operation | Method and path | Role (operations page) | Rate / burst | Reach |
|---|---|---|---|---|
| `getInventorySummaries` | `GET /fba/inventory/v1/summaries` | AF; PL (NA, EU, FE) | 2 / 2 | yes |
| `createInventoryItem`, `deleteInventoryItem`, `addInventory` | `POST /fba/inventory/v1/items`, `DELETE …/items/{sellerSku}`, `POST …/items/inventory` | AF; PL | sandbox only | not production |

Parameters of `getInventorySummaries` (model descriptions quoted):

| Parameter | Required | Model's words |
|---|---|---|
| `details` | no, default false | "true to return inventory summaries with additional summarized inventory details and quantities. Otherwise, returns inventory summaries only (default value)." |
| `granularityType` | yes | enum `Marketplace` only |
| `granularityId` | yes | "When granularityType is Marketplace, specify the marketplaceId." |
| `marketplaceIds` | yes, max 1 | the store the summaries are for |
| `startDateTime` | no | "If specified, all inventory summaries that have changed since then are returned. You must specify a date and time that is no earlier than 18 months prior to the date and time when you call the API. Note: Changes in inboundWorkingQuantity, inboundShippedQuantity and inboundReceivingQuantity are not detected." |
| `sellerSkus` | no, max 50 | "You may specify up to 50 SKUs." |
| `sellerSku` | no | one SKU; `sellerSkus` wins when both are sent |
| `nextToken` | no | "The string token will expire 30 seconds after being created." |

The operation's description adds: with `startDateTime`, `sellerSkus` and `sellerSku` are ignored; "Important: To avoid
errors, use both startDateTime and nextToken to get the next page"; SKUs need URL encoding. Paging is
`pagination.nextToken`. [official]

Response fields (`payload.inventorySummaries[]`):

| Field | Model's words |
|---|---|
| `asin`, `fnSku`, `sellerSku` | identifiers |
| `condition` | "as described by the seller (for example, New Item)" |
| `productName` | "localized language product title" |
| `lastUpdatedTime` | "The date and time that any quantity was last updated." |
| `totalQuantity` | "The total number of units in an inbound shipment or in Amazon fulfillment centers." |
| `stores` | "A list of seller-enrolled stores that apply to this seller SKU." |
| `inventoryDetails` | "will not appear if the details parameter in the request is false" |
| `…fulfillableQuantity` | "The item quantity that can be picked, packed, and shipped." With Marketplace granularity "the fulfillable quantity will reflect inventory that could be fulfilled in the given marketplace." |
| `…inboundWorkingQuantity` | units in a shipment "for which you have notified Amazon" |
| `…inboundShippedQuantity` | units "notified Amazon about and have provided a tracking number" |
| `…inboundReceivingQuantity` | units "not yet been received at an Amazon fulfillment center for processing, but are part of an inbound shipment with some units that have already been received and processed" |
| `…reservedQuantity.totalReservedQuantity` | units "currently being picked, packed, and shipped; or are sidelined for measurement, sampling, or other internal processes" |
| `…reservedQuantity.pendingCustomerOrderQuantity`, `pendingTransshipmentQuantity`, `fcProcessingQuantity` | customer orders; "being transferred from one fulfillment center to another"; "sidelined at the fulfillment center for additional processing" |
| `…researchingQuantity.totalResearchingQuantity` and `researchingQuantityBreakdown[]` | names `researchingQuantityInShortTerm` ("Short Term for 1-10 days."), `…InMidTerm` ("Mid Term for 11-20 days."), `…InLongTerm` ("Long Term for 21 days or longer.") |
| `…unfulfillableQuantity` | `totalUnfulfillableQuantity`, `customerDamagedQuantity`, `warehouseDamagedQuantity`, `distributorDamagedQuantity`, `carrierDamagedQuantity`, `defectiveQuantity`, `expiredQuantity` |

The response has no inventory age, no storage volume, no capacity limit, no days of supply and no per-fulfilment-centre
split. [official, by the model's field list]

### C. Fulfillment Inbound (v2024-03-20, v0) and FBA Inbound Eligibility v1

Role for every operation: AF (NA, EU, FE). Reach: yes. Models
`fulfillment-inbound-api-model/fulfillmentInbound_2024-03-20.json`, `fulfillmentInboundV0.json`,
`fba-inbound-eligibility-api-model/fbaInbound.json`. Base path of v2024-03-20: `/inbound/fba/2024-03-20`. [official]

Reads, v2024-03-20 (rate / burst from the model; where the rate-limits page differs it is in section J):

| Operation | What it answers | Rate / burst |
|---|---|---|
| `listInboundPlans`, `getInboundPlan` | the seller's inbound plans and one plan's state | 2 / 6 |
| `listInboundPlanItems`, `listInboundPlanBoxes`, `listInboundPlanPallets` | a plan's SKUs and quantities, boxes, pallets | 2 / 6 |
| `listPackingOptions`, `listPackingGroupItems`, `listPackingGroupBoxes` | packing options and their groups | 2 / 6; 2 / 30; 2 / 30 |
| `listPlacementOptions` | placement options with their fees and shipments | 2 / 6 |
| `getShipment`, `listShipmentItems`, `listShipmentBoxes`, `listShipmentPallets` | one shipment's destination, status and contents | 2 / 6; 2 / 30; 2 / 30; 2 / 30 |
| `listTransportationOptions`, `listDeliveryWindowOptions` | carrier quotes; delivery windows | 2 / 6; 2 / 30 |
| `listShipmentContentUpdatePreviews`, `getShipmentContentUpdatePreview` | previews of a content change | 2 / 30 |
| `listItemComplianceDetails`, `getDeliveryChallanDocument` | India-only compliance and challan | 2 / 6 |
| `listPrepDetails` | prep category and owner per SKU | model states none; rate page 2 / 30 |
| `getInboundOperationStatus` (`/operations/{operationId}`) | the result of an asynchronous write | 2 / 6 |
| `getSelfShipAppointmentSlots` | self-ship slots (MX, BR, EG, SA, AE, IN) | rate page 2 / 6 |

Writes, v2024-03-20: `createInboundPlan`, `setPackingInformation`, `generatePackingOptions`, `confirmPackingOption`,
`generatePlacementOptions`, `confirmPlacementOption`, `generateTransportationOptions`, `confirmTransportationOptions`,
`updateShipmentTrackingDetails`, `cancelInboundPlan` (2 / 2); `updateInboundPlanName`, `updateShipmentName`,
`updateShipmentSourceAddress`, `generateShipmentContentUpdatePreviews`, `confirmShipmentContentUpdatePreview`,
`generateDeliveryWindowOptions`, `confirmDeliveryWindowOptions`, `createMarketplaceItemLabels`, `setPrepDetails`
(2 / 30); `updateItemComplianceDetails` (2 / 6, India); the self-ship appointment writes. Permanent or charged, in the
model's words: `confirmPlacementOption` "Once confirmed, it cannot be changed for the Inbound Plan.";
`confirmTransportationOptions` "Once confirmed, new transportation options can not be generated or confirmed";
`cancelInboundPlan` charges apply outside the void window (24 hours small parcel, 1 hour LTL);
`confirmShipmentContentUpdatePreview` accepts the transport cost change the preview shows. [official]

v0 reads that remain (the v0 creates were removed 2025-01-21): `getShipments` `GET /fba/inbound/v0/shipments`,
`getShipmentItems` `GET /fba/inbound/v0/shipmentItems`, `getShipmentItemsByShipmentId`
`…/shipments/{shipmentId}/items`, `getPrepInstructions` `GET /fba/inbound/v0/prepInstructions`, `getLabels`
`…/shipments/{shipmentId}/labels`, `getBillOfLading` `…/shipments/{shipmentId}/billOfLading`; each 2 / 30, AF. [official]

FBA Inbound Eligibility v1: `getItemEligibilityPreview`, `GET /fba/inbound/v1/eligibility/itemPreview`, AF, 1 / 1;
previews `INBOUND` or `COMMINGLING` eligibility. [official]

### D. Fulfillment Outbound (Multi-Channel Fulfillment)

| Version | Operation | Method and path | Role | Rate / burst |
|---|---|---|---|---|
| 2020-07-01 | `getFulfillmentPreview` | `POST /fba/outbound/2020-07-01/fulfillmentOrders/preview` | AF | 2 / 30 |
| | `deliveryOffers` | `POST …/deliveryOffers` | AF | 5 / 30 |
| | `listAllFulfillmentOrders`, `getFulfillmentOrder` | `GET …/fulfillmentOrders`, `…/{sellerFulfillmentOrderId}` | AF | 2 / 30 |
| | `createFulfillmentOrder`, `updateFulfillmentOrder`, `createFulfillmentReturn` | `POST`, `PUT`, `PUT …/return` | AF | 2 / 30 |
| | `cancelFulfillmentOrder` | `PUT …/{sellerFulfillmentOrderId}/cancel` | AF; PL | 2 / 30 |
| | `getPackageTrackingDetails`, `listReturnReasonCodes` | `GET …/tracking`, `…/returnReasonCodes` | AF | 2 / 30 |
| | `getFeatures`, `getFeatureInventory`, `getFeatureSKU` | `GET …/features`, `…/features/inventory/{featureName}`, `…/{sellerSku}` | AF | 2 / 30 |
| 2026-07-04 | `getOrderPreview`, `getOffers` | `POST /fulfillment/outbound/2026-07-04/previews`, `…/offers` | AF (guide only) | 2 / 30; 5 / 30 |
| | `listOrders`, `getOrder` | `GET …/orders`, `…/orders/{orderId}` | AF (guide only) | 2 / 30 |
| | `createOrder`, `updateOrder`, `cancelOrder` | `POST …/orders`, `PUT …/{orderId}`, `PUT …/{orderId}/cancel` | AF (guide only) | 2 / 30 |

Reach: yes. The stock-bearing reads: `getFeatureInventory` returns `featureSkus[]` with `sellerSku`, `fnSku`, `asin`,
`skuCount` ("The number of SKUs available for this service.") and `overlappingSkus` ("Other seller SKUs that are shared
across the same inventory."); a preview's `isFulfillable`, `unfulfillablePreviewItems[]` and `estimatedFees` ("The fees
data will not be available for IN marketplace orders."). v2026-07-04 launched 2026-07-29 and has no feature-inventory
operation in its model. [official: both models; release notes 2026-07-29]

### E. Amazon Warehousing and Distribution v2024-05-09

Guide `amazon-warehousing-and-distribution-api` (updated 2026-09-09): "This API is available in the Amazon US store."
Role: AWD, NA only, on the operations page for 11 operations; outside the five. Model
`amazon-warehousing-and-distribution-model/awd_2024-05-09.json` has 21. [official]

| Operation | Method and path | Rate / burst | On role page |
|---|---|---|---|
| `listInventory` | `GET /awd/2024-05-09/inventory` | 2 / 2 | yes |
| `listInboundShipments`, `getInboundShipment` | `GET …/inboundShipments`, `…/{shipmentId}` | 1 / 1; 2 / 2 | yes |
| `getInbound` | `GET …/inboundOrders/{orderId}` | 2 / 2 | yes |
| `createInbound`, `updateInbound`, `cancelInbound`, `confirmInbound`, `checkInboundEligibility`, `updateInboundShipmentTransportDetails` | writes | 1 / 1 | yes |
| `getInboundShipmentLabels`, `getLabelPageTypes` | `GET …/inboundShipments/{shipmentId}/labels`, `…/labelPageTypes` | 1 / 2 | labels yes; page types no |
| `listOutbounds`, `getOutbound`, `createOutbound`, `updateOutbound`, `confirmOutbound` | `…/outboundOrders…` | 1 / 1 | no |
| `listReplenishmentOrders`, `getReplenishmentOrder`, `createReplenishmentOrder`, `confirmReplenishmentOrder` | `…/replenishmentOrders…` | model states none | no |

`listInventory` takes `sku`, `sortOrder`, `details` (`SHOW` | `HIDE`, default `HIDE`), `maxResults` (default 25, max
200) and `nextToken` ("this operation can return empty pages"). It returns per SKU `totalOnhandQuantity` ("Total
quantity that is present in AWD distribution centers."), `totalInboundQuantity` ("in-transit from the seller and has
not yet been received at an AWD Distribution Center") and, with `SHOW`, `availableDistributableQuantity` ("available for
downstream channel replenishment"), `reservedDistributableQuantity`, `replenishmentQuantity` ("in transit from AWD and
has not yet been received at FBA") and `expirationDetails[]`. [official]

### F. Listings Items, Catalog Items, Product Fees

| API | Operation | Method and path | Role | Rate / burst | Reach |
|---|---|---|---|---|---|
| Listings Items 2021-08-01 | `getListingsItem` | `GET /listings/2021-08-01/items/{sellerId}/{sku}` | IOT; PL | 5 / 10 | yes |
| | `searchListingsItems` | `GET /listings/2021-08-01/items/{sellerId}` | IOT; PL | 5 / 5 | yes |
| | `patchListingsItem` | `PATCH …/items/{sellerId}/{sku}` | IOT; PL | 5 / 5 | yes |
| | `putListingsItem`, `deleteListingsItem` | `PUT`, `DELETE` | IOT; PL | 5 / 10; 5 / 5 | yes |
| Catalog Items 2022-04-01 | `getCatalogItem`, `searchCatalogItems` | `GET /catalog/2022-04-01/items/{asin}`, `/items` | PL | 2 / 2 | yes |
| Product Fees v0 | `getMyFeesEstimateForSKU`, `…ForASIN` | `POST /products/fees/v0/listings/{SellerSKU}/feesEstimate`, `…/items/{Asin}/feesEstimate` | AF, FA, PR, PL and others | 1 / 2 | yes |
| | `getMyFeesEstimates` | `POST /products/fees/v0/feesEstimate` (up to 20 items) | PR; PL | 0.5 / 1 | yes |

- Listings: `includedData=fulfillmentAvailability` returns `fulfillmentChannelCode` and `quantity` ("The item quantity
  that you're making available for sale.", minimum 0); `summaries` carries `fnSku` and `status[]`.
  `searchListingsItems` filters by `withStatus` / `withoutStatus` (`BUYABLE`, `DISCOVERABLE`), `identifiersType` (incl.
  `FNSKU`), page size at most 20. A quantity change is a `patchListingsItem`; release notes 2025-05-28: the `merge`
  operation lets a caller "update the quantity field in fulfillmentAvailability without including optional fields like
  restock_date or lead_time_to_ship_max_days". `mode=VALIDATION_PREVIEW` validates without changing. [official]
- Catalog: `includedData=dimensions` returns, per marketplace, `item` and `package`, each with `height`, `length`,
  `width`, `weight` as `{unit, value}`. The package block is the one a size tier or a cubic-foot figure is computed
  from; the model states no size tier and no volume. [official for the fields; the use is [seat]]
- Product Fees: "The estimated fees returned by this API are not guaranteed. Actual fees can vary." (guide, updated
  2026-09-09). A request carries price, `IsAmazonFulfilled` and `OptionalFulfillmentProgram` (`FBA_CORE`, `FBA_SNL`,
  `FBA_EFN`); the reply is `TotalFeesEstimate` and a `FeeDetailList` of `FeeType` strings. The model contains the word
  "storage" nowhere: the API estimates per-sale fees, not storage, aged-inventory or removal fees. [official]

### G. Demand reads: Sales v1, Orders v2026-01-01, Replenishment v2022-11-07

| Operation | Method and path | Role | Rate / burst | Reach |
|---|---|---|---|---|
| `getOrderMetrics` | `GET /sales/v1/orderMetrics` | PL; IOT in all regions; AF, FA, PR and others "(FE only)" | 0.5 / 15 | yes (PL) |
| `searchOrders` | `GET /orders/2026-01-01/orders` | AF, FA, PR, PL, IOT, SPI and others | 0.0056 / 20 | yes |
| `getOrder` | `GET /orders/2026-01-01/orders/{orderId}` | same | 0.5 / 30 | yes |
| `listOffers`, `listOfferMetrics`, `getSellingPartnerMetrics` | `POST /replenishment/2022-11-07/offers/search`, `…/offers/metrics/search`, `…/sellingPartners/metrics/search` | BA; IOT | 1 / 1 | yes (BA) |

- `getOrderMetrics` (model `sales-api-model/sales.json`): `interval` is "two dates separated by two hyphens (first date
  is inclusive; second date is exclusive)" in absolute time; `granularity` is `Hour`, `Day`, `Week`, `Month`, `Year`,
  `Total`; "Specifying granularity=Hour results in a successful request only if the interval specified is less than or
  equal to 30 days from now. For all other granularities, the interval specified must be less or equal to 2 years from
  now."; `granularityTimeZone` is "An IANA-compatible time zone for determining the day boundary. Required when
  specifying a granularity value greater than Hour" and "must align with the offset of the specified interval value";
  `fulfillmentNetwork` is `MFN` or `AFN`; `asin` or `sku` (both together is an error); `buyerType` `B2B` | `B2C` |
  `All`; `firstDayOfWeek` `Monday` (default) | `Sunday`; `amazonProgram` `AmazonHaul`; one marketplace. Each interval
  returns `unitCount` ("The number of units in orders based on the specified filters."), `orderItemCount`,
  `orderCount`, `averageUnitPrice`, `totalSales`; the first and last interval "might contain incomplete data". [official]
- `searchOrders` (model `orders-api-model/orders_2026-01-01.json`): exactly one of `createdAfter` or `lastUpdatedAfter`;
  the `…Before` bound must be "at least two minutes before the time of the request"; `fulfilledBy` `MERCHANT` |
  `AMAZON`; `fulfillmentStatuses`; up to 50 marketplaces; at most 100 orders a page. Each order carries `orderItems[]`
  with `quantityOrdered`, `product.asin`, `product.sellerSku`, `programs` (`SUBSCRIBE_AND_SAVE`, `TRANSPARENCY`), and
  the order's `createdTime`, `fulfillment.fulfillmentStatus`, `salesChannel.marketplaceId`. Items arrive inside the
  order, so units by SKU need no second call. [official]
- Replenishment is Subscribe & Save: `listOffers` returns `inventory` ("The available inventory count for the offer."),
  `stockRisk`, `subscriptions`, `forecastDeliveries`; metrics include `NOT_DELIVERED_DUE_TO_OOS` and
  `LOST_REVENUE_DUE_TO_OOS`. Supported stores for sellers: "US, CA, ES, UK, FR, IT, IN, DE, and JP". It is not FBA
  restock. [official]

### H. Reports

Report-type pages read: `report-type-values-fba` (updated 2026-10-13), `-inventory`, `-analytics`, `-order`,
`-returns`, `-performance` (2026-10-28), `-payment` (2026-09-09), index `report-type-values` (2026-09-10). [official]

Rules that hold for the FBA page: "A near real-time FBA report is generated no more than once every 30 minutes";
"A daily FBA report is generated no more than once every four hours."; "These frequencies describe how often Amazon
generates updated report content. They do not set how many report requests you can submit. However, some FBA report
types also limit the number of requests Amazon accepts." Every FBA report is a tab-delimited flat file except the XML
all-orders pair. Every FBA report "can only be requested" except `GET_FBA_STORAGE_FEE_CHARGES_DATA` ("can be requested
or scheduled"). The page states no time zone for any report's dates and no character encoding. Index: "If an explicit
retention is not specified for a report type, then the report will be retained for 90 days." [official]

"—" below means the page states nothing on that point. Roles are the type page's own Roles line; where the types
page differs it is said in the row or in section A.

| Report type | Holds | Range and options | Freshness and request limits | Stores | Role | Reach |
|---|---|---|---|---|---|---|
| `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` | FBA quantities by SKU, "active (not archived)" | snapshot | near real-time | — | AF; PR | yes |
| `GET_FBA_MYI_ALL_INVENTORY_DATA` | same, "all (including archived)" | snapshot | near real-time | — | AF; PR | yes |
| `GET_AFN_INVENTORY_DATA` | sellable and unsellable units by condition | snapshot | near real-time | — | AF | yes |
| `GET_AFN_INVENTORY_DATA_BY_COUNTRY` | units for local fulfilment by country | snapshot | near real-time | Europe | AF; PR (types page: AF only) | yes |
| `GET_RESERVED_INVENTORY_DATA` | reserved units by reason | snapshot | near real-time | — | AF; PR | yes |
| `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT` | Amazon's restock recommendation | snapshot | near real-time | "All stores except India (IN)" | AF; PR | yes |
| `GET_FBA_INVENTORY_PLANNING_DATA` | age, sell-through, excess, storage-cost and surcharge estimates | snapshot | — | "Not available in the NL, PL, SE, or BE stores"; Brazil gets a reduced set | AF | yes |
| `GET_STRANDED_INVENTORY_UI_DATA` | stranded units and reasons | snapshot | near real-time | — | AF; PR | yes |
| `GET_STRANDED_INVENTORY_LOADER_DATA` | stranded SKUs in loader layout | snapshot | near real-time | — | AF; PR | yes |
| `GET_LEDGER_SUMMARY_VIEW_DATA` | opening and closing balance and movements | range; `aggregateByLocation` `COUNTRY` (default) \| `FC`; `aggregatedByTimePeriod` `MONTHLY` (default) \| `WEEKLY` \| `DAILY`; `FNSKU`, `MSKU`, `ASIN` | — | — | AF | yes |
| `GET_LEDGER_DETAIL_VIEW_DATA` | every movement, 18 months | range; `eventType` `Adjustments` \| `CustomerReturns` \| `Receipts` \| `Shipments` \| `VendorReturns` \| `WhseTransfers` (empty = all); `FNSKU`, `MSKU`, `ASIN` | — | — | AF | yes |
| `GET_FBA_STORAGE_FEE_CHARGES_DATA` | "estimated monthly inventory storage fees for each ASIN" | range | requested or scheduled | — | AF; PR | yes |
| `GET_FBA_FULFILLMENT_LONGTERM_STORAGE_FEE_CHARGES_DATA` | aged-inventory surcharge charged | range "should be equal to one month" | — | — | AF; PR | yes |
| `GET_FBA_OVERAGE_FEE_CHARGES_DATA` | "Estimated inventory storage overage fees for each storage type" (columns `charged_date`, `charged_fee_amount`) | — | — | — | AF | yes |
| `GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA` | fee preview for active FBA offers | `dataStartTime` at least 72 hours before now, `dataEndTime` now | "updated at least once every 72 hours"; "can only be requested once per day per seller" | columns vary by store | AF; PR | yes |
| `GET_FBA_REIMBURSEMENTS_DATA` | reimbursements | range | daily | — | AF; PR | yes |
| `GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA` | removal orders | range | near real-time | — | AF; PR | yes |
| `GET_FBA_FULFILLMENT_REMOVAL_SHIPMENT_DETAIL_DATA` | removal shipments; "will not include canceled returns or disposed items" | range | near real-time | — | AF; PR | yes |
| `GET_FBA_RECOMMENDED_REMOVAL_DATA` | units due for the next long-term-storage clean-up | snapshot | daily | — | AF; PR | yes |
| `GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA` | inbound problems and their fees | range | daily | — | AF; PR | yes |
| `GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA` | customer returns | range | daily | — | AF; PR | yes |
| `GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_REPLACEMENT_DATA` | replacements | range | daily | NA and IN | AF | yes |
| `GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_SALES_DATA` | shipped units by fulfilment centre | range | "updated in near real-time in Europe (EU), Japan, and North America (NA)"; 1–3 hours' delay, rarely 24; the page states no freshness for other regions and no store restriction | — | AF | yes |
| `GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL` | shipment lines with buyer address (restricted data) | up to one month | near real-time; "a maximum of 12 requests for this report every 8 hours, per selling partner account", Seller Central requests included; near real-time is stated for EU, JP, NA only | — | AF; IOT; PR (types page: AF only) | yes |
| `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL`, `…_BY_LAST_UPDATE_GENERAL` (and XML twins) | order lines "regardless of fulfillment channel or shipment status" | range; the order page says "The date range for these reports is limited to 30 days." | exempt from the 30-minute rule; not schedulable | — | AF, DTC, IOT, PR (last-update flat also PL; the order page omits PR for it) | yes |
| `GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_PROMOTION_DATA` | promotions on shipped units | range | daily | NA | AF; PR | yes |
| `GET_REMOTE_FULFILLMENT_ELIGIBILITY` | remote-fulfilment eligibility by SKU | snapshot | "can take up to 24 hours to generate" | — | AF; IOT | yes |
| `GET_MERCHANT_LISTINGS_ALL_DATA` | every listing with quantity and channel | snapshot; `custom`, `preferredReportDocumentLocale` | cached "between one and six hours depending on the number of entries"; one store per report | — | DTC, IOT, PR, PL | yes |
| `GET_MERCHANT_LISTINGS_DATA`, `_INACTIVE_DATA`, `_DATA_LITE`, `_DATA_LITER`, `GET_FLAT_FILE_OPEN_LISTINGS_DATA`, `GET_MERCHANT_CANCELLED_LISTINGS_DATA` | active, inactive, short and cancelled listing lists | snapshot | — | — | PR, PL among others | yes |
| `GET_MERCHANTS_LISTINGS_FYP_REPORT` | suppressed listings | snapshot | requested or scheduled | — | PL | yes |
| `GET_PAN_EU_OFFER_STATUS` | Pan-EU enrolment by SKU | snapshot | — | ES, UK, FR, DE, IT | AF, DTC, IOT, PR, PL | yes |
| `GET_REFERRAL_FEE_PREVIEW_REPORT` | referral fee preview | — | up to 24 hours old; once per 24 hours | — | FA | yes |
| `GET_SALES_AND_TRAFFIC_REPORT` | units ordered, shipped, refunded; sessions (JSON) | start at most two years back; `dateGranularity` `DAY` \| `WEEK` \| `MONTH`; `asinGranularity` `PARENT` \| `CHILD` \| `SKU` | "up to three times every five minutes"; requested or scheduled | — | BA | yes |
| `GET_OUT_OF_STOCK_MFN_INFORMATION` | seller-fulfilled out-of-stock | — | — | — | IOT | no |
| `GET_FLAT_FILE_PENDING_ORDERS_DATA`, `GET_PENDING_ORDERS_DATA` | pending seller-fulfilled orders | "38-day lookback" | flat: requested or scheduled; XML: scheduled | "only available in the Amazon Japan store" | IOT (the XML one has no Roles line on the order page; types page IOT) | no |
| `GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE` | seller-fulfilled returns | range; "up to 60 days of data in a single report" | requested or scheduled | — | DTC; IOT | no |
| `GET_V2_SELLER_PERFORMANCE_REPORT` | account health | — | — | — | SPI | no |

Removed, with dates from the deprecation schedule (updated 2026-09-09): `GET_FBA_SNS_FORECAST_DATA`,
`GET_FBA_SNS_PERFORMANCE_DATA` 2025-12-11; `GET_FBA_UNO_INVENTORY_DATA` 2024-03-27;
`GET_FBA_FULFILLMENT_CURRENT_INVENTORY_DATA`, `…_INVENTORY_ADJUSTMENTS_DATA`, `…_INVENTORY_RECEIPTS_DATA`,
`…_INVENTORY_SUMMARY_DATA`, `…_MONTHLY_INVENTORY_DATA`, `GET_FBA_RECONCILIATION_REPORT_DATA` 2023-01-31 (the ledger
pair replaces them); `GET_EXCESS_INVENTORY_DATA`, `GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA`,
`GET_FBA_INVENTORY_AGED_DATA` 2022-06-27 (the planning report replaces them). [official]

Ledger date rules (FBA page): `MONTHLY` "dataStartTime must be set to first of the month and dataEndTime must be set
to last day of the month"; `WEEKLY` the start and end of a week (example Monday 2023-01-09 to Sunday 2023-01-15);
`DAILY` example `2023-01-15T00:00:00+00:00` to `23:59:59`; the summary "can return empty data if invalid
dataStartTime/dataEndTime is passed". Detail: "You can view all historical movements of your inventory for 18 months in
this report." [official]

Reports FAQ (updated 2026-09-09): "You can request some reports (for example, FBA reports) only once within a
specified time period. Any subsequent requests … are cancelled"; "Deprecated columns are retained to maintain the
original column order"; "Seller Central provides additional reports that you can't access using the Reports API".
Reports guide: "Amazon periodically adds new fields and field values to reports". [official]

#### Column lists, as the page prints them (read 2026-11-10)

- `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` and `GET_FBA_MYI_ALL_INVENTORY_DATA` (same 24): sku, fnsku, asin,
  product-name, condition, your-price, mfn-listing-exists, mfn-fulfillable-quantity, afn-listing-exists,
  afn-warehouse-quantity, afn-fulfillable-quantity, afn-unsellable-quantity, afn-reserved-quantity,
  afn-total-quantity, per-unit-volume, afn-inbound-working-quantity, afn-inbound-shipped-quantity,
  afn-inbound-receiving-quantity, afn-researching-quantity, afn-reserved-future-supply, afn-future-supply-buyable,
  afn-fc-transfer-quantity, afn-onhand-buyable-quantity, store.
- `GET_AFN_INVENTORY_DATA`: seller-sku, fulfillment-channel-sku, asin, condition-type, Warehouse-Condition-code,
  Quantity Available.
- `GET_AFN_INVENTORY_DATA_BY_COUNTRY`: seller-sku, fulfillment-channel-sku, asin, condition-type, country,
  quantity-for-local-fulfillment.
- `GET_RESERVED_INVENTORY_DATA`: sku, fnsku, asin, product-name, reserved_qty, reserved_customerorders,
  reserved_fc-processing, reserved_staging (US, CA, JP, UK, DE, FR, IT, ES stores), program.
- `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`: Country, Product Name, FNSKU, Merchant SKU, ASIN, Condition,
  Supplier, Supplier part no., Currency code, Price, Sales last 30 days, Units Sold Last 30 Days, Total Units, Inbound,
  Available, FC transfer, FC Processing, Customer Order, Unfulfillable, Working, Shipped, Receiving, Fulfilled by,
  Total Days of Supply (including units from open shipments), Days of Supply at Amazon Fulfillment Network, Alert,
  Recommended replenishment qty, Recommended ship date, Recommended action (US store), Unit storage size (US, CA, UK,
  DE, FR, IT, ES stores).
- `GET_FBA_INVENTORY_PLANNING_DATA`: snapshot-date, sku, fnsku, asin, product-name, condition, available, fc-transfer,
  pending-removal-quantity, inv-age-0-to-90-days, inv-age-91-to-180-days, inv-age-181-to-270-days,
  inv-age-271-to-365-days, currency, units-shipped-t7, units-shipped-t30, units-shipped-t60, units-shipped-t90, alert,
  your-price, sales-price, lowest-price-new-plus-shipping, lowest-price-used, recommended-action, DEPRECATED
  healthy-inventory-level, recommended-sales-price, recommended-sale-duration-days, recommended-removal-quantity,
  estimated-cost-savings-of-recommended-actions, sell-through, item-volume, volume-unit-measurement, storage-type,
  storage-volume, marketplace, product-group, sales-rank, days-of-supply, estimated-excess-quantity,
  weeks-of-cover-t30, weeks-of-cover-t90, featuredoffer-price, sales-shipped-last-7-days, sales-shipped-last-30-days,
  sales-shipped-last-60-days, sales-shipped-last-90-days, inv-age-0-to-30-days, inv-age-31-to-60-days,
  inv-age-61-to-90-days, inv-age-181-to-330-days, inv-age-331-to-365-days, inv-age-365-plus-days (not US, DE, UK, FR,
  IT, ES), estimated-storage-cost-next-month, inbound-quantity, inbound-working, inbound-shipped, inbound-received,
  no-sale-last-6-months, Total Reserved Quantity, unfulfillable-quantity, then a quantity-to-be-charged-ais and an
  estimated-ais column for each of 181-210, 211-240, 241-270, 271-300, 301-330, 331-365 days, and for 365-plus days
  (not US, DE, UK, FR, IT, ES), historical-days-of-supply, fba-minimum-inventory-level,
  fba-inventory-level-health-status, Recommended ship-in quantity, Recommended ship-in date, Last updated date for
  Historical Days of Supply, Exempted from Low-Inventory-Level fee?, Low-Inventory-Level fee applied in current week?,
  Short term historical days of supply, Long term historical days of supply, Inventory age snapshot date, Inventory
  Supply at FBA, Reserved FC Processing, Reserved Customer Order, Reserved Staging, Total Days of Supply (including
  units from open shipments), supplier, is-seasonal-in-next-3-months, season-name, season-start-date, season-end-date,
  Fulfillment Service and Programs. US, DE, UK, FR, IT, ES only: inv-age-366-to-455-days, inv-age-456-plus-days,
  quantity-to-be-charged-ais-366-455-days, estimated-ais-366-455-days, quantity-to-be-charged-ais-456-plus-days,
  estimated-ais-456-plus-days. Brazil only: qty-to-be-charged-ltsf-6-mo, projected-ltsf-6-mo,
  qty-to-be-charged-ltsf-12-mo, estimated-ltsf-next-charge, weeks-of-cover, weeks-of-cover-estimated-excess-quantity,
  recommended-order-quantity, recommended-order-date. "Attributes vary by store."
- `GET_STRANDED_INVENTORY_UI_DATA`: primary-action, date-stranded, Date-to-take-auto-removal, status-primary,
  status-secondary, error-message, stranded-reason, asin, sku, fnsku, product-name, condition, fulfilled-by,
  fulfillable-qty, your-price, unfulfillable-qty, reserved-quantity, inbound-shipped-qty.
- `GET_LEDGER_SUMMARY_VIEW_DATA`: Date, FNSKU, ASIN, MSKU, Title, Disposition, Starting Warehouse Balance, In Transit
  Between Warehouses, Receipts, Customer Shipments, Customer Returns, Vendor Returns, Warehouse Transfer In/Out, Found,
  Lost, Damaged, Disposed, Other Events, Ending Warehouse Balance, Unknown Events, Location, Store.
- `GET_LEDGER_DETAIL_VIEW_DATA`: Date, FNSKU, ASIN, MSKU, Title, Event Type, Reference ID, Quantity, Fulfillment
  Center, Disposition, Reason, Country, Reconciled Quantity, Unreconciled Quantity, Date and Time, Store.
- `GET_FBA_STORAGE_FEE_CHARGES_DATA`: asin, fnsku, product_name, fulfillment_center, country_code, longest_side,
  median_side, shortest_side, measurement_units, weight, weight_units, item_volume, volume_units, product_size_tier,
  average_quantity_on_hand, average_quantity_pending_removal, estimated_total_item_volume, month_of_charge,
  storage_rate, storage_utilization_ratio, storage_utilization_ratio_units, base_rate, utilization_surcharge_rate,
  avg_qty_for_sus, est_vol_for_sus, est_base_msf, est_sus, currency, estimated_monthly_storage_fee,
  dangerous_goods_storage_type, eligible_for_inventory_discount, qualifies_for_inventory_discount,
  total_incentive_fee_amount, breakdown_incentive_fee_amount, average_quantity_customer_orders.
- `GET_FBA_FULFILLMENT_LONGTERM_STORAGE_FEE_CHARGES_DATA`: snapshot-date, sku, fnsku, asin, product-name, condition,
  per-unit-volume, currency, volume-unit, country, qty-charged, amount-charged, surcharge-age-tier, rate-surcharge.
- `GET_FBA_OVERAGE_FEE_CHARGES_DATA`: charged_date, country_code, storage_type, charge_rate, storage_usage_volume,
  storage_limit_volume, overage_volume, volume_unit, charged_fee_amount, currency_code.
- `GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA`, all stores: sku, fnsku, asin, amazon-store, product-name, product-group,
  brand, fulfilled-by, your-price, sales-price, longest-side, median-side, shortest-side, length-and-girth,
  unit-of-dimension, item-package-weight, unit-of-weight, currency, estimated-fee-total,
  estimated-referral-fee-per-unit. US only: product-size-tier, estimated-future-order-handling-fee-per-order,
  expected-future-fulfillment-fee-per-unit. US and UK: estimated-order-handling-fee-per-order. US and CA:
  estimated-variable-closing-fee, expected-fulfillment-fee-per-unit. US and MX: estimated-future-fee,
  estimated-future-pick-pack-fee-per-unit, estimated-future-weight-handling-fee-per-unit. MX:
  estimated-pick-pack-fee-per-unit, estimated-weight-handling-fee-per-unit. BR, IN, TR, SA, AE, EG, SG:
  estimated-fixed-closing-fee. EU: has-local-inventory, product-size-weight-band,
  expected-domestic-fulfilment-fee-per-unit, expected-efn-fulfilment-fee-per-unit-uk, -de, -fr, -it, -es, -se. It
  holds no storage fee.
- `GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA`: request-date, order-id, order-source, order-type, service-speed,
  order-status, last-updated-date, sku, fnsku, disposition, requested-quantity, cancelled-quantity, disposed-quantity,
  shipped-quantity, in-process-quantity, removal-fee, currency, service-speed (EU stores; the page lists it twice).
- `GET_FBA_FULFILLMENT_REMOVAL_SHIPMENT_DETAIL_DATA`: request-date, order-id, shipment-date, sku, fnsku, disposition,
  shipped-quantity, carrier, tracking-number, shipment-status (IN store only), removal-order-type.
- `GET_FBA_RECOMMENDED_REMOVAL_DATA`: snapshot-date, sku, fnsku, asin, product-name, condition, sellable-quantity,
  sellable-121-180-days (US, JP, EU), sellable-181-270-days (US, JP, EU), sellable-271-365-days, sellable-365+-days,
  sellable-removal-quantity, unsellable-quantity, unsellable-0-7-days, unsellable-8-60-days, unsellable-61-90-days.
- `GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA`: issue-reported-date, shipment-creation-date, fba-shipment-id,
  fba-carton-id, fulfillment-center-id, sku, fnsku, asin, product-name, problem-type, problem-quantity,
  expected-quantity, received-quantity, performance-measurement-unit, coaching-level, fee-type, currency, fee-total,
  problem-level, alert-status.
- `GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA`: return-date, order-id, sku, asin, fnsku, product-name, quantity,
  fulfillment-center-id, detailed-disposition, reason, status, license-plate-number, customer-comments.
- `GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_SALES_DATA`: shipment-date, sku, fnsku, asin, fulfillment-center-id,
  quantity, amazon-order-id, currency, item-price-per-unit, shipping-price, gift-wrap-price, ship-city, ship-state,
  ship-postal-code, points-granted (JP store only).
- `GET_MERCHANT_LISTINGS_ALL_DATA` (29): item-name, item-description, listing-id, seller-sku, price, quantity,
  open-date, image-url, item-is-marketplace, product-id-type, zshop-shipping-fee, item-note, item-condition,
  zshop-category1, zshop-browse-path, zshop-storefront-feature, asin1, asin2, asin3, will-ship-internationally,
  expedited-shipping, zshop-boldface, product-id, bid-for-featured-placement, add-delete, pending-quantity,
  fulfillment-channel, merchant-shipping-group, status. "This report includes a UTF-8 Byte Order Mark (BOM) as the
  first 3 bytes." Its header language follows `preferredReportDocumentLocale`, and "Requesting the same report within
  the cache period … may return headers in a different locale than requested."

Every one of the 21 has a column list on Amazon's developer page; none needed a help page or a third party.

### I. Data Kiosk

Schemas in `schemas/data-kiosk/`. Operations (`createQuery`, `getQuery`, `getQueries`, `cancelQuery`, `getDocument`):
see the door for paths and rates. Every field in the three datasets carries `@resultRetention(duration: "P30D")`. [official]

- **`analytics_economics_2024_03_15`**. Query `economics(startDate, endDate, aggregateBy, marketplaceIds,
  includeComponentsForFeeTypes)`: start "no more than two years ago"; date granularity `DAY` | `WEEK` | `MONTH` |
  `RANGE`; product granularity `CHILD_ASIN` | `MSKU` | `PARENT_ASIN` (`FNSKU` removed 2025-12-22, though field
  comments still mention it). A row has `sales` (`unitsOrdered`, `unitsRefunded`, `netUnitsSold`), `fees[]` as
  `FeeSummary{feeTypeName, charges[]}` where `feeTypeName` is a free string ("FBA fulfillment fees") and each charge
  splits at fee-change dates with `aggregatedDetail{amount, amountPerUnit, quantity, totalAmount, …}`, `ads`, and
  seller-entered costs (`shippingToAmazonCost`, `storageCost`, `costOfGoodsSold`). `includeComponentsForFeeTypes`
  takes `FeeType`: `FBA_FULFILLMENT_FEE` or `FBA_STORAGE_FEE` ("Fulfillment by Amazon (FBA) Monthly Inventory Storage
  Fee, including base rate and surcharges."). Release notes 2026-09-30: "Updated the Analytics Economics dataset with
  deal, coupon, removal, disposal, and fuel fees"; the schema at `db2936aa` has no enum value for removal, disposal or
  liquidation, so those arrive, if at all, as `feeTypeName` strings.
- Query `economicsPreview(startDate, endDate, aggregateBy, feeTypes, marketplaceIds)`: start today or later, end at
  most 120 days after today; `MSKU` and `RANGE` only. `PreviewFeeType` holds `AGED_INVENTORY_SURCHARGE` ("previously
  known as the Long-term Storage Fee"), `BASE_MONTHLY_STORAGE_FEE`, `MONTHLY_INVENTORY_STORAGE_FEES` ("including base
  rate and surcharges"), `STORAGE_UTILIZATION_SURCHARGE`, `LOW_INVENTORY_LEVEL_FEE`,
  `FBA_INBOUND_PLACEMENT_SERVICE_FEE`, `BASE_FBA_FULFILLMENT_FEE`, `FBA_FULFILLMENT_FEES`, `PAN_EU_OVERSIZE_FEE`,
  `HIGH_RETURN_RATE_FEE`, `RETURN_PROCESSING_FEE`, `REFERRAL_FEES`, `CLOSING_FEES`, `PER_ITEM_SELLING_FEES`,
  `SPONSORED_PRODUCTS_CHARGES`, `DIGITAL_SERVICES_FEE_FBA`, `DIGITAL_SERVICES_FEE_SOA`. No removal, disposal or
  liquidation value.
- Query `economicsSimulation(actionTypes: AWD | SIPP, …)`: up to 100 products, end at most 90 days after today; its
  defaults are Amazon's (12 weeks of weekly sales sent to AWD, 1 week lead time, 20 units a carton).
- **`analytics_salesAndTraffic_2024_04_24`**. `salesAndTrafficByDate` and `salesAndTrafficByAsin` (`PARENT` | `CHILD` |
  `SKU`): `unitsOrdered` ("The number of units ordered."), `unitsShipped`, `unitsRefunded`, `sessions`,
  `buyBoxPercentage`; start "no more than two years ago"; `WEEK` snaps to Sunday–Saturday. `salesAndTrafficTrends`
  added 2025-08-27.
- **`analytics_sellerAnalytics_2025_03_31`** (added 2026-09-30). One stock field: `totalFbaInventoryValue`, "Total
  worth of seller's inventory stored in FBA warehouses based on 15-day average selling price." It is an account-level
  value with benchmarking, not a per-SKU quantity. Its guide (updated 2026-09-30) gates fields by "Sales and traffic
  access" or "Sales and lending access" and names no role for either; it lists `totalFbaInventoryValue` under the
  `lending` metric group, which "Sales and lending access" grants.
- **The role.** Two Amazon pages, quoted as read 2026-11-10. (1) *Data Kiosk API* guide (updated 2026-10-20),
  section "Roles for the Data Kiosk API v2023-11-15": "Each field available with Data Kiosk requires a certain role.
  Data Kiosk determines whether the requester has the required roles for each field in the query upon query
  creation."; its table for each of the five operations reads "Required roles (need at least one) | Brand Analytics".
  *Role Mappings for SP-API Operations* (updated 2026-10-28) gives the same single role for the five. Neither names a
  role per dataset. (2) Changelog *Correction: Data Kiosk role requirements*
  (`…/sp-api/changelog/correction-data-kiosk-role-requirements`; the rendered page shows no date, its page source
  carries `createdAt` 2024-07-02): "The initial version of that announcement stated that all datasets require the
  Brand Analytics role. This is not correct. The Vendor Analytics and Sales and Traffic datasets require the Brand
  Analytics role. The Economics dataset requires the Selling Partner Insights role." The launch announcement it
  corrects (*Data Kiosk reporting suite launches to general availability*, 2024-06-19) now carries the same note.
  The economics and sales-and-traffic schemas carry no role directive. The pages do not strictly contradict: the
  operation tables are newer and say which role opens the operation; the correction is older and says which role a
  dataset's fields need. Read together, Economics is not reached by the five. The door's reference states the
  correction's reading. [official, both]

### J. Feeds and notifications

Feeds (`fulfillment-by-amazon-feed-type-values`, updated 2026-10-14; `listings-feed-type-values`, 2026-09-09;
`feed-type-values`, 2026-11-05). `createFeed` is 0.0083 / 15; `createFeedDocument` 0.5 / 15; `getFeed` 2 / 15. [official]

| Feed type | Does | Role | Status |
|---|---|---|---|
| `POST_FLAT_FILE_FBA_CREATE_REMOVAL` | "Creates a bulk removal order." | AF | live; static sandbox scenarios added 2026-09-30 |
| `POST_FBA_INBOUND_CARTON_CONTENTS`, `POST_FLAT_FILE_FROM_EXCEL_FBA_CREATE_CARTON_INFO` | carton contents of an inbound shipment | AF | on the FBA page / the types page |
| `POST_FULFILLMENT_ORDER_REQUEST_DATA`, `POST_FLAT_FILE_FULFILLMENT_ORDER_REQUEST_DATA` and the two cancellation twins | Multi-Channel Fulfillment orders | AF | live |
| `JSON_LISTINGS_FEED` | listing changes in the Listings Items format, quantity included | PL (type page); IOT, PL (types page) | live; `DONE` only after all processing (2026-02-23) |
| `POST_FLAT_FILE_INVLOADER_DATA`, `POST_INVENTORY_AVAILABILITY_DATA`, `POST_FLAT_FILE_PRICEANDQUANTITYONLY_UPDATE_DATA` | legacy quantity feeds | — | removed; the listings page says 2025-07-31, the schedule 2025-12-03 |

There is no feed and no operation that creates a removal order except the flat-file feed, and none that reads one
except the two removal reports. [official, by absence from the models and pages read]

Notifications (`notification-type-values`, updated 2026-10-28; schemas in `schemas/notifications/`). Each type's
workflow is Amazon SQS or Amazon EventBridge; the Notifications guide offers no other destination, so a box without an
AWS queue polls. Subscription operations are 1 / 5. [official]

| Type | Sent when | Payload fields that matter | Role | Reach |
|---|---|---|---|---|
| `FBA_INVENTORY_AVAILABILITY_CHANGES` (SQS) | "whenever there is a change in the Fulfillment By Amazon (FBA) inventory quantities"; "a snapshot of the FBA inventory in all eligible Amazon stores in a particular region" | `SKU`, `FNSKU`, `ASIN`, per marketplace `Fulfillable`, `Unfulfillable`, `Researching`, `InboundQuantityBreakdown{Working, Shipped, Receiving}`, `ReservedQuantityBreakdown{WarehouseProcessing, WarehouseTransfer, PendingCustomerOrder}`, `FutureSupplyBuyable`, `PendingCustomerOrderInTransit`, `Stores` | AF | yes |
| `FBA_OUTBOUND_SHIPMENT_STATUS` (SQS) | Amazon creates or cancels an FBA shipment; "only for FBA Onsite shipments … only in the Amazon Brazil store" | `AmazonOrderId`, `AmazonShipmentId`, `ShipmentStatus` | AF | yes |
| `FULFILLMENT_ORDER_STATUS` (SQS) | a Multi-Channel Fulfillment order, shipment or package changes status; payload version 2026-07-04 | order and package status | AF | yes |
| `ITEM_INVENTORY_EVENT_CHANGE` (SQS) | "five minutes after the beginning of each hour", previous hour plus data delayed up to 24 hours | `asin`, `marketplaceId`, `startTime`, `endTime` (UTC), `highlyAvailableInventory` | BA | yes |
| `ITEM_SALES_EVENT_CHANGE` (SQS) | hourly sales by ASIN | `orderedUnits` ("can be negative if there are more cancellations than orders"), `orderedRevenue`, UTC range | BA | yes |
| `LISTINGS_ITEM_STATUS_CHANGE` (EventBridge) | a listing "is created, deleted, or its buyability changes" | `Sku`, `Asin`, `MarketplaceId`, `Status[]` | PL | yes |
| `LISTINGS_ITEM_MFN_QUANTITY_CHANGE` | the seller-fulfilled available quantity changes | `Sku`, `FulfillmentChannelCode`, `Quantity` | PL | yes |
| `REPORT_PROCESSING_FINISHED` (SQS) | a requested report reaches `DONE`, `CANCELLED` or `FATAL` | `reportId`, `reportType`, `processingStatus`, `reportDocumentId` | AF, BA, PR, PL, IOT and three restricted roles | yes |
| `DATA_KIOSK_QUERY_PROCESSING_FINISHED` | a query ends | query and document ids | AWD; BA | yes (BA) |

The inventory notification's payload has two fields the API and the MYI report name differently or not at all:
`FutureSupplyBuyable` and `PendingCustomerOrderInTransit` (In-Stock Head Start). [official]

### K. Limits and lags in one place

- **Rates.** `createReport` and `createQuery` 0.0167 / 15 (one a minute once the burst is spent); `getReportDocument`
  and `getDocument` 0.0167 / 15; `getReports` 0.0222 / 10; `getReport` 2 / 15; `searchOrders` 0.0056 / 20 (one every
  three minutes); `getOrderMetrics` 0.5 / 15; `getInventorySummaries` 2 / 2; AWD `listInventory` 2 / 2; Product Fees
  1 / 2 and 0.5 / 1. The live rate is the `x-amzn-RateLimit-Limit` header where Amazon sends it. [official: models]
- **Model against page.** Release notes 2025-06-25 and *Fulfillment Inbound API rate limits* (updated 2026-09-09) give
  5 a second for `getShipment` (burst 6), `listShipmentBoxes` (30), `listDeliveryWindowOptions` (30),
  `listTransportationOptions` (6), `getInboundOperationStatus` (6) and v0 `getLabels` (30); the model at `db2936aa`
  still says 2 for each. [official, both]
- **History.** `getInventorySummaries` `startDateTime` 18 months; ledger detail 18 months; `getOrderMetrics` two years
  (30 days at `Hour`); Sales and Traffic report and both Data Kiosk datasets two years; `economicsPreview` 120 days
  ahead. Reports are kept 90 days unless a type says otherwise; Data Kiosk results 30 days.
- **Missing stores.** AWD: US only. Restock report: not India. Planning report: not NL, PL, SE, BE; Brazil reduced.
  `GET_AFN_INVENTORY_DATA_BY_COUNTRY`: Europe. Replacements report: NA and India. Promotions report: NA. Pending
  order reports: Japan. Customer shipment sales and fulfilled shipments: near real-time is stated for EU, JP and NA
  only. Replenishment for sellers: nine stores. `FBA_OUTBOUND_SHIPMENT_STATUS`: Brazil.
- **Time zones.** `getOrderMetrics`: the caller sets the day boundary with `granularityTimeZone`. Economics:
  granularity is "against marketplace local time", week and month snapping is described in UTC+0. Hourly inventory and
  sales notifications: UTC. FBA reports: Amazon's pages state none.
- **Page disagreements**, beyond those in A, I and above: the FBA page's introduction names a Subscribe and Save
  category that has no section; `GET_STRANDED_INVENTORY_LOADER_DATA` still tells the reader to submit through
  `POST_FLAT_FILE_INVLOADER_DATA`, a removed feed; the 2023 Sales and Traffic dataset's removal is 2026-02-26 in the
  release notes and 2026-03-27 on the schedule.
- **Release notes that touch stock** (`sp-api-release-notes`, updated 2026-11-04). 2025-01-29 AWD
  `replenishmentQuantity`. 2025-02-26 AWD inbound operations. 2025-05-28 Sales `amazonProgram`; Listings `merge`.
  2025-06-25 inbound rates. 2025-08-27 Product Fees `itemPrice` removed from the preview context; the
  listing-status and seller-fulfilled inventory guide. 2025-10-01 External Fulfillment APIs. 2025-12-03 inbound
  delivery windows gain `DISCOUNTED` and `BLOCKED` and become one Sunday–Saturday week ("You will not be able to select
  delivery windows with BLOCKED status after February 28, 2026"). 2025-12-22 Economics `FNSKU` granularity removed.
  2026-04-01 Inbound Eligibility `FBA_INB_0465`; Replenishment inventory and delivery-health filters. 2026-05-27
  notification `filterExpression`. 2026-07-29 Fulfillment Outbound v2026-07-04; inbound `discounts` on
  `listDeliveryWindowOptions`. 2026-09-30 Seller Analytics dataset; Economics fee additions; removal-feed sandbox.
  2026-10-28 Action Items and Action Plans APIs (role SPI).
- **2027.** The schedule removes Orders v0 reads on 2027-03-27 and Finances v0 `listFinancialEvents*` on 2027-08-27.
  No stock API, report, feed or notification has a 2027 date. The Data Kiosk guide says "Reports within the Reports API
  will be deprecated after they are onboarded to Data Kiosk", with no date for any FBA report. [official]

## What practitioners add

All four are developers writing on Amazon's own models repository; read 2026-11-10 through GitHub's issue API. [opinion]

- **P1.** LukaszWypych, issue #4955, 2025-09-08, open: a `GET_MERCHANT_LISTINGS_ALL_DATA` requested through the API
  arrived "encoded with cp-1252 with already replaced characters with "?"", while the same report started in Seller
  Central was correct.
- **P2.** jlefortseb, issue #4762, 2025-04-29, closed: from 2025-04-23 report document URLs carried
  `response-content-encoding=identity`, which broke a Java client ("Unsupported encoding: identity").
- **P3.** asd6979448, issue #5339, 2026-07-31, closed: a `GET_LEDGER_DETAIL_VIEW_DATA` request for Germany showed in
  Seller Central one hour off the range sent. Amazon's Jawher (Selling Partner Developer Services) answered that
  "Germany follows Daylight Saving Time … in May the timezone is CEST which is 2 hours ahead of UTC" — the nearest thing
  to an Amazon statement that the ledger's days are store-local days. [official, via GitHub issue reply]
- **P4.** mystery4f, issue #5209, 2026-04-28, open with two comments: whether analytics reports read
  `dataStartTime` as UTC or store-local time; no Amazon answer in the issue. The second comment (spiohq, 2026-05-08)
  cites an earlier issue in which, by that commenter's quotation, an Amazon solutions architect said of Vendor Retail
  Analytics reports "we don't use the timestamp beyond the day. The rest (hour:min:second) is ignored".
  [official, via spiohq; vendor reports only]

#### What ERPs say of these reads (gap fill 2026-11-10)

From the survey's `03-tools-cn.md` and `03-tools-en.md`, read 2026-11-09 by the survey seat and re-read as files by
the verifier; the vendors' pages were not re-fetched. [opinion, via the survey]

- **P5.** 赛狐 SellFox help (`sellfox.com/help/features.html?id=359`): FBA inventory "数据来源：取自亚马逊接口" (taken
  from Amazon's interface), "除库龄外30分钟更新一次" (refreshed every 30 minutes except age). The cadence equals
  Amazon's 30-minute generation rule for near real-time FBA reports (H); SellFox syncs AWD at 00:00 and 12:00.
- **P6.** 积加 Gerpgo help, by the survey: it reads "管理亚马逊物流库存报告：存档" (Manage FBA Inventory, Archived:
  `GET_FBA_MYI_ALL_INVENTORY_DATA`), the reserved inventory report, the inventory age report and the multi-country
  inventory report; inventory refreshes hourly, age every six hours.
- **P7.** The survey's summary across the Chinese ERPs: they name Amazon reports, not operations, as their stock
  source ("They rarely name SP-API, saying only 亚马逊接口 or API"), refresh inventory every 15 minutes to an hour
  and age three to four times a day. None of the tools' pages the survey read reports a lag, a throttle or an
  encoding fault of a named endpoint; the English tool pages say nothing of endpoints at all.

## Published research

None bears on an API surface; none was sought.

## Stable enough for a skill

- The role beside each read, and which reads the five roles reach (sections B–J; the role pages' dates in A).
- `getInventorySummaries`' field definitions, its 18-month and 30-second limits, and what it lacks (B).
- The report table's enums, options and the column lists (H), stated as "as printed 2026-11-10; Amazon adds columns".
- The Product Fees API estimates no storage (F); the fee preview report holds none (H).
- The removal order is written only by a feed and read only by two reports (J).
- Every notification destination is AWS (J).
- AWD is US-only and needs a role outside the five (E).

## What cx must read at run time

- **R1. On-hand by SKU.** `getInventorySummaries` with `details=true`. Role AF or PL. 2 / 2. A page token dies in 30
  seconds; inbound quantity changes do not count as a change for `startDateTime`.
- **R2. On-hand with listing context.** `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA`. Role AF or PR. Near real-time, so
  at most a new document each 30 minutes. Columns `afn-fulfillable-quantity`, `afn-reserved-quantity`,
  `afn-inbound-*`, `afn-researching-quantity`, `afn-unsellable-quantity`, `store`.
- **R3. Age, excess and Amazon's surcharge estimates.** `GET_FBA_INVENTORY_PLANNING_DATA`. Role AF only. No freshness
  stated; columns differ by store; absent in NL, PL, SE, BE.
- **R4. Amazon's restock view.** `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`. Role AF or PR. Not India.
- **R5. Movements and reconciliation.** The ledger pair. Role AF only. Monthly ranges must be whole months; a wrong
  range can return an empty document rather than an error.
- **R6. Storage cost charged.** `GET_FBA_STORAGE_FEE_CHARGES_DATA`, `GET_FBA_FULFILLMENT_LONGTERM_STORAGE_FEE_CHARGES_DATA`
  (one-month range), `GET_FBA_OVERAGE_FEE_CHARGES_DATA` (AF only). Role AF or PR for the first two.
- **R7. Demand.** `getOrderMetrics` (PL; units ordered, caller's time zone, `fulfillmentNetwork=AFN`),
  `GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_SALES_DATA` (AF; units shipped, by fulfilment centre),
  `GET_SALES_AND_TRAFFIC_REPORT` or the Sales and Traffic dataset (BA), `searchOrders` (AF, PR, PL, FA; 0.0056 / s).
- **R8. Removals.** The two removal reports (AF or PR) and `GET_FBA_RECOMMENDED_REMOVAL_DATA`.
- **R9. Inbound.** `listInboundPlans`, `getShipment`, `listShipmentItems`, v0 `getShipments` and `getShipmentItems`
  (AF); `GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA` (AF or PR).
- **R10. Dimensions.** `getCatalogItem` with `includedData=dimensions` (PL); the storage-fee report's own
  `item_volume` and `product_size_tier` are Amazon's measured values.
- **R11. The applied rate.** `x-amzn-RateLimit-Limit` in a receipt's headers (the door states when Amazon sends it).

## Reads that need a role outside the five

- **AWD role:** all of section E — AWD on-hand, inbound to AWD, replenishment to FBA. US only.
- **Selling Partner Insights:** Supply Sources v2020-07-01 (six operations under `/supplySources/2020-07-01/…`;
  Multi-Location Inventory locations; the model states no rates; *Supply Sources API Rate Limits*, updated
  2026-09-09, gives rate / burst `getSupplySources` 10 / 10, `createSupplySource` 2 / 2, `getSupplySource` 40 / 40,
  `updateSupplySource` 1 / 1, `archiveSupplySource` 20 / 20, `updateSupplySourceStatus` 20 / 20); Action Items and Action Plans (2026-10-28);
  `GET_V2_SELLER_PERFORMANCE_REPORT`; and, by Amazon's correction, the Economics dataset (section I).
- **Direct-to-Consumer Shipping (Restricted):** External Fulfillment Inventory `batchInventory`
  (`POST /externalFulfillment/inventory/2024-09-11/inventories`, up to 10 requests, absolute location-level quantity
  for Seller Flex, Easy Ship, Self Ship and others; the model states no rate; *External Fulfillment APIs Rate
  Limits* gives `batchInventory` 50 / 100, Returns `listReturns` and `getReturn` 10 / 20, Shipping `getShipments` and
  `getShipment` 2 / 5 and its eight writes 1 / 5); seller-fulfilled returns reports (60 days a report).
- **Inventory and Order Tracking only:** `GET_OUT_OF_STOCK_MFN_INFORMATION` (on the types page only; no type page
  describes it), `GET_FLAT_FILE_PENDING_ORDERS_DATA` and `GET_PENDING_ORDERS_DATA` (Japan store only).

## Only in Seller Central

Established by absence from every model and page read on 2026-11-10; `method/seller-central-only.md` compiles these.

- Capacity limits, capacity requests and reservation fees: no operation; only overage fees already charged (a report).
- Inventory Performance Index score: no field found in the FBA models, the FBA reports or the three datasets.
- Creating a removal order one at a time, liquidation and donation settings, automated removals: only the bulk feed.
- Low-inventory-level fee charged per unit: the planning report shows exemption and "applied in current week?"; the
  amount is in `economics` fees, whose role is disputed (I).
- Inventory at AWD for a seller whose application lacks the AWD role, and anywhere outside the US.
- "Seller Central provides additional reports that you can't access using the Reports API" (Reports FAQ).

## The seller's choices

- Which read is "demand": units ordered (`getOrderMetrics`, Sales and Traffic) or units shipped (customer shipment
  sales, the planning report's `units-shipped-t*`). They differ by pending and cancelled orders.
- The day boundary for `getOrderMetrics`: store-local, UTC or the seller's own zone; it changes each day's count.
- Whether to add a role (AWD, SPI, IOT) and re-authorise the store; each opens the reads listed above.
- Whether to keep an AWS queue for notifications or to poll.

## Open questions

1. Which role the Economics dataset needs in practice: settled by Amazon's reply to a first `createQuery` under the
   five roles.
2. Whether Amazon applies 5 or 2 a second to the six inbound reads: `x-amzn-RateLimit-Limit` on a live reply.
3. The time zone of each FBA report's date columns and of `dataStartTime`: Amazon's pages are silent; P3 suggests
   store-local for the ledger.
4. The character encoding of each FBA report as actually served (P1); the document's `Content-Type` charset on a
   first run.
5. Whether removal, disposal and liquidation fees appear in `economics` as `feeTypeName` strings, and their names.
6. What `GET_FBA_FULFILLMENT_INVENTORY_EXPIRATION_DATE_DATA` returns; no page describes it.
7. The freshness of the planning report and the request limit on the ledger pair; the page states neither.
8. Rates of the four AWD replenishment-order operations: the model states none, the AWD guide states none, and
   `llms.txt` lists no AWD rate-limit page (a GET of `amazon-warehousing-and-distribution-api-rate-limits.md`
   returns the site's not-found shell). Supply Sources and External Fulfillment rates are now in *Reads that need a
   role outside the five*.
9. Help pages named by the schemas and guides and not read first-hand: `GZ8Y22NL2FSRY8M5` and `GQNVDV46U9JQ25HY`
   (supported fee types), `GJQNPA23YWVA4SBD` (aged inventory surcharge), `G3EDYEF6KUCFQTNM` (monthly storage),
   `GV43F6S76Y9DHYRH` (low inventory level), `GC3Q44PBK8BXQW3Z` (inbound placement), `GYCAQ9XRL273EVDX`
   (Multi-Location Inventory).
10. Closed by the verifier: the door's `references/door.md`, as read 2026-11-10, states the correction's reading
    ("the Economics dataset needs Selling Partner Insights"); no follow-up is owed.
11. Column lists of the order, returns and performance report types were not transcribed here; the pages print
    them (`report-type-values-order`, `-returns`, `-performance`).

What the door lacks for a stock job (follow-ups, not changes): the 30-minute and four-hour generation rules and the
per-type request limits (H); `reportOptions` per stock type; any statement on a stock report's encoding; the 30-second
life of an inventory page token.

## Positions

- **P-sp-api-stock-surface-1.** Amazon's operations role page names Amazon Fulfillment or Product Listing for
  `getInventorySummaries`, at 2 requests a second, burst 2. Sources: Role Mappings for SP-API Operations (updated
  2026-10-28); `fbaInventory.json`. §B.
- **P-sp-api-stock-surface-2.** `getInventorySummaries` returns quantities only with `details=true`, accepts one
  marketplace and at most 50 SKUs, and its page token expires 30 seconds after it is created. Source: `fbaInventory.json`. §B.
- **P-sp-api-stock-surface-3.** `startDateTime` reaches back at most 18 months and does not detect changes in the three
  inbound quantities. Source: `fbaInventory.json`. §B.
- **P-sp-api-stock-surface-4.** Amazon defines `fulfillableQuantity` as "The item quantity that can be picked, packed,
  and shipped" and, at Marketplace granularity, as inventory that could be fulfilled in that marketplace. Source:
  `fbaInventory.json`. §B.
- **P-sp-api-stock-surface-5.** The FBA Inventory API carries no inventory age, storage volume, capacity limit or
  per-fulfilment-centre quantity. Source: `fbaInventory.json`. §B.
- **P-sp-api-stock-surface-6.** Amazon's FBA Inventory guide says on 2026-11-10 "This API is available in all
  marketplaces." Source: FBA Inventory API guide (updated 2026-09-09). §B.
- **P-sp-api-stock-surface-7.** Every Fulfillment Inbound operation, v2024-03-20 and v0, and the inbound eligibility
  preview need Amazon Fulfillment. Source: Role Mappings for SP-API Operations. §C.
- **P-sp-api-stock-surface-8.** A confirmed placement option cannot be changed for its inbound plan, and cancelling a
  plan outside the void window (for Amazon Partnered Carriers, 24 hours small parcel and one hour LTL) may be charged. Source:
  `fulfillmentInbound_2024-03-20.json`. §C.
- **P-sp-api-stock-surface-9.** Amazon's inbound rate-limit page and its 2025-06-25 release note give 5 requests a
  second for six inbound reads where the model still gives 2. Sources: Fulfillment Inbound API rate limits; release
  notes; the model. §K.
- **P-sp-api-stock-surface-10.** Fulfillment Outbound v2026-07-04 is absent from the operations role page; its guide
  names Amazon Fulfillment for each operation. Sources: both pages. §A, §D.
- **P-sp-api-stock-surface-11.** The AWD API is US-only and its role, Amazon Warehousing and Distribution, is outside
  the door's five. Sources: AWD API guide; Role Mappings for SP-API Operations. §E.
- **P-sp-api-stock-surface-12.** AWD `listInventory` separates on-hand, inbound to AWD, and `replenishmentQuantity`
  "in transit from AWD and has not yet been received at FBA". Source: `awd_2024-05-09.json`. §E.
- **P-sp-api-stock-surface-13.** The Product Fees API estimates per-sale fees and no storage fee; Amazon says its
  estimates "are not guaranteed". Sources: `productFeesV0.json`; Product Fees API guide. §F.
- **P-sp-api-stock-surface-14.** Catalog Items returns item and package length, width, height and weight under
  `includedData=dimensions`, and no size tier. Source: `catalogItems_2022-04-01.json`. §F.
- **P-sp-api-stock-surface-15.** A seller-fulfilled quantity is read and changed through Listings Items
  `fulfillmentAvailability`; Product Listing reaches it. Sources: `listingsItems_2021-08-01.json`; role page. §F.
- **P-sp-api-stock-surface-16.** `getOrderMetrics` counts units in orders, filters by `AFN` or `MFN`, and takes its
  day boundary from the caller's `granularityTimeZone`; hourly data reaches back 30 days, other granularities two
  years. Source: `sales.json`. §G.
- **P-sp-api-stock-surface-17.** Outside the Far East region, the roles Amazon names for `getOrderMetrics` are Product
  Listing and Inventory and Order Tracking. Source: Role Mappings for SP-API Operations. §G.
- **P-sp-api-stock-surface-18.** `searchOrders` returns each order's items with `quantityOrdered` and seller SKU, at
  0.0056 requests a second, burst 20. Source: `orders_2026-01-01.json`. §G.
- **P-sp-api-stock-surface-19.** The Replenishment API is Subscribe & Save, not FBA restock. Source:
  `replenishment-2022-11-07.json`. §G.
- **P-sp-api-stock-surface-20.** Amazon generates a near real-time FBA report at most once every 30 minutes and a daily
  one at most once every four hours, and says these are not request limits. Source: FBA report-type page (updated
  2026-10-13). §H.
- **P-sp-api-stock-surface-21.** On both of Amazon's role sources, Amazon Fulfillment is a named role for every
  unrestricted report on the FBA report-type page. The ledger detail and summary, the planning report,
  `GET_AFN_INVENTORY_DATA`, the overage fee report, the customer shipment sales report and the replacements report
  name Amazon Fulfillment alone; the other FBA stock reports also name Pricing. Sources: FBA report-type page
  (updated 2026-10-13), each type's Roles line; Role Mappings for SP-API Types (updated 2026-09-09). §A, §H.
- **P-sp-api-stock-surface-22.** On 2026-11-10 the types role page and the FBA report-type page disagree on two FBA
  reports' other roles: `GET_AFN_INVENTORY_DATA_BY_COUNTRY` (type page adds Pricing) and
  `GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL` (type page adds Pricing and Inventory and Order Tracking); they
  agree on the rest. Source: both pages. §A.
- **P-sp-api-stock-surface-23.** The ledger summary takes `aggregateByLocation` and `aggregatedByTimePeriod`; a monthly
  request must run from the first to the last day of a month, and a wrong range can return empty data. Source: FBA
  report-type page. §H.
- **P-sp-api-stock-surface-24.** The ledger detail holds 18 months of movements and filters by `eventType`. Source:
  FBA report-type page. §H.
- **P-sp-api-stock-surface-25.** The planning report's columns vary by store, it is absent in NL, PL, SE and BE, and
  the page states no freshness for it. Source: FBA report-type page. §H.
- **P-sp-api-stock-surface-26.** The restock report is available in every store except India. Source: FBA report-type
  page. §H.
- **P-sp-api-stock-surface-27.** The fee preview report can be requested once a day per seller, is refreshed at least
  every 72 hours, and holds no storage fee. Source: FBA report-type page. §H.
- **P-sp-api-stock-surface-28.** Amazon's pages state no time zone and no character encoding for any FBA report.
  Source: FBA report-type page; Reports FAQ. §H, §K.
- **P-sp-api-stock-surface-29.** Amazon retains deprecated report columns to keep column order and adds columns
  without notice. Sources: Reports FAQ; Reports API guide. §H.
- **P-sp-api-stock-surface-30.** Amazon's Data Kiosk guide (updated 2026-10-20) lists Brand Analytics for each of the
  five operations and says each field requires a role checked at query creation; Amazon's changelog correction
  (created 2024-07-02) says "The Economics dataset requires the Selling Partner Insights role", a role outside the
  door's five. Sources: Data Kiosk API; Correction: Data Kiosk role requirements. §I.
- **P-sp-api-stock-surface-31.** `economicsPreview` projects fees up to 120 days ahead by MSKU, including monthly
  storage, the aged inventory surcharge, the storage utilization surcharge and the low-inventory-level fee; it has no
  removal, disposal or liquidation type. Source: `analytics_economics_2024_03_15.graphql`. §I.
- **P-sp-api-stock-surface-32.** Seller Analytics carries one stock field, `totalFbaInventoryValue`, an account-level
  value on a 15-day average selling price; the dataset guide lists it under the `lending` group, granted by "Sales
  and lending access", for which the guide names no role. Sources: `analytics_sellerAnalytics_2025_03_31.graphql`;
  Seller Analytics dataset guide (updated 2026-09-30). §I.
- **P-sp-api-stock-surface-33.** A removal order is created through the SP-API only by the feed
  `POST_FLAT_FILE_FBA_CREATE_REMOVAL` (Amazon Fulfillment) and read only through the removal reports. Sources: FBA feed
  type page; models. §J.
- **P-sp-api-stock-surface-34.** The legacy quantity feeds are removed; a quantity change goes through Listings Items
  or `JSON_LISTINGS_FEED`. Sources: deprecation schedule; Listings feed type page. §J.
- **P-sp-api-stock-surface-35.** Every notification is delivered to Amazon SQS or Amazon EventBridge only.
  Source: Notification Type Values; Notifications API guide. §J.
- **P-sp-api-stock-surface-36.** `FBA_INVENTORY_AVAILABILITY_CHANGES` (Amazon Fulfillment) carries a regional
  snapshot per SKU, including In-Stock Head Start quantities. Source: the notification's schema. §J.
- **P-sp-api-stock-surface-37.** No stock API, report, feed or notification has a removal date in 2027 on Amazon's
  schedule as read 2026-11-10. Source: SP-API deprecation schedule (updated 2026-09-09). §K.
- **P-sp-api-stock-surface-38.** A developer reported in 2025 that an API-requested listings report arrived in
  cp-1252 with characters replaced (their report; the issue is open). Source: GitHub issue #4955, LukaszWypych. §P1.

The seat's own (no source; enters no skill):

- **Can cx write each call itself?** Yes for all of it, with two places where a single turn-by-turn agent loop is too
  slow and cx has to write a small shell loop at run time. (a) Create, poll, download: three `cx raw` calls and a
  wait; the door adds no wait and no retry, so the pacing is cx's, and one report a minute after a burst of 15 is slow
  but simple. (b) Download and decompress: the document URL lives five minutes and is fetched by the box; `gunzip`
  handles `GZIP`. (c) Decode: read the charset from the download's `Content-Type`; where it is missing or wrong (P1)
  cx can test for the BOM and for invalid UTF-8. (d) Large TSV: a shell with `awk` or Python reads a 100,000-row file
  without difficulty; the risk is column drift, met by reading the header row, not positions. (e) Ledger over 18
  months: 18 monthly `createReport` calls exceed the burst of 15 by three, so the last three wait a minute each; the
  whole-month rule is the pitfall, not the volume. (f) Data Kiosk: a query is a string under 8,000 characters; the
  schema files give the field names. (g) Paging `getInventorySummaries`: the 30-second token is the one place where
  an agent that thinks between pages can lose the token; a loop that pages without pausing does not. I could not test
  whether `cx raw` is comfortable inside a shell loop; the door's `--json` output suggests it is. On this evidence no
  shipped script is justified by inability; one might be justified by the 30-second token alone, if a first run shows
  cx losing it.
- Removal and disposal fees added to Economics on 2026-09-30 probably arrive as `feeTypeName` strings.
- **The other side, argued by the verifier (gap fill 2026-11-10; [seat]).** Nothing in the door's documented
  behaviour makes a call impossible for cx, so the brief's test ("cx cannot write the call itself") is not met by
  any step. What the research seat's "yes" passes over: (1) The 30-second token is not a matter of care. Every
  `cx raw` is a separate process with its own token trade, and a model turn between two pages will usually exceed
  30 seconds, so paging `getInventorySummaries` works only inside one shell loop that cx writes before the first
  page. That is still cx writing the call; and two reads avoid the token altogether: `sellerSkus` in batches of 50
  (no token) and the MYI report. (2) Long waits. Past the burst, `createReport` is one a minute: a job of five
  stores by ten report types is 50 creates, about 35 minutes of waiting, plus polling. Whether a loop of that
  length survives inside a cx turn, and whether `cx raw` runs unattended in a loop, is untested by either seat. (3)
  The five-minute document URL: the door's skill says the download is the box's own, so create, poll and download
  must be chained without a model turn between `getReportDocument` and the fetch on a slow day; again a loop, not
  an inability. (4) Decoding: Amazon states no encoding for FBA reports and P1 shows cp-1252 where UTF-8 was
  expected; a shipped script would know no more than cx does. (5) Sameness: a ledger reconciliation or a
  month-by-month slice done by freshly written code each run can differ run to run. A script would buy
  repeatability, which is a reason of quality, not of inability, and so falls outside the brief's test. Where a
  script would be justified, if anywhere: a single create-poll-download-decompress loop with back-off on `429`,
  and only if a first run shows cx cannot hold such a loop in one turn; and token-paged `getInventorySummaries`
  only if a first run shows the batches-of-50 route is unusable for a large catalogue. Neither is shown today.

## Pages read

All read 2026-11-10 by plain GET of the `.md` twin unless noted. URL = `https://developer-docs.amazon.com/sp-api/docs/<slug>`.

| Page | Slug or URL | Updated | Tag | Reached |
|---|---|---|---|---|
| Role Mappings for SP-API Operations | `role-mappings` | 2026-10-28 | official | yes |
| Role Mappings for SP-API Types | `role-mappings-for-types` | 2026-09-09 | official | yes |
| Roles in the Selling Partner API | `roles-in-the-selling-partner-api` | 2026-11-03 | official | yes |
| SP-API release notes | `sp-api-release-notes` | 2026-11-04 | official | yes |
| SP-API deprecation schedule | `sp-api-deprecations` | 2026-09-09 | official | yes |
| FBA Inventory API; inventory summaries tutorial | `fba-inventory-api`, `get-fba-inventory-summaries` | 2026-09-09 | official | yes |
| Report Type Values (index, FBA, inventory, analytics, order, returns, payment, performance) | `report-type-values`, `report-type-values-fba`, `-inventory`, `-analytics`, `-order`, `-returns`, `-payment`, `-performance` | 2026-09-09 to 2026-10-28 | official | yes; order, returns, performance and payment read only for role lines |
| Reports API guide, FAQ, retrieve a report, schedule and retrieve | `reports-api`, `reports-faq`, `retrieve-a-report`, `schedule-and-retrieve-reports` | 2026-09-09; 2026-10-14 | official | yes |
| Feed Type Values; FBA feed types; Listings feed types | `feed-type-values`, `fulfillment-by-amazon-feed-type-values`, `listings-feed-type-values` | 2026-11-05; 2026-10-14; 2026-09-09 | official | yes |
| Notification Type Values; Notifications API | `notification-type-values`, `notifications-api` | 2026-10-28; 2026-09-09 | official | yes |
| Data Kiosk API; Seller Analytics dataset guide | `data-kiosk-api`, `seller-analytics-dataset-guide` | 2026-10-20; 2026-09-30 | official | yes |
| Correction: Data Kiosk role requirements | `https://developer-docs.amazon.com/sp-api/changelog/correction-data-kiosk-role-requirements` | undated | official | yes |
| Fulfillment Inbound API rate limits | `fulfillment-inbound-api-rate-limits` | 2026-09-09 | official | yes |
| Fulfillment Outbound API | `fulfillment-outbound-api` | 2026-09-09 | official | yes |
| AWD API | `amazon-warehousing-and-distribution-api` | 2026-09-09 | official | yes |
| Product Fees, Supply Sources, External Fulfillment Inventory guides | `product-fees-api`, `supply-sources-api`, `external-fulfillment-inventory` | 2026-09-09 | official | yes, opening sections |
| Sales, Orders, Replenishment, Catalog Items, Listings Items guides; other rate-limit pages | various | 2026-09-09 | official | downloaded, not relied on; facts are from the models |
| SP-API models and schemas | local clone, commit `db2936aa` | 2026-10-29 | official | local |
| Commit list of `amzn/selling-partner-api-models` since 2026-10-29 | `https://api.github.com/repos/amzn/selling-partner-api-models/commits?since=2026-10-29T00:00:00Z` | — | official | yes |
| Issues #4955, #4762, #5339 (with comments), #5209 | `https://api.github.com/repos/amzn/selling-partner-api-models/issues/<n>` | — | opinion | yes |
| The door's skill and reference | `packages/cx-amazon-sp-api-305/skills/amazon-sp-api/` | — | local | yes |
| Survey stock notes | `scratch/sp-api-plugins/03-job-stock.md` lines 1–407 | — | starting material | yes; its four-role premise is superseded by the door's five |
| Verifier's re-fetch of every page above, plus the 11 other report-type and feed-type pages, the Supply Sources and External Fulfillment rate-limit pages and the Data Kiosk launch announcement | `.md` twins; `…/sp-api/changelog/data-kiosk-reports-experience-general-availability-launch.md` | as above | official | yes, 2026-11-10; copies under `scratch/stock-playbook/sp-api-stock-surface/verify/` |
| Survey tool notes | `scratch/sp-api-plugins/03-tools-en.md`, `03-tools-cn.md` | read 2026-11-09 by the survey | opinion, via the survey | local files; vendors' pages not re-fetched |
| Seller Central help pages named in Open question 9 | `sellercentral.amazon.com/help/hub/reference/external/<id>` | — | — | unreachable by ruling; not tried |

## Gap fills by the verifier (gap fill 2026-11-10)

- **Order, returns and pending-order reports** (pages `report-type-values-order`, `-returns`, updated 2026-10-28):
  the order-tracking (all orders) reports' "date range … is limited to 30 days"; the pending order reports are "only
  available in the Amazon Japan store" with "a 38-day lookback period"; the seller-fulfilled returns reports take "up
  to 60 days of data in a single report" and exclude FBA returns ("Use the FBA Returns Report … instead").
  `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL` is described on both the FBA page and the order page with
  different Roles lines (A). [official]
- **`searchOrders` page token**: "The token will expire after 24 hours" (`orders_2026-01-01.json`), against 30
  seconds for `getInventorySummaries`. [official]
- **`getInventorySummaries` token, the sentence**: `fbaInventory.json`, parameter `nextToken`: "String token returned
  in the response of your previous request. The string token will expire 30 seconds after being created." The guide
  and its tutorial (both updated 2026-09-09) do not repeat it. [official]
- **Rates outside the models**: Supply Sources and External Fulfillment (in *Reads that need a role outside the
  five*). [official]

## Verification

2026-11-10, by the verifier. Every developer-docs page in *Pages read* was fetched again today by plain GET of its
`.md` twin; `updatedAt` matched the file on all of them. Models were re-read at `db2936aa`; GitHub's commit list
since 2026-10-29 still returns that one commit. The four GitHub issues were re-read through `gh api`.

**Checked.** 38 positions. Beyond them: roles of about 110 operations and 90 feed, report and notification types
re-parsed from the two role pages (350 and 181 rows) and compared mechanically with the Roles line of all 125 types
that carry one; rate and burst of every operation in sections B–J re-extracted from the models; the 21 column lists
compared with the page; 43 model quotations string-matched; the release-note and deprecation dates in K.

**Changes.**

- §A, 4th bullet. Said 88 types carry a Roles line, that the two sources agree on every FBA stock report, and that
  the order page gives PL for `GET_PENDING_ORDERS_DATA`. The pages: 125 types; two FBA reports and four other types
  differ; `GET_PENDING_ORDERS_DATA` has no Roles line (PL is the converged flat-file report's). Rewritten.
- P-22. Said the sources agree for every FBA stock report. They differ on two. Reworded to state the two.
- P-21. Added the replacements report to the AF-only list and the statement, checked per type, that AF is named for
  every unrestricted FBA-page report on both sources (the claim a skill leans on: it holds).
- §H table. `GET_STRANDED_INVENTORY_LOADER_DATA` freshness "—" became near real-time (page: "Content updated in near
  real-time"). Overage report "fees charged" became Amazon's "Estimated … overage fees". "Stores: EU, JP, NA" on the
  customer shipment sales and fulfilled shipments rows was the freshness sentence, not a store restriction; moved.
  All-orders row gained the 30-day limit and the role difference; pending-orders and returns rows filled; the
  sentence above the table no longer claims the types page as the roles' source. §K *Missing stores* follows.
- §I role paragraph and P-30. Both pages are now quoted with dates; the correction's date (2024-07-02) is from the
  page source, the rendered page shows none; added that the corrected launch announcement says the same and that the
  two statements are of different things (operation role, dataset role). Removed "the door's line follows the
  first": the door states the correction. Open question 10 closed accordingly.
- §I and P-32. `totalFbaInventoryValue` under the `lending` group moved from the seat's guess to the guide's
  statement.
- §J. `REPORT_PROCESSING_FINISHED` roles: the types page also names three restricted roles.
- P-8. Said cancelling outside the void window "is charged"; the model says charges "may apply" and limits the
  window to Amazon Partnered Carriers. Reworded.
- P-38. "unanswered" became "the issue is open" (it has two comments, not read for an Amazon answer).
- Practitioners. P4 gained the second comment; P5–P7 added from the survey's tool notes, tagged as the survey's read.
- The seat's own. The script question now carries the other side and where a script would be justified.

No position was removed. No position was found to be worded as an instruction to cx. No position rests on a read
outside the five roles: P-11, P-12 and P-30 state that AWD and Economics lie outside them.

**Not re-opened.** The payload field lists of the notifications other than `FBA_INVENTORY_AVAILABILITY_CHANGES`
(its five named fields were found in the schema); the Catalog Items `dimensions` structure; `searchOrders`' 100 a
page and `getMyFeesEstimates`' 20 items (the 50-marketplace limit was found); the Sales and Traffic schema's field
descriptions; the economics `FeeSummary` structure; the inbound writes' rate groups one by one (reads were
re-extracted; writes were sampled); the Replenishment store list was matched in the research seat's saved copy of
the guide, not a fresh fetch; the vendors' pages behind P5–P7. The void-window wording behind P-8 was re-read: "Charges may apply if the cancellation is
performed outside of a void window. The window for Amazon Partnered Carriers is 24 hours for Small Parcel Delivery
(SPD) and one hour for Less-Than-Truckload (LTL) carrier shipments." It holds; the model says charges "may apply"
and names Amazon Partnered Carriers, which P-8's "is charged" compresses.

**Gaps filled.** Supply Sources and External Fulfillment rate tables; order, returns and pending-order report
facts; the ERP notes; the token sentence; the Economics role quotations; the script argument.

**Gaps left.** AWD replenishment-order rates (no Amazon page states them). Column lists of order, returns and
performance reports. The time zone and encoding of each FBA report (Amazon's pages are silent; first-run
questions). What `GET_FBA_FULFILLMENT_INVENTORY_EXPIRATION_DATE_DATA` and `GET_OUT_OF_STOCK_MFN_INFORMATION` return.
What a long-serving inventory manager would still miss here: any API read of capacity limits or the IPI score
(none exists; stated), lot or expiry dates outside AWD's `expirationDetails`, and per-fulfilment-centre on-hand
other than through the ledger summary by `FC`, the storage-fee report and the shipment reports.
