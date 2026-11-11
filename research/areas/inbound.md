# Inbound to Amazon, as far as a stock position needs it

Read 2026-11-10 by the research seat.

Tags: **[official]** is Amazon's own words on a page opened in this session or in a local file (the SP-API models at
commit `db2936aa`, 2026-10-29; the SP-API documentation; sell.amazon.com; posts by Amazon accounts on the Seller
Forums). **[official, via <who>]** is Amazon's text as quoted or reported by a third party. **[snippet]** is a search
result line whose page was not opened. **[opinion]** is a named practitioner or tool. **[seat]** is this seat's own
inference and enters no skill.

How pages were reached. SP-API documentation was fetched as markdown with a plain GET from
`https://developer-docs.amazon/sp-api/docs/<slug>.md` (the old host `developer-docs.amazon.com` redirects there; the
index is `https://developer-docs.amazon/sp-api/llms.txt`). Seller Forums threads
(`https://sellercentral.amazon.com/seller-forums/discussions/t/<id>`) and `sell.amazon.com/blog/...` serve their text
to a plain GET. **Seller Central help pages do not**: every form tried (`/help/hub/reference/external/<ID>`, with
`?locale=en-US`, `/gp/help/external/<ID>`, the `.co.uk` twin) returned a script shell with no article text, and the
content call is off limits by the lead's ruling of 2026-11-10. Help-page facts therefore come from four places, each
marked where used: Amazon's own forum announcements that restate the page; the listing playbook's quotations of
2026-10-14 (`cx-listing-playbook/research/angles/inventory-and-fulfillment.md`, **cited as that seat's read, not
re-read**); one local capture of 2026-10-14 (*Prime Day readiness playbook*, `GM2ADTH3XH3A5N57` v4, in the office's
capture folder); and third parties. Every help page not read first-hand is listed in *Open questions*.

## What this covers

- What a stock position needs to read about inbound: which units are on their way, in what state, when they become
  sellable, what went missing, and what the inbound itself cost.
- The states of an inbound plan and of a shipment in Fulfillment Inbound v2024-03-20 and in the six v0 reads that
  remain; shipped against received per SKU; how inbound shows in `getInventorySummaries` and in the inventory reports.
- Time from ship to sellable as Amazon states it; the automatic-closure rule; the delivery-window requirement.
- Inbound placement (the options, when the fee is charged, what is permanent), inbound defects, and the Inbound
  Performance report.
- Reconciliation of shipped against received, and the claim windows as Amazon has announced them.
- What constrains an inbound at creation: eligibility per ASIN, plan size, expiration, prep and label ownership,
  capacity, peak arrive-by dates for 2025 and 2026.
- The writes the Amazon Fulfillment role carries, stated as facts: which confirmation is permanent, which charges,
  which expires, which can be voided and for how long.
- Where this pack ends and an inbound plugin (`cx-inbound-shipments`) begins.

Owned elsewhere and only cross-referenced:

- `areas/stock-states.md`: the full state model of FBA stock (fulfillable, reserved, unfulfillable, researching);
  this file owns only the inbound states.
- `areas/holding-costs.md`: every fee amount, including the inbound placement service fee table, the inbound defect
  fee table, peak fees and storage. This file states when and why an inbound fee arises, not its rate card.
- `areas/running-out.md` and `areas/restock-and-forecast.md`: what a late or short inbound does to cover, and how
  lead time enters a reorder point.
- `areas/stuck-stock.md`: stranded and unfulfillable stock after receipt.
- `areas/fbm-and-outside-fba.md`: seller-fulfilled stock and non-Amazon warehouses.
- `beyond/programs-and-regions.md`: AWD, AGL, Amazon SEND, Pan-EU and the other programs as programs.
- `method/sp-api-stock-surface.md`: the operation and report catalogue; `method/seller-central-only.md`: the pages
  with no API.
- A claims plugin (`cx-reimbursement-claims`) would own filing; this file owns only reading the discrepancy.

## Amazon's own rules

### A. The two API generations and what is left of v0

A1. The current creation API is Fulfillment Inbound v2024-03-20 (45 operations in the model
`fulfillment-inbound-api-model/fulfillmentInbound_2024-03-20.json`). Its `info` text says: "The API has
interoperability with the Send-to-Amazon user interface." [official] It reached general availability on 2024-06-27:
"You can use this API to select from multiple inbound placement service options and create inbound plans with
support for up to 1500 SKUs." [official] *SP-API release notes*, entry June 27, 2024,
https://developer-docs.amazon/sp-api/docs/sp-api-release-notes.md, read 2026-11-10.

A2. Ten v0 operations were removed on **January 21, 2025** (deprecation announced April 1, 2024): `confirmPreorder`,
`confirmTransport`, `createInboundShipment`, `createInboundShipmentPlan`, `estimateTransport`, `getPreorderInfo`,
`getTransportDetails`, `putTransportDetails`, `updateInboundShipment`, `voidTransport`. `getInboundGuidance` was
removed on March 27, 2024. The flat-file feeds `POST_FLAT_FILE_FBA_CREATE_INBOUND_PLAN` and
`POST_FLAT_FILE_FBA_UPDATE_INBOUND_PLAN` were removed on March 27, 2024. [official] *SP-API deprecations*,
https://developer-docs.amazon/sp-api/docs/sp-api-deprecations.md (updatedAt 2026-09-09), read 2026-11-10.

A3. Six v0 operations remain and are not deprecated: "`getLabels`, `getBillOfLading`, `getPrepInstructions`,
`getShipments`, `getShipmentItemsByShipmentId`, `getShipmentItems`." [official] *Fulfillment Inbound API* guide,
https://developer-docs.amazon/sp-api/docs/fulfillment-inbound-api.md (updatedAt 2026-09-09), read 2026-11-10. The
migration guide says what they are for: `getShipmentItemsByShipmentId` / `getShipmentItems`, "Get quantity shipped
and quantity received."; `getShipments`, "Get shipment status."; and "Use `shipmentConfirmationID` in place of
`shipmentId` for all v0 operations that are not deprecated." [official] *Migrating Fulfillment Inbound workflows*,
https://developer-docs.amazon/sp-api/docs/migrating-fulfillment-inbound-workflows.md (updatedAt 2026-09-09).

A4. **v2024-03-20 carries no received quantity; among API operations only the v0 item reads do.** Every quantity
property in the v2024-03-20 model is a planned figure: `Item.quantity` ("The number of the specified MSKU."),
`ItemInput.quantity` ("The number of units of the specified MSKU that will be shipped."), `Box.quantity`,
`BoxInput.quantity`, `BoxUpdateInput.quantity`, `Pallet.quantity`, `PalletInput.quantity` (each "The number of
containers where all other properties like weight or dimensions are identical.") and `MskuQuantity.quantity` (label
printing). A search of the model for "receiv" finds only status text, a set-packaging label text and the
`MANUAL_PROCESS` box-content description. Outside the API operations, a received figure per SKU and shipment also
appears in the Inbound Performance report (D5, problem rows only) and receipts appear in the Inventory Ledger (F7).
The v0
`InboundShipmentItem` carries `QuantityShipped` ("The item quantity that you are shipping.") and `QuantityReceived`
("The item quantity that has been received at an Amazon fulfillment center."). [official] models,
`fulfillmentInboundV0.json` definition `InboundShipmentItem`.

A5. Two identifiers name one shipment. `createInboundPlan` and placement generation issue a `shipmentId`;
`confirmPlacementOption` issues the `shipmentConfirmationId`, "the identifier that appears on labels (for example,
`FBA1234ABCD`)". Both are returned by `getShipment`. `getLabels` takes "the `shipmentId` (from v0) or the
`shipmentConfirmationId` (from v2024-03-20). Do not use the `shipmentId` from v2024-03-20." [official] *Create an
inbound shipment*, https://developer-docs.amazon/sp-api/docs/create-an-inbound-shipment.md, read 2026-11-10.

A6. Plans made in Seller Central are readable through the API, and the reverse. "Plans created with the Fulfillment
Inbound API can be accessed and edited on Amazon's UI, Send to Amazon (STA), once placement and transportation
options are confirmed. You can also use the API to access plans that were created in STA after you confirm placement
and transportation options." [official] *Fulfillment Inbound API* guide. The FAQ: "For shipments created with the
Send to Amazon UI, you can retrieve all inbound details with the `listInboundPlans` operation and the … GET
operations." [official] *Fulfillment Inbound API FAQ*,
https://developer-docs.amazon/sp-api/docs/fulfillment-inbound-faq.md (updatedAt 2026-09-09). A plan that is switched
from the API to STA before its options are confirmed loses them: "new options are generated in STA and all previous
options are discarded." [official] guide. During the placement step, "You cannot access API-created shipments on
Send to Amazon". [official] *Create an inbound shipment*.

A7. Where it works. The guide: "The Fulfillment Inbound API supports shipment creation in all Amazon stores except
Brazil." The FAQ of the same date lists Canada, US, Mexico, Spain, UK, France, Netherlands, Germany, Italy, Sweden,
Poland, Egypt, Saudi Arabia, United Arab Emirates, Singapore, Australia and Japan, and says "We will announce
support" for Brazil, Turkey and India. The release note of August 27, 2025 added `districtOrCounty` so that the API
can "create shipments in the Amazon TR store", and the model carries India-only operations
(`updateItemComplianceDetails`, `getDeliveryChallanDocument`). The guide itself has a section "Ship inventory in the Amazon India store" pointing to the tutorial *Ship Inventory
to Amazon Fulfillment Centers in India*. **The FAQ's "We will announce support" list (Brazil, Turkey, India)
disagrees with the guide, the release note of August 27, 2025 and the model on Turkey and India**; all are on pages
fetched 2026-11-10, and all are recorded. [official] guide, FAQ, release notes, model.

### B. States

B1. Plan status (v2024-03-20 `InboundPlan.status`): `ACTIVE`, `VOIDED`, `SHIPPED`, `ERRORED`. `listInboundPlans`
filters on `ACTIVE`, `VOIDED`, `SHIPPED`; sorts by `LAST_UPDATED_TIME` or `CREATION_TIME`; has no marketplace
filter; page size 1–30, default 10. `InboundPlan.shipments` is populated after a placement option is confirmed.
"`listInboundPlans` is a paginated call. When you make follow-up calls to get more pages of data, you must pass the
same filters as you did in the original call". [official] model; *Additional functionality*,
https://developer-docs.amazon/sp-api/docs/additional-functionality-fulfillment-inbound.md.

B2. Shipment status in v2024-03-20, from the model: "will typically start as `UNCONFIRMED`, then transition to
`WORKING` after a placement option has been confirmed, and then to `READY_TO_SHIP` once labels are generated.
Possible values: `ABANDONED`, `CANCELLED`, `CHECKED_IN`, `CLOSED`, `DELETED`, `DELIVERED`, `IN_TRANSIT`, `MIXED`,
`READY_TO_SHIP`, `RECEIVING`, `SHIPPED`, `UNCONFIRMED`, `WORKING`". [official] model. Amazon's definitions, from
the FAQ table [official]:

| Status | Amazon's definition (FAQ, updatedAt 2026-09-09) |
|---|---|
| `ABANDONED` | "Indicates something went wrong during the shipment creation process." |
| `CANCELED` (FAQ spelling; the model's value is `CANCELLED`) | "Indicates that the shipment was canceled." |
| `CHECKED_IN` | "the fulfillment center has acknowledged delivery of the shipment and has checked it in." |
| `CLOSED` | "there are no further actions to take on the shipment." |
| `DELETED` | "the shipment was deleted prior to it being shipped." |
| `DELIVERED` | "the carrier has delivered the shipment to the fulfillment center, but the fulfillment center has not yet checked it in." |
| `IN_TRANSIT` | "the shipment is within the carrier network and is in the process of being couriered." |
| `MIXED` | "Used for a special placement option where sellers send in a single shipment but the carrier will distribute it across Amazon fulfillment centers." |
| `READY_TO_SHIP` | "shipment preparation is complete and the shipment is ready to be shipped." |
| `RECEIVING` | "the fulfillment center is receiving the shipment's contents." |
| `SHIPPED` | "the shipment was dropped off at (or picked up by) a carrier." |
| `UNCONFIRMED` | "A tentative shipment exists, but it is still in the planning stage." |
| `WORKING` | "The initial status of a shipment once created." |

B3. Shipment status in v0 (`getShipments`): `WORKING` "The shipment was created by the seller, but has not yet
shipped."; `READY_TO_SHIP` "The seller has printed box labels (for Small parcel shipments) or pallet labels (for
Less Than Truckload shipments)." (present in the `ShipmentStatusList` query enum, absent from the `ShipmentStatus`
definition); `SHIPPED` "The shipment was picked up by the carrier."; `IN_TRANSIT` "The carrier has notified the
fulfillment center that it is aware of the shipment."; `DELIVERED` "The shipment was delivered by the carrier to the
fulfillment center."; `CHECKED_IN` "The shipment was checked-in at the receiving dock of the fulfillment center.";
`RECEIVING` "The shipment has arrived at the fulfillment center, but not all items have been marked as received.";
`CLOSED` "The shipment has arrived at the fulfillment center and all items have been marked as received.";
`CANCELLED` "The shipment was cancelled by the seller after the shipment was sent to the fulfillment center.";
`DELETED` "The shipment was cancelled by the seller before the shipment was sent to the fulfillment center.";
`ERROR` "There was an error with the shipment and it was not processed by Amazon." [official]
`fulfillmentInboundV0.json`. v0 has no `ABANDONED`, `MIXED` or `UNCONFIRMED`; v2024-03-20 has no `ERROR`.

B4. **`CLOSED` does not mean fully received.** The v0 model's wording ("all items have been marked as received") is
contradicted by Amazon's seller-facing definition: "Closed: Either we've confirmed all units received in your
shipment, or the shipment has been open for more than 45 days for a domestic shipment or 75 days for an
international shipment." [official] *How to track FBA shipments*, sell.amazon.com,
https://sell.amazon.com/blog/fba-shipment-tracking (published 2025-01-07, modified 2025-10-03), read 2026-11-10.

B5. The seller-facing stages, same page [official]: "Ready to ship: This status automatically updates when you
print labels."; "In transit: Your shipment enters this status when we receive carrier information verifying that the
shipment is being transported."; "Delivered: This status indicates the shipment is ready to arrive at Amazon's
location, or it's at Amazon's location but not yet checked in."; "Checked in: Your shipment enters this status when
it has moved from the facility yard to the dock door and is ready to be unloaded."; "Receiving: Your shipment enters
this status when we scan your first shipment label. Received units are available for sale, but before they're
available for immediate shipping, we might transfer them to other locations for optimal delivery to customers."

B6. No "mark as shipped" in the new API: "You do not need to mark your shipments as shipped in v2024-03-20. Amazon
automatically tracks the shipments based on the carrier and tracking details." [official] migration guide.

B7. Inbound in the inventory summary (`getInventorySummaries`, FBA Inventory v1), from
`fba-inventory-api-model/fbaInventory.json` [official]: `inboundWorkingQuantity` "units in an inbound shipment for
which you have notified Amazon."; `inboundShippedQuantity` "units in an inbound shipment that you have notified
Amazon about and have provided a tracking number."; `inboundReceivingQuantity` "units that have not yet been
received at an Amazon fulfillment center for processing, but are part of an inbound shipment with some units that
have already been received and processed."; `totalQuantity` "The total number of units in an inbound shipment or in
Amazon fulfillment centers." The `startDateTime` filter does not see inbound movement: "Changes in
inboundWorkingQuantity, inboundShippedQuantity and inboundReceivingQuantity are not detected."

B8. Inbound in the reports (*FBA report type values*,
https://developer-docs.amazon/sp-api/docs/report-type-values-fba.md, updatedAt 2026-10-13) [official]:
`GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` carries `afn-inbound-working-quantity`, `afn-inbound-shipped-quantity`,
`afn-inbound-receiving-quantity` ("Content updated in near real-time"). `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`
carries `Inbound`, `Working`, `Shipped`, `Receiving`, `FC transfer`, `FC Processing` and "`Total Days of Supply`
(including units from open shipments)". `GET_FBA_INVENTORY_PLANNING_DATA` carries `inbound-quantity`,
`inbound-working`, `inbound-shipped`, `inbound-received`. The notification `FBA_INVENTORY_AVAILABILITY_CHANGES`
carries an `InboundQuantityBreakdown` ("inbound units, which are either still in `WORKING` status or on the way to be
received in Amazon warehouses"). [official] *Notification type values*.

### C. From shipped to sellable

C1. Amazon states stage windows, not one figure. Posted by an Amazon moderator (Dominic_Amazon, *FBA Receiving
Times*, 2024-08-08, https://sellercentral.amazon.com/seller-forums/discussions/t/3fb02a04-bace-4bcb-9458-a93f0148c613,
read 2026-11-10) [official]:
- Delivered → Checked in: "For small-parcel shipments, it can take up to four days for your shipment to move to
  Checked in status from your scheduled delivery date. For LTL and FTL shipments, it can take up to 10 days. During
  peak times, it may take longer."
- Checked in → Receiving: "For small-parcel shipments, it can take up to two days to move from Checked in status to
  Receiving status. For LTL and FTL shipments, it can take up to nine days. During peak times, it may take longer."
- Receiving: "Units are available for sale as soon as they are received. However, because units may be sent to other
  fulfillment centers closer to customers, it can take up to 18 days for received units to be available for
  immediate shipping."
- "Occasionally, a shipment that has been delivered to the fulfillment center will not display as Delivered. This
  can occur because of information between the carrier and the fulfillment center not syncing."
- "you can only request an investigation once the shipment is closed. In some cases the reconciliation date may be
  extended."
The stage text matches Amazon's help wording; the help page itself was not read.

C2. Amazon gives no service level: "FBA shipment times can vary based on many factors… during high-volume periods,
like holiday seasons or the lead-up to shopping events like Prime Day, it can take longer for shipments to move from
one stage to another… a shipment might be checked in several days after the date it arrives at an Amazon location."
[official] sell.amazon.com tracking page.

C3. Peak. "Our fulfillment center teams focus on receiving holiday shipments in September and October, then shift to
processing customer orders in November and December. So, you may see lower capacity limits during this time."
[official] News_Amazon, *Holiday 2026: Same fees, same eligibility, earlier deadlines*, 2026-07-07,
https://sellercentral.amazon.com/seller-forums/discussions/t/3e31fbb7-04e0-4ed4-873e-f74b1052e2ff, read 2026-11-10.

C4. Delivery window. Introduced in the US from April 24, 2023: "if you use a non-partnered carrier for small parcel
or less-than-truckload shipments, you must provide a delivery window on Send to Amazon. If you use an
Amazon-partnered carrier or Amazon Global Logistics, no action is required, because the carrier will provide us with
shipment arrival information." "we'll ask you to specify a seven-day delivery window for domestic shipments, or a
14-day delivery window for cross-border shipments… you can update the information until the start of your delivery
window". [official] News_Amazon, *New delivery window requirement for FBA shipments*, 2023-04-11,
https://sellercentral.amazon.com/seller-forums/discussions/t/1ecdd7e2db64f05b036f5beb7bb58257. The same requirement
was announced on the Canada forum on 2024-02-06 (start February 9, 2024; thread `4f4ffafc-…`, whose marketplace
field is Canada, not the UK) and on the UK forum on 2024-02-15 with the same seven-day and 14-day lengths (News_Amazon,
*New delivery-window requirement for Fulfilment by Amazon (FBA) shipments*, sellercentral-europe forum
`c1aebd75-9a21-4f0f-986a-9d09e09854d2`). [official]
The API states the same lengths: non-partnered carriers "require you to specify a delivery window of seven days for
domestic shipments or 14 days for international shipments", and "You must schedule your shipment delivery within
**45 days** for domestic shipments and **75 days** for international shipments. These time frames are reflected in
the available delivery window options `endDate`." [official] *Create an inbound shipment*; *Create a shipment with a
non-partnered carrier*, https://developer-docs.amazon/sp-api/docs/create-non-partnered-carrier-shipment.md.
A seller's post of 2025-10-21 quotes a later rule, "Effective September, all shipments both domestic and
international will be required to provide a one calendar week (Sun - Sat) delivery window"; the Amazon moderator's
reply did not contradict it and named a defect: "to avoid missed delivery window defects: Plan 3+ weeks in advance…".
[official, via a seller's post, with an Amazon reply] thread `2e5c056b-…`. **The API guide (14 days international)
and that post (one calendar week for all) disagree**; both recorded.

C5. Arriving inside the window matters to receiving order: "Shipments arriving within their scheduled window will
receive priority processing, while shipments arriving outside of their scheduled delivery windows may face
appointment and receiving delays." [official] *Prime Day readiness playbook* `GM2ADTH3XH3A5N57` v4, local capture
of 2026-10-14. The seller stays answerable even when a carrier updates the window: "you remain responsible for
delivery window performance regardless of automation." [official] Amazon moderator reply, 2026-02, thread
`4d7ef61c-…` (FIST, FBA Inbound Shipment Tracking, carriers).

C6. Partnered against own carrier. "Amazon-partnered carrier shipments are available only in the contiguous United
States. For shipments outside this region, you must use your own carrier." [official] *Create a shipment with an
Amazon-partnered carrier*. (The same documentation set also describes the partnered program in Europe, where the
carrier's and the program's terms must be accepted in Seller Central first or "the service returns an error"; the
"contiguous United States" sentence reads as US-scoped. [official] *Create an inbound shipment*.) With a partnered
carrier Amazon may leave the destination unset: with `destinationType` `AMAZON_OPTIMIZED` "the destination
fulfillment center address may differ from the actual address, or this field may be empty." [official] same page.
Non-partnered LTL/FTL needs a dock appointment booked by the carrier inside the confirmed window; Amazon's forum
guidance for a shipment in transit but already `CLOSED` is to "ask your carrier to visit Carrier Central and confirm
they have a valid and active delivery appointment". [official] Dominic_Amazon, 2024-10, thread `130b5dc4-…`.

C7. Cross-border programs (AGL, Amazon SEND / 亚马逊跨境物流) were not researched at source here; they are
`beyond/programs-and-regions.md`'s. Two facts were met on the way: AGL and partnered carriers supply arrival
information themselves (C4), and the end of US prep services covers inventory arriving through AWD, AGL, Amazon SEND
and Supply Chain Portal (G2).

### D. Automatic closure, and deleted, abandoned and misrouted shipments

D1. History of the closure rule.
- 2020-12-16: "shipments created beginning today will be automatically updated to Closed status if they become more
  than 90 days old… Amazon will continue to receive shipments that are already in transit. You cannot ship
  additional units for a closed shipment." [official] News_Amazon, *Update to FBA shipment closure timelines*,
  thread `6fef45de7219073fea69f637c32c62f6`.
- From **February 1, 2024** (US): shipments are closed automatically when they have not arrived: "Domestic shipments
  from US addresses that haven't arrived within 45 days after the shipment creation date; International shipments
  that originate from outside the US that haven't arrived within 75 days after the shipment creation date; Shipments
  in a multiple-destination shipping plan must arrive within 30 days after the first shipment in that plan has
  arrived. Shipments are considered arrived once the shipment status changes to in-transit, checked-in, delivered,
  or receiving. Shipments with the statuses of working, ready to ship, and shipped are subject to the automatic
  closure policy… We'll exempt shipments that are delayed due to unforeseen circumstances, such as weather or port
  congestion". [official] News_Amazon, *Automatic closure policy for FBA shipments will be updated on February 1*,
  2024-01-11 (updated 2024-01-16), thread `ef22088c-…`.
- Peak 2024, temporary (US): "effective immediately… Extended automatic closure window to 90 days for shipments
  created after August 7, through October 31, 2024… Extended abandoned shipments window from 30 days to 45 days from
  first receive for shipments created between August 7 and October 31, 2024." Amazon gave its reason: "High demand
  has led to longer receive times at some of our West Coast inbound locations and for palletized freight."
  [official] News_Amazon, *Updates to support US FBA peak inventory shipments*, 2024-10-24, thread
  `4ade7ec5-b16e-4ee3-b669-45cdcc0b97a5`, read 2026-11-10 (gap fill 2026-11-10).
- Peak 2026, temporary (US forum; **international** shipment plans created between August 1 and November 30, 2026):
  "We've extended the window for related shipments to arrive after the first shipment in a multi-destination plan is
  received from 30 to 45 days. You won't be charged the deleted or abandoned defect fee as long as your remaining
  shipments are received within 45 days of the first receive. We've extended the automatic shipment closure window
  to 90 days… The defect will still be flagged on your Inbound Performance Dashboard but the fee is waived for
  eligible shipments… Any inbound defect fees already charged on eligible shipments will be reimbursed. Go to your
  Reimbursement report to view details. No action is required." [official] News_Amazon, *Temporary peak season
  extensions for international FBA shipments*, 2026-10-30, thread `f25ba535-e06e-4fa3-8bb0-cb3a095fd696`, read
  2026-11-10 (the verifier found Amazon's post; the research seat had it through AMZ123,
  https://www.amz123.com/t/9rC7BjAH, whose Chinese summary matches). The post names no domestic plans. Sellers
  replying on 2026-11-02 report plans created in July 2026 falling outside it. [opinion: sellers in that thread]

D2. What a closed-while-travelling shipment faces. Amazon's 2020 text says in-transit shipments are still received.
A seller's report of 2026-01-27 describes the opposite under the 2024 rule: an international shipment delivered 8
days after day 75 was marked `ABANDONED` and "the receiving dock cannot/will not scan the pallets"; the Amazon reply
only pointed to the help pages *Deleted, misrouted, and incomplete shipments* and *Missing inbound FBA inventory*.
[opinion: a seller on the Seller Forums; Amazon reply official] thread `c5388f8d-…`. Between the two stands an
Amazon moderator's statement of 2024-11-18 (C6): a shipment in transit but already `CLOSED` can be received if the
carrier holds "a valid and active delivery appointment"; "If the dock appointment is invalid and delivery fails,
contact your carrier to return the shipment. Once returned, you will need to recreate the shipment and relabel the
shipping boxes with new FBA box ID labels". [official] Dominic_Amazon, thread `130b5dc4-…`, read 2026-11-10.

D3. Abandoning part of a plan. "when your shipping plan includes multiple shipments, you must create and send all of
those shipments. If you ignore, delete, or abandon any shipment in the plan, it will generate an abandoned shipment
defect. These defects are subject to inbound defect fees. Additionally… the FBA inbound placement service fee will
be recalculated. If you had an Amazon-optimized shipping plan but only completed one shipment, you'll be charged the
Minimal shipment splits rate… If you're using a third-party integration, reach out to the provider, as they may be
abandoning shipments on your behalf without your knowledge!" [official] Bryce_Amazon, *Sailing Smoothly: Avoid
Abandoned Shipment Fees on Amazon*, 2024-06-27, thread `8eb6e29c-…`.

D4. The 2026 change. The listing playbook quotes the 2026 US fee summary (`G201411300` v47, read 2026-10-14, not
re-read): "A single inbound defect fee replaced the double charge", effective January 15, 2026. Amazon's
announcement of 2025-10-15 gives the frame: "There will be no new FBA fee types in 2026… Unless otherwise noted, all
changes will be effective January 15, 2026." [official] News_Amazon, *2026 Updates to US Referral and Fulfillment by
Amazon Fees*, thread `f3fa3211-…`. The rate table is `areas/holding-costs.md`'s; the help page *Inbound defect fees*
(`GL5XA3MNXAJKJE8E`) was not read.

D5. The Inbound Performance report is `GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA`: "Contains inbound shipment
problems by product and shipment. Content updated daily." Columns: `issue-reported-date`, `shipment-creation-date`,
`fba-shipment-id`, `fba-carton-id`, `fulfillment-center-id`, `sku`, `fnsku`, `asin`, `product-name`, `problem-type`,
`problem-quantity`, `expected-quantity`, `received-quantity`, `performance-measurement-unit`, `coaching-level`,
`fee-type`, `currency`, `fee-total`, `problem-level`, `alert-status`. [official] *FBA report type values*.

D6. Unprepared or unlabelled arrivals: "Inventory that arrives at a fulfillment center without proper preparation or
labeling might incur a preparation fee" (*Unplanned services*). Not supplying box contents: "there may be defects in
the receiving process and fees for manual processing" (*FBA manual processing fee*, `G202061550`). [official]
*Additional functionality*; *Create an inbound shipment*. Neither help page was read.

### E. Inbound placement

E1. The fee was announced on 2023-12-05: "We will introduce an inbound placement service fee for standard and Large
Bulky-sized products to reflect our cost of distributing inventory to fulfillment centers close to customers. These
fees will average $0.27 per unit for standard-sized products and $1.58 per unit for Large Bulky-sized products…
These fees will be effective starting March 1, 2024, and the fees will be charged 45 days after products are
received." [official] News_Amazon, *Update to US referral and Fulfillment by Amazon fees*, thread `ce3a1455-…`.

E2. The options, as an Amazon moderator restated the help page (2024-11, thread `5d437c4b-…`) [official]: "Minimal
shipment splits: You can send your inventory to the minimal number of inbound locations, generally to a single
location, for a fee… The fee may vary by inbound location—for example, there may be higher fees for shipments sent
to locations in the West… Partial or Amazon-optimized shipment splits: Send your inventory to multiple inbound
locations yourself for a reduced or no fee… To qualify for the Amazon-optimized inbound option with no inbound fee,
your shipments must include at least five identical cartons or pallets per item. Each carton or pallet must contain
the same quantity per item and the same item mix… You'll be charged the FBA inbound placement service fee 45 days
after your shipment is received, based on the inbound location and the quantities received." The same reply names
where the charge is seen: Payments, Transaction view, Service fees, with the shipment ID under Order ID; and a
downloadable *FBA inbound placement service fee* report at shipping plan, shipment and SKU level. The listing
playbook's read of `GC3Q44PBK8BXQW3Z` v16 (2026-10-14, not re-read) agrees and adds that the fee "doesn't apply to
Extra-Large products" and that partial splits are for Bulky only.

E3. Partial splits: "As of **February 20, 2025**, partial shipment splits are not available on the Send to Amazon
workflow for standard-sized products. Partial shipment splits remain available for large products." [official]
*Create an inbound shipment*.

E4. In the API a placement option carries its own `fees` and `discounts` (`Incentive`: `target` 'Placement Services'
or 'Fulfillment Fee Discount'; `type` `FEE` or `DISCOUNT`), a `status` (`OFFERED`, `ACCEPTED`, `EXPIRED`), an
`expiration` and its `shipmentIds`. [official] model. The amounts are quoted, not tabulated: "Each option can
include fees or discounts determined by an algorithm during shipment creation, not calculated using set rates. The
algorithm for the rebate value and the ship-to location uses multiple factors… including expected volume, the
availability of carrier appointments, and fulfillment speed." Options generated before box contents are known "can
differ from the placement options that are generated after you provide box content information". [official] *Create
an inbound shipment*.

E5. Permanence. `confirmPlacementOption`: "Once confirmed, it cannot be changed for the Inbound Plan." [official]
model. "This option cannot be reversed after it is selected." [official] *Create an inbound shipment*.

E6. The placement choice moves the peak arrive-by date by a week (see H). The amount moved in 2026: a 3PL's blog
says standard-size minimal-split fees "rose about $0.05 per unit on average" on January 15, 2026. [opinion] AMZ
Prep, https://amzprep.com/amazon-inbound-placement-fees/. The live figure for a given plan is the option's `fees`.

E7. Outside the US: no Amazon source for an inbound placement fee in the EU, UK or Japan was found in this session.
What the API guide does state for Europe is an Amazon-recommended **packing** option carrying a fulfilment discount
for small-parcel boxes under 15 kg in Spain, the UK, France, Germany and Italy (help `GV6GL3KJRDPT8TNY` on
`.co.uk`, not read). [official] *Fulfillment Inbound API* guide. Open.

### F. Reconciliation of shipped against received

F1. The flow, sell.amazon.com tracking page [official]: the Contents tab of the Shipment summary "will display the
difference between expected units and units located"; "Once the shipment status is "Closed," eligible products will
have an Action required dropdown menu"; the choices are to "confirm you sent a different number of units… or request
that we research the difference", with "proof of inventory ownership and proof of delivery"; requests for more
information are to be answered "within five business days". Not eligible when: "The shipment is still being
processed or hasn't arrived at Amazon's location. The receiving stage is pending confirmation on final unit counts.
The shipment contents have been received in full or are already reconciled."

F2. Timing of the research, from an Amazon moderator (Christine_Amazon, *How to Resolve FBA Shipment Discrepancies*,
2025-11-14, thread `83caf79b-…`) [official]: "Typically, this process takes anywhere from 2 to 30 days, though in
some cases it can extend up to 60 days… not all discrepancies result in reimbursement." Documents named: invoices
(date, quantity, issuer and purchaser name and address) or, for a manufacturer, a signed packing slip.

F3. The claim window for units missing from an inbound shipment. **The statements differ by store; for the US every
Amazon statement read says nine months.** (Rewritten by the verifier, 2026-11-10: the 15–60 day statement was posted
to the United Arab Emirates forum, not the US one. Each thread's store is the `marketplaceId` in the page's own data:
`ATVPDKIKX0DER` US, `A2VIGQ35RCS4UG` UAE, `A1F83G8C2ARO7P` UK, `A39IBJ37TRP1C6` Australia, `A2EUQ1WTGCTBG2` Canada.)
- US, Amazon's own page, read first-hand 2026-11-10: "Once a shipment is shown as eligible for investigation in the
  Status column on the Contents tab of the Summary page in your shipping workflow, you can file a claim. You must
  submit your claim no later than nine months after the verified date of a shipment delivery to an Amazon
  fulfillment center or to a third-party facility operated on Amazon's behalf. Claims submitted outside of this
  window are not eligible for reimbursement." And, under fulfilment-centre claims: "The inventory reimbursement
  policy for the eligibility claim windows, except for shipment to Amazon claims, is 60 days." [official] Amazon
  Supply Chain, *Reimbursements* support page, https://supplychain.amazon.com/support/reimbursements (footer © 2026
  Amazon.com Services LLC; the page carries no revision date, and its removal window still reads 15–75 days, so it
  may predate a later change to removals). (gap fill 2026-11-10)
- US, News_Amazon, 2024-07-24, thread `81c3235d-4c44-47ba-96c5-883cecab3244`: the eligibility windows effective
  October 23, 2024 cover fulfilment-centre operations claims (60 days), customer returns (60–120 days), removals
  lost in transit (15–75 days from shipment creation) and other removals (60 days). **It lists no window for
  shipments to Amazon**; a seller's question in the thread whether "lost in transit" means inbound got no Amazon
  answer in the posts read. [official] (gap fill 2026-11-10)
- US, a seller's post of 2024-09-26 quotes the policy page (`GEYPWTSQRTXXXMVB`) as "nine months after the verified
  delivery date"; the Amazon moderator's reply (Dominic_Amazon, 2024-09-27) did not dispute the figure. [official,
  via a seller's post] thread `2b32f5d5-…`.
- US, an Amazon moderator, 2026-08-13: "Shipment to Amazon (MFI) claims: File after your shipment is closed/finalized
  (allow time for reconciliation) and within 9 months". [official] Indy_Amazon, *FBA Lost Your Inventory? Steps to
  File a Reimbursement Claim*, thread `0e07abc1-…`. The post does not say what the nine months run from; the
  supply-chain page and the seller's quotation say the verified delivery date.
- **UAE**, News_Amazon, 2024-08-06, effective September 5, 2024: "Units missing from shipments sent to Amazon
  fulfillment centers: No sooner than 15 calendar days from the shipment delivery date but no later than 60 calendar
  days." [official] *Update on reimbursement claim window eligibility on FBA*, thread `96a05f4a-…` (marketplace
  field UAE; the page shows no other store for it).
- **Australia** forum, News_Amazon, 2025-08-14, effective October 15, 2025: lost or damaged items (60 days),
  customer returns (45–105 days), removals lost (15–135 days from shipment creation), removals damaged and grading
  (120 days), re-evaluation (90 days). It lists no window for shipments to Amazon. [official] thread `d8f9a56c-…`.
  Whether the same list was issued for the US was not established.
No Amazon statement read gives a 15–60 day inbound window for the US. The Seller Central policy page itself was not
read. The live answer for a shipment is the eligibility Seller Central shows on it (the Contents tab's Status
column and the Action required menu).

F4. Automatic reimbursement announced so far covers loss inside fulfilment centres, not inbound shortfalls:
"Starting January 15, 2025, we'll proactively reimburse you for Fulfilment by Amazon (FBA) items that are lost in
our fulfilment centres… if you do not receive an automatic reimbursement and you believe that your inventory has
been lost or damaged, you will need to file a manual claim." [official] News_Amazon, 2024-10-10, thread `d0fc997e-…`,
which is the UK forum's text. The US text, read first-hand: "Starting November 1, 2024, we'll proactively reimburse
you for Fulfillment by Amazon (FBA) items that are lost in our fulfillment centers… if you do not receive an automatic
reimbursement and you believe that your inventory has been lost or damaged, you will need to file a manual claim."
[official] News_Amazon, 2024-07-24, thread `81c3235d-…`, read 2026-11-10.

F5. Valuation. "Effective March 10, 2025, we'll reimburse you based on the product manufacturing cost of the
affected inventory… It excludes costs such as shipping, handling, customs duties, or other costs." [official]
News_Amazon, 2024-12-18, thread `a941ac02-…` (the UK forum's text; the US announcement was not opened). For the US:
"For shipment to Amazon claims, removals claims, and fulfillment
center operations claims that occur before fulfillment, we will reimburse you the sourcing cost of the item."
[official] Indy_Amazon, 2026-08-13.

F6. Labels decide eligibility: "if Amazon determines that the units were not included in the shipment you would not
be eligible for reimbursement. This could be from box or product labeling issues which would cause the units to not
be properly tied to the shipment." [official] Amazon moderator reply, 2025-12, thread `bb14816c-…`. After January 1,
2026 a third party reports Amazon's notice that US shipments arriving without proper prep or labelling are not
eligible for reimbursement if lost or damaged. [snippet]

F7. The ledger side. `GET_LEDGER_DETAIL_VIEW_DATA` "analyze[s] your inventory movements to and from Amazon
fulfillment centers… You can view all historical movements of your inventory for 18 months"; it filters on
`eventType` `Receipts` (also `Adjustments`, `CustomerReturns`, `Shipments`, `VendorReturns`, `WhseTransfers`) and
carries `Reference ID`, `Quantity`, `Fulfillment Center`, `Disposition`, `Reason`, `Reconciled Quantity`,
`Unreconciled Quantity`. `GET_LEDGER_SUMMARY_VIEW_DATA` carries `Receipts`, `In Transit Between Warehouses`,
`Warehouse Transfer In/Out`, `Found`, `Lost`, and aggregates by `COUNTRY` or `FC` and by day, week or month.
`GET_FBA_REIMBURSEMENTS_DATA` ("Content updated daily") carries `reason`, `case-id`, `amount-per-unit`,
`quantity-reimbursed-cash`, `quantity-reimbursed-inventory`. [official] *FBA report type values*.

### G. What constrains an inbound at creation

G1. Plan size: "For one inbound plan, you can add a maximum of 1,500 SKUs and a maximum of 10,000 items for each
SKU." [official] FAQ.

G2. Prep and labels in the US. "Starting **January 1, 2026**, prep and item labeling services for Fulfillment by
Amazon (FBA) shipments will no longer be available in the US marketplace. This change applies to all inventory that
is sent to the US FBA service", including through AWD, AGL, Amazon SEND and Supply Chain Portal; "`AMAZON` will no
longer be an accepted value for `prepOwner` or `labelOwner` across all Fulfillment Inbound API operations in the US
marketplace." [official] SP-API changelog, *US FBA prep and labeling services to end January 1, 2026*,
https://developer-docs.amazon/sp-api/changelog/us-fba-prep-and-labeling-services-to-end-january-1-2026.md. The model
repeats it on `LabelOwner` and `PrepOwner`, and on AWD's (`AMAZON`/`SELF`). A third party gives July 1, 2026 for
Canada. [snippet]

G3. Prep details. "You must call the `setPrepDetails` operation in order to retrieve prep details with the
`listPrepDetails` operation. Prep details you add in Seller Central are not returned by `listPrepDetails`."
[official] guide. The migration guide says the opposite direction: "`PrepDetailList` is not available as an input.
The seller must enter the prep category in Seller Central in advance for each SKU." [official] Both stand on pages
of the same date. `MskuPrepDetail` returns the owner constraints (`AMAZON_ONLY`, `NONE_ONLY`, `SELLER_ONLY`;
`MUST_MATCH`). [official] model.

G4. Expiration and lot. "Multiple expiration dates per SKU on a single inbound plan are not supported. To send a SKU
with multiple expiration dates to the fulfillment network, you must create multiple plans." [official] *Create an
inbound shipment*; FAQ. `Item.expiration`: "The same MSKU with different expiration dates cannot go into the same
box." [official] model.

G5. Eligibility per ASIN: `getItemEligibilityPreview` (FBA Inbound Eligibility v1) returns `isEligibleForProgram`
and `ineligibilityReasonList` for one `asin`, a `program` (`INBOUND` or `COMMINGLING`) and, for `INBOUND`,
`marketplaceIds`. It answers for the ASIN, not for a quantity or for capacity. Reason codes with a stock meaning,
from the model [official]: `FBA_INB_0004` missing package dimensions; `0007`–`0014` dangerous-goods review states
("The review process takes 4 business days"; `0014` "generally takes 4 - 7 business days"); `0015` regulated,
unfulfillable, Amazon "will need to dispose"; `0016` fulfillable dangerous good that may need the FBA dangerous
goods program; `0017` not in the destination catalogue; `0035` expiration-dated or lot-controlled, needs labelling;
`0037` missing tax documents ("up to 48 hours"); `0050` no fulfilment centre in the destination country can receive
it; `0051` "blocked by FBA"; `0053` too large or heavy; `0068` account not set up for expiration-dated products;
`0095` barcode tied to more than one product; `0097` fully regulated dangerous good; `0098` not authorised in the
destination marketplace; `0104` requires a manufacturer barcode; `0197` safety or compliance documents; `0342` and
`0465` (added 2024-08-14 and 2026-04-01) manufacturer-barcode ineligibility. Dangerous goods also shape packing:
"SKUs that are classified as dangerous goods cannot be packed with other SKUs, because dangerous goods SKUs are
shipped to special fulfillment centers". [official] *Create an inbound shipment*.

G6. Capacity. From the listing playbook's read of *FBA capacity limits* (`GAFNWEYTJUV2GBFC` v22, 2026-10-14, not
re-read): "If your on-hand inventory plus shipments on the way to our fulfillment centers exceeds your capacity
limit, you'll be blocked from creating new shipments to Amazon."; "Open shipments count toward your total capacity
usage". Amazon in October 2026: "AWD-replenished inventory bypasses FBA capacity limits during peak". [official]
Indy_Amazon, *BFCM 2026*, 2026-10-14, thread `6a6f3b4a-…`. No SP-API operation or report in the files read returns
the capacity limit; the guides' capacity text is in Seller Central (Capacity Monitor, Capacity Manager).

G7. Box and pallet limits: the FAQ points to *Small-parcel delivery to Amazon* (`G200280260`) and *Pallets (LTL/FTL)
delivery* (`G200978400`); neither was read. The model warns that "Non-standard minimum and maximum box weights might
be enforced." Without carton-level information only LTL/FTL can be created. [official] FAQ; model.

G8. Editing after confirmation: possible "after you confirm transportation options and before the shipment is in
Receiving status… you can edit the number of units in a shipment by up to five percent or six units per SKU per
shipment, whichever is greater. You can also remove a SKU from a shipment, as long as the original quantity is six
units or fewer… You can't remove all SKUs". [official] *Additional functionality*.

G9. New-ASIN quantity limits, restricted fulfilment centres and hazmat storage limits were not found in any page
read in this session. Open.

### H. Peak arrive-by dates

Amazon publishes arrival dates, not ship dates, and ties them to the placement option.

| Event | AWD | FBA, minimal splits | FBA, Amazon-optimized splits | Source |
|---|---|---|---|---|
| Prime Day 2026 (June) | May 27, 2026 | May 27, 2026 | June 5, 2026 | [official] News_Amazon 2026-04-29, thread `59a5cd20-…`; same in playbook `GM2ADTH3XH3A5N57` v4 |
| Prime Big Deal Days 2026 | September 2 | September 9 | September 16 | [official] News_Amazon 2026-07-07, thread `3e31fbb7-…` |
| Black Friday Week / Cyber Monday 2026 | October 14 | October 21 | October 28 | [official] same; repeated by Indy_Amazon 2026-10-14 |
| Black Friday / Cyber Monday 2025 | October 9 [opinion: PPC Land] | October 20 [opinion: PPC Land] | **October 30, 2025** [official] Indy_Amazon 2025-10-22, thread `b93d7dfa-…` | as marked |
| Prime Big Deal Days 2025 | August 29 [opinion] | September 10 [opinion] | September 19 [opinion] | PPC Land, citing Forest Shipping |

"While we'll continue to receive inventory after these dates, late arrivals may not be processed in time for Prime
eligibility." [official] News_Amazon 2026-04-29. The Holiday 2026 post (2026-07-07) adds "(most sellers select this option)" beside
the Amazon-optimized dates; the Prime Day post does not. For 2025 Amazon's own sentence read is "October 30th, 2025
is your FBA "Amazon-optimized shipment splits" cutoff" (Indy_Amazon, 2025-10-22). The Prime Day playbook: "we recommend that you schedule your delivery appointment at least 7
days before the dates listed above." [official] capture of 2026-10-14. No Amazon text for a Christmas arrive-by date
(2025 or 2026), nor for EU, UK or Japan dates, was found; third-party calendars give December dates that disagree
with each other. [snippet] Open.

### I. AWD inbound and AWD → FBA

I1. The AWD API (v2024-05-09) is a separate role: Role Mappings lists eleven operations under **Amazon Warehousing
and Distribution**, region NA: `getInboundShipment`, `listInboundShipments`, `listInventory`, `createInbound`,
`getInbound`, `updateInbound`, `cancelInbound`, `confirmInbound`, `getInboundShipmentLabels`,
`updateInboundShipmentTransportDetails`, `checkInboundEligibility`. The model has 21 operations: it also defines
`getLabelPageTypes` and outbound and
replenishment operations (`listOutbounds`, `createOutbound`, `getOutbound`, `updateOutbound`, `confirmOutbound`,
`listReplenishmentOrders`, `createReplenishmentOrder`, `getReplenishmentOrder`, `confirmReplenishmentOrder`), which
**Role Mappings does not list**. [official] *Role Mappings for SP-API Operations*,
https://developer-docs.amazon/sp-api/docs/role-mappings.md, read 2026-11-10; model `awd_2024-05-09.json`.

I2. What the AWD reads carry is listed under *Reads that need a role outside the five*.

### J. The writes the Amazon Fulfillment role carries, as facts

J1. Shape. "All POST operations in the new flow are asynchronous": each returns an `operationId`, read with
`getInboundOperationStatus` (`SUCCESS`, `FAILED`, `IN_PROGRESS`; problems of severity `WARNING` or `ERROR`;
"Non-blocking errors are warnings that can be ignored"). Options follow generate → list → confirm:
`generatePackingOptions` / `listPackingOptions` / `confirmPackingOption`; `generatePlacementOptions` /
`listPlacementOptions` / `confirmPlacementOption`; `generateTransportationOptions` / `listTransportationOptions` /
`confirmTransportationOptions`; `generateDeliveryWindowOptions` / `listDeliveryWindowOptions` /
`confirmDeliveryWindowOptions`; `generateShipmentContentUpdatePreviews` / `listShipmentContentUpdatePreviews` /
`confirmShipmentContentUpdatePreview`. [official] migration guide; model. Every one needs **Amazon Fulfillment**.

J2. Permanent: `confirmPlacementOption` (E5). `confirmTransportationOptions`: "Once confirmed, new transportation
options can not be generated or confirmed for the Inbound Plan." `confirmDeliveryWindowOptions`: "Once confirmed,
new delivery window options cannot be generated, but the chosen delivery window option can be updated before
shipment closure." `updateShipmentSourceAddress` "can only be updated prior to the confirmation of the shipment
carriers" and invalidates existing transportation options. [official] model.

J3. Charging. For a partnered carrier, `confirmTransportationOptions` "confirms that you accept the Amazon-partnered
shipping estimate, agree to allow Amazon to charge your account for the shipping cost, and request that the
Amazon-partnered carrier ship the inbound shipment." "You can void Small parcel shipment requests within 24 hours of
confirmation. For Less than truckload / Full Truckload (LTL/FTL) shipments, you have one hour… After these time
periods expire, your account is charged for the shipping cost." [official] *Create an inbound shipment*.
`cancelInboundPlan` cancels the plan and all its shipments and "also cancels the fees associated with the
transportation options… if this operation is called within the void window". "The charge restrictions don't apply
for non-partnered carrier options." [official] *Additional functionality*; FAQ. A quote carries its own
`voidableUntil` and `expiration`; "Expiry date and void window are only returned for transportation options that are
confirmed". `BoxContentInformationSource` `MANUAL_PROCESS`: "This service incurs charges." Confirming a content
update preview accepts "the changes in transportation costs". The placement fee is not charged at confirmation but
45 days after receipt (E2). [official] model; guide; FAQ.

J4. Expiry. Packing, placement and delivery-window options expire (`expiration`, `validUntil`); "Call the
`generatePlacementOptions` operation to regenerate placement options when they expire." Editing box contents after
placement options were generated requires generating them again before confirming. [official] *Create an inbound
shipment*.

J5. Order constraints Amazon states: a placement option must be confirmed before transportation options are
confirmed; a transportation option whose `preconditions` include `CONFIRMED_DELIVERY_WINDOW` (the guides call the
program `DELIVERY_WINDOW_REQUIRED`) needs a confirmed delivery window first; "You must confirm a transportation
option before printing labels, even for non Amazon-partnered transportation."; with several small-parcel shipments
in one plan, "ensure that all shipments use the same carrier"; LTL options are not generated without pallet
information. [official] model; migration guide; partnered-carrier tutorial.

J6. Carton contents. The feed `POST_FBA_INBOUND_CARTON_CONTENTS` still appears in *Fulfillment by Amazon feed type
values* (role Amazon Fulfillment) while the migration guide says it is replaced by `setPackingInformation`.
[official] both pages.

J7. Amazon's own agent skill (`fba-inbound-management`, v1.0.0, Apache-2.0, local copy). Stated there as fact and
confirmed above: placement confirmation is permanent; void windows 24 hours (small parcel) and 1 hour (LTL);
non-partnered carriers need a confirmed delivery window; `getLabels` takes the `shipmentConfirmationId`; from
January 1, 2026 US sellers prep and label themselves; one expiration date per SKU per plan. Stated there and **not
found in, or contradicted by, Amazon's documentation**: "500K units per SKU" per plan (the FAQ says 10,000 items per
SKU and 1,500 SKUs); "V0 shipments not accessible / Only plans created with the v2024-03-20 flow are visible" (the
guide and FAQ say STA plans are readable); packing groups expiring in "24–72h" and a partnered LTL freight-ready
date "within 2 weeks" (no figure in the model or guides read; the live value is the option's `expiration`). Names it
uses, checked against every JSON model at `db2936aa`: the operation `updateBoxIdentifiers` and the field
`readyToShipDate` exist in no model; `shipFromAddress` exists only in the Merchant Fulfillment, Shipping and Orders
models, not in Fulfillment Inbound (whose `generateTransportationOptions` takes `readyToShipWindow`, and whose
ship-from is the plan's `sourceAddress`); and, in its `stockout-prevention` skill per the survey,
`estimatedDeliveryWindow` (`skills/stockout-prevention/SKILL.md` lines 97 and 101), which is in no model (the
Fulfillment Inbound model has `selectedDeliveryWindow` on a shipment). The limits are in
`skills/fba-inbound-management/references/tools-and-additional.md`: "500K units per SKU | Max per inbound plan" and
"V0 shipments not accessible | Only v2024-03-20 plans are visible". Its own
gates (a fixed step order, a typed `CONFIRM`, a polling cap) are its design, not Amazon's rules.

## What practitioners add

P1. **Receiving allowances are a named line in every tool's lead time.** 积加 (Gerpgo): "目标库存天数 = 备货计划
与审批时间 + 采购交期 + 质检时间 + 物流方式(天) + 入库处理天数 + … + 安全库存天数 + 补货周期" (target cover =
approval + supplier lead + QC + freight days + receiving days + … + safety days + cycle), default 入库处理天数
(receiving days) 3. SoStocked defaults warehouse-to-Amazon transfer to 10 days. Sellerboard splits lead time into
manufacturing, to prep centre, to FBA and "an FBA check-in buffer". eComEngine (RestockPro) lists "Receiving and
check-in time" as a lead-time part. [opinion] the survey's `03-tools-en.md` and `03-tools-cn.md`, read 2026-11-09 by
the survey seat, not re-read at the vendors' pages.

P2. **Reported receiving durations, with dates.** My Amazon Guy (2026-04-20): Amazon "publishes a separate window
for each shipment status, and the windows… stack on top of each other"; "units can take up to 18 days to become
available after receiving starts, even when nothing has gone wrong"; during a backlog a case "will come back with a
wait instruction"; "sending smaller parcel shipments can get the inventory checked in faster". [opinion]
https://myamazonguy.com/logistics/fix-amazon-receiving-delays/. SupplyKick: "A shipment that should take three to
five days can sit in receiving status for two weeks or longer"; in Q4 "three or four weeks"; its own practice "ship
at least three weeks earlier for LTL and two weeks earlier for parcel… add an extra week" before Q4 or Prime Day; it
attributes to Amazon "up to 30 days from the time they're received at the loading dock to when all units become
available" (no Amazon page found for the 30 days). [opinion]
https://www.supplykick.com/blog/amazon-fba-processing-times. AMZ Prep restates Amazon's 4+2 and 10+9 day windows.
[opinion] https://amzprep.com/shipping-delays/. Other planners' buffers seen only in search results: 10–14 days,
21 days in Q4. [snippet]

P3. **Chinese sellers on 上架慢 (slow to shelf).** AMZ123 Q&A (2024): "快的2天就上架，慢的，有半个月都没上架的"
(fast ones are on the shelf in 2 days, slow ones are still not after half a month). [snippet] AMZ123 (2026-04):
"货到了却进不了仓：贴标没贴对、送达时段或仓库地址对不上，上架一拖就是一两周" (the goods arrive but cannot enter:
wrong labels, a missed delivery window or the wrong warehouse address, and shelving slips a week or two). [snippet]

P4. **The inbound defect fee is treated as newly material from January 15, 2026.** AMZ123 (2025-11-09): "对于重量
不超过 16 盎司的商品，入库缺陷费将从 0.04 美元暴涨至 0.32 美元" (for items up to 16 oz the inbound defect fee
goes from $0.04 to $0.32), and lists the triggers: misrouted, deleted or missing after plan approval, incomplete,
domestic not arrived in 45 days, international in 75, and "多目的地入库延迟…其他货件在 30 天内未送达" (in a
multi-destination plan, other shipments not arriving within 30 days of the first). [opinion]
https://www.amz123.com/t/3PEcbbvv. English blogs give other ranges ($0.32–$5.72; "averages $0.60 per unit").
[snippet] The rate is `areas/holding-costs.md`'s to establish.

P5. **Sellers report being charged both fees, and defects on shipments delivered in time.** Seller Forums threads of
2025-06 to 2026-04 (`d06cf5f9-…`, `7940364d-…`, `e102af8a-…`, `b37b0d23-…`). Amazon's reply in the first: the
30-day window "is in place to support efficient inventory management"; for customs holds or port congestion
"exceptions may be granted when the circumstances are clearly documented". [opinion: sellers; the reply official]

P6. **What tools do with inbound, and what they say the API lacks.** 积加 creates, views and edits STA shipments
through the API; "一旦点击"货件预览"，此时就会提交给亚马逊" (clicking preview submits to Amazon) and "两次预览
结果有可能会存在差异" (two previews may differ); "目前仅支持"非亚马逊合作承运人"，不支持"AGL"、"亚马逊合作承运
人"(亚马逊未提供API)" (only non-partnered carriers; AGL and partnered carriers unsupported, "Amazon provides no
API"). The partnered-carrier claim is at odds with Amazon's own tutorial for partnered shipments through
v2024-03-20; it may describe the tool's date or region. 领星: "FBA货件：货件中的数据是从亚马逊的shipment获取的
数据" (shipment data is taken from Amazon's shipment), in-transit taken from shipments of the last 6 months. 赛狐
creates shipments "使用新版API接口" (with the new API) and counts AWD in-transit from statuses SHIPPED, IN_TRANSIT,
DELIVERED, CHECKED_IN, RECEIVING. SoStocked "does not directly create FBA shipments in Amazon"; RestockPro is
file-based. 积加 pulls capacity from Seller Central pages four times a day, not from an API. [opinion] the survey's
tool notes, not re-read.

P7. **Reconciliation practice.** Sellers on the forums report capturing the expected-against-located view before it
changes and filing with an invoice and packing slip; a recurring complaint is the Action required menu never
appearing after an automatic closure. [snippet] ConnectBooks' help notes a closed shipment can take up to 24 hours
to appear in its data. [snippet]

P8. **Peak.** EcomCrew (2026-07-07) on the 2026 dates: "Treat these as hard stops, not targets." PPC Land reads the
option as a trade: sellers who choose minimal splits "trade that convenience for a week less runway". [opinion]

## Published research

None found on FBA receiving times, placement or inbound loss as sellers meet them. One adjacent work
(gap fill 2026-11-10): Michael Chun, *Improving inbound visibility through shipment arrival modeling*, MIT thesis,
2014, https://dspace.mit.edu/handle/1721.1/90779 (abstract read 2026-11-10): for Amazon's own vendor purchase
orders, "Although estimated delivery dates are routinely received for each of these inbound shipments, only about
half of the purchase orders actually arrives by these dates." [research] It concerns retail (vendor) inbound in
2014, not FBA sellers' shipments. A survey figure seen only in a search result (Pattern, *2025 State of Fulfillment
Report*: "41% reporting 3–4 week receiving times") was not opened. [snippet] The general literature on lead-time
variability and safety stock belongs to `areas/restock-and-forecast.md`.

## Stable enough for a skill

- The two generations and which read carries what: status and options in v2024-03-20, received quantity in v0 only
  (A3–A5).
- The status vocabulary and Amazon's definitions, including that `CLOSED` is also a timeout (B2–B5).
- STA plans are readable by the API after placement and transportation are confirmed (A6).
- The three inbound quantities of `getInventorySummaries` and their report twins (B7, B8).
- Amazon's stage windows as Amazon's statement, dated 2024-08-08, with "During peak times, it may take longer" (C1).
- The closure rule as a dated rule with its history (D1), and that abandoning part of a plan re-prices placement (D3).
- Placement confirmation is permanent; the fee is charged 45 days after receipt on quantities received (E2, E5).
- The US claim window for inbound shortfalls as Amazon states it (nine months from verified delivery), with the
  other stores' differing statements kept apart (F3).
- Plan size, one expiration date per SKU per plan, US prep ownership since 2026-01-01 (G1, G2, G4).
- Peak dates are arrival dates and differ by placement option (H).
- The void windows and what each confirmation fixes (J2, J3).

## What cx must read at run time

Roles are from *Role Mappings for SP-API Operations* and *for SP-API Types*, and from *FBA report type values*,
read 2026-11-10. AF = Amazon Fulfillment, PL = Product Listing, PR = Pricing.

R1. `listInboundPlans`, then `getInboundPlan` (Fulfillment Inbound v2024-03-20). Fields: `status`, `shipments`,
`placementOptions`, `packingOptions`, `sourceAddress`, timestamps. **Role: AF.** Model rate 2 requests/s; page size
up to 30; no marketplace filter; follow-up pages need the same filters. Shows STA plans only after their options are
confirmed (A6).

R2. `getShipment`. Fields: `status`, `shipmentConfirmationId`, `destination` (may be empty for `AMAZON_OPTIMIZED`),
`selectedDeliveryWindow` (`startDate`, `endDate`, `availabilityType`, `editableUntil`), `trackingDetails`,
`placementOptionId`, `selectedTransportationOptionId`. **Role: AF.** No received quantity.
`listShipmentItems`, `listShipmentBoxes`, `listShipmentPallets`, `listInboundPlanItems`, `listInboundPlanBoxes`:
what was planned, per shipment or plan; page size up to 1000. **Role: AF.**

R3. `getShipments` (v0), by `ShipmentStatusList`, `ShipmentIdList` or `LastUpdatedAfter`/`Before`, with `QueryType`
and `MarketplaceId` required. Fields: `ShipmentStatus`, `DestinationFulfillmentCenterId`, `ShipmentName`,
`LabelPrepType`, `BoxContentsSource`, `ConfirmedNeedByDate`. **Role: AF.** The ID to pass is the
`shipmentConfirmationId`.

R4. `getShipmentItemsByShipmentId` and `getShipmentItems` (v0). Fields: `SellerSKU`, `FulfillmentNetworkSKU`,
`QuantityShipped`, `QuantityReceived`. **Role: AF.** The only API read of received units per SKU per shipment. The
model gives 2 requests/s, burst 30, for the v0 reads; the release note of June 25, 2025 says `getLabels` and
`getInboundOperationStatus` were raised to five per second. The live rate is the `x-amzn-RateLimit-Limit` response
header.

R5. `listPlacementOptions`, `listTransportationOptions`, `listPackingOptions`, `listDeliveryWindowOptions`. Fields:
`fees`, `discounts`, `status`, `expiration`; `quote.cost`, `quote.voidableUntil`, `quote.expiration`,
`shippingSolution`, `shippingMode`, `preconditions`; `availabilityType`, `validUntil`. **Role: AF.** After
confirmation `listTransportationOptions` returns the one confirmed option, which is how partnered against own
carrier is told (FAQ). Transportation options page at 10, maximum 20. Options exist only after their `generate…`
call, which is a write.

R6. `getInventorySummaries` (FBA Inventory v1) with `details=true`. Fields: `inboundWorkingQuantity`,
`inboundShippedQuantity`, `inboundReceivingQuantity`. **Role: AF or PL.** Pitfall: `startDateTime` does not detect
inbound changes; the three figures are per SKU, not per shipment.

R7. `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA`: `afn-inbound-working-quantity`, `afn-inbound-shipped-quantity`,
`afn-inbound-receiving-quantity`. **Roles: PR or AF.** Near real-time (regenerated at most every 30 minutes).

R8. `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`: `Inbound`, `Working`, `Shipped`, `Receiving`, `FC transfer`,
`FC Processing`, `Total Days of Supply`. **Roles: PR or AF.** Not available in India.
`GET_FBA_INVENTORY_PLANNING_DATA`: `inbound-quantity`, `inbound-working`, `inbound-shipped`, `inbound-received`.
**Role: AF.** Not available in NL, PL, SE, BE; Brazil returns a reduced set.

R9. `GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA` (columns in D5). **Roles: PR or AF.** Daily. It is the only
report read that names a defect, its `fee-type` and `fee-total` per shipment and SKU.

R10. `GET_LEDGER_DETAIL_VIEW_DATA` with `eventType` `Receipts` (and `WhseTransfers`, `Adjustments`), and
`GET_LEDGER_SUMMARY_VIEW_DATA` (`aggregateByLocation` `FC`). **Role: AF.** 18 months. Receipts are per fulfilment
centre and day, so one shipment's receipt arrives as several rows over time; the summary view returns empty data
when the date range does not match the aggregation period.

R11. `GET_FBA_REIMBURSEMENTS_DATA`: `reason`, `case-id`, `sku`, quantities and amounts. **Roles: PR or AF.** Daily.

R12. `getItemEligibilityPreview` (FBA Inbound Eligibility v1). **Role: AF.** Model rate 1 request/s. One ASIN per
call.

R13. `listPrepDetails`, `getPrepInstructions` (v0), `listItemComplianceDetails`. **Role: AF.** `listPrepDetails`
returns only what `setPrepDetails` set (G3).

R14. Notification `FBA_INVENTORY_AVAILABILITY_CHANGES` (`InboundQuantityBreakdown`). **Role: AF.**

R15. Live values and where they are: a placement fee for a plan, the option's `fees`; a partnered carrier's price
and void deadline, the option's `quote`; a delivery window's latest date, `listDeliveryWindowOptions`; the defect fee
charged, R9; the placement fee charged, the settlement and transaction data (owned by `areas/holding-costs.md`);
peak dates, Amazon's announcement on the Seller Forums each year.

## Reads that need a role outside the five

**Amazon Warehousing and Distribution** (NA only; nothing here is built on it).
- `listInboundShipments` (filters `shipmentStatus`, `updatedAfter`/`Before`; sort `UPDATED_AT`/`CREATED_AT`) and
  `getInboundShipment` with `skuQuantities=SHOW`: per-SKU `expectedQuantity` and `receivedQuantity`, which the FBA
  v2024-03-20 API does not have. Shipment statuses: `CREATED`, `SHIPPED`, `IN_TRANSIT`, `DELIVERED` ("has been
  delivered to the facility yard. The shipment receive process at the warehouse will start soon."), `RECEIVING`
  ("partially received"), `CLOSED`, `CANCELLED`.
- `getInbound`: order status `DRAFT`, `VALIDATING`, `CONFIRMED`, `CLOSED`, `EXPIRED` ("not confirmed within a time
  limit"), `CANCELLED`.
- `listInventory` with `details=SHOW`: `totalInboundQuantity` ("in-transit from the seller and has not yet been
  received at an AWD Distribution Center"), `totalOnhandQuantity`, `availableDistributableQuantity`,
  `reservedDistributableQuantity`, and `replenishmentQuantity` ("in transit from AWD and has not yet been received
  at FBA", added 2025-01-29).
- `checkInboundEligibility`; the writes `createInbound` ("creates one shipment per order"), `updateInbound` (DRAFT
  only), `confirmInbound`, `cancelInbound`, `updateInboundShipmentTransportDetails`, `getInboundShipmentLabels`.
- Replenishment orders and outbounds exist in the model (statuses `CREATED`, `VALIDATING`, `ELIGIBLE`, `INELIGIBLE`,
  `CONFIRMED`, `EXECUTING`, `INVENTORY_OUTBOUND`, `SUCCESS`, `FAILURE`) but have no row in Role Mappings and no
  usage plan in the model; whether they are callable is open.
- Without this role, AWD → FBA stock in motion is still partly visible to AF: it arrives as FBA inbound
  (`inbound…Quantity`) once an FBA shipment exists. [seat]

**Inventory and Order Tracking** is named beside some FBA sales reports; no inbound read found needs it.

## Only in Seller Central

Established by finding no operation, report column or dataset for it in the models and report pages read; not by
testing an account.

- The capacity limit, its usage and Capacity Manager (G6).
- The Shipment summary's Contents tab (expected against located), the Action required menu, the reconciliation
  request and its case (F1). The API gives shipped and received (R4) but not eligibility or the request.
- Shipment events history (the dated trail of status changes); the API gives the current status only.
- The Shipment Performance / Inbound Performance dashboard's coaching and dispute actions (the report R9 gives the
  rows).
- The *FBA inbound placement service fee* downloadable report (E2): no report type by that name is in *FBA report
  type values*.
- Delivery-window alerts in the Shipping Queue; Carrier Central appointments (the carrier's tool).
- Manufacturing cost for reimbursement (Manage Your Manufacturing Cost).

## The seller's choices

- **Placement option.** Minimal splits: one destination, a fee per unit, an earlier peak arrive-by date. Amazon-
  optimized: several destinations, no fee when the five-identical-cartons condition is met, a later arrive-by date,
  and every shipment of the plan must then be sent or the plan is re-priced (D3). Partial: large products only.
- **Carrier.** Partnered: Amazon's quote, charged after the void window, arrival information supplied by the
  carrier. Own carrier: no Amazon charge or void limit, a delivery window to confirm and keep, appointments through
  the carrier for LTL/FTL.
- **Small parcel or pallets.** Amazon's stated windows differ (4+2 days against 10+9); pack-later exists only for
  LTL/FTL.
- **When to create the plan.** The closure clock runs from shipment creation (45/75 days) and, in a
  multi-destination plan, from the first shipment's arrival (30 days).
- **How much receiving time to allow.** Amazon's windows, a tool's default, or the seller's own shipped-to-received
  history from R4 and R10.
- **Whether to reconcile a shortfall, and when.** Only after `CLOSED`; the window is Amazon's per store (F3).
- **Direct to FBA or through AWD.** Different arrive-by dates and capacity treatment (G6, H).
- **Who creates shipments**: Seller Central, an ERP, or cx through an inbound plugin. This pack reads either way.

## Open questions

Help pages not read first-hand (script shell to a plain GET; content call off limits):
`GC3Q44PBK8BXQW3Z` FBA inbound placement service fee; `GL5XA3MNXAJKJE8E` Inbound defect fees; *Deleted, misrouted,
and incomplete shipments* (id not found); *Missing inbound FBA inventory* (id not found); `201214140` Reconcile your
shipment; `GEYPWTSQRTXXXMVB` FBA inventory reimbursement policy: shipment to Amazon claims; `GAFNWEYTJUV2GBFC` FBA
capacity limits; `G4QH4XCRWUXRJBLY` Q4 2026 peak readiness playbook; `G201411300` 2026 US fee summary; `G200280260`
Small-parcel delivery to Amazon; `G200978400` Pallets (LTL/FTL) delivery; `G201119120` Partnered Carrier program;
`G201530080` Send shipments to Amazon FBA; `G202061550` FBA manual processing fee; `201000230` Unplanned services;
`G201023020` FBA Prep Service; `GRND5GXAPBE4Z9PX` (cited by the API guide for both the Label Service and placement);
`200141500` Product packaging requirements; `G200140860` FBA product restrictions; `GV6GL3KJRDPT8TNY` (UK packing
discount); *Send to Amazon: Delivery window*; *Send to Amazon: FIST carrier*; `901` Carrier requirements.

1. Narrowed by the verifier: for the US, Amazon's statements read all say nine months from verified delivery (F3);
   the 15–60 day statement is the UAE forum's. Still open: the Seller Central policy page `GEYPWTSQRTXXXMVB` itself;
   whether the October 15, 2025 list (Australia forum) was issued for the US; the inbound window in the EU, UK,
   Japan and Canada.
2. Is the delivery window now one calendar week for international shipments too, and what is the "missed delivery
   window" defect's consequence (fee, or coaching only)?
3. Does a shipment closed by timeout still get received when it arrives (2020 text) or not (2026 seller report)?
4. Closed by the verifier: Amazon's post of 2026-10-30 is quoted in D1. Still open: whether domestic plans get
   anything, and whether a July-created plan can be excepted.
5. Do `listInboundPlans` and `getShipment` return a plan made in STA on a real account, and with which statuses?
   Does `getShipments` (v0) accept every `shipmentConfirmationId`, including AWD-originated FBA shipments?
6. Is there an inbound placement fee, or an equivalent, in the EU, UK, Japan, Canada?
7. New-ASIN quantity limits, restricted fulfilment centres, box and pallet limits: no source read.
8. Christmas arrive-by dates, and EU/UK/JP peak dates, for 2025 and 2026.
9. Are AWD outbound and replenishment operations callable, and under which role?
10. Turkey and India: the guide (India section), the release note of August 27, 2025 (Turkey) and the model say
   creation is supported; the FAQ's list still says support will be announced. Not testable without an account.
11. `setPrepDetails` against "enter the prep category in Seller Central": which governs a new SKU.
12. AGL and Amazon SEND: how their shipments appear in R1–R4.

## Positions

**P-inbound-1.** Amazon's current inbound creation API is Fulfillment Inbound v2024-03-20; ten v0 operations
(including `createInboundShipmentPlan`, `createInboundShipment`, `putTransportDetails`, `confirmTransport`,
`voidTransport`) were removed on January 21, 2025. [official] *SP-API deprecations*; release notes. (A1, A2)

**P-inbound-2.** Six v0 operations remain and are not deprecated: `getShipments`, `getShipmentItems`,
`getShipmentItemsByShipmentId`, `getLabels`, `getBillOfLading`, `getPrepInstructions`; each needs the Amazon
Fulfillment role. [official] *Fulfillment Inbound API* guide; *Role Mappings for SP-API Operations*. (A3)

**P-inbound-3.** The v2024-03-20 API returns no received quantity (every quantity field in its model is a planned
figure); among API operations, received units per SKU per shipment are only `QuantityReceived` beside
`QuantityShipped` in the v0 item reads, and outside them receipts appear in the Inventory Ledger and, for problem
rows, in the Inbound Performance report. [official] models; migration guide; *FBA report type values*. (A4, D5, F7)

**P-inbound-4.** A shipment has two identifiers: the `shipmentId` issued at planning and the
`shipmentConfirmationId` issued by `confirmPlacementOption`, which is the one printed on labels and the one the
remaining v0 operations take. [official] *Create an inbound shipment*; migration guide. (A5)

**P-inbound-5.** A plan created in Send to Amazon is readable through `listInboundPlans` and the v2024-03-20 GET
operations once its placement and transportation options are confirmed; a plan moved to Send to Amazon before that
has its options discarded and regenerated. [official] *Fulfillment Inbound API* guide; FAQ. (A6)

**P-inbound-6.** `listInboundPlans` has no marketplace filter, pages at most 30 plans, filters on `ACTIVE`,
`VOIDED`, `SHIPPED`, and requires the same filters on every follow-up page. [official] model; *Additional
functionality*. (B1)

**P-inbound-7.** A v2024-03-20 shipment's status is one of `UNCONFIRMED`, `WORKING`, `READY_TO_SHIP`, `SHIPPED`,
`IN_TRANSIT`, `DELIVERED`, `CHECKED_IN`, `RECEIVING`, `CLOSED`, `CANCELLED`, `DELETED`, `ABANDONED`, `MIXED`;
Amazon's FAQ spells the cancelled value `CANCELED`, the model `CANCELLED`. [official] model; FAQ. (B2)

**P-inbound-8.** `DELIVERED` means the carrier has delivered and the fulfilment centre has not yet checked the
shipment in; `CHECKED_IN` means it has moved from the yard to the dock door; `RECEIVING` begins when the first
shipment label is scanned. [official] FAQ; sell.amazon.com *How to track FBA shipments*. (B2, B5)

**P-inbound-9.** `CLOSED` is not proof of full receipt: Amazon defines it as either all units confirmed received or
the shipment having been open more than 45 days (domestic) or 75 days (international). [official] sell.amazon.com
*How to track FBA shipments* (modified 2025-10-03). (B4)

**P-inbound-10.** `getInventorySummaries` splits inbound into working (Amazon notified), shipped (tracking number
provided) and receiving (units not yet received in a shipment that is partly received), per SKU and not per
shipment; its `startDateTime` filter does not detect changes in these three. Roles: Amazon Fulfillment or Product
Listing. [official] FBA Inventory model; Role Mappings. (B7)

**P-inbound-11.** The same three inbound quantities appear as `afn-inbound-working-quantity`,
`afn-inbound-shipped-quantity` and `afn-inbound-receiving-quantity` in `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA`,
and as `Working`, `Shipped`, `Receiving` in the Restock report, whose `Total Days of Supply` includes units from
open shipments. [official] *FBA report type values*. (B8)

**P-inbound-12.** Amazon states stage windows and no overall receiving time: up to 4 days (small parcel) or 10 days
(LTL/FTL) from scheduled delivery to Checked in, up to 2 or 9 days from Checked in to Receiving, and up to 18 days
for received units to be available for immediate shipping, each longer at peak. [official] Dominic_Amazon, *FBA
Receiving Times*, Seller Forums, 2024-08-08. (C1)

**P-inbound-13.** Units count as available for sale as soon as they are received, while still possibly in transfer
to other fulfilment centres. [official] same post; sell.amazon.com tracking page. (C1, B5)

**P-inbound-14.** Amazon says its fulfilment centres focus on receiving in September and October and on customer
orders in November and December, and that capacity limits may be lower then. [official] News_Amazon, *Holiday 2026*,
2026-07-07. (C3)

**P-inbound-15.** A shipment sent with a non-partnered carrier needs a confirmed delivery window (seven days
domestic, 14 days international in the API guide), editable until the window starts; partnered carriers and AGL
supply arrival information themselves. US since April 24, 2023; Canada from February 9, 2024; announced for the UK
on 2024-02-15. [official] News_Amazon 2023-04-11, 2024-02-06, 2024-02-15; *Create an inbound shipment*. (C4)

**P-inbound-16.** Delivery-window options end no later than 45 days (domestic) or 75 days (international) out.
[official] *Create a shipment with a non-partnered carrier*. (C4)

**P-inbound-17.** Amazon says shipments arriving inside their delivery window get priority processing and those
outside it may face appointment and receiving delays, and that the seller stays responsible for the window even when
a carrier updates it. [official] *Prime Day readiness playbook* (capture 2026-10-14); Amazon moderator reply,
2026-02. (C5)

**P-inbound-18.** In the US since February 1, 2024, a shipment is closed automatically if it has not arrived within
45 days of creation (domestic) or 75 days (international), and shipments of a multi-destination plan must arrive
within 30 days of the first; "arrived" means the status reached in-transit, delivered, checked-in or receiving.
[official] News_Amazon, 2024-01-11. (D1)

**P-inbound-19.** For international shipment plans created between August 1 and November 30, 2026 (US), Amazon
lengthened the automatic-closure window to 90 days and the multi-destination window to 45 days from first receipt,
keeps the defect on the Inbound Performance Dashboard, waives its fee and reimburses fees already charged; it made
the same two extensions for shipments created August 7 to October 31, 2024. [official] News_Amazon, 2026-10-30 and
2024-10-24, Seller Forums. (D1)

**P-inbound-20.** Ignoring, deleting or abandoning one shipment of a multi-shipment plan creates an abandoned-
shipment defect subject to the inbound defect fee and re-prices the plan's placement fee at the minimal-splits rate.
[official] Bryce_Amazon, Seller Forums, 2024-06-27. (D3)

**P-inbound-21.** `GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA` (roles Pricing or Amazon Fulfillment, updated
daily) lists inbound problems per shipment and SKU with `problem-type`, `expected-quantity`, `received-quantity`,
`fee-type` and `fee-total`. [official] *FBA report type values*. (D5)

**P-inbound-22.** The US inbound placement service fee took effect March 1, 2024 and is charged 45 days after the
shipment is received, on the inbound location and the quantities received. [official] News_Amazon 2023-12-05; Amazon
moderator, 2024-11. (E1, E2)

**P-inbound-23.** Minimal shipment splits send to generally one location for a fee that varies by location;
Amazon-optimized splits carry no fee when each item ships in at least five identical cartons or pallets; partial
splits have been unavailable for standard-size products since February 20, 2025. US. [official] Amazon moderator,
2024-11; *Create an inbound shipment*. (E2, E3)

**P-inbound-24.** Through the API a placement option's fee or discount is a quoted figure on the option, set by an
algorithm at creation and not by a rate table, and options generated before box contents are known can differ from
those generated after. [official] *Create an inbound shipment*; model. (E4)

**P-inbound-25.** `confirmPlacementOption` cannot be reversed or changed for the plan. [official] model; *Create an
inbound shipment*. (E5)

**P-inbound-26.** A discrepancy can be researched only after the shipment is `CLOSED`, and not while final counts
are pending or when the contents are fully received or already reconciled. [official] sell.amazon.com tracking page;
Dominic_Amazon 2024-08-08. (F1, C1)

**P-inbound-27.** For the US, Amazon states the claim window for units missing from an inbound shipment as no later
than nine months after the verified delivery date, once the shipment shows as eligible for investigation (Amazon
Supply Chain's *Reimbursements* page, read 2026-11-10; an Amazon moderator, 2026-08-13: "within 9 months"); the
15-to-60-calendar-day window of News_Amazon's 2024-08-06 post was issued on the United Arab Emirates forum.
[official] supplychain.amazon.com/support/reimbursements; Seller Forums threads `0e07abc1-…`, `96a05f4a-…`. (F3)

**P-inbound-28.** Amazon's proactive reimbursement, as announced (US from November 1, 2024; UK from January 15,
2025), covers items lost in fulfilment centres; units missing from an inbound shipment go through reconciliation.
[official] News_Amazon 2024-07-24 (US) and 2024-10-10 (UK); sell.amazon.com tracking page. (F4, F1)

**P-inbound-29.** Amazon reimburses losses before a customer order, shipment-to-Amazon claims included, at the
item's sourcing (manufacturing) cost, excluding shipping, handling and duties: stated for the US by an Amazon
moderator on 2026-08-13, and announced on the UK forum as effective March 10, 2025. [official] Indy_Amazon
2026-08-13; News_Amazon 2024-12-18 (UK forum). (F5)

**P-inbound-30.** Amazon may refuse reimbursement where it determines units were not in the shipment, including
when box or unit labels did not tie them to it. [official] Amazon moderator reply, 2025-12. (F6)

**P-inbound-31.** The Inventory Ledger detail report (role Amazon Fulfillment, 18 months) records receipts per
fulfilment centre and date under `eventType` `Receipts`, with reconciled and unreconciled quantities. [official]
*FBA report type values*. (F7)

**P-inbound-32.** One inbound plan holds at most 1,500 SKUs and 10,000 items per SKU, and one expiration date per
SKU. [official] FAQ; *Create an inbound shipment*. (G1, G4)

**P-inbound-33.** Since January 1, 2026 Amazon provides no prep or item-label service for US FBA inventory,
including inventory arriving through AWD, AGL, Amazon SEND and Supply Chain Portal, and `AMAZON` is not accepted as
`prepOwner` or `labelOwner` in the US. [official] SP-API changelog; model. (G2)

**P-inbound-34.** `getItemEligibilityPreview` (role Amazon Fulfillment) answers whether one ASIN may be inbounded to
one marketplace and why not; it does not answer for a quantity or for capacity. [official] FBA Inbound Eligibility
model. (G5)

**P-inbound-35.** After transportation is confirmed and before Receiving, a shipment's units can be changed by up to
five percent or six units per SKU, whichever is greater. [official] *Additional functionality*. (G8)

**P-inbound-36.** Amazon's peak dates are arrival dates and differ by placement option: for Black Friday Week and
Cyber Monday 2026, October 14 (AWD), October 21 (minimal splits), October 28 (Amazon-optimized); for Prime Big Deal
Days 2026, September 2, 9 and 16; for Prime Day 2026, May 27, May 27 and June 5. US. [official] News_Amazon
2026-07-07 and 2026-04-29. (H)

**P-inbound-37.** Amazon keeps receiving after a peak date but says late arrivals may not be processed in time for
Prime eligibility. [official] News_Amazon 2026-04-29. (H)

**P-inbound-38.** Every write of the v2024-03-20 API is asynchronous and returns an `operationId` read with
`getInboundOperationStatus`; options are generated, listed and confirmed, and unconfirmed options expire. Role:
Amazon Fulfillment. [official] migration guide; model. (J1, J4)

**P-inbound-39.** Confirming a partnered-carrier transportation option agrees to the charge; it can be voided within
24 hours for small parcel and one hour for LTL/FTL, after which the account is charged; the limits do not apply to
non-partnered options. [official] *Create an inbound shipment*; FAQ. (J3)

**P-inbound-40.** `cancelInboundPlan` cancels the whole plan and all its shipments. [official] *Additional
functionality*. (J3)

**P-inbound-41.** The AWD API needs the Amazon Warehousing and Distribution role, which is outside the five; Role
Mappings lists eleven AWD operations and none of the outbound or replenishment operations the model defines.
[official] Role Mappings; AWD model (21 operations). (I1)

**P-inbound-42.** Amazon's own `fba-inbound-management` skill states a 500,000-unit per-SKU plan limit and that
only API-created plans are visible, against Amazon's FAQ (10,000 per SKU; STA plans readable), and names an
operation (`updateBoxIdentifiers`) and a field (`readyToShipDate`) found in no SP-API model, and a field
(`shipFromAddress`) found in no Fulfillment Inbound model. [official] the skill's files; FAQ; models. (J7)

**P-inbound-43.** Tools carry an explicit receiving allowance in lead time: 积加 defaults 入库处理天数 to 3 days,
SoStocked defaults warehouse-to-Amazon transfer to 10 days (their practice). [opinion] the survey's tool notes. (P1)

**P-inbound-44.** SupplyKick's practice is to ship three weeks ahead for LTL and two for parcel, plus a week before
Q4 or Prime Day; My Amazon Guy reports that a case opened during a receiving backlog returns a wait instruction.
[opinion] SupplyKick; My Amazon Guy, 2026-04-20. (P2)

**P-inbound-45.** An Amazon moderator's guidance of 2024-11-18 for a shipment still in transit after automatic
closure: it can be received if the carrier holds a valid, active delivery appointment in Carrier Central; if not,
the goods go back and the shipment is recreated with new box labels. A seller's report of 2026-01-27 describes
pallets delivered after day 75 left unscanned. US. [official] Dominic_Amazon, Seller Forums; [opinion] the seller.
(D2, C6)

### The seat's own (no source; enters no skill)

- A shipped-against-received shortfall on a shipment that is not yet `CLOSED` is not yet a loss; on one that is
  `CLOSED` it may be a timeout rather than a count.
- The seller's own history of creation date, first receipt and last receipt (R3, R4, R10) is a better receiving
  allowance for that seller than any published window.
- The line to an inbound plugin falls at the first `generate…` call: listing options that exist is a read, making
  them exist is a write, and three confirmations (placement, partnered transportation, content update) carry money
  or permanence.
- Units moving from AWD to FBA are visible without the AWD role only once they are an FBA shipment.

## Pages read

All read 2026-11-10 (session ran 2026-11-09 to 2026-11-10 Pacific time). Forum ids are the path after
`https://sellercentral.amazon.com/seller-forums/discussions/t/`.

| Page | URL or path | Tag | Reached how |
|---|---|---|---|
| Fulfillment Inbound v2024-03-20, v0; FBA Inbound Eligibility; AWD 2024-05-09; FBA Inventory models | `scratch/sp-api-plugins/models/models/…` at `db2936aa` | official | local |
| Fulfillment Inbound API (guide) | developer-docs.amazon/sp-api/docs/fulfillment-inbound-api.md | official | GET |
| Create an inbound shipment | …/create-an-inbound-shipment.md | official | GET |
| Create a shipment with an Amazon-partnered carrier | …/create-amazon-partnered-carrier-shipment.md | official | GET |
| Create a shipment with a non-partnered carrier | …/create-non-partnered-carrier-shipment.md | official | GET |
| Pack later (unknown carton) | …/pack-later-unknown-carton.md | official | GET, skimmed |
| Additional functionality | …/additional-functionality-fulfillment-inbound.md | official | GET |
| Fulfillment Inbound API FAQ | …/fulfillment-inbound-faq.md | official | GET |
| Migrating Fulfillment Inbound workflows | …/migrating-fulfillment-inbound-workflows.md | official | GET |
| SP-API deprecations; release notes | …/sp-api-deprecations.md; …/sp-api-release-notes.md | official | GET |
| Role Mappings for SP-API Operations; for SP-API Types | …/role-mappings.md; …/role-mappings-for-types.md | official | GET |
| FBA report type values; FBA feed type values; Notification type values | …/report-type-values-fba.md; …/fulfillment-by-amazon-feed-type-values.md; …/notification-type-values.md | official | GET |
| Changelog: US FBA prep and labeling services to end January 1, 2026 | developer-docs.amazon/sp-api/changelog/us-fba-prep-and-labeling-services-to-end-january-1-2026.md | official | GET |
| How to track FBA shipments | sell.amazon.com/blog/fba-shipment-tracking | official | GET |
| FBA Receiving Times (Dominic_Amazon, 2024-08-08) | forum `3fb02a04-bace-4bcb-9458-a93f0148c613` | official | GET |
| Amazon Receiving Timeframe (Amazon reply, 2024) | forum `306799d1-aadb-40e8-840d-3ab9529591ff` | official | GET |
| Automatic closure policy… February 1 (News_Amazon, 2024-01-11) | forum `ef22088c-72d7-417b-b369-911e4ff6244a` | official | GET |
| Update to FBA shipment closure timelines (News_Amazon, 2020-12-16) | forum `6fef45de7219073fea69f637c32c62f6` | official | GET |
| Request to reopen shipment… closed after 90 days (Amazon reply, 2024-10) | forum `130b5dc4-fc76-426c-9344-094cacfc65bb` | official reply | GET |
| Sailing Smoothly: Avoid Abandoned Shipment Fees (Bryce_Amazon, 2024-06-27) | forum `8eb6e29c-ea59-4a5d-b3e4-c40ebd2d85d3` | official | GET |
| New delivery window requirement (News_Amazon, 2023-04-11 US; 2024-02-06 Canada) | forum `1ecdd7e2db64f05b036f5beb7bb58257`; `4f4ffafc-7c7b-414f-85cf-23463adb2aa8` | official | GET |
| International sellers and the 1-week delivery window (2025-10-21) | forum `2e5c056b-abb9-47d7-9d45-940f8b346230` | seller post, official reply | GET |
| Missed Delivery Window defect with FIST carrier (2026-02-16) | forum `4d7ef61c-636d-4cb3-b757-1fa04c720476` | seller post, official reply | GET |
| Update to US referral and FBA fees (News_Amazon, 2023-12-05) | forum `ce3a1455-3fdb-4317-991d-ca501f0a75a3` | official | GET |
| 2026 Updates to US Referral and FBA Fees (News_Amazon, 2025-10-15) | forum `f3fa3211-820b-4e2e-a023-158a9cf55f99` | official | GET |
| When and how will the placement fees be charged (Amazon reply, 2024-11) | forum `5d437c4b-6e3d-49a2-8754-8c77ce1dc4c7` | official reply | GET |
| Update on reimbursement claim window eligibility (News_Amazon, 2024-08-06) | forum `96a05f4a-537a-49d2-a918-703c47716bc0` | official | GET |
| Update on Reimbursement Automation and Eligibility Window (News_Amazon, 2024-10-10) | forum `d0fc997e-de50-4100-9803-76b7993b66df` | official | GET |
| Update to the FBA lost and damage inventory reimbursement policy (News_Amazon, 2024-12-18) | forum `a941ac02-d389-409a-9d62-00ab9db5bc4a` | official | GET |
| Update to FBA inventory reimbursement claim windows (News_Amazon, 2025-08-14) | forum `d8f9a56c-882f-437c-ad34-cccd11cfa465` | official | GET |
| Clarification on the claim window: shipment to Amazon (seller, 2024-09-26) | forum `2b32f5d5-28e2-4445-8318-17793237a735` | official, via a seller | GET |
| FBA Lost Your Inventory? Steps to File (Indy_Amazon, 2026-08-13) | forum `0e07abc1-9026-4540-a005-153d9e78bf04` | official | GET |
| How to Resolve FBA Shipment Discrepancies (Christine_Amazon, 2025-11-14) | forum `83caf79b-4ca1-4e1c-9564-9f328739e0f7` | official | GET |
| Amazon is no longer responsible for lost FBA shipments? (Amazon reply, 2025-12) | forum `bb14816c-3c48-422b-8ddf-3b339e64f192` | official reply | GET |
| International shipment marked ABANDONED (2026-01-27) | forum `c5388f8d-3f2b-4bac-aa8e-c8c948add69c` | seller post, official reply | GET |
| 30-day multi-destination thread (2025-06, Amazon reply) | sellercentral-europe.amazon.com forum `d06cf5f9-5ef1-4b9b-a269-a4b394fdc02f` | seller post, official reply | GET |
| It's official, Prime Day 2026 is in June (News_Amazon, 2026-04-29) | forum `59a5cd20-deae-4bb9-9282-e5ec24c3871f` | official | GET |
| Holiday 2026: Same fees, same eligibility, earlier deadlines (News_Amazon, 2026-07-07) | forum `3e31fbb7-04e0-4ed4-873e-f74b1052e2ff` | official | GET |
| BFCM 2026 checklist (Indy_Amazon, 2026-10-14); Peak Season Alert (2025-10-22) | forum `6a6f3b4a-97a8-4f04-b671-4f7a1ae6046b`; `b93d7dfa-e56d-4098-bcea-b320df803a22` | official | GET |
| Prime Day readiness playbook `GM2ADTH3XH3A5N57` v4 | office capture folder, file of 2026-10-14 | official | local capture by the listing seat |
| Listing playbook, inventory and fulfillment angle | `cx-listing-playbook/research/angles/inventory-and-fulfillment.md` | official, via that seat | local, not re-read at source |
| Amazon's `fba-inbound-management` skill | `scratch/sp-api-plugins/amazon-plugin-zip/skills/fba-inbound-management/` | official | local |
| Survey tool notes | `scratch/sp-api-plugins/03-tools-en.md`, `03-tools-cn.md`, `03-job-stock.md` | opinion | local, vendors not re-read |
| AMZ123: 旺季临时政策 (2026-11-02); 退入库缺陷费 (2026-11-01); 调整入库缺陷费 (2025-11-09) | amz123.com/t/9rC7BjAH; /t/dybZP4Sg; /t/3PEcbbvv | official via AMZ123; opinion | GET |
| Temporary peak season extensions for international FBA shipments (News_Amazon, 2026-10-30) | forum `f25ba535-e06e-4fa3-8bb0-cb3a095fd696` | official | GET, by the verifier |
| Updates to support US FBA peak inventory shipments (News_Amazon, 2024-10-24) | forum `4ade7ec5-b16e-4ee3-b669-45cdcc0b97a5` | official | GET, by the verifier |
| Update on Reimbursement Automation and Eligibility Window, US text (News_Amazon, 2024-07-24) | forum `81c3235d-4c44-47ba-96c5-883cecab3244` | official | GET, by the verifier |
| New delivery-window requirement, UK (News_Amazon, 2024-02-15) | sellercentral-europe forum `c1aebd75-9a21-4f0f-986a-9d09e09854d2` | official | GET, by the verifier |
| Amazon Supply Chain, Reimbursements support page | supplychain.amazon.com/support/reimbursements | official | GET, by the verifier |
| Chun, Improving inbound visibility through shipment arrival modeling (MIT, 2014) | dspace.mit.edu/handle/1721.1/90779 | research | GET, abstract only, by the verifier |
| Update to European referral and FBA fees for 2026 | aboutamazon.eu/news/empowering-small-business/update-to-european-referral-and-fulfilment-by-amazon-fees-for-2026 | official | GET, by the verifier; the word "inbound" does not occur |
| EcomCrew, Amazon Is Waiving Some Inbound Fees (2026-11-03) | ecomcrew.com/amazon-is-waiving-some-inbound-fees-check-your-shipments/ | opinion | GET, by the verifier; gave the link to Amazon's post |
| My Amazon Guy, Fix Amazon receiving delays (2026-04-20) | myamazonguy.com/logistics/fix-amazon-receiving-delays/ | opinion | GET |
| SupplyKick, Amazon FBA processing times | supplykick.com/blog/amazon-fba-processing-times | opinion | GET |
| AMZ Prep, shipping delays; inbound placement fees | amzprep.com/shipping-delays/; amzprep.com/amazon-inbound-placement-fees/ | opinion | GET |
| EcomCrew, Q4 2026 deadlines (2026-07-07); PPC Land 2025 and 2026 holiday deadlines | ecomcrew.com/…; ppc.land/… | opinion | GET |
| Seller Central help pages listed in *Open questions* | sellercentral.amazon.com/help/hub/reference/external/<ID> | **unreachable** | plain GET, `?locale=en-US`, `/gp/help/external/`, `.co.uk` twin: script shell each time |
| sell.amazon.com guessed pages (placement fee, AWD, capacity, Send to Amazon, AGL) | sell.amazon.com/blog/… and /fulfillment-by-amazon/… | **unreachable** | guessed URLs returned 404; not searched further |
| Helium 10, FBA reimbursement policy update | helium10.com/blog/amazon-fba-inventory-reimbursement-policy-update/ | not used | downloaded, not read |

## Verification

Verified 2026-11-10 by the verifier seat. Every page below was fetched again today with a plain GET (no Amazon API
host, no POST, no help-hub content call); local models were opened at `db2936aa`; Amazon's skill was read in
`scratch/sp-api-plugins/amazon-plugin-zip/`.

**Counted.** 44 positions checked; 8 corrected (P-inbound-3, 15, 19, 27, 28, 29, 41, 42); none removed; 1 added
(P-inbound-45). Beyond the positions, roughly 150 other claims (an estimate, not a tally) were re-opened by searching today's
page for the carrying phrase: the quotations behind every position from the nine SP-API documentation pages, the
deprecations and release-notes dates, the 27 forum threads (author, date, store, and the phrases the positions rest
on; the FAQ's status table in B2 and the longer quotations in C2, D6, F1, F2 and G3 were spot-checked, not compared
word for word), the sell.amazon.com tracking page, the model enums and descriptions in sections A, B, E, G, I and J, the
report columns in D5, F7 and B8, and the role of every operation, report, notification and feed named.

**Roles.** All match *Role Mappings for SP-API Operations* and *for SP-API Types* as fetched today: all 45
v2024-03-20 operations (each Amazon Fulfillment, regions NA, EU, FE), the six v0 operations, `getItemEligibilityPreview` (Amazon Fulfillment);
`getInventorySummaries` (Amazon Fulfillment or Product Listing); the MYI, Restock, Inbound Performance and
Reimbursements reports (Amazon Fulfillment or Pricing); FBA Inventory Planning, both Ledger reports,
`FBA_INVENTORY_AVAILABILITY_CHANGES` and `POST_FBA_INBOUND_CARTON_CONTENTS` (Amazon Fulfillment); eleven AWD
operations (Amazon Warehousing and Distribution, region NA), which sit in the section for roles outside the five. No
position rests on a read outside the five.

**The four claims the lead asked to test hardest.**
1. No received quantity in v2024-03-20: **holds.** Every property of the model whose name contains quantity, units,
   count, shipped or received was listed; the eight found are planned figures (now named in A4). The claim "only in
   v0" was narrowed to "among API operations"; the Ledger and the Inbound Performance report also carry receipts.
2. `CLOSED` by timeout: **holds.** Amazon's sentence is on sell.amazon.com/blog/fba-shipment-tracking today, word for
   word as quoted in B4.
3. The claim window: **corrected.** The 15–60 day post (`96a05f4a-…`) carries the UAE `marketplaceId`, not the
   US one; the 2025-08-14 list is the Australia forum's; the 2024-10-10 and 2024-12-18 posts are the UK forum's. A
   third statement was found and settles the US reading as far as public pages go: Amazon Supply Chain's
   *Reimbursements* page says nine months after the verified delivery date and excepts shipment-to-Amazon claims
   from the 60-day windows. F3 was rewritten; P-inbound-27 no longer says Amazon's statements disagree for the US.
4. Amazon's skill: **holds, with one correction.** "500K units per SKU", "Only v2024-03-20 plans are visible",
   "24–72h" and "within 2 weeks" are in its files as quoted; the FAQ says 10,000 items per SKU. `updateBoxIdentifiers`,
   `readyToShipDate` and `estimatedDeliveryWindow` occur in no JSON model. `shipFromAddress` does occur, in the
   Merchant Fulfillment, Shipping and Orders models, so "exists in no model" was wrong; J7 and P-inbound-42 now say
   no Fulfillment Inbound model.

**Changes.**
- P-inbound-3 / A4. Said the received quantity lives only in v0. The models say so only for API operations; reports
  carry receipts. Reworded, and the eight quantity fields named.
- P-inbound-15 / C4. Said the 2024-02-06 post was the UK/EU text. Its marketplace field is Canada; the UK post is
  2024-02-15 (`c1aebd75-…`). Fixed, both cited.
- P-inbound-19 / D1. Was `[official, via AMZ123]`. Amazon's own post was found (News_Amazon, 2026-10-30,
  `f25ba535-…`); quoted and retagged `[official]`. The 2024 precedent (`4ade7ec5-…`) added.
- P-inbound-27 / F3. See claim 3.
- P-inbound-28 / F4. US date was a `[snippet]`. The US post (`81c3235d-…`, 2024-07-24) was read: November 1, 2024.
  Retagged; the 2024-10-10 post marked as the UK's.
- P-inbound-29 / F5. Said "Since March 10, 2025" on the strength of a UK forum post. Scope now stated; the US rests
  on the moderator's post of 2026-08-13.
- P-inbound-41 / I1. The AWD model has 21 operations; `getLabelPageTypes` is also absent from Role Mappings. Added.
- P-inbound-42 / J7. See claim 4.
- A7. The guide's own India section was added; the disagreement is the FAQ against the guide, release note and model.
- D2. The moderator's guidance on a shipment closed while in transit was added beside the seller's report, and
  stated as P-inbound-45.
- H. "(most sellers select this option)" is in the Holiday 2026 post only, not the Prime Day post. Fixed. Amazon's
  2025 sentence for October 30 quoted.
- Published research: one adjacent thesis added; the section no longer says nothing exists.
- Open questions 1, 4 and 10 rewritten to what is still open.

**Wording.** Each position was read against the pack's rule. None instructs cx, fixes an order of steps or sets a
threshold; tools' and practitioners' figures carry their names (P-inbound-43, 44); Amazon's figures read as dated
statements. No rewording was needed on that ground.

**Could not re-open.**
- Every Seller Central help page (script shell; content call off limits): unchanged from *Open questions*.
- The listing playbook's quotations (D4 fee summary, E2 `GC3Q44PBK8BXQW3Z`, G6 capacity) and the *Prime Day
  readiness playbook* capture (C5, H): cited as that seat's read, not re-read by the verifier.
- The survey's tool notes behind P1, P6 and P-inbound-43 (积加, SoStocked, Sellerboard, RestockPro, 领星, 赛狐): the
  vendors' pages were not opened.
- PPC Land and EcomCrew's dates pages (H 2025 rows, P8), AMZ Prep's delays page, `amz123.com/t/dybZP4Sg`, and the
  forum threads behind P5 other than `d06cf5f9-…` (`7940364d-…`, `e102af8a-…`, `b37b0d23-…`): not re-fetched. My
  Amazon Guy, SupplyKick, AMZ Prep's placement page, and AMZ123 `9rC7BjAH` and `3PEcbbvv` were re-fetched and their
  quoted strings found.
- The dates given for reason codes `FBA_INB_0342` and `FBA_INB_0465` (G5): the release notes name both additions,
  the entry dates were not checked.
- Rate figures in R1, R4, R12 beyond `confirmPlacementOption`'s usage plan: not re-read line by line.
- The store of each forum thread is read from the page's `marketplaceId`; that the field is the store the post was
  issued for is the verifier's inference from spelling and dates agreeing with it in every thread checked.

**Gaps filled (each marked `gap fill 2026-11-10` where it stands).** Amazon's own text for the August–November 2026
relaxation; the 2024 precedent; the US nine-month claim window on Amazon's own page; the US proactive-reimbursement
text; one piece of adjacent published research.

**Gaps left.**
- Delivery window: no Amazon text for "one calendar week (Sun - Sat)" for all shipments was found; the API guide
  (seven days domestic, 14 international) and the seller's quotation still stand side by side. The consequence of a
  missed-window defect (fee or coaching) is not established.
- An inbound placement fee in the EU, UK, Japan or Canada: none found. Amazon's 2026 European fee announcement on
  aboutamazon.eu does not contain the word "inbound"; that is absence on one page, not a finding. [seat]
- Christmas arrive-by dates, and EU/UK/JP peak dates, for 2025 and 2026: no Amazon text found. For 2025 only the
  October 30 Amazon-optimized date is Amazon's own.
- New-ASIN quantity limits, box and pallet limit texts, AGL and Amazon SEND at source: not read.
- What a long-time inventory manager would also look for and not find here: the importer-of-record and customs
  position of an international inbound; units received over the plan or under another SKU (overage, "found" units);
  minimum remaining shelf life at receipt; 2D-barcode box content; how the placement fee is corrected after a
  reconciliation changes the received quantity; the inbound window for stores other than the US and UAE; receive
  dates as the start of storage age (owned by `areas/holding-costs.md`, not cross-referenced here).
