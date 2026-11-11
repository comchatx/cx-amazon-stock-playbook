# Reads: what the API and the reports show of inbound

## Operations and roles

- Amazon's current inbound creation API is Fulfillment Inbound v2024-03-20 (I1).
- Ten v0 operations, `createInboundShipmentPlan`, `createInboundShipment`, `putTransportDetails`, `confirmTransport` and `voidTransport` among them, were removed on 2025-01-21 (I1).
- Six v0 reads remain and are not deprecated: `getShipments`, `getShipmentItems`, `getShipmentItemsByShipmentId`, `getLabels`, `getBillOfLading` and `getPrepInstructions` (I1).
- Every Fulfillment Inbound operation of both versions, and the inbound eligibility preview, needs the Amazon Fulfillment role (I1).
- Amazon's inbound rate-limit page and its release note of 2025-06-25 give 5 requests a second for six inbound reads, where the `fulfillmentInbound` model still gives 2 (I2).
- Which of the two rates holds was read in Amazon's documents and not yet seen on a live store (I2).
- How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.

## Identifiers and plans

- A shipment has two identifiers: the `shipmentId` issued at planning, and the `shipmentConfirmationId` issued by `confirmPlacementOption`, printed on labels and taken by the remaining v0 operations (I4).
- That v0 `getShipments` takes every `shipmentConfirmationId`, AWD-originated shipments included, was read in Amazon's documents and not yet seen on a live store (I4).
- Amazon's Fulfillment Inbound guide and FAQ say a plan created in Send to Amazon is readable through `listInboundPlans` and the v2024-03-20 GET operations once its placement and transportation options are confirmed (I5).
- A plan moved to Send to Amazon before that has its options discarded and regenerated (I5).
- Amazon's own `fba-inbound-management` agent skill says instead that only API-created plans are visible, gives a 500,000-unit per-SKU limit, and names an operation (`updateBoxIdentifiers`) and a field (`readyToShipDate`) found in no SP-API model, and a field (`shipFromAddress`) in no Fulfillment Inbound model (I5).
- How Send to Amazon, AGL and Amazon SEND plans appear in the inbound reads was read in Amazon's documents and not yet seen on a live store (I5).
- `listInboundPlans` has no marketplace filter, returns at most 30 plans a page, filters on `ACTIVE`, `VOIDED` and `SHIPPED`, and needs the same filters on every follow-up page (I6).
- One plan holds at most 1,500 SKUs and 10,000 items per SKU, by Amazon's FAQ, and one expiration date per SKU (I6).

## Quantities

- Amazon defines inbound working as units in a shipment the seller has notified Amazon of, inbound shipped as units the seller has also given a tracking number for, and inbound receiving as units not yet received in a shipment some of whose units have been (W7).
- The three are `afn-inbound-working/shipped/receiving-quantity` in the MYI report and `Working`, `Shipped`, `Receiving` in the Restock report, whose `Total Days of Supply` counts units from open shipments (W7).
- Every quantity field in the v2024-03-20 model is a planned figure; no operation of that version returns a received quantity (I3).
- Among API operations, received units per SKU per shipment are only `QuantityReceived` beside `QuantityShipped` in the v0 item reads (I3).
- The Inventory Ledger detail lists receipts per fulfilment centre and date under the `Receipts` event type (W27).
- The ledger carries no inbound quantity (W28).
- Every state beside inbound, and where the reads do not tie: ../../stock-position/SKILL.md.

## Reports

- The FBA Inbound Performance Report `GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA` (Pricing or Amazon Fulfillment, updated daily) lists inbound problems per shipment and SKU (I14).
- Its columns include `problem-type`, `coaching-level`, `expected-quantity`, `received-quantity`, `fee-type`, `fee-total` and `alert-status` (I14).

## What the API returns and what it does not

- For plans created through it, the v2024-03-20 API returns partnered-carrier options with quotes, placement options with fees, self-ship appointment slots and item labels (I18).
- AGL bookings, Carrier Central, remeasurement requests and dangerous-goods document upload appear in no model (I18).

## Eligibility

- `getItemEligibilityPreview` (Amazon Fulfillment) answers whether one ASIN may be inbounded to one marketplace and why not, with Amazon's reason code, a dangerous-goods review among them (I20).
- It does not answer for a quantity or for capacity (I20).

## AWD

- With the five roles, AWD stock, its inbound to AWD and `replenishmentQuantity` (in transit from AWD, not yet received at FBA) are not readable: every AWD operation on the role page needs the Amazon Warehousing and Distribution role, which the five do not open (W38).
