# Multi-Channel Fulfillment as a drain on FBA stock

How a call is made: the amazon-sp-api skill's references/door.md.

## One pool

- An MCF order ships from the same FBA inventory that serves Amazon orders, "a single pool of inventory across channels" (F20).
- Units Seller Central shows in stock can be unavailable to an MCF order because they are reserved for other orders, in transfer, unfulfillable or still receiving (F20).
- At which Fulfillment Outbound status an MCF order's units leave `fulfillableQuantity`, whether they appear under `pendingCustomerOrderQuantity`, and how an MCF shipment is typed in the ledger, is not stated in Amazon's documents as read and is not yet seen on a live store (F20).
- FBA's own states and the ledger: ../stock-position/SKILL.md.

## Versions and roles

- Fulfillment Outbound has a current version v2026-07-04, launched 2026-07-29, and a legacy v2020-07-01 with no removal date on the deprecation schedule read 2026-11-10 (F21).
- *Role Mappings for SP-API Operations* lists every operation of v2020-07-01 under Amazon Fulfillment, with `cancelFulfillmentOrder` also under Product Listing, and has no v2026-07-04 section (F21).
- The v2026-07-04 guide names Amazon Fulfillment for each operation (F21).
- Whether v2026-07-04 is granted on the Amazon Fulfillment role was read in Amazon's documents and not yet seen on a live store (F21).
- Package tracking moves to the Tracking API's `getShipmentTracking`, which is grantless and US-only (F21).

## Reads and writes

- In v2026-07-04, `getOrderPreview` (v2020-07-01: `getFulfillmentPreview`) creates nothing and returns fulfillability, constraints, planned shipments and estimated MCF fees, and is Amazon's named check for fulfillability (F22).
- `updateOrderStatus` and `updatePackage` are sandbox-only (F22).
- The feature-eligibility operations (`getFeatures`, `getFeatureSKU`, `getFeatureInventory`) and the return operations have no v2026-07-04 counterpart and are deprecated, though v2020-07-01 still serves them (F22).
- v2020-07-01 `getFeatures` returns a marketplace's MCF features and whether the seller is enrolled in each (F22).
- `createOrder`, `updateOrder` and `cancelOrder` (and their v2020-07-01 counterparts) make Amazon ship, change or cancel a shipment of FBA units at MCF fees (F23).
- A legacy order can be cancelled in `Received` and `Planning`, and not once `Processing` has begun (F23).
- An MCF order created with action `HOLD` reserves inventory without shipping and is cancelled automatically after a set time; that duration, and the unit cap on a hold order in India, are read in *MCF best practices* (developer-docs) and the store's *Supply Chain Portal help guide* (F24).
- A hold order's state is read from Fulfillment Outbound `getFulfillmentOrder` (F24).
- The default fill policy is fill-or-kill; `FILL_ALL` waits for every item and `FILL_ALL_AVAILABLE` ships what it can (F24).
- Blocking Amazon Logistics on an MCF order carries a fee surcharge, "may increase the risk of unfulfilled or delayed deliveries", and overrides the Seller Central account setting (F25).
- No operation states that surcharge; the rule is in the *Supply Chain Portal help guide* (2025-07-18) and *MCF best practices* (developer-docs) (F25).

## Sync and stock guidance

- Amazon's guidance to MCF integrators is to read `getInventorySummaries` once a day, take changes from `FULFILLMENT_ORDER_STATUS` and `FBA_INVENTORY_AVAILABILITY_CHANGES`, and "Operate with safety stock settings to prevent overselling between sync jobs", with no figure given (F26).
- Amazon's *Supply Chain Portal help guide* (2025-07-18) recommends, as a best practice, a minimum cover in weeks and a minimum unit count received in a fulfilment centre; it is a recommendation, not an eligibility rule, and its figures are read in that guide (F26).
- `FULFILLMENT_ORDER_STATUS` payload 1.0 is deprecated in favour of 2026-07-04, with no removal date on the schedule (F26).

## Fees and orders

- MCF fee amounts for an order are read at run time from v2026-07-04 `getOrderPreview`, and the fee table is *Multichannel Fulfillment (MCF)* on supplychain.amazon.com (F26, F27).
- Amazon's MCF page announced on 2026-11-10 updated US fulfilment fees for 2027; the effective date and amounts are on that page (F27).
- `searchOrders` (Orders v2026-01-01) filters by `fulfilledBy` and `fulfillmentStatuses` and is open to Amazon Fulfillment, Finance and Accounting, Pricing and Product Listing (F28).
- Its rate is the one the amazon-sp-api skill states (F28).
