# Reads and roles: what each stock read returns and which role opens it

How a call is made and a report is asked for and landed, and how rates and roles work at the door: the amazon-sp-api skill's references/door.md.

## `getInventorySummaries`

- `getInventorySummaries` returns one summary per seller SKU for one marketplace (W2).
- Its `totalQuantity` is "the total number of units in an inbound shipment or in Amazon fulfillment centers", so it includes inbound (W2).
- Amazon's guide says the FBA Inventory API "is available in all marketplaces" (W2).
- The quantity breakdown is returned only when the request sets `details=true`, whose default is false (W3).
- A request takes one marketplace and at most 50 SKUs; its rate is stated in its model (W3).
- A request with `startDateTime` returns summaries changed since then, reaches back at most 18 months, ignores the SKU filters, and does not detect changes in the three inbound quantities (W4).
- A `nextToken` expires 30 seconds after it is created, and a `startDateTime` request must repeat `startDateTime` with every token (W5).
- An empty page that still carries a token is expected, by Amazon support as a developer quoted it (W5).
- The `searchOrders` token, by contrast, lives 24 hours (W5).
- The FBA Inventory API carries no inventory age, storage volume, capacity limit or per-fulfilment-centre quantity (W45).
- Per-centre on-hand is reached through the ledger summary by fulfilment centre, the storage-fee report and the shipment reports (W45).

## Notifications

- `FBA_INVENTORY_AVAILABILITY_CHANGES` is sent on any change in FBA quantities and carries a snapshot per SKU for every eligible store in the region, with inbound, reserved and In-Stock Head Start breakdowns (W33).
- Every SP-API notification is delivered to Amazon SQS or Amazon EventBridge only (W33).
- Under Pan-European FBA, whether this notification repeats the EU sum per marketplace was read in Amazon's documents and not yet seen on a live store (W18, W33).
- `ITEM_INVENTORY_EVENT_CHANGE` is sent hourly at ASIN grain with data delayed up to 24 hours (W34).
- Its `highlyAvailableInventory` subtracts units in customer shopping carts or bound for other orders (W34).
- Whether it reports a third-party seller's own FBA units was read in Amazon's documents and not yet seen on a live store (W34).

## Other reads

- Catalog Items returns item and package length, width, height and weight under `includedData=dimensions`, and no size tier (A1).
- Seller Analytics in Data Kiosk carries one stock field, `totalFbaInventoryValue`, an account-level value on a 15-day average selling price (A4).
- That field is listed under the `lending` group granted by "Sales and lending access", for which Amazon's guide names no role (A4).
- Amazon's pages state no time zone and no character encoding for any FBA report; the time zone of each report's date columns was read in Amazon's documents and not yet seen on a live store (A2).
- Amazon retains deprecated report columns to keep column order, and adds columns without notice (A3).
- No stock API, report, feed or notification has a removal date in 2027 on Amazon's deprecation schedule as read on 2026-11-10 (A5).

## Roles

- The door's application holds five roles: Product Listing, Pricing, Brand Analytics, Finance and Accounting, and Amazon Fulfillment (W46).
- `getInventorySummaries` needs Amazon Fulfillment or Product Listing, by *Role Mappings for SP-API Operations* and the API guide (W3, W46).
- Amazon's *Get inventory summaries* tutorial names Product Listing alone as its prerequisite (W3).
- The MYI, reserved and Restock reports need Amazon Fulfillment or Pricing (W46).
- `GET_AFN_INVENTORY_DATA`, the planning report, both ledger views, the overage fee, customer shipment sales and replacements reports, and `FBA_INVENTORY_AVAILABILITY_CHANGES` need Amazon Fulfillment alone (W22, W23, W33, W46).
- `ITEM_INVENTORY_EVENT_CHANGE`, Sales and Traffic and the Replenishment API need Brand Analytics (W34, W46).
- Amazon Fulfillment is named for every unrestricted report on the FBA page on both of Amazon's role sources (W46).
- The two sources disagree on two reports: the type page adds Pricing on `GET_AFN_INVENTORY_DATA_BY_COUNTRY`, and Pricing and Inventory and Order Tracking on `GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL` (W46).
- Every read the stock-out file names is open to at least one of the five roles (W46).
- `GET_PAN_EU_OFFER_STATUS` needs Product Listing, Pricing or Amazon Fulfillment, and also accepts Inventory and Order Tracking or Direct to Consumer Shipping (G4).
- `GET_REMOTE_FULFILLMENT_ELIGIBILITY` needs Amazon Fulfillment (G10).
- Every AWD operation on Amazon's role page, `listInventory` and `checkInboundEligibility` among them, needs the Amazon Warehousing and Distribution role, which the five do not include (W38, G15).
