# Writes: what each charges and what is permanent

## The async model

- A v2024-03-20 write whose response carries an `operationId` is asynchronous, its outcome read with `getInboundOperationStatus` (I16).
- `updateInboundPlanName` and `updateShipmentName` answer 204 with no body, `scheduleSelfShipAppointment` answers with the appointment, and `createMarketplaceItemLabels` with the label documents; none carries an `operationId` (I16).
- Options are generated, listed and confirmed, and unconfirmed options expire (I16).

## Placement

- Through the API a placement option's fee or discount is a quoted figure on the option, set by an algorithm at creation and not by a rate table (I15).
- Options generated before box contents are known can differ from those generated after (I15).
- `confirmPlacementOption` cannot be reversed or changed for the plan (I15).
- The US inbound placement service fee has applied since 2024-03-01, differs by split, and is charged after receipt on the actual inbound location and received quantities, so the figure at creation is an estimate (C29).
- A plan's quoted fee is `fees` on `listPlacementOptions`, the charged amount is in Finances, and the rate table is a Seller Central help page this research could not read (C29).
- The placement fee among the other charges: ../../stock-cost/SKILL.md.
- No published study was found, by searches of 2026-11-10, of the inbound placement fee and sellers' stocking behaviour (T5).

## Transportation

- Confirming a partnered-carrier transportation option agrees to the charge (I16).
- It can be voided within 24 hours for small parcel or one hour for LTL/FTL, outside which charges "may apply", and these limits do not apply to non-partnered options (I16).
- `cancelInboundPlan` cancels the whole plan and all its shipments (I16).

## Changing a shipment

- After transportation is confirmed and before Receiving, a shipment's units per SKU can be changed within a bound stated on the *Additional functionality* page of Amazon's Fulfillment Inbound guide, a share of the units or a unit count, whichever is greater (I17).

## Abandoning a shipment

- Ignoring, deleting or abandoning one shipment of a multi-shipment plan creates an abandoned-shipment defect subject to the inbound defect fee, and re-prices the plan's placement fee at the minimal-splits rate, by Bryce_Amazon's forum post of 2024-06-27 (I13).
- The inbound defect fee's value is on a Seller Central help page this research could not read (I13).

## Prep and labels

- Since 2026-01-01 Amazon provides no prep or item-label service for US FBA inventory, including inventory arriving through AWD, AGL, Amazon SEND and Supply Chain Portal, and `AMAZON` is not accepted as `prepOwner` or `labelOwner` in the US (I19).

## Seller Central only

- AGL bookings, Carrier Central, remeasurement requests and dangerous-goods document upload appear in no model (I18).
