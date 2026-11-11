# FBM quantity, and Amazon-sold stock outside FBA's shelves or leaving by another channel

Read 2026-11-10 by the research seat. (The session ran across 2026-11-09 and 2026-11-10; every date read below is
written as 2026-11-10.)

Tags: **[official]** is Amazon's own words on a page opened in this session (developer documentation, sell.amazon.com,
supplychain.amazon.com, sellingpartners.aboutamazon.com, posts by Amazon staff on the seller forums) or in the local
SP-API models at commit `db2936aa` (2026-10-29). **[official, via listing playbook 2026-10-14]** is a quotation another
seat took from a Seller Central help page on 2026-10-14; it was not re-read here. **[official, via <who>]** and
**[snippet]** are Amazon's words seen only in a third party's quotation or a search result. **[opinion]** is a named
practitioner or tool. **[research]** is a published study. **[seat]** is this seat's inference and enters no skill.

How pages were reached. Developer documentation was read as markdown with a plain GET of
`https://developer-docs.amazon/sp-api/docs/<slug>.md` (slugs from `https://developer-docs.amazon/sp-api/llms.txt`).
Forum posts, sell.amazon.com, supplychain.amazon.com and practitioner pages were read with a plain GET. Seller Central
help pages returned a script shell with no article body to a plain GET (`/help/hub/reference/external/<ID>?locale=en-US`,
`/gp/help/external/<ID>`, the `.co.uk` twin; the sell.amazon.com twin gave 404; web.archive.org had no capture for the
id tried); the content call is a POST and is off limits by the lead's ruling of 2026-11-10, so every help page is
listed as unreachable with its id in *Open questions* and *Pages read*. Models are cited by path under
a local clone of `amzn/selling-partner-api-models`, `models/`. No Amazon API host was called.

Short names used for roles: PL Product Listing, PR Pricing, BA Brand Analytics, FA Finance and Accounting,
AF Amazon Fulfillment (the five the door holds); IOT Inventory and Order Tracking, SPI Selling Partner Insights,
DTC Direct-to-Consumer Shipping (Restricted) (outside the five).

## What this covers

- The seller-fulfilled (FBM, in API words MFN) quantity as Amazon holds it: where it is written, where it is read,
  which copy is live, how stale each copy can be, and what a quantity of zero does to the listing.
- How Amazon moves that number on its own: orders placed, orders cancelled, pending orders; and the settings around it
  that change what a given quantity promises (handling time, order handling capacity, vacation status, multi-location
  inventory).
- One ASIN sold through both FBA and FBM: two SKUs, or one SKU carrying both fulfilment records; what Amazon says about
  which stock is used first; switching a SKU between channels.
- Multi-Channel Fulfillment (MCF) as a drain on FBA stock: the Fulfillment Outbound API in its two versions, when an
  MCF order takes units, holds, fill policies, packaging and carrier features, and what the seller sees of it.
- Stock that is Amazon-sold but never on FBA's shelves: own warehouse or 3PL, multi-location inventory, the External
  Fulfillment channels (Seller Flex and others), Easy Ship by country.
- One pool of stock sold on several channels: what Amazon's API offers a synchronising tool, and what the tools sellers
  pay for say they do.

Owned elsewhere and only cross-referenced:

- `areas/stock-states.md`: the FBA inventory states (fulfillable, reserved and its three parts, inbound, unfulfillable,
  researching) and the ledger. This file only says where MCF touches them.
- `areas/holding-costs.md`: storage and fulfilment fees, including MCF fee amounts.
- `areas/running-out.md`: what an FBA stock-out costs in rank and Featured Offer; this file covers only the FBM offer
  as something that exists while FBA is empty.
- `areas/restock-and-forecast.md`: how much to send and when. `areas/inbound.md`: shipments into FBA, including the
  FBM-to-FBA conversion as the first step of an inbound plan. `areas/stuck-stock.md`: stranded and unfulfillable units.
- `beyond/programs-and-regions.md`: AWD, Supply Chain by Amazon, Pan-EU, remote fulfilment, Seller Flex as a programme.
- `method/sp-api-stock-surface.md`: the full map of stock operations and reports. `method/seller-central-only.md`: the
  full list of what only Seller Central shows.
- `cx-account-health` (another pack): the seller-fulfilled performance metrics. This file names the metrics an
  oversell moves and stops there.
- The listing playbook's `research/method/listing-writes.md` (sections A–I): the write path of the Listings Items API
  in general. Section *L* below says what is the same and what is specific to quantity.

## Amazon's own rules

### A. Two copies of the FBM quantity: what the seller last sent, and what a shopper can buy now

A1. The Listings Items API returns the quantity in two places, and they are not the same number. [official]
*Understanding Amazon listing status and seller-fulfilled inventory management*,
https://developer-docs.amazon/sp-api/docs/understanding-amazon-listing-status-and-seller-fulfilled-inventory-management.md
(page metadata `updatedAt` 2026-09-09), read 2026-11-10:

> "there is a distinction between the latest fulfillment availability data submitted by the selling partner and the
> actual fulfillment availability data. If you submit an inventory quantity of 1 and sell the item, the
> `fulfillment_availability` attribute within the attributes property shows 1 and the `fulfillmentAvailability`
> property shows 0 as the live quantity available for purchase and source of truth for actual inventory levels."

*Listings Items API* (https://developer-docs.amazon/sp-api/docs/listings-items-api.md, "Attributes"), read 2026-11-10,
says the same in other words: "The attributes section shows the latest data provided by the selling partner. Other
sections, such as `fulfillmentAvailability`, represent the latest live data for the listing." The listing playbook's
P-inventory-and-fulfillment-2 states the same split (worded there as a rule for cx). So `attributes.fulfillment_availability` (returned with
`includedData=attributes`) is the last submission; `fulfillmentAvailability` (returned with
`includedData=fulfillmentAvailability`) is the live figure.

A2. The live data set's shape, from the model. [official]
`listings-items-api-model/listingsItems_2021-08-01.json#/definitions/FulfillmentAvailability`: `fulfillmentChannelCode`
(required, "Designates which fulfillment network is used.") and `quantity` ("The item quantity that you're making
available for sale.", integer, minimum 0). The model's live record carries no handling time and no restock date; those
are attributes only.

A3. What "available" means for a seller-fulfilled SKU. [official] *Notification Type Values*,
https://developer-docs.amazon/sp-api/docs/notification-type-values.md, `LISTINGS_ITEM_MFN_QUANTITY_CHANGE`, read
2026-11-10:

> "The available quantity is the number of units available at Amazon for customers to order. When a customer places an
> order, Amazon decrements the number of ordered units from the available quantity for that listings item. When the
> available quantity reaches zero, customers can no longer place orders on the item. Selling partners typically update
> Amazon with the exact number of units available in their stock."

and the notification is sent when the quantity "changes because of… inventory quantity updates from the selling
partner, new orders being placed, and existing orders being canceled." Three things follow as Amazon's statements: an
order decrements at placement (not at payment and not at shipment); a cancellation is a quantity event; and Amazon
keeps the counter between the seller's updates.

A4. The attribute is an array of records keyed by channel. [official] *Manage Amazon Haul, Advanced Multiple-Offer, and
Multiple-Fulfillment Use Cases*,
https://developer-docs.amazon/sp-api/docs/manage-amazon-haul-advanced-multiple-offer-multiple-fulfillment-use-cases.md
(`updatedAt` 2026-10-28), read 2026-11-10: `fulfillment_availability` "is an array that accepts one or more distinct
fulfillment records, each keyed by the `fulfillment_channel_code` to which the fulfillment record is applicable." The
page's seller-fulfilled example is
`{"fulfillment_channel_code":"DEFAULT","quantity":10,"restock_date":"2025-01-01","lead_time_to_ship_max_days":5}`.
The common codes it names are `DEFAULT` (MFN) and `AMAZON_NA`, `AMAZON_EU`, `AMAZON_JP` (FBA); *Additional
functionality (Fulfillment Inbound)*,
https://developer-docs.amazon/sp-api/docs/additional-functionality-fulfillment-inbound.md, read 2026-11-10, adds
`AMAZON_IN`. The codes valid for a given seller and store are read from the product type's schema with the seller's id
(Product Type Definitions API, `getDefinitionsProductType`; role IOT or PL).

A5. Quantity belongs to the seller-fulfilled record only. [official] same page as A4: "`quantity` information is
supported for MFN fulfillment, but not for Fulfillment by Amazon (FBA) fulfillment." An FBA record is the channel code
alone (`{"fulfillment_channel_code":"AMAZON_NA"}`); the FBA count is Amazon's and lives in the FBA inventory reads
(`areas/stock-states.md`).

A6. Handling time on the record. [official] same page as A4: "you no longer need to include the
`lead_time_to_ship_max_days` value to maintain the handling time defined at the SKU-level." The help page *Manage your
handling time* (G200955560, v50) was not readable here; the listing playbook's read of 2026-10-14 quotes it as saying
empty handling fields fall back to the account default, a changed offer shows "within 15 minutes" and "up to 24 hours"
at maximum load, and Automated Handling Time overrides the SKU and the default. [official, via listing playbook
2026-10-14]

A7. Not established at the source: the schema descriptions of `restock_date`, `lead_time_to_ship_max_days` and
`is_inventory_available`. The product type schema is served only by the API (not called). Lengow's help centre is
reported by a search result as saying `is_inventory_available` is an alternative to `quantity` and cannot be sent with
it; the page gave 403 here. [snippet] See *Open questions*.

### B. Writing the FBM quantity

B1. The operation. `patchListingsItem` (Listings Items API v2021-08-01; role IOT or PL, so PL carries it) with
`productType` and at least one patch. [official] `listingsItems_2021-08-01.json#/definitions/ListingsItemPatchRequest`
(requires `productType`, `patches` minItems 1) and `#/definitions/PatchOperation` (`op` enum `add`, `replace`, `merge`,
`delete`). The operation's description: "Only top-level listings item attributes can be patched. Patching nested
attributes is not supported." Rate in the model: 5 requests per second, burst 5.

B2. `replace` sets the whole attribute. [official] *Submit Listings data*,
https://developer-docs.amazon/sp-api/docs/submit-listings-data.md ("Submit inventory data"), read 2026-11-10:

```json
{"productType":"PRODUCT","patches":[{"op":"replace","path":"/attributes/fulfillment_availability",
 "value":[{"fulfillment_channel_code":"DEFAULT","quantity":5}]}]}
```

Because the path is the top-level attribute, a `replace` (or `add`, which the model describes identically: both "adds
or replaces the target property") writes the whole array: a record or an optional field left out of the value is not
kept. [official for the grammar; the consequence for omitted records is **[seat]**, read from "Only top-level… can be
patched" plus the merge page's reason for existing, B3.]

B3. `merge` changes the quantity and leaves the rest. [official] *Merge a listing*,
https://developer-docs.amazon/sp-api/docs/merge-a-listing.md, read 2026-11-10:

> "You can use the Patch `merge` operation to update the `quantity` field within the `fulfillment_availability`
> without specifying other optional fields such as `restock_date` and `lead_time_to_ship_max_days`. You must provide
> non-empty values for the selector field such as `fulfillment_channel_code`. There are no changes to other optional
> fields if not included"

```json
{"patches":[{"op":"merge","path":"/attributes/fulfillment_availability",
 "value":[{"fulfillment_channel_code":"DEFAULT","quantity":20}]}]}
```

*Listings Items API* (release notes on the page) dates `merge` to May 28, 2025 and says it is "not supported for other
attributes outside of `fulfillment_availability` and `purchasable_offer`".

B4. `PRODUCT` as product type. [official] *Listings Items API*: the `PRODUCT` product type serves offer-only and
partial updates, so a quantity write does not need the item's real product type. The multi-location guide (F3) makes
`PRODUCT` mandatory for location quantity.

B5. Preview and statuses. [official] the model: `mode=VALIDATION_PREVIEW` validates without writing; submission
`status` is `ACCEPTED`, `INVALID` or `VALID` ("Only returned when the `mode` is `VALIDATION_PREVIEW`"). *Listings
Items API*: "Responses do not include issues that occur after accepting the submission for processing". *Listings APIs
FAQ*, https://developer-docs.amazon/sp-api/docs/listings-apis-faq.md, read 2026-11-10: "Your listing might have
experienced an issue after submission (an asynchronous issue)" and the place to see it is `getListingsItem`.
`ACCEPTED` is therefore an acknowledgement of receipt, not proof that the shopper-facing quantity changed.

B6. Latency after a write. [official] *Listings APIs FAQ*: "the Amazon backend updates every 15 minutes… a 15-20
minute delay for the `LISTINGS_ITEM_ISSUES_CHANGE` and `LISTINGS_ITEM_STATUS_CHANGE` notifications is normal" while
`getListingsItem` "results are available faster (within 1-5 minutes)." The FAQ gives no figure for the quantity
itself; the handling-time help page's "within 15 minutes… up to 24 hours" (A6) is about the offer and was not re-read.

B7. Order of two writes. [official] *Listings APIs FAQ*: "Amazon uses submission timestamps to ensure that updates
happen in the correct order… Amazon records the feed submission time as the timestamp for all updates within the
feed… if the `patchListingsItem` operation gets processed first, then it overrides the data provided in the
`JSON_LISTINGS_FEED`." A feed submitted before a patch does not undo the patch even if the feed finishes later.

B8. Bulk. `JSON_LISTINGS_FEED` (Feeds API v2021-06-30; role IOT or PL per *Role Mappings for SP-API Types*; the
*Listings Feed Type Values* page says Product Listing). Messages carry `messageId`, `sku`, `operationType` (`UPDATE` or
`PATCH`; `PATCH` takes the same patches as B2–B3). [official] *Submit Listings data*. Limits: "up to 25,000 SKUs in a
single request and submit five requests every five minutes" (*Listings APIs FAQ*). *Additional functionality
(Fulfillment Inbound)*: "Bulk submissions are optimal for processing 1500 items or more." Release note of
February 23, 2026 (*SP-API release notes*, https://developer-docs.amazon/sp-api/docs/sp-api-release-notes.md, read
2026-11-10): the feed reports `DONE` only after all its processing is complete.

B9. The legacy inventory feeds are gone, and Amazon's pages give two dates. [official]
- *Listings Feed Type Values*, https://developer-docs.amazon/sp-api/docs/listings-feed-type-values.md, read
  2026-11-10: "Starting July 31, 2025, the Feeds API no longer supports legacy XML and flat file listing feeds", and
  such a feed gets a fatal `processingStatus`. The release notes record the date moving: February 26, 2025 (March 31
  → June 30, 2025) and June 25, 2025 (June 30 → July 31, 2025).
- *SP-API Deprecation Schedule*, https://developer-docs.amazon/sp-api/docs/sp-api-deprecations.md, read 2026-11-10,
  lists `POST_FLAT_FILE_INVLOADER_DATA`, `POST_FLAT_FILE_LISTINGS_DATA`,
  `POST_FLAT_FILE_PRICEANDQUANTITYONLY_UPDATE_DATA`, `POST_INVENTORY_AVAILABILITY_DATA`, `POST_PRODUCT_DATA` and
  others with deprecation March 18, 2024 and **removal December 3, 2025**.
Both dates are past on 2026-11-10; the two pages disagree on which was the removal (the June 25, 2025 release note
itself calls July 31, 2025 "the removal date"). Either way a tool or a tutorial that updates FBM quantity through the
price-and-quantity flat file or the inventory-availability XML describes a path the Feeds API no longer takes.
(gap fill 2026-11-10) Amazon's original announcement, *Deprecation of Feeds API support for XML and Flat File Listings
Feeds*, https://developer-docs.amazon.com/sp-api/changelog/deprecation-of-feeds-api-support-for-xml-and-flat-file-listings-feeds.md,
read 2026-11-10, names `POST_FLAT_FILE_PRICEANDQUANTITYONLY_UPDATE_DATA`, `POST_INVENTORY_AVAILABILITY_DATA` and
`POST_FLAT_FILE_INVLOADER_DATA` among the feeds sunset and says: "This deprecation does not impact any listings feeds
submitted by sellers directly through Seller Central." [official] So the inventory flat files leaving the Feeds API did
not, on Amazon's word, take them out of Seller Central's own upload page.

### C. Reading the FBM quantity

C1. One SKU, live. `getListingsItem` with `includedData=fulfillmentAvailability` (role IOT or PL; rate 5 per second,
burst 10 in the model). The release notes on *Listings Items API* date multiple `marketplaceIds` in `getListingsItem`
and `searchListingsItems` to July 29, 2026.

C2. Many SKUs, live, with a hard ceiling. `searchListingsItems` (role IOT or PL; rate 5 per second, burst 5; `pageSize`
default 10, maximum 20; `includedData` includes `fulfillmentAvailability`; filters `withStatus` / `withoutStatus` over
`BUYABLE`, `DISCOVERABLE`; identifier types ASIN, EAN, FNSKU, GTIN, ISBN, JAN, MINSAN, SKU, UPC; sort by `sku`,
`createdDate`, `lastUpdatedDate`). [official] model. The ceiling: it "retrieves listings in batches, but is limited to
1000 listings total across all pages" (*Understanding Amazon listing status…*). A catalogue above 1,000 SKUs cannot be
walked with it unfiltered; the page's own example narrows by status (`withoutStatus=BUYABLE` with
`withStatus=DISCOVERABLE`, the listings that exist but cannot be bought).

C3. The whole catalogue, by report, hours old. [official] *Report Type Values: Inventory*,
https://developer-docs.amazon/sp-api/docs/report-type-values-inventory.md, and *Understanding Amazon listing status…*,
both read 2026-11-10:

| Report type | What Amazon says it holds | Quantity columns named | Role (Types page) |
|---|---|---|---|
| `GET_MERCHANT_LISTINGS_ALL_DATA` | "all the listings in the seller inventory… both active, inactive and suppressed" | `quantity`, `pending-quantity`, `fulfillment-channel`, `status` | DTC; IOT; PR; PL |
| `GET_MERCHANT_LISTINGS_DATA` | "seller listings which are either purchasable or have zero inventory"; "also contains listings with zero (0) inventory quantity, which are considered inactive" | `quantity`, `pending-quantity`, `fulfillment-channel` (no `status`) | DTC; IOT; PR; PL |
| `GET_MERCHANT_LISTINGS_INACTIVE_DATA` | "listings that have zero (0) quantity, listings that are blocked, listings that are suppressed, listings that are not yet opened, and listings that are past their sale end date" | as above | IOT; PR; PL |
| `GET_FLAT_FILE_OPEN_LISTINGS_DATA` | "a summary of the seller's product listings with the price and quantity for each SKU" | `quantity` | DTC; IOT; PR; PL |
| `GET_MERCHANT_LISTINGS_DATA_LITE` | "only the SKU, ASIN, Price, and Quantity fields for items that have a quantity greater than zero" | Quantity | DTC; IOT; PR; PL |
| `GET_MERCHANT_LISTINGS_DATA_LITER` | "only the SKU and Quantity fields for items that have a quantity greater than zero" | Quantity | DTC; IOT; PR; PL |
| `GET_MERCHANT_LISTINGS_DATA_BACK_COMPAT` | "An open listings report." | quantity | DTC; IOT; PR; PL |
| `GET_MERCHANT_CANCELLED_LISTINGS_DATA` | cancelled listings | n/a | DTC; IOT; PR; PL |
| `GET_MERCHANTS_LISTINGS_FYP_REPORT` | "suppressed listings, the reason each listing is suppressed, and instructions for removing each suppression" | n/a | PL (report page and Types page) |

Every row is reachable with PL or PR. Freshness: "Inventory reports are not near real-time. The SLA for stock data
freshness is 3 hours. For subsequent report calls from the same merchant account, data is 1 to 6 hours old, depending
on inventory size." One marketplace per report; the open-listings file starts with a UTF-8 byte-order mark.

C4. Not established at the source: what `pending-quantity` counts, and what `quantity` holds on a row whose
`fulfillment-channel` is Amazon's. The report page names the columns without defining them. A5 (quantity "not
supported" for FBA) says the seller does not set an FBA quantity; it does not say what the report prints. Until read on
a real file, no position is built on either. See *Open questions*.

C5. By push. `LISTINGS_ITEM_MFN_QUANTITY_CHANGE` (role PL; delivered through Amazon EventBridge, not SQS; payload
`SellerId`, `FulfillmentChannelCode`, `Sku`, `Quantity`). Amazon's advice, on *Understanding Amazon listing status…*:
"Avoid frequent polling of inventory reports by relying on this notification."; the *Notification Type Values* entry
says subscribers "do not need to frequently poll the inventory report or call… `getListingsItem`". A subscription needs an AWS destination on the application's side, which is the
door's fact, not this file's. `LISTINGS_ITEM_STATUS_CHANGE` (PL, EventBridge) fires when a listing is created, deleted
or its buyability changes.

### D. Quantity zero, and what brings a listing back

D1. Amazon's two states and the reports' four words. [official] *Understanding Amazon listing status…*: an API listing
is `BUYABLE` and/or `DISCOVERABLE`; reports say Open, Active, Inactive, Cancelled. An open listing is one that "Have
proper pricing and inventory information; Are seller-fulfilled; Have a running offer…; In Buyable status". An inactive
listing "Is out of stock; Is past scheduled sale period; Has no offer provided; Is blocked from offer by Amazon; Is not
buyable". Model: `BUYABLE` means the listing "can be purchased by shoppers. This status does not apply to vendor
listings".

D2. Out of stock is one of five reasons for Inactive, and the report does not say which. The inactive report mixes
zero quantity, blocked, suppressed, not-yet-opened and past-sale-date listings (C3). Telling them apart takes the
`quantity` column, the issues (`includedData=issues`, with `enforcements` such as `LISTING_SUPPRESSED`,
`SEARCH_SUPPRESSED`) and the offer's sale dates.

D3. What brings it back. [official] same page: "An offer must have a purchasable offer with pricing and a positive
fulfillment availability quantity." and "Restock an item: Reactivate your out of stock listing by updating its
inventory levels." For a seller-fulfilled SKU a positive quantity is the whole repair when zero quantity was the only
reason. The Featured Offer page (G201687550, v20) is quoted by the listing playbook as "Your offer can't become
featured if you're out of stock". [official, via listing playbook 2026-10-14]

D4. Closing on purpose is a different write. [official] same page: closing a listing is removing the purchasable offer
or changing the sale period; deleting is `deleteListingsItem` and "completely removes it from the seller inventory. It
does not appear in any of the reports or API data." That zero quantity keeps the SKU, its price and its history is
**[seat]**, read from the page treating restock as the whole repair; no page read says it in those words.

D5 (gap fill 2026-11-10). Deleting and zeroing are separate in Seller Central. *Stop selling a product* (G200216110,
v9), in the listing playbook's capture of 2026-10-14
(`office-mailbox/from-engineering/20261014-1510-listing-playbook-help-pages/G200216110-v9.txt`, read locally
2026-11-10): "update the inventory quantity to zero (0) and select Delete Product and Listing… If the inventory is not
updated to zero (0), the offer will remain live on the All-Offers Display since SKU deletion and inventory quantity
deletion are separate operations." [official, via listing playbook capture 2026-10-14] Whether the same holds for
`deleteListingsItem` is not stated on any developer page (the listing playbook's open question 12).

### E. What Amazon does to FBM stock without being asked, and the settings around it

E1. Pending orders. [official] *How to manage seller-fulfilled orders on Amazon* (sell.amazon.com blog, dated
January 31, 2025), https://sell.amazon.com/blog/amazon-order-management, read 2026-11-10: "Pending: The buyer's payment
is being processed or verified. You cannot ship the order or contact the buyer until payment is confirmed." and
"Pending orders occur when a buyer's payment hasn't been completed or verified. These orders are automatically updated
once the payment is cleared… Don't ship the order yet. Wait until the status changes from 'Pending' to 'Unshipped.'"
Read with A3 (decrement at placement), a pending order has already taken its units from the available quantity although
it cannot be shipped and may yet be cancelled; when it is cancelled the quantity moves again (A3 names cancellation as a
cause). [seat, from A3 and E1; no page says it of pending orders in so many words; *Open questions* 2] The Orders API model says the same of status: `PENDING` "The order has been placed but is not ready for
shipment. For standard orders, the initial order status is `PENDING`"; `PENDING_AVAILABILITY` is for pre-orders only.
[official] `orders-api-model/orders_2026-01-01.json`.

E2. The oversell and its price. A seller who writes a quantity above what is on the shelf sells units that do not
exist; the order is then cancelled by the seller or shipped late. Amazon's staff post *Navigating the Account Health
Page* (Atlas_Amazon; the forum shows it as moderated "2 years ago"),
https://sellercentral.amazon.com/seller-forums/discussions/t/8a41416f-e1ad-4221-9675-7145d5cc5e28, read 2026-11-10,
gives the seller-fulfilled metrics as that post stated them: Late Shipment Rate "Target: Under 4%", measured "over both
10-days and 30-days"; Pre-fulfillment Cancel Rate "Target: Under 2.5% - Time Window: 7-days with a one-day delay";
Valid Tracking Rate (window "30-days with a 10-day delay") and On-Time Delivery Rate ("Target: Over 90%"); and that the shipping metrics "only apply to seller-fulfilled orders".
These are an undated forum post's figures; the live targets and windows are `cx-account-health`'s to read. The reports
that carry the seller's own figures (`GET_V2_SELLER_PERFORMANCE_REPORT`) need SPI, outside the five.

E3. Handling time changes the promise, not the count. See A6. The listing playbook's read records Amazon's
June 29, 2026 requirement on accurate handling time. [official, via listing playbook 2026-10-14]

E4. Order handling capacity. [official] *Automatic minimum thresholds for order handling capacity* (News_Amazon;
"updated on February 7, 2025"),
https://sellercentral.amazon.com/seller-forums/discussions/t/d2e0afe7-b710-4c2c-b704-161baf2ada6a, read 2026-11-10:

> "The order handling capacity feature allows you to set a limit for the number of orders you can manage in a day.
> Once this limit is reached, customers who browse your products will see a delivery promise that's a day longer, and
> you'll have an additional day of handling time… order handling capacity only applies to Standard and Free Economy
> shipping options, not to Premium Shipping or Seller Fulfilled Prime orders."

> "Effective February 24, 2025, we'll automatically set a minimum threshold for you… a conservative estimate of the
> volume capacity you can handle based on your average daily orders over the past 30 days. We'll recalculate the
> minimum order handling capacity every week… If you fall below the minimum order handling capacity, we'll
> automatically adjust the threshold so it's closer to what you've been able to handle. You can set a higher limit at
> any time in Order handling settings."

The European announcement (News_Amazon, shown as "5 years ago"),
https://sellercentral-europe.amazon.com/seller-forums/discussions/t/b0d1631c8b61f0bec4847542a81d4c6f, read
2026-11-10: "If you get one more order than your limit, one day will be added to handling time for all additional
orders… limited to seller-fulfilled (non-Prime), standard shipping orders for domestic and out-of-country locations. It
does not apply to "Prime" and "Premium shipping" orders." Neither post says capacity stops orders or changes the
quantity; both describe it as lengthening the promise and the handling time. No SP-API operation for it was found (see *Only in Seller Central*).

E5. Vacation status. [official] *Deck the Halls, Not the Inbox: Vacation Mode* (TaylorR_Amazon; US forum),
https://sellercentral.amazon.com/seller-forums/discussions/t/44a5d2c0-ec70-4c58-bbbe-895a2ffcd542, read 2026-11-10:

> "change your Listings Status to Inactive. Within one hour, your seller-fulfilled listings will be removed from Amazon
> product detail pages and search results… be mindful of any pending orders that sneak through… If you have any
> Fulfillment by Amazon listings, they will remain active on Amazon."

and while inactive "Any pending orders must be resolved; You must process return requests and respond to messages from
customers within 24 hours", "Any applicable monthly subscription fees will continue to be charged", and pricing rules
on those listings are paused. The setting can be changed "for one or multiple marketplaces". The UK
post *Account vacation settings and support for the holidays*,
https://sellercentral.amazon.co.uk/seller-forums/discussions/t/e00ce497-3707-4db3-9633-8f7fd1adddad, read 2026-11-10:
"This setting temporarily removes your seller-fulfilled listings from product detail pages and search results" and,
for holiday settings, "Allow up to four hours for any changes to be reflected in your delivery promise and orders
received." FBA offers keep selling (Amazon's words). That vacation status leaves the quantity untouched, so a report
read during a vacation shows stock on SKUs that cannot be bought, is **[seat]**: neither post mentions quantity.

E6. Seller Fulfilled Prime. [official] *Seller Fulfilled Prime* (sell.amazon.com),
https://sell.amazon.com/programs/seller-fulfilled-prime, read 2026-11-10: enrolment needs prequalification on
"late-shipment, valid-tracking, and cancellation rates" and a "30-day trial". The page states no stock-holding
requirement. The policy pages (G201812300 v7, G202072550 v15, G202098380 v5) were read by the listing playbook on
2026-10-14 and not here; any stock or delivery-speed requirement is theirs to cite. Order handling capacity does not
apply to SFP orders (E4), so an SFP offer has no capacity cushion.

E7. Local Selling / in-store pickup. Not read at a source. The only first-hand trace is the Supply Sources page's
caution that multi-location inventory is not available to BOPIS sellers (F2). See *Open questions*.

### F. Multi-Location Inventory: FBM quantity per warehouse

F1. What it is and for whom. [official] *Multi-Location Inventory* (sell.amazon.com),
https://sell.amazon.com/programs/multi-location-inventory, read 2026-11-10: "Multi-location inventory is available for
all Fulfilled by Merchant sellers with single or multiple locations in the US who provide their inventory via SP-API,
Feeds API, Seller Central templ[ates]…"; "your promised delivery dates are automatically calculated from the closest
stocked warehouse to the customer"; "Currently, the program is not available for FBA inventory"; "Shipping Settings
Automation must be enabled"; FAQ: "Can I use multi-location inventory for Seller-Fulfilled Prime? Yes." Amazon's own measured claims on that page: sellers
using both "saw more than 20% higher sales conversion on average" and "had delivery dates that were over 55% more
accurate" (footnoted; the footnotes' terms were not captured).

F2. One Amazon page disagrees with two others about Seller Central and about FBA sellers. The program page's FAQ (F1)
lists "feed file upload in Seller Central, and Manage All Inventory in Seller Central" among the ways to provide
location inventory. *Multi-location inventory integration guide*,
https://developer-docs.amazon/sp-api/docs/mli-integration-guide.md (`updatedAt` 2026-09-09), read 2026-11-10, says the
same in its prerequisites ("**Seller Central feed upload:** Upload a feed file in Seller Central"; "**Seller Central
inventory management:** Use the **Manage All Inventory** option") and limits the exclusion to inventory: "Multi-location
inventory is currently not available for: FBA inventory; Inventory that is outside of the Amazon US store". *Supply
Sources API*, https://developer-docs.amazon/sp-api/docs/supply-sources-api.md (`updatedAt` 2026-09-09), read
2026-11-10, cautions that MLI "is currently not available for the following sellers": BOPIS sellers, "Sellers who use
FBA inventory" and "Sellers who manage their inventory via Seller Central". So the Supply Sources page stands alone
against the guide and the program page on Seller Central, and it excludes sellers who use FBA where the other two
exclude only the FBA inventory. Both developer pages carry the same `updatedAt` date, so the date does not settle it.

F3. How the quantity is written. [official] *MLI integration guide*: the supply source's id (a UUID) is used as the
`fulfillment_channel_code` in `fulfillment_availability`, with `productType` = `PRODUCT` and path
`/attributes/fulfillment_availability` (a `patchListingsItem` or `JSON_LISTINGS_FEED` write; the role-mapping pages name
IOT or PL for both). The locations themselves are made and read with the Supply Sources API, all six operations of
which need **SPI** (outside the five). The default location and the locations on Shipping-Settings-Automation templates
are added as supply sources automatically (*Supply Sources API*). Both developer pages list, as the last prerequisite
of an MLI integration, "Add the Selling Partner Insights role to your developer profile". Whether a location-quantity
patch succeeds for an application holding PL without SPI is therefore not established: the operation's role mapping
says PL suffices, the integration guide asks for SPI as well. No position rests on PL alone for MLI writes.

F4. The `DEFAULT` trap. [official] same guide: "(First time only) Zero out your 'default' fulfillment channel
inventory" and

> "You must set the `DEFAULT` channel to `0`. Failure to set… results in two listed offers: one multi-location
> inventory offer and one non-multi-location inventory offer… does not affect the buyability… but the
> non-multi-location inventory offer might display inaccurate inventory and shipping timelines."

On a multi-location seller, the SKU's sellable FBM stock is the sum over the location records, and a `DEFAULT` record
above zero is a second offer, not a total. [the sum is **[seat]**; the second offer is Amazon's words] The multi-offer
page shows one `replace` patch carrying a `DEFAULT` record and a supply-source record together (*Manage Amazon Haul…*,
section "Multiple fulfillment channels with MFN supply sources": `DEFAULT` 3, a location 7), so Amazon's own example
there does not zero `DEFAULT`; the two pages are in tension and the MLI guide's "must" is the explicit rule.

### G. One ASIN sold through FBA and FBM

G1. Amazon's API documents one SKU carrying both records, with FBA stock used first. [official] *Manage Amazon Haul,
Advanced Multiple-Offer, and Multiple-Fulfillment Use Cases* (`updatedAt` 2026-10-28), read 2026-11-10:

> "Selling partners who are enrolled in FBA typically create listings that are MFN or FBA-enabled. Through the SP-API,
> you can configure both options on a listing. When FBA inventory is available, it is used first. MFN inventory is
> used after the FBA inventory is depleted."

Its example sets `fulfillment_availability` to a `DEFAULT` record with a quantity and an `AMAZON_NA` record together.
The page warns that "not all Selling Partner tools support these features… limited (or no) support on Seller Central".
The page gives the behaviour no product name, states no marketplace scope, and says nothing about the price, the
handling time or the Prime badge of the offer while it runs on MFN stock. This is the only Amazon statement found of an
automatic FBA-to-FBM fallback.

G2. The practice most sellers describe is two SKUs. My Amazon Guy (P1) and SellerLogic (P3) build the backup as a
second SKU on the same ASIN; the forum sellers (P4) convert one SKU back and forth; SellerActive (P2) flips one SKU by
software. No Amazon help page on converting a SKU between channels was read: G200216110, which the research seat took
for a channel-change page, is *Stop selling a product* (capture `G200216110-v9`, opened by the verifier on 2026-11-10)
and says nothing about conversion. The claim that Amazon allows at most two offers per ASIN in one condition, one per
channel, reaches this file only through My Amazon Guy quoting a forum moderator (P1) and SellerLogic's own rule (P3).
[opinion]

G3. Which offer a shopper sees. The Featured Offer page (G201687550, v20), as the listing playbook quotes it: an
out-of-stock offer cannot be featured; fulfilment method and Prime are not considered "if all other factors are equal";
"As of September 2026, Amazon no longer maintains a seller eligibility requirement". [official, via listing playbook
capture `G201687550-v20` of 2026-10-14, re-read locally by the verifier 2026-11-10: "Your offer can't become featured
if you're out of stock"; "Fulfillment method: If all other factors are equal, offers fulfilled by Amazon or Fulfilled by
Merchant are equally likely to be featured."; the September 2026 sentence as quoted] The measured side of FBA against FBM is in *Published research*.

G4. Switching a SKU from FBM to FBA is documented; the reverse is not, on any page read. [official] *Additional
functionality (Fulfillment Inbound)*: the conversion is a `patchListingsItem` with `op: add` of the Amazon channel
record and `op: delete` with value `[{"fulfillment_channel_code":"DEFAULT"}]`; "Set `fulfillment_channel_code` to
`AMAZON_NA`, `AMAZON_EU`, `AMAZON_IN`, or `AMAZON_JP`"; the conversion fails where battery or dangerous-goods
information is missing. The mirror write (add `DEFAULT` with a quantity, delete the Amazon record) follows from the
same grammar but no Amazon page read here shows it or says what becomes of units still in fulfilment centres.
[seat] Two European forum threads from about 2022 (sellers, not Amazon) describe the Seller Central conversion not
taking while one unit was in reserve, and "for the last week nothing will convert to FBM":
https://sellercentral-europe.amazon.com/seller-forums/discussions/t/c05cc456a966777cf0e6537078935e95 and
…/t/a78714a5ee9585dfdeb522fd6d630987, read 2026-11-10. [opinion]

G5. `GET_MFN_PANEU_OFFER_STATUS` (*Report Type Values: Inventory*): "Self-fulfilled listings are not allowed in the
Pan-European FBA program, and this report can help sellers determine whether to convert any o[f them]". An FBM SKU on
an ASIN is a reason that ASIN is not Pan-EU enrolled; the programme is `beyond/programs-and-regions.md`'s. The report
is for the Spain, UK, France, Germany and Italy stores; its section on the report page carries no Roles line, and the
*Role Mappings for SP-API Types* page has no entry for it (checked 2026-11-10), so its role is unknown.

### H. Multi-Channel Fulfillment: FBA stock leaving for an order that was not placed on Amazon

H1. One pool. [official] *Grow your revenue streams with Amazon Multichannel Fulfillment (MCF)* (sell.amazon.com
blog), https://sell.amazon.com/blog/multichannel-fulfillment, read 2026-11-10: "By using a single pool of inventory
across channels". *Amazon launches innovations that power sellers' businesses across sales channels*,
https://sellingpartners.aboutamazon.com/innovations-power-sellers-businesses-across-sales-channels, read 2026-11-10:
"By sharing one pool of inventory for all sales channels, sellers who use Multi-Channel Fulfillment… see reduced
out-of-stock rates and improved inventory turnover." The Seller Central MCF help page (200332450) is reported by a
search result as saying an MCF order is "fulfilled from the same pool of inventory at Amazon fulfillment centers that
is used for FBA orders" [snippet]. There is no separate MCF quantity: every MCF unit is a unit an Amazon shopper can
no longer buy. [seat, from the "single pool" sentences]

H2. Two API versions. [official] *Fulfillment Outbound API*,
https://developer-docs.amazon/sp-api/docs/fulfillment-outbound-api.md, and *Fulfillment Outbound migration guide*,
https://developer-docs.amazon/sp-api/docs/fulfillment-outbound-migration-guide.md, read 2026-11-10. Current is
v2026-07-04 (launched July 29, 2026 per the release notes), base path `/fulfillment/outbound/2026-07-04`; legacy is
v2020-07-01, base path `/fba/outbound/2020-07-01`. The deprecation schedule read on 2026-11-10 has no Fulfillment
Outbound entry, so the legacy version has no removal date.

| v2020-07-01 | v2026-07-04 | Note |
|---|---|---|
| `getFulfillmentPreview` | `getOrderPreview` (`POST …/previews`) | read-only despite the POST |
| `deliveryOffers` (US only) | `getOffers` | |
| `createFulfillmentOrder` | `createOrder` (`POST …/orders`) | may answer 202 Accepted; new status `INVALID` |
| `listAllFulfillmentOrders` | `listOrders` (`GET …/orders`) | |
| `getFulfillmentOrder` | `getOrder` | |
| `updateFulfillmentOrder` | `updateOrder` (`PUT …/orders/{orderId}`) | |
| `cancelFulfillmentOrder` | `cancelOrder` (`PUT …/orders/{orderId}/cancel`) | |
| `getPackageTrackingDetails` | Tracking API 2026-01-30 `getShipmentTracking` ("superseded by") | grantless, NA (US only) on the role-mapping page |
| `submitFulfillmentOrderStatusUpdate` | `updateOrderStatus` (`PUT …/orders/{orderId}/status`) | sandbox-only in the v2026 model |
| none | `updatePackage` | sandbox-only in the v2026 model |
| none | `getInvoiceHeaders` | on the API page's role list; not in the model at `db2936aa` |
| `getFeatures`, `getFeatureSKU` | none: "deprecated. Refer to the documentation for supported feature constraints and services" | gap fill 2026-11-10 |
| `getFeatureInventory` | none: "deprecated. Use the `getOrderPreview` operation to check if products are fulfillable" | |
| `createFulfillmentReturn`, `listReturnReasonCodes` | none: "deprecated", "still supported in previous API version" | |

Role: every v2020-07-01 operation is AF on *Role Mappings for SP-API Operations* (`cancelFulfillmentOrder`: AF or PL).
That page, read 2026-11-10, has **no section for v2026-07-04**; the *Fulfillment Outbound API* page lists the
v2026-07-04 operations with Amazon Fulfillment. Rates in the v2026-07-04 model: 2 per second, burst 30, for every
operation except `getOffers` (5, burst 30).

H3. The write side, as fact. `createOrder` / `createFulfillmentOrder` makes Amazon ship FBA units to an address and
charges MCF fees; `updateOrder` changes an order not yet picking; `cancelOrder` cancels one. All AF. `getOrderPreview`
writes nothing: it returns whether the items are fulfillable, the planned shipments, constraints (for example
`ItemQuantityNotAvailable`) and estimated fees (fee type example `MCFTransportationFee`). [official]
`fulfillment-outbound-api-model/fulfillmentOutbound_2026-07-04.json`.

H4. When an MCF order takes units. [official] `fulfillmentOutbound_2020-07-01.json`, `FulfillmentOrderStatus`:
`Received` means the order "was received and validated… Amazon's records indicate that the seller has enough sellable
(undamaged) inventory to fulfill the order. The seller can cancel"; `Planning` means it was "sent to Amazon's
fulfillment network to begin shipment planning, but no unit in any shipment has been picked from inventory yet…
can cancel"; `Processing` means "picking… has begun… cannot cancel"; `Unfulfillable` means "fulfillment center workers
found no inventory… or… not in sellable condition". The v2026-07-04 statuses are `PROCESSING`, `COMPLETE`,
`COMPLETE_PARTIAL`, `CANCELLED`, `UNFULFILLABLE`, `INVALID`. The models do not say at which status the units leave the
fulfillable count. *Fulfillment Outbound troubleshooting*,
https://developer-docs.amazon/sp-api/docs/fulfillment-outbound-troubleshooting.md, read 2026-11-10, says the other
half: "Item shows 'in stock' in Seller Central but still constrained: Inventory may be reserved for other orders, in
transfer between fulfillment centers, or in 'unfulfillable' status" and "Inventory in 'receiving' status is not yet
available for MCF". The FBA Inventory model's `pendingCustomerOrderQuantity` is "The number of units reserved for
customer orders." (`fba-inventory-api-model/fbaInventory.json:683`); no page read says in so many words that an MCF
order's units are counted there. [seat: likely, unproven.]

H5. Holds. [official] *MCF best practices*, https://developer-docs.amazon/sp-api/docs/mcf-best-practices.md, read
2026-11-10: "`HOLD`: Reserves inventory for up to 14 days without requiring immediate shipment." v2020 model: "`Hold`
orders are automatically canceled after 14 days." *Supply Chain Portal help guide* ("Dated: July 18, 2025"),
https://supplychain.amazon.com/support/help-guide, read 2026-11-10: "if you select Create hold order, an order will
be planned and placed on hold, reserving your inventory… If the hold order isn't activated within 14 days, the order
will be canceled automatically." A hold is the one documented way a seller takes FBA units off Amazon's shelf for up
to 14 days without shipping them. (gap fill 2026-11-10) Amazon India: *What is MCF and what are the key features?*
(Smart Commerce by Amazon, dated Jan 24, 2023), https://smartcommerce.amazon.in/blog/mcf-what-is-mcf-and-key-features,
read 2026-11-10 by the verifier: "Creating a hold order will plan an order and reserve your inventory. By reserving
your inventory, you can set aside specific units from your FBA offer for a fixed duration of two weeks. Note – You can
only reserve a maximum of 250 units in a hold order… If the "hold order" isn't converted to a "Place order" within two
weeks, the order will be canceled." [official] The 250-unit cap is stated for India only; no US or EU page read states
a cap.

H6. Fill policies. [official] v2026 model: `FILL_OR_KILL` (default): if an item is "determined to be unfulfillable
before any shipment in the order has acquired the status of Processing… then the entire order is considered
unfulfillable"; `FILL_ALL`: the order "remains in a processing state until all items are either shipped by Amazon or
cancelled by the seller"; `FILL_ALL_AVAILABLE`: ship what can be shipped. v2020 model: "The `Hold` state overrides the
`FillAll` fulfillment policy… If you use the `FillAll` policy with the `Ship` state, and there are unshipped items,
then the order becomes `Unfulfillable` or `CompletePartialled` after 24 hours." Line items carry `amount`,
`cancelledAmount` and `unfulfillableAmount`.

H7. Packaging and carrier features. [official] v2020 model `FeatureSettings`: `BLANK_BOX`, `BLOCK_AMZL` ("will incur
additional fee surcharges… may increase the risk of unfulfilled or delayed deliveries… takes precedence over your
Seller Central account setting"), `OVERBOX`, `PACKING_SLIP`, `SIGNATURE_CONFIRMATION` (extra fees; US only), each
`Required` or `NotRequired`. v2026 model: `packagingOption` `UNBRANDED` or `ANY`, `overbox` `REQUIRED` or
`NOT_REQUIRED`, a packing slip, and a free-text `channel` (for example "SHOPIFY", up to 40 characters). Not every unit
qualifies for unbranded packaging or a non-Amazon carrier, so requiring a feature can make an in-stock SKU
unfulfillable for that order; in v2020-07-01 the eligible count is read with `getFeatureInventory` (AF), in v2026-07-04
with `getOrderPreview` (AF). *Multichannel Fulfillment (MCF)* (supplychain.amazon.com),
https://supplychain.amazon.com/multichannel-fulfillment, read 2026-11-10, says today: "We pick and pack orders with
unbranded packaging by default". Service tiers in the v2026 model: `STANDARD`, `EXPEDITED`, `PRIORITY` (Canada, India,
Mexico only), `SCHEDULED` (Japan).

H8. Fees are read, not remembered. The same supplychain.amazon.com page carried a banner on 2026-11-10: "Updates to
MCF US fulfillment fees go into effect January 15, 2027." The amounts are `areas/holding-costs.md`'s; the live estimate
for a given order is `getOrderPreview`'s fee list.

H9. Amazon's own guidance on stock for MCF. [official] *Supply Chain Portal help guide*: "as a best practice, we
recommend maintaining at least 8 weeks of cover and 100 units that are received and stored in a fulfillment center",
given inside its list of cases where delivery "may be longer" ("Orders including items without sufficient inventory"),
which also names "Inventory showing in the Reserved column". This is Amazon's recommendation to MCF
users, dated July 18, 2025, on a page addressed to Supply Chain Portal merchants; it is not a rule and not an
eligibility test.

H10. Keeping an outside storefront's stock number right. [official] *MCF best practices*: subscribe to
`FULFILLMENT_ORDER_STATUS` (AF; SQS; payload version 2026-07-04 added September 30, 2026) and
`FBA_INVENTORY_AVAILABILITY_CHANGES` (AF; SQS); "call the `getInventorySummaries` operation once a day… Avoid calling
this operation more than once every 24 hours to prevent receiving stale inventory data"; without notifications,
"Maintain an internal inventory record based on orders placed and canceled… Operate with safety stock settings to
prevent overselling between sync jobs". `getInventorySummaries` is AF or PL. The safety-stock sentence is Amazon's
advice to integrators; it names no number. (gap fill 2026-11-10) *Notification Type Values* marks
`FULFILLMENT_ORDER_STATUS` payload version `1.0` as deprecated ("Migrate to `2026-07-04`"); no removal date is on the
deprecation schedule read 2026-11-10.

H11. Buy with Prime. The Buy with Prime knowledge-centre page gave 403 to a plain GET. Search results report that Buy
with Prime orders are fulfilled through MCF from FBA inventory. [snippet] Nothing is built on it.

H12. MCF and AWD. [official] *Amazon launches innovations…* (aboutamazon): Multi-Channel Distribution lets a seller
"hold one unified inventory pool in AWD that can serve all channels", and "consolidating into a single inventory pool
in AWD reduces total inventory stock needs by an average of 20%" (Amazon's own claim). AWD is
`beyond/programs-and-regions.md`'s and its reads need a role outside the five.

### I. Amazon-sold stock that never sits on FBA's shelves

I1. Own warehouse or a 3PL: this is plain FBM. Amazon knows only the number the seller (or the 3PL's software, through
the seller's authorisation) writes (sections A–B), per location if multi-location inventory is used (F).

I2. External Fulfillment. [official] *External Fulfillment Inventory*,
https://developer-docs.amazon/sp-api/docs/external-fulfillment-inventory.md, read 2026-11-10: the channels are "Seller
Flex / FBA Onsite; Multi Seller Flex; Easy ship; Self ship; MFN Self Delivery; Amazon Pharmacy"; the API lets sellers
"publish absolute location-level inventory from their own inventory management systems" with `batchInventory`, up to
ten requests a batch; `locationId` is `DEFAULT` for single-location MFN, a channel location id for multi-location MFN,
and a four-character warehouse code for Seller Flex. Role: DTC (Restricted), and the seller must be allow-listed. All
outside the five.

I3. Easy Ship. [official] *Easy Ship API*, https://developer-docs.amazon/sp-api/docs/easy-ship-api.md, read
2026-11-10: available in Mexico, India, Turkey, Australia, Singapore, Japan, the Netherlands and Poland. Role DTC
(Restricted). Easy Ship stock is the seller's own, written as FBM quantity.

I4. AWD and Supply Chain by Amazon hold stock that is upstream of FBA and cannot be bought until it reaches a
fulfilment centre; `beyond/programs-and-regions.md` owns them.

### J. Orders as the other half of the count

J1. `searchOrders` (Orders API v2026-01-01; roles include AF, FA, PR and PL, so the five carry it). [official]
`orders_2026-01-01.json` and *Orders API rate limits*, https://developer-docs.amazon/sp-api/docs/orders-api-rate-limits.md,
read 2026-11-10: rate **0.0056 requests per second** (one every three minutes), burst 20; exactly one of
`createdAfter` or `lastUpdatedAfter`; `fulfilledBy` `MERCHANT` or `AMAZON`; `fulfillmentStatuses`
`PENDING_AVAILABILITY`, `PENDING`, `UNSHIPPED`, `PARTIALLY_SHIPPED`, `SHIPPED`, `CANCELLED`, `UNFULFILLABLE`; 1–100
results a page. `getOrder`: 0.5 per second, burst 30.

J2. The v0 operations (`getOrders` and the rest) were deprecated January 28, 2026 with removal March 27, 2027
(deprecation schedule). `ORDER_CHANGE` (roles AF, DTC or IOT; SQS) is the push for order status and buyer-requested
cancellation; `ORDER_STATUS_CHANGE` was removed July 29, 2026.

J3. Order reports: `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL` (AF; DTC; IOT; PR; PL) and
`…_BY_ORDER_DATE_GENERAL` (AF; DTC; IOT; PR) are within the five. `GET_CONVERGED_FLAT_FILE_PENDING_ORDERS_DATA` is PL.
`GET_FLAT_FILE_PENDING_ORDERS_DATA` / `GET_PENDING_ORDERS_DATA` are IOT only; the unshipped-order reports
(`GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_SHIPPING`, `GET_ORDER_REPORT_DATA_SHIPPING`) are DTC.

### K. Roles at a glance (from *Role Mappings for SP-API Operations* and *…for SP-API Types*, read 2026-11-10)

| Read or write | Role Amazon names | Within the five? |
|---|---|---|
| Listings Items v2021-08-01, every operation | IOT; PL | yes (PL) |
| Product Type Definitions | IOT; PL | yes (PL) |
| `JSON_LISTINGS_FEED` | IOT; PL | yes (PL) |
| Listing reports in C3 (including `GET_MERCHANTS_LISTINGS_FYP_REPORT`: PL only) | PL among others | yes |
| `GET_MFN_PANEU_OFFER_STATUS` | none stated (no Roles line; absent from the Types page) | unknown |
| Location-quantity write under MLI (`patchListingsItem` with a supply-source code) | IOT; PL on the role mapping; the MLI guide adds SPI as a prerequisite | not established |
| Tracking API 2026-01-30 `getShipmentTracking` | none (grantless), NA (US only) | yes, needs no role |
| `LISTINGS_ITEM_MFN_QUANTITY_CHANGE`, `_STATUS_CHANGE`, `_ISSUES_CHANGE` | PL | yes |
| Fulfillment Outbound v2020-07-01 | AF (`cancelFulfillmentOrder`: AF; PL) | yes |
| Fulfillment Outbound v2026-07-04 | AF (API page; absent from the role-mapping page) | yes, on the API page's word |
| `FULFILLMENT_ORDER_STATUS`, `FBA_INVENTORY_AVAILABILITY_CHANGES` | AF | yes |
| FBA Inventory `getInventorySummaries` | AF; PL | yes |
| Orders v2026-01-01 `searchOrders`, `getOrder` | AF, FA, PR, PL and others | yes |
| `ORDER_CHANGE` | AF; DTC; IOT | yes (AF) |
| MCF order feeds (`POST_FLAT_FILE_FULFILLMENT_ORDER_REQUEST_DATA` and the XML and cancellation variants) | AF | yes; whether these feed types are still accepted was not checked |
| Supply Sources, all six operations | SPI | no |
| External Fulfillment Inventory / Shipping / Returns; Easy Ship; Merchant Fulfillment | DTC (Restricted) | no |
| `GET_V1/V2_SELLER_PERFORMANCE_REPORT` | SPI | no |
| `POST_ORDER_FULFILLMENT_DATA` (ship confirmation) | DTC; IOT | no |
| `GET_FLAT_FILE_PENDING_ORDERS_DATA`, `GET_PENDING_ORDERS_DATA` | IOT | no |

### L. Against the listing playbook's `listing-writes.md`: what is the same, what is specific to quantity

That file (sections A–I; not re-read in full here, headings and the quantity lines only) covers `patchListingsItem`,
`putListingsItem`, validation preview, submission statuses, issues, deletion (its G) and the bulk feed (its H). All of
that applies unchanged to a quantity write: same operation, same roles, same preview mode, same `ACCEPTED` /
`INVALID` / `VALID`, same asynchronous issues, same feed.

Specific to quantity, and stated in this file: (1) `merge` exists for this attribute and one other, and keeps handling
time and restock date (B3); a `replace` rewrites the array (B2). (2) The read-back is not the write: the attribute
shows what was sent, the `fulfillmentAvailability` data set shows what is left (A1). (3) Amazon changes the number
itself on every order and cancellation (A3), so a write is a correction of a moving counter, not a setting. (4) The
record is keyed by channel, an FBA record takes no quantity, a supply-source id is a channel code, and `DEFAULT` must
be zero under multi-location inventory (A4, A5, F3, F4). (5) `PRODUCT` suffices as product type (B4). (6) A patch and a
feed are ordered by submission time (B7). (7) Zero is a state of the listing, not a deletion (D).

(gap fill 2026-11-10, verifier's read of `listing-writes.md` B10–B14 and D) Where the two files overlap they agree: the
op enum and the "adds or replaces" wording, top-level-only patching, `merge` from May 28, 2025 and its two attributes,
`PRODUCT` for partial updates, 25,000 messages a feed and five feeds per five minutes, `DONE` only after all
processing since February 23, 2026, `ACCEPTED` as not done, 1–5 minutes for `getListingsItem` against 15–20 minutes for
the notifications, and the submission-timestamp answer. Differences: (a) `listing-writes.md` names Product Listing
alone as the role; this file gives IOT or PL from the role-mapping page, which carries both; no conflict for the door.
(b) It adds facts this file lacks and that bear on a quantity feed: feed submissions "are not guaranteed to be
processed in the same order"; "a feed with only a few records can still take several hours"; "The suggested minimum
feed size is 1,500 items" (the workflows guide; this file cites the same 1,500 from *Additional functionality*);
validation previews are limited to 20 requests per application per second. (c) It notes the FAQ's timestamp example
is about inventory updates and does not extend it to content; for this file that example is exactly the case. (d) It
records that `putListingsItem` for sellers "merges previously submitted sales term attributes"; whether
`fulfillment_availability` counts as a sales term for that rule is not stated on any page read by either seat.

## What practitioners add

**P1. My Amazon Guy (Steven Pope), "How to Run Amazon FBA and FBM Together Without Losing Rank"**, dated August 10,
2026, updated September 14, 2026, https://myamazonguy.com/fba/how-to-run-amazon-fba-and-fbm/, read 2026-11-10.
[opinion] Their practice, in their words: "One ASIN holds two offers; FBA offer wins the Buy Box; FBM offer catches
the stockout; Suffix the SKU, never duplicate; Warm the backup before Q4". The FBM offer is a second SKU on the same
ASIN, "each with its own SKU and its own inventory pool"; they tell clients to "Set the handling time your warehouse
actually hits", "Load a small live quantity, never zero", "Price the offer to cover your own shipping" and "Push a
handful of real orders through it every month". Their Cyber Week figure: "Hold 15% to 20% of your peak 30-day forecast
in the FBM offer". They distinguish "dual fulfillment" (both offers live) from "hybrid fulfillment" (software swaps one
offer from FBA to FBM when FBA stock reaches zero), and say "the integration platforms that run it document a changeover
of roughly 15 minutes" per swap (no platform named; not followed). They report "a moderator answering a Seller Central forum thread
described a maximum of two offers per ASIN, one per fulfillment channel, with anything past that treated as offer
manipulation"; the thread itself was not found. They cite "Roughly 82% of Amazon sellers run FBA" and Jungle Scout's 9%
of sellers on both channels, without links this seat followed. The article's claim that the backup "protects the rank
and the ad performance" is asserted, not measured.

**P2. SellerActive / Marketplace Management, "auto-flip" setting**,
https://www.selleractive.com/support/amazon-fba-fbm-autoflip-fulfillment-type, read 2026-11-10. [opinion] A tool's
description of the one-SKU approach: "For Amazon US only… Marketplace Management will detect when your FBA quantity
goes to 0 and will update your Fulfilled by Status to 'Merchant' as well as send your FBM quantity to Amazon." And the
way back: "if/when you send in more FBA inventory to Amazon for the same SKU… Amazon will switch your listing from FBM
to FBA and SKU ABC123 will display your FBA inventory", adding that "For some SKUs, Amazon may require additional
information when the SKU is converted back to FB[A]". This is a tool's account of Amazon's behaviour, consistent with
G1 and G4 but not Amazon's statement.

**P3. SellerLogic repricer FAQ**,
https://support.sellerlogic.com/faq/how-do-i-list-an-asin-for-an-fba-and-fbm-product-so-that-they-do-not-interfere-with-each-other,
read 2026-11-10. [opinion] "Both SKUs must have the BuyBox strategy set. Then the FBA product price is optimized for
the BuyBox and the FBM product catches up with the FBA product. If the FBA product is sold out, the FBM product is
optimized for the BuyBox until the FBA product is in stock again. Note: FBA & FBM Prime offers must not be combined.
No more than 2 offers in the same condition (FBA & FBM) may be used." The pitfall they name is the seller's two SKUs
repricing against each other.

**P4. European forum sellers on converting FBA to FBM when FBA runs out** (two threads, shown as "4 years ago"), URLs
in G4, read 2026-11-10. [opinion] One seller of twelve years: "always convert our FBA stock to FBM when it runs out
before new stock reaches the warehouse… however for the last week nothing will convert to FBM"; another could not
convert while one unit was in reserve. The practice is old and common; the conversion is not always available at the
moment it is wanted.

**P5. Linnworks / SkuVault, "Sync online sales with quantity updates and buffers"**,
https://www.linnworks.com/blog/sync-online-sales-with-quantity-updates-and-buffers/ (published 2018-08-31, modified
2025-04-22 per the page metadata), read 2026-11-10 by the verifier with a browser user-agent (the research seat got
403). [opinion] "Buffers are holds you can set for your inventory on your specific marketplace channels… You can set a
max buffer so even if you have 500 water bottles in your warehouse, Amazon will only list that you have 10 available to
sell. Once those products sell, SkuVault Core will always update Amazon… back to that max buffer number so long as you
have the inventory in stock". Three buffer types: "'Maximum Quantity'", "'Push Constant Quantity'" ("always have a
certain amount of product available no matter how much you physically have on hand") and "'Low Quantity Cutoff'" ("a
cutoff in available quantity at a designated point above zero to prevent oversells on fast selling items"). The page
also argues a capped quantity "creates a sense of urgency to buyers". Its stated sync is "real-time throughout the day";
no interval in minutes is given.

**P6. Veeqo, "How to Guarantee You Never Oversell in Your Ecommerce Business"** (February 1, 2018),
https://www.veeqo.com/blog/prevent-overselling, read 2026-11-10. [opinion] General practice only: accurate stock
takes, reorder points, "Update stock levels regularly", "Dedicate stock to separate stores". No Amazon-specific
setting or sync interval is stated. A seller thread on Amazon's European forum complaining of Veeqo and Amazon stock
not syncing appeared in search and was not opened. [snippet]

**P7. Buffer sizes others publish** (search results only, not opened). [snippet] Jarvio: reserve 15–20% of shared
inventory as buffer per channel. An unnamed guide: buffer equal to the units that could sell elsewhere during the
worst observed sync delay, plus one. Another: hold back 5–10% for Amazon FBM. These are those writers' figures.

**P8. UpSeller ERP,《库存同步使用指南》** (更新于 2026年09月10日), https://www.upseller.com/zh-CN/doc-article/1253, read
2026-11-10. [opinion] "同一个产品在多个店铺售卖时，当其中一个店铺有销售，系统会将最新库存数量自动同步至其他店铺" (when
one store sells a unit, the system pushes the new stock figure to the other stores). "为避免在线产品更新库存与实际不符，
导致店铺超卖或少卖… 库存清单，各商品 SKU 库存数与线下实际库存数保持一致；商品SKU与产品SKU之间的配对关系一定要准确" (to
avoid overselling or underselling, the warehouse count must match the physical count and the SKU pairing must be
exact). Daily sync quotas by plan (免费版 10000 … 专业版 不限). And: "亚马逊 FBA的订单 不支持在UpSeller上库存…" (Amazon
FBA orders are not handled by its stock sync; the sentence was cut in the capture). The tool's sync covers FBM only.

**P9. The tools named in the brief that could not be read.** Sellbrite, Rithum (ChannelAdvisor), 店小秘, 马帮, 易仓 and
领星: no help page of theirs on Amazon FBM quantity sync, buffers or sync interval was opened in this session (searches
returned third-party summaries or nothing). Rithum's product page is reported by a search result as offering rules to
"hide or route orders differently if an item is nearly out of stock". [snippet] The AMZ123 Q&A pages opened
(https://www.amz123.com/ask/ShUaMhFq, 2024-09-15, on FBM shipping settings; …/vf0fisqD on exporting FBM stock) are
generic walkthroughs with nothing an experienced seller lacks. This is a gap of this file, listed in *Open questions*.

**P10 (gap fill 2026-11-10). SellerActive, "How do I add Maximum and Minimum inventory buffers to my listings?"**,
https://www.selleractive.com/support/adding-max-and-min-buffers, read 2026-11-10 by the verifier. [opinion] "These
buffers are marketplace specific… Inventory buffers can interact with FBA quantities on non-Amazon marketplaces. For
example, a Maximum Buffer will work with an FBA SKU that is on eBay but it will not impact the quantity on the Amazon
site itself." The fields are "Min Threshold (MinListing Buffer)" and "Max Visible (MaxListing Buffer)", and "Saving the
buffer will immediately prompt an update to the sales channel." A tool's account: a buffer on FBA stock acts on the
outside storefront that MCF serves, never on Amazon's own FBA count, which the seller does not set (A5).

## Published research

Two studies on Amazon itself measure the weight of fulfilment method in who gets the Featured Offer (the Buy Box).
Neither measures a seller switching one ASIN between FBA and FBM, and none found here measures the sales effect of an
FBM backup offer during an FBA stock-out.

- **Chen, Mislove and Wilson, "An Empirical Analysis of Algorithmic Pricing on Amazon Marketplace", WWW 2016**,
  https://www.khoury.northeastern.edu/home/cbw/static/pdf/amazon-www16.pdf, read 2026-11-10. [research] Four months of
  data on 1,641 best-seller products. A random-forest classifier predicted the Buy Box winner with "75–85% accuracy
  even in the most challenging cases with many sellers". Table 1, relative feature importance: price difference to the
  lowest 0.36; price ratio to the lowest 0.33; positive feedback 0.10; is Amazon the seller 0.10; feedback count 0.06;
  average rating 0.03; "Is the Product FBA?" 0.02. The authors' caveat: they crawled without a Prime account, and
  "Amazon may alter pages for Prime users, typically to highlight sellers and products that are eligible for expedited
  Prime shipping. Thus, some of our analysis and conclusions may not extend to Prime users." They cite 82% of sales
  going through the Buy Box.
- **Raval, "Steering in One Click: Platform Self-Preferencing in the Amazon Buy Box"**, draft dated December 31, 2023,
  https://deveshraval.github.io/buyBox.pdf, read 2026-11-10 (text extracted from the PDF; first pages and the passages
  quoted). [research] "Using data on hundreds of thousands of products and several countries, I show that the Amazon
  platform substantially prioritizes its retail arm and fulfillment arm in the recommendation algorithm." Against an
  Amazon Retail offer, "a perfect FBA seller receives a penalty equivalent to a 16% increase in price… while a FBM
  offer for the same seller receives a penalty equivalent to a 46% increase in price"; "These self-preferencing effects
  are quite similar across countries." The paper notes that shipping time is not observed for all offers, so "estimated
  premia over FBM potentially include shipping time differences." Its model "correctly predicts the Buy Box offer 88%
  of the time across all categories, and 80% of the time for products with multiple offers." It cites Feedvisor (2020)
  for 80% of sales coming through the Buy Box.

The two disagree in size (0.02 importance in 2015-era data without Prime; a 30-point price-equivalent gap between FBA
and FBM in the later data), and both predate Amazon's September 2026 statement that it no longer keeps a seller
eligibility requirement for the Featured Offer (G3). Amazon's own published figures on FBM are its marketing claims
for multi-location inventory (F1) and for AWD pooling (H12).

Operations research on pooled inventory across channels (risk pooling) is `areas/restock-and-forecast.md`'s ground and
was not searched here.

## Stable enough for a skill

- The two copies of the FBM quantity and which is live (A1–A2).
- Amazon decrements at order placement and counts cancellations; zero stops orders (A3).
- The record is keyed by channel; codes; quantity is MFN-only (A4–A5).
- `merge` against `replace` on `fulfillment_availability`; `PRODUCT`; nothing nested (B1–B4).
- `ACCEPTED` is not applied; issues arrive later; read-back in 1–5 minutes, notifications 15–20 minutes (B5–B6).
- Patch and feed are ordered by submission time (B7).
- Legacy inventory feeds are removed; the two dates Amazon gives (B9).
- The listing reports, what each includes, their 3-hour / 1–6-hour staleness, the 1,000-listing ceiling of
  `searchListingsItems` (C2–C3).
- Inactive has five causes; zero quantity is one; a positive quantity plus a priced offer reopens it (D).
- Pending orders: placed, counted, not shippable (E1).
- Order handling capacity lengthens the promise and never blocks orders; excludes Premium and SFP; automatic minimum
  from February 24, 2025 (E4).
- Vacation status removes FBM offers within about an hour and leaves FBA offers live (E5); that it leaves quantities
  as they were is the seat's inference, not a source.
- Multi-location inventory: US store only, not FBA stock, supply-source id as channel code, `DEFAULT` must be zero,
  Supply Sources needs SPI and the MLI guide lists SPI as an integration prerequisite; Amazon's pages disagree on
  Seller Central (F).
- Amazon's documented one-SKU dual configuration with FBA stock used first (G1), stated with its caveats.
- MCF draws on the FBA pool; the two API versions and the mapping; hold 14 days; fill policies; features can make
  in-stock units unfulfillable for an order; preview is the read (H).
- `searchOrders` is one request every three minutes (J1).
- Role table (K).

## What cx must read at run time

**R1. Live FBM quantity of a SKU.** `getListingsItem`, `includedData=fulfillmentAvailability` (plus `attributes`,
`summaries`, `issues` as needed). Fields: `fulfillmentAvailability[].fulfillmentChannelCode`, `.quantity`; in
attributes, `fulfillment_availability[]` with `quantity`, `lead_time_to_ship_max_days`, `restock_date`. **Role: PL**
(or IOT). Rate 5/s, burst 10. Pitfalls: the attribute is the last submission, not the live count (A1); a
multi-location SKU has one record per supply source and `DEFAULT` should read 0 (F4); an FBA record has no quantity
(A5); a SKU with both records exists (G1).

**R2. Live FBM quantities across SKUs.** `searchListingsItems` with `includedData=fulfillmentAvailability`.
**Role: PL** (or IOT). Rate 5/s, burst 5; 20 a page; **1,000 listings in total**. Pitfall: above 1,000 SKUs it is a
filtered view (by status, identifier or date), not an inventory.

**R3. The catalogue's quantities by report.** `GET_MERCHANT_LISTINGS_ALL_DATA` (columns `seller-sku`, `asin1`,
`quantity`, `pending-quantity`, `fulfillment-channel`, `merchant-shipping-group`, `status`), or
`GET_FLAT_FILE_OPEN_LISTINGS_DATA` / `GET_MERCHANT_LISTINGS_DATA_LITE` / `_LITER` for SKU and quantity only.
**Role: PL or PR** (also DTC, IOT). Freshness: 3-hour stock SLA; a repeat request returns data 1–6 hours old. One
marketplace per report. Pitfalls: `_LITE` and `_LITER` omit zero-quantity SKUs, so absence there is not deletion;
`GET_MERCHANT_LISTINGS_DATA` has no `status` column; the meaning of `pending-quantity` and of `quantity` on
Amazon-fulfilled rows is not sourced (C4); vacation status does not zero the column (E5).

**R4. Why a SKU is inactive.** `GET_MERCHANT_LISTINGS_INACTIVE_DATA` (**Role: PL or PR**, also IOT) for the list;
`getListingsItem` with `summaries` and `issues` (**PL**) for the reason. Pitfall: five causes share the report (D2).

**R5. Dry run of a quantity write.** `patchListingsItem` with `mode=VALIDATION_PREVIEW`. **Role: PL** (or IOT).
Returns `VALID` or `INVALID` with issues; writes nothing. The write itself is the same call without the mode; bulk is
`JSON_LISTINGS_FEED` (**PL** or IOT; 25,000 SKUs a feed, five feeds per five minutes).

**R6. Seller-fulfilled orders that have taken stock.** `searchOrders` with `fulfilledBy=MERCHANT` and
`fulfillmentStatuses` (`PENDING`, `UNSHIPPED`, `PARTIALLY_SHIPPED`, `CANCELLED`). **Role: AF, FA, PR or PL.** Rate
0.0056/s, burst 20; 100 a page. Or `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL` (**AF, PR or PL**), or
`GET_CONVERGED_FLAT_FILE_PENDING_ORDERS_DATA` (**PL**). Pitfall: the rate makes `searchOrders` a periodic read, not a
per-SKU lookup.

**R7. Whether FBA units can serve an MCF order, and at what fee.** `getOrderPreview` (v2026-07-04) or
`getFulfillmentPreview` (v2020-07-01). **Role: AF.** Rate 2/s, burst 30. Returns fulfillability, planned shipments,
constraints, estimated fees. Pitfalls: a POST that writes nothing; "in stock" in Seller Central can still be
constrained (reserved, in transfer, unfulfillable, receiving); requiring unbranded packaging or blocking Amazon
Logistics narrows the eligible units.

**R8. MCF orders open and recent.** `listOrders` / `getOrder` (v2026-07-04) or `listAllFulfillmentOrders` /
`getFulfillmentOrder` (v2020-07-01). **Role: AF.** Fields: status, `action` (`SHIP`/`HOLD`), policy, line `amount`,
`cancelledAmount`, `unfulfillableAmount`, `channel`. Pitfall: a `HOLD` order reserves units for up to 14 days and then
cancels itself.

**R9. FBA units an Amazon shopper or an MCF order can take now.** `getInventorySummaries` with `details=true`
(**Role: AF or PL**): `fulfillableQuantity`, `reservedQuantity.pendingCustomerOrderQuantity` and the other reserved
parts. Owned by `areas/stock-states.md`. Amazon's MCF guidance is to call it once a day and rely on notifications
between.

**R10. Units eligible for a packaging or carrier feature (legacy API only).** `getFeatureInventory`, `getFeatureSKU`,
`getFeatures` (v2020-07-01; **Role: AF**); deprecated in v2026-07-04 in favour of `getOrderPreview`.

**R11. Channel codes valid for this seller and store.** `getDefinitionsProductType` with `sellerId` (**Role: PL** or
IOT): the enumeration of `fulfillment_channel_code` under `fulfillment_availability`, and the schema's own description
of `restock_date`, `lead_time_to_ship_max_days` and any `is_inventory_available`.

**R12. MCF fee amounts and dated changes.** `getOrderPreview` for an order's estimate (AF);
https://supplychain.amazon.com/multichannel-fulfillment and the Seller Central fee pages for the schedule (a US change
is announced for January 15, 2027). Amounts are `areas/holding-costs.md`'s.

**R13. Push instead of polling** (needs an AWS destination; the door's matter): `LISTINGS_ITEM_MFN_QUANTITY_CHANGE`
(**PL**, EventBridge), `LISTINGS_ITEM_STATUS_CHANGE` (**PL**, EventBridge), `ORDER_CHANGE` (**AF**, SQS),
`FULFILLMENT_ORDER_STATUS` (**AF**, SQS), `FBA_INVENTORY_AVAILABILITY_CHANGES` (**AF**, SQS).

## Reads that need a role outside the five

- **Supply Sources API** (`getSupplySources`, `getSupplySource`, create, update, status, archive): **SPI**. Would open
  the list of the seller's locations, their ids (the channel codes of multi-location records), addresses, operating
  hours and status. Without it a multi-location SKU's records can still be read through R1 as opaque UUIDs.
- **`GET_V2_SELLER_PERFORMANCE_REPORT` / `GET_V1_…`**: **SPI**. Would open the seller's late shipment, pre-fulfilment
  cancellation, valid tracking and on-time delivery rates, the measured cost of overselling.
- **External Fulfillment Inventory / Shipping / Returns**: **DTC (Restricted)** plus allow-listing. Would open
  location-level stock for Seller Flex, Multi Seller Flex, Easy Ship, Self Ship and MFN Self Delivery.
- **Easy Ship API; Merchant Fulfillment API**: **DTC (Restricted)**. Would open scheduled pickups and purchased
  shipping for seller-fulfilled orders.
- **`GET_FLAT_FILE_PENDING_ORDERS_DATA`, `GET_PENDING_ORDERS_DATA`**: **IOT**. Pending orders by report; the PL-reachable
  `GET_CONVERGED_FLAT_FILE_PENDING_ORDERS_DATA` and `searchOrders` cover the same ground.
- **`GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_SHIPPING`, `GET_ORDER_REPORT_DATA_SHIPPING`; `POST_ORDER_FULFILLMENT_DATA`;
  Orders v0 `confirmShipment`**: **DTC** (the last two also IOT). Unshipped orders with addresses, and ship
  confirmation.
- **AWD API**: Amazon Warehousing and Distribution role; `beyond/programs-and-regions.md`.

## Only in Seller Central

Established by finding no operation, report type or notification for it in the pages and models read (the Listings
Items, Orders, Supply Sources, Fulfillment Outbound and Notifications pages; the inventory report list), not by a
statement of Amazon's that none exists:

- Vacation / listing status (Settings → Account Info → Store Status → Vacation Settings, per marketplace) and holiday
  settings. No API read of whether a store is on vacation was found; its trace in the API is FBM SKUs that have
  quantity and are not `BUYABLE`.
- Order handling capacity (the limit, the automatic minimum, whether it has tripped today).
- Account default handling time, Automated Handling Time, shipping templates and Shipping Settings Automation. A SKU's
  own `lead_time_to_ship_max_days` and its `merchant-shipping-group` name are readable (R1, R3); the template's content
  is not.
- The Seller Central setting that blocks Amazon Logistics for all MCF orders (the API's `BLOCK_AMZL` "takes precedence
  over your Seller Central account setting", so the setting exists and is not read by any operation found).
- Enrolment state of Seller Fulfilled Prime and its trial.
- The "Convert to Fulfilled by Merchant / by Amazon" action as Seller Central performs it; the API equivalent is the
  patch in G4.

## The seller's choices

Each is the seller's; none is picked here.

1. **Whether to publish the true shelf count or less.** Publishing all of it sells every unit and exposes the seller
   to an oversell whenever the shelf count is wrong or another channel sells first; publishing less (a buffer, a cap)
   lowers that risk and hides sellable units, and a SKU can read zero on Amazon while stock exists. Tools and writers
   name their own buffer kinds and sizes (P5, P7, P10); Amazon names none (H10).
2. **How often the number is corrected.** Amazon decrements for its own orders; nothing but the seller's write
   accounts for sales elsewhere, damage or receipts. More frequent writes narrow the oversell window; the reports that
   verify them lag by hours (C3).
3. **Zero quantity, a longer handling time, vacation status, or closing the offer, when the seller cannot ship.** Zero
   makes the one SKU inactive; a longer handling time keeps it selling with a later promise; vacation status takes
   every FBM offer in that marketplace down and leaves FBA selling; closing the offer removes price and sale dates.
4. **An FBM offer behind an FBA offer, or not.** With it, the ASIN can stay buyable through an FBA stock-out, at the
   seller's handling time and under seller-fulfilled metrics; without it the ASIN is unavailable until FBA stock
   lands. Whether that protects rank is asserted by practitioners (P1) and not measured in anything read.
5. **Two SKUs, one SKU converted by hand or by a tool, or one SKU carrying both records.** Two SKUs keep both offers
   live and can reprice against each other (P3); conversion leaves a gap and has been reported to fail (P4); the
   dual-record SKU is Amazon's documented API behaviour with little Seller Central support (G1).
6. **How the FBM backup is priced and what quantity it shows.** Practitioners give their own answers (P1, P3).
7. **Whether FBA stock also serves other channels through MCF.** One pool means fewer units stranded on the wrong
   channel and means an outside sale can empty the Amazon offer; a `HOLD` or a withheld quantity on the outside
   storefront are the levers Amazon documents (H5, H10).
8. **Which MCF features to require.** Unbranded packaging and blocking Amazon Logistics narrow eligible units and the
   latter adds a surcharge (H7); `FILL_OR_KILL`, `FILL_ALL` and `FILL_ALL_AVAILABLE` trade a complete order against a
   shipped one (H6).
9. **One location or several for FBM stock (US).** Multi-location inventory changes the delivery promise by buyer
   location and changes how the quantity is written (F); it needs Shipping Settings Automation.
10. **Order handling capacity above Amazon's automatic minimum.** A higher limit keeps the shorter promise through a
    spike; a lower one lengthens it sooner (E4).

## Open questions

For a first run on a real account:

1. What `pending-quantity` holds, and what `quantity` holds on rows with an Amazon `fulfillment-channel`, in
   `GET_MERCHANT_LISTINGS_ALL_DATA` (C4).
2. Whether the live `fulfillmentAvailability.quantity` falls when an order is `PENDING` (A3 and E1 say it should) and
   rises on cancellation, and how soon.
3. The product-type schema's descriptions of `restock_date`, `lead_time_to_ship_max_days` and `is_inventory_available`
   and the channel-code enumeration for the account (R11).
4. Whether a SKU carrying both `DEFAULT` and an `AMAZON_*` record (G1) is accepted in the seller's store, how it shows
   in Seller Central and in the listing reports, and what offer (price, handling time, Prime) a shopper sees once FBA
   stock is gone.
5. What a `delete` of the Amazon record plus an `add` of `DEFAULT` (FBA to FBM by API) does while FBA units are
   fulfillable, reserved or inbound.
6. At which Fulfillment Outbound status an MCF order's units leave `fulfillableQuantity`, whether they appear under
   `pendingCustomerOrderQuantity`, and how an MCF shipment is typed in the inventory ledger
   (`GET_LEDGER_DETAIL_VIEW_DATA`, AF).
7. Whether the door's application is granted Fulfillment Outbound v2026-07-04 on the AF role, given the role-mapping
   page omits that version.
8. Whether a vacation-status store is detectable from the API beyond "quantity above zero and not `BUYABLE`".

For the office:

9. Which date is right for the removal of the legacy inventory feeds (July 31, 2025 on the feed page and in the
   June 25, 2025 release note; December 3, 2025 on the deprecation schedule), if it matters to any wording. Either way
   Amazon's announcement says Seller Central uploads were not affected (B9).
10. Multi-location inventory and Seller Central: the program page and the MLI integration guide list Manage All
    Inventory and file upload; the Supply Sources API page excludes sellers who manage inventory in Seller Central and
    sellers who use FBA inventory (F2). And whether a location-quantity write needs SPI beside PL (F3).
11. The practitioner gap: no first-hand read of Sellbrite, Rithum, 店小秘, 马帮, 易仓 or 领星 on FBM quantity sync (P9);
    Linnworks was read by the verifier (P5).
12. Local Selling / in-store pickup and Buy with Prime were not read at any Amazon source.

Help pages not read first-hand (script shell to a plain GET; the content call is off limits):

| Id | Page | What it would settle |
|---|---|---|
| G200955560 | Manage your handling time | latency of quantity and handling-time changes; default fallback |
| G201687550 | Featured Offer | out-of-stock and fulfilment-method wording |
| G201812300, G202072550, G202098380 | Seller Fulfilled Prime policy pages | any stock or delivery requirement |
| G8WRJF2N5B787XKQ | Shipping Settings Automation | template behaviour |
| GYCAQ9XRL273EVDX | Get started with Multi-Location Inventory | Seller Central support (F2) |
| 200332450 | Multi-Channel Fulfillment | "same pool" sentence; reserved stock under MCF |
| G200216110 | Stop selling a product (read by the verifier from the listing playbook's capture v9; not a conversion page) | the help page on converting FBA ↔ FBM was not identified |
| id not found | Listing status for vacations, holidays, and other absences | vacation rules |
| id not found | Manage Holiday Settings | holiday override |
| id not found | Modify order handling capacity | capacity rules |
| id not found | MCF fee pages; blank box / block Amazon Logistics settings | fee and setting wording |

## Positions

**P-fbm-and-outside-fba-1.** The Listings Items API holds two copies of a seller-fulfilled quantity: the
`fulfillment_availability` attribute is the seller's last submission, and the `fulfillmentAvailability` data set is
"the live quantity available for purchase and source of truth for actual inventory levels". [official] *Understanding
Amazon listing status and seller-fulfilled inventory management*; *Listings Items API* (A1)

**P-fbm-and-outside-fba-2.** Amazon decrements a seller-fulfilled SKU's available quantity when an order is placed,
changes it again when an order is cancelled, and stops taking orders at zero. [official] *Notification Type Values*,
`LISTINGS_ITEM_MFN_QUANTITY_CHANGE` (A3)

**P-fbm-and-outside-fba-3.** `fulfillment_availability` is an array of records keyed by `fulfillment_channel_code`:
`DEFAULT` is the seller-fulfilled channel, `AMAZON_NA`, `AMAZON_EU`, `AMAZON_JP` and `AMAZON_IN` are FBA, and the codes
valid for a seller and store are read from the product type schema. [official] *Manage Amazon Haul, Advanced
Multiple-Offer, and Multiple-Fulfillment Use Cases*; *Additional functionality (Fulfillment Inbound)* (A4)

**P-fbm-and-outside-fba-4.** A seller sets `quantity` only on a seller-fulfilled record; Amazon states that quantity
"is supported for MFN fulfillment, but not for Fulfillment by Amazon (FBA) fulfillment". [official] *Manage Amazon
Haul… Multiple-Fulfillment Use Cases* (A5)

**P-fbm-and-outside-fba-5.** A patch with `op: merge` on `/attributes/fulfillment_availability` changes `quantity` for
the named channel and leaves `restock_date` and `lead_time_to_ship_max_days` as they were; the channel code must be
given as the selector. [official] *Merge a listing* (B3)

**P-fbm-and-outside-fba-6.** Only top-level attributes can be patched, so a `replace` on `fulfillment_availability`
submits the whole array; `merge` has been available for this attribute since May 28, 2025 and is supported only for it
and `purchasable_offer`. [official] `listingsItems_2021-08-01.json` (patchListingsItem); *Listings Items API* (B1–B3)

**P-fbm-and-outside-fba-7.** A quantity write can use the product type `PRODUCT`, and both `patchListingsItem` and
`JSON_LISTINGS_FEED` are open to the Product Listing role. [official] *Listings Items API*; *Submit Listings data*;
*Role Mappings for SP-API Operations*; *Role Mappings for SP-API Types* (B1, B4, B8, K)

**P-fbm-and-outside-fba-8.** A submission status of `ACCEPTED` means the write was taken for processing; issues that
arise afterwards are not in the response and are read from `getListingsItem`. [official] *Listings Items API*;
*Listings APIs FAQ* (B5)

**P-fbm-and-outside-fba-9.** Amazon states that `getListingsItem` reflects a change "within 1-5 minutes" while the
listing status and issues notifications normally lag 15–20 minutes. [official] *Listings APIs FAQ* (B6)

**P-fbm-and-outside-fba-10.** Amazon orders a patch and a feed by submission time, with the feed's submission time
applied to every message in it, so an earlier-submitted feed does not overwrite a later patch. [official] *Listings
APIs FAQ* (B7)

**P-fbm-and-outside-fba-11.** `JSON_LISTINGS_FEED` takes up to 25,000 SKUs a feed and five feeds every five minutes.
[official] *Listings APIs FAQ* (B8)

**P-fbm-and-outside-fba-12.** The Feeds API no longer accepts the legacy flat-file and XML inventory feeds
(`POST_FLAT_FILE_INVLOADER_DATA`, `POST_FLAT_FILE_PRICEANDQUANTITYONLY_UPDATE_DATA`,
`POST_INVENTORY_AVAILABILITY_DATA` and the rest); Amazon's feed page and the June 25, 2025 release note date the end
to July 31, 2025 and its deprecation schedule dates the removal to December 3, 2025. Amazon's announcement states the
deprecation "does not impact any listings feeds submitted by sellers directly through Seller Central". [official]
*Listings Feed Type Values*; *SP-API Deprecation Schedule*; *SP-API release notes*; *Deprecation of Feeds API support
for XML and Flat File Listings Feeds* (B9)

**P-fbm-and-outside-fba-13.** `searchListingsItems` returns at most 1,000 listings across all pages, 20 a page.
[official] *Understanding Amazon listing status…*; `listingsItems_2021-08-01.json` (C2)

**P-fbm-and-outside-fba-14.** Amazon's listing reports are not near real time: the stated freshness is 3 hours, and a
repeat request from the same account returns data 1 to 6 hours old depending on catalogue size. [official]
*Understanding Amazon listing status…* (C3)

**P-fbm-and-outside-fba-15.** `GET_MERCHANT_LISTINGS_ALL_DATA` holds active, inactive and suppressed listings with a
`status` column; `GET_MERCHANT_LISTINGS_DATA` holds purchasable and zero-quantity listings without it;
`GET_MERCHANT_LISTINGS_DATA_LITE` and `_LITER` hold only SKUs with quantity above zero. All are open to Product
Listing or Pricing. [official] *Report Type Values: Inventory*; *Understanding Amazon listing status…*; *Role Mappings
for SP-API Types* (C3)

**P-fbm-and-outside-fba-16.** `GET_MERCHANT_LISTINGS_INACTIVE_DATA` mixes five kinds of listing: zero quantity,
blocked, suppressed, not yet opened and past the sale end date. [official] *Understanding Amazon listing status…* (D2)

**P-fbm-and-outside-fba-17.** Amazon classes an out-of-stock listing as inactive, names "updating its inventory levels"
as the way to reactivate it, and states that an open offer needs "a purchasable offer with pricing and a positive
fulfillment availability quantity"; deleting a listing, by contrast, removes it from all reports and API data.
[official] *Understanding Amazon listing status…* (D1, D3, D4)

**P-fbm-and-outside-fba-18.** `LISTINGS_ITEM_MFN_QUANTITY_CHANGE` carries the SKU, channel code and new available
quantity, is delivered through Amazon EventBridge, and is open to the Product Listing role. [official] *Notification
Type Values*; *Role Mappings for SP-API Types* (C5)

**P-fbm-and-outside-fba-19.** A pending order is one whose payment is still being verified; Amazon says not to ship it
until it becomes Unshipped, and it is the initial status of a standard order. [official] *How to manage
seller-fulfilled orders on Amazon* (January 31, 2025); `orders_2026-01-01.json` (E1)

**P-fbm-and-outside-fba-20.** Amazon describes order handling capacity as lengthening the promise, not stopping
sales: once the daily limit is reached, further orders get one more day of handling time and shoppers see a promise
one day longer; it applies to Standard and Free Economy shipping and not to Premium Shipping or Seller Fulfilled Prime
(the European post: not to Prime or Premium shipping). [official]
*Automatic minimum thresholds for order handling capacity* (News_Amazon, updated February 7, 2025); *Use Order handling
capacity to manage your delivery time* (News_Amazon, Europe) (E4)

**P-fbm-and-outside-fba-21.** From February 24, 2025 Amazon sets a minimum order handling capacity from the seller's
average daily orders over the past 30 days and recalculates it weekly, adjusting it when the seller falls below it; the
seller can set a higher limit. [official] *Automatic minimum thresholds for order handling capacity* (E4)

**P-fbm-and-outside-fba-22.** Setting a store's listing status to Inactive (vacation) removes seller-fulfilled
listings from detail pages and search within about an hour, per marketplace; FBA listings stay active, and pending
orders, returns and messages still have to be handled. [official] *Deck the Halls, Not the Inbox: Vacation Mode*
(TaylorR_Amazon); *Account vacation settings and support for the holidays* (UK forum) (E5)

**P-fbm-and-outside-fba-23.** Multi-Location Inventory is for seller-fulfilled stock in the Amazon US store only and
is not available for FBA inventory; each location's quantity is written as a `fulfillment_availability` record whose
channel code is the supply source's id, with product type `PRODUCT`; the integration guide lists adding the Selling
Partner Insights role as a prerequisite of an MLI integration. [official] *Multi-location inventory integration
guide*; *Multi-Location Inventory* (sell.amazon.com) (F1, F3)

**P-fbm-and-outside-fba-24.** Under Multi-Location Inventory the `DEFAULT` channel must be set to 0; a `DEFAULT`
quantity above zero produces a second, non-location offer that "might display inaccurate inventory and shipping
timelines". [official] *Multi-location inventory integration guide* (F4)

**P-fbm-and-outside-fba-25.** The Supply Sources API, which lists and manages a seller's locations, needs the Selling
Partner Insights role. [official] *Role Mappings for SP-API Operations*; *Multi-location inventory integration guide*
(F3, K)

**P-fbm-and-outside-fba-26.** Amazon's pages disagree on Multi-Location Inventory: the program page and the MLI
integration guide list Seller Central file upload and Manage All Inventory as ways to provide location inventory and
exclude only FBA inventory, while the Supply Sources API page says the feature is not available to sellers who manage
inventory in Seller Central or to sellers who use FBA inventory (all read 2026-11-10). [official] *Multi-Location
Inventory* (sell.amazon.com); *Multi-location inventory integration guide*; *Supply Sources API* (F2)

**P-fbm-and-outside-fba-27.** Amazon's developer documentation states that one listing can carry both a
seller-fulfilled and an FBA fulfilment record through the SP-API, and that "When FBA inventory is available, it is used
first. MFN inventory is used after the FBA inventory is depleted"; the same page warns of limited or no Seller Central
support. [official] *Manage Amazon Haul, Advanced Multiple-Offer, and Multiple-Fulfillment Use Cases* (updated
2026-10-28) (G1)

**P-fbm-and-outside-fba-28.** Converting a SKU from FBM to FBA by API is a patch that adds the `AMAZON_*` record and
deletes the `DEFAULT` record; it fails when required battery or dangerous-goods information is missing. [official]
*Additional functionality (Fulfillment Inbound)* (G4)

**P-fbm-and-outside-fba-29.** My Amazon Guy and SellerLogic describe an FBM backup as a second SKU on the same ASIN
(their practice; SellerActive instead flips one SKU by software, P2); My Amazon Guy's stated practice is a suffixed SKU with "a small live quantity, never zero", its real handling time, a price that
covers shipping, and 15–20% of the peak 30-day forecast held in it for Cyber Week (their practice and figures).
[opinion] My Amazon Guy, "How to Run Amazon FBA and FBM Together Without Losing Rank" (P1)

**P-fbm-and-outside-fba-30.** Tools that run an FBA and an FBM SKU on one ASIN warn that the two can reprice against
each other; SellerLogic's rule is a Buy Box strategy on both, no more than two offers in one condition, and no
combining of FBA with FBM Prime offers (their rule). [opinion] SellerLogic repricer FAQ (P3)

**P-fbm-and-outside-fba-31.** An MCF order ships from the same FBA inventory that serves Amazon orders; Amazon
describes it as "a single pool of inventory across channels". [official] *Grow your revenue streams with Amazon
Multichannel Fulfillment (MCF)*; *Amazon launches innovations that power sellers' businesses across sales channels*
(H1)

**P-fbm-and-outside-fba-32.** The Fulfillment Outbound API has a current version v2026-07-04 (launched July 29, 2026)
and a legacy version v2020-07-01 with no removal date on the deprecation schedule read 2026-11-10; all operations of
both are listed under the Amazon Fulfillment role (v2020-07-01 `cancelFulfillmentOrder` also under Product Listing),
and the role-mapping page has no v2026-07-04 section; package tracking moves to the Tracking API's `getShipmentTracking`,
which is grantless and US-only. [official] *Fulfillment Outbound API*; *Fulfillment Outbound migration guide*; *Role
Mappings for SP-API Operations*; *SP-API Deprecation Schedule* (H2)

**P-fbm-and-outside-fba-33.** `getOrderPreview` (v2026-07-04) and `getFulfillmentPreview` (v2020-07-01) create
nothing: they return whether the items are fulfillable, constraints, planned shipments and estimated MCF fees.
[official] `fulfillmentOutbound_2026-07-04.json`; *MCF best practices* (H3)

**P-fbm-and-outside-fba-34.** `createOrder`, `updateOrder` and `cancelOrder` (v2026-07-04) and their v2020-07-01
counterparts make Amazon ship, change or cancel a shipment of FBA units at MCF fees; a legacy order can be cancelled in
`Received` and `Planning` and not once `Processing` (picking) has begun. [official] `fulfillmentOutbound_2020-07-01.json`;
*Fulfillment Outbound migration guide* (H3, H4)

**P-fbm-and-outside-fba-35.** An MCF order created with action `HOLD` reserves inventory without shipping for up to 14
days and is then cancelled automatically; in India Amazon caps a hold order at 250 units. [official] *MCF best
practices*; `fulfillmentOutbound_2020-07-01.json`; *Supply Chain Portal help guide* (July 18, 2025); *What is MCF and
what are the key features?* (Smart Commerce by Amazon, India, January 24, 2023) (H5)

**P-fbm-and-outside-fba-36.** The default MCF fill policy is fill-or-kill (the whole order is unfulfillable if any
item is before picking starts); `FILL_ALL` waits for every item and `FILL_ALL_AVAILABLE` ships what it can. [official]
`fulfillmentOutbound_2026-07-04.json`; `fulfillmentOutbound_2020-07-01.json` (H6)

**P-fbm-and-outside-fba-37.** Units that Seller Central shows in stock can be unavailable to an MCF order because
they are reserved for other orders, in transfer between fulfilment centres, unfulfillable or still receiving.
[official] *Fulfillment Outbound troubleshooting* (H4)

**P-fbm-and-outside-fba-38.** Blocking Amazon Logistics on an MCF order carries a fee surcharge and "may increase the
risk of unfulfilled or delayed deliveries", and overrides the Seller Central account setting; in v2026-07-04 the
feature-eligibility operations are deprecated and `getOrderPreview` is the check. [official]
`fulfillmentOutbound_2020-07-01.json`; *Fulfillment Outbound migration guide* (H7)

**P-fbm-and-outside-fba-39.** Amazon's guidance to MCF integrators is to read `getInventorySummaries` once a day, take
changes from `FULFILLMENT_ORDER_STATUS` and `FBA_INVENTORY_AVAILABILITY_CHANGES`, and "Operate with safety stock
settings to prevent overselling between sync jobs"; it gives no figure. [official] *MCF best practices* (H10)

**P-fbm-and-outside-fba-40.** Amazon's Supply Chain Portal guide (July 18, 2025) recommends, as a best practice for
MCF, "at least 8 weeks of cover and 100 units" received in a fulfilment centre; it is a recommendation, not an
eligibility rule. [official] *Supply Chain Portal help guide* (H9)

**P-fbm-and-outside-fba-41.** MCF fee amounts are read at run time: `getOrderPreview` returns an order's estimated
fees, and Amazon's MCF page announced on 2026-11-10 that updated US fulfilment fees take effect January 15, 2027.
[official] `fulfillmentOutbound_2026-07-04.json`; *Multichannel Fulfillment (MCF)* (supplychain.amazon.com) (H8)

**P-fbm-and-outside-fba-42.** `searchOrders` (Orders API v2026-01-01) is limited to 0.0056 requests per second with a
burst of 20, filters by `fulfilledBy` and `fulfillmentStatuses`, and is open to the Amazon Fulfillment, Finance,
Pricing and Product Listing roles. [official] *Orders API rate limits*; `orders_2026-01-01.json`; *Role Mappings for
SP-API Operations* (J1)

**P-fbm-and-outside-fba-43.** Location-level stock for Seller Flex, Multi Seller Flex, Easy Ship and Self Ship is
published through the External Fulfillment Inventory API, which needs the restricted Direct-to-Consumer Shipping role
and allow-listing; Easy Ship exists in Mexico, India, Turkey, Australia, Singapore, Japan, the Netherlands and Poland.
[official] *External Fulfillment Inventory*; *Easy Ship API*; *Role Mappings for SP-API Operations* (I2, I3)

**P-fbm-and-outside-fba-44.** In data from 2015-era Amazon read without a Prime account, FBA carried a relative
importance of 0.02 in predicting the Buy Box winner, far below price (0.36 and 0.33); in later data across several
countries, an FBM offer from an otherwise perfect seller was penalised by the equivalent of a 46% price increase
against Amazon Retail, compared with 16% for the same seller's FBA offer. [research] Chen, Mislove and Wilson, WWW
2016; Raval, "Steering in One Click" (December 31, 2023) (Published research)

**P-fbm-and-outside-fba-45.** Amazon's seller-fulfilled shipping metrics (late shipment rate, pre-fulfilment cancel
rate, valid tracking rate, on-time delivery rate) apply only to seller-fulfilled orders; the seller's own figures are
in reports that need the Selling Partner Insights role. [official] *Navigating the Account Health Page*
(Atlas_Amazon); *Role Mappings for SP-API Types* (E2, K)

**P-fbm-and-outside-fba-46 (gap fill 2026-11-10).** In Seller Central, deleting a SKU and zeroing its quantity are
separate operations: Amazon's *Stop selling a product* page says an offer whose quantity is not set to zero "will
remain live on the All-Offers Display". Whether `deleteListingsItem` behaves the same is not stated. [official, via
listing playbook capture 2026-10-14] *Stop selling a product* (G200216110 v9) (D5)

**P-fbm-and-outside-fba-47 (gap fill 2026-11-10).** In v2026-07-04 of the Fulfillment Outbound API, `updateOrderStatus`
and `updatePackage` are sandbox-only, the feature-eligibility operations (`getFeatures`, `getFeatureSKU`,
`getFeatureInventory`) and the return operations (`createFulfillmentReturn`, `listReturnReasonCodes`) have no
counterpart and are deprecated though still served by v2020-07-01, and `getOrderPreview` is Amazon's named check for
fulfillability. [official] `fulfillmentOutbound_2026-07-04.json`; *Fulfillment Outbound migration guide* (H2)

**P-fbm-and-outside-fba-48 (gap fill 2026-11-10).** `FULFILLMENT_ORDER_STATUS` payload version 1.0 is deprecated in
favour of 2026-07-04; no removal date is on the deprecation schedule read 2026-11-10. [official] *Notification Type
Values*; *SP-API Deprecation Schedule* (H10)

**P-fbm-and-outside-fba-49 (gap fill 2026-11-10).** Inventory tools sell channel-level buffers on a shared stock
figure: SkuVault Core (Linnworks) names Maximum Quantity, Push Constant Quantity and Low Quantity Cutoff buffers;
SellerActive names per-marketplace Min Threshold and Max Visible buffers and says a buffer on an FBA SKU acts on the
outside channel, "but it will not impact the quantity on the Amazon site itself" (their products' behaviour).
[opinion] Linnworks, "Sync online sales with quantity updates and buffers"; SellerActive, "How do I add Maximum and
Minimum inventory buffers" (P5, P10)

The seat's own (no source; enters no skill):

- A `replace` that names only the `DEFAULT` record probably drops an FBA or supply-source record on the same SKU,
  since the patch target is the whole array; not tested.
- An MCF order's units are probably counted under `pendingCustomerOrderQuantity` from `Received` or `Planning`; no
  page says so.
- The dual-record SKU of G1 looks like the Amazon-side mechanism behind the tools' "auto-flip" (P2), which would
  explain "Amazon will switch your listing from FBM to FBA" when FBA stock returns; unproven.
- The FBA-to-FBM patch is the mirror of the documented FBM-to-FBA patch; what it does to units in fulfilment centres
  is unknown.
- A store on vacation should show as FBM SKUs with quantity above zero that are `DISCOVERABLE` and not `BUYABLE`
  with no issue attached; not verified.
- (moved here by the verifier) Vacation status leaves the FBM quantity untouched (E5); zero quantity keeps the SKU,
  price and history (D4); a multi-location SKU's sellable FBM stock is the sum of its location records (F4); a pending
  order has already taken its units (E1); every MCF unit is one an Amazon shopper can no longer buy (H1).
- The 2016 study's low weight for FBA and Raval's high one are compatible if the weight sits mostly in Prime
  eligibility and delivery speed, which the first could not see.

## Pages read

| Page | URL | Date read | Tag | Reached how / unreachable |
|---|---|---|---|---|
| Understanding Amazon listing status and seller-fulfilled inventory management | https://developer-docs.amazon/sp-api/docs/understanding-amazon-listing-status-and-seller-fulfilled-inventory-management.md | 2026-11-10 | official | GET, markdown |
| Listings Items API | https://developer-docs.amazon/sp-api/docs/listings-items-api.md | 2026-11-10 | official | GET, markdown |
| Merge a listing | https://developer-docs.amazon/sp-api/docs/merge-a-listing.md | 2026-11-10 | official | GET, markdown |
| Submit Listings data | https://developer-docs.amazon/sp-api/docs/submit-listings-data.md | 2026-11-10 | official | GET, markdown |
| Manage Amazon Haul, Advanced Multiple-Offer, and Multiple-Fulfillment Use Cases | https://developer-docs.amazon/sp-api/docs/manage-amazon-haul-advanced-multiple-offer-multiple-fulfillment-use-cases.md | 2026-11-10 | official | GET, markdown |
| Additional functionality (Fulfillment Inbound) | https://developer-docs.amazon/sp-api/docs/additional-functionality-fulfillment-inbound.md | 2026-11-10 | official | GET, markdown; conversion section only |
| Listings APIs FAQ | https://developer-docs.amazon/sp-api/docs/listings-apis-faq.md | 2026-11-10 | official | GET, markdown |
| Listings Feed Type Values | https://developer-docs.amazon/sp-api/docs/listings-feed-type-values.md | 2026-11-10 | official | GET, markdown |
| SP-API Deprecation Schedule | https://developer-docs.amazon/sp-api/docs/sp-api-deprecations.md | 2026-11-10 | official | GET, markdown |
| SP-API release notes | https://developer-docs.amazon/sp-api/docs/sp-api-release-notes.md | 2026-11-10 | official | GET, markdown; searched by term |
| Report Type Values: Inventory | https://developer-docs.amazon/sp-api/docs/report-type-values-inventory.md | 2026-11-10 | official | GET, markdown |
| Notification Type Values | https://developer-docs.amazon/sp-api/docs/notification-type-values.md | 2026-11-10 | official | GET, markdown |
| Role Mappings for SP-API Operations | https://developer-docs.amazon/sp-api/docs/role-mappings.md | 2026-11-10 | official | GET, markdown |
| Role Mappings for SP-API Types | https://developer-docs.amazon/sp-api/docs/role-mappings-for-types.md | 2026-11-10 | official | GET, markdown |
| Multi-location inventory integration guide | https://developer-docs.amazon/sp-api/docs/mli-integration-guide.md | 2026-11-10 | official | GET, markdown |
| Supply Sources API | https://developer-docs.amazon/sp-api/docs/supply-sources-api.md | 2026-11-10 | official | GET, markdown |
| Fulfillment Outbound API | https://developer-docs.amazon/sp-api/docs/fulfillment-outbound-api.md | 2026-11-10 | official | GET, markdown |
| Fulfillment Outbound migration guide | https://developer-docs.amazon/sp-api/docs/fulfillment-outbound-migration-guide.md | 2026-11-10 | official | GET, markdown |
| Fulfillment Outbound troubleshooting | https://developer-docs.amazon/sp-api/docs/fulfillment-outbound-troubleshooting.md | 2026-11-10 | official | GET, markdown |
| MCF best practices | https://developer-docs.amazon/sp-api/docs/mcf-best-practices.md | 2026-11-10 | official | GET, markdown |
| Orders API rate limits | https://developer-docs.amazon/sp-api/docs/orders-api-rate-limits.md | 2026-11-10 | official | GET, markdown |
| External Fulfillment Inventory | https://developer-docs.amazon/sp-api/docs/external-fulfillment-inventory.md | 2026-11-10 | official | GET, markdown |
| Easy Ship API | https://developer-docs.amazon/sp-api/docs/easy-ship-api.md | 2026-11-10 | official | GET, markdown |
| Other developer pages downloaded and not relied on (partially-update-a-listing, preview-errors…, search-for-listings-items-by-id, listings-items-api-rate-limits, manage-listings-issues, place-fulfillment-order, fulfillment-outbound-api-rate-limits, retrieve-feature-list, retrieve-inventory-eligible-for-blank-box, create-order-unbranded-block-amzl, external-fulfillment-shipping, merchant-fulfillment-api, orders-api, orders-api-migration-guide, track-partially-fulfilled-order, create-mcf-return, feed-type-values, order-feed-type-values) | https://developer-docs.amazon/sp-api/docs/<slug>.md | 2026-11-10 | official | GET; saved, not read in detail; no fact taken |
| SP-API models: `listingsItems_2021-08-01.json`, `fulfillmentOutbound_2026-07-04.json`, `fulfillmentOutbound_2020-07-01.json`, `orders_2026-01-01.json`, `fbaInventory.json` | local clone, commit `db2936aa` (2026-10-29) | 2026-11-10 | official | local file |
| Multi-Location Inventory | https://sell.amazon.com/programs/multi-location-inventory | 2026-11-10 | official | GET |
| Seller Fulfilled Prime | https://sell.amazon.com/programs/seller-fulfilled-prime | 2026-11-10 | official | GET |
| Fulfilled by Merchant | https://sell.amazon.com/programs/fulfilled-by-merchant | 2026-11-10 | official | GET; marketing only, no fact taken |
| How to manage seller-fulfilled orders on Amazon (January 31, 2025) | https://sell.amazon.com/blog/amazon-order-management | 2026-11-10 | official | GET |
| Grow your revenue streams with Amazon Multichannel Fulfillment (MCF) | https://sell.amazon.com/blog/multichannel-fulfillment | 2026-11-10 | official | GET |
| Multichannel Fulfillment (MCF) | https://supplychain.amazon.com/multichannel-fulfillment | 2026-11-10 | official | GET |
| Supply Chain Portal help guide (July 18, 2025) | https://supplychain.amazon.com/support/help-guide | 2026-11-10 | official | GET |
| Amazon launches innovations that power sellers' businesses across sales channels | https://sellingpartners.aboutamazon.com/innovations-power-sellers-businesses-across-sales-channels | 2026-11-10 | official | GET |
| Automatic minimum thresholds for order handling capacity (News_Amazon) | https://sellercentral.amazon.com/seller-forums/discussions/t/d2e0afe7-b710-4c2c-b704-161baf2ada6a | 2026-11-10 | official | GET |
| Use Order handling capacity to manage your delivery time (News_Amazon, Europe) | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/b0d1631c8b61f0bec4847542a81d4c6f | 2026-11-10 | official | GET |
| Deck the Halls, Not the Inbox: Vacation Mode (TaylorR_Amazon) | https://sellercentral.amazon.com/seller-forums/discussions/t/44a5d2c0-ec70-4c58-bbbe-895a2ffcd542 | 2026-11-10 | official | GET |
| Account vacation settings and support for the holidays (UK) | https://sellercentral.amazon.co.uk/seller-forums/discussions/t/e00ce497-3707-4db3-9633-8f7fd1adddad | 2026-11-10 | official | GET |
| Navigating the Account Health Page (Atlas_Amazon) | https://sellercentral.amazon.com/seller-forums/discussions/t/8a41416f-e1ad-4221-9675-7145d5cc5e28 | 2026-11-10 | official | GET |
| Changing product from FBA to FBM while in reserve (seller thread) | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/c05cc456a966777cf0e6537078935e95 | 2026-11-10 | opinion | GET; opening post only |
| Can't convert from FBA to FBM? (seller thread) | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/a78714a5ee9585dfdeb522fd6d630987 | 2026-11-10 | opinion | GET; opening post only |
| My Amazon Guy, How to Run Amazon FBA and FBM Together Without Losing Rank | https://myamazonguy.com/fba/how-to-run-amazon-fba-and-fbm/ | 2026-11-10 | opinion | GET |
| My Amazon Guy, FBM failover article | https://myamazonguy.com/?p=177711 | 2026-11-10 | opinion | GET; saved, not mined |
| SellerActive, auto-flip fulfilment type | https://www.selleractive.com/support/amazon-fba-fbm-autoflip-fulfillment-type | 2026-11-10 | opinion | GET |
| SellerActive, adding max and min buffers | https://www.selleractive.com/support/adding-max-and-min-buffers | 2026-11-10 | opinion | GET; body extracted by the verifier (P10) |
| Deprecation of Feeds API support for XML and Flat File Listings Feeds (verifier) | https://developer-docs.amazon.com/sp-api/changelog/deprecation-of-feeds-api-support-for-xml-and-flat-file-listings-feeds.md | 2026-11-10 | official | GET, markdown |
| Stop selling a product (G200216110 v9); Featured Offer (G201687550 v20) (verifier) | local: `office-mailbox/from-engineering/20261014-1510-listing-playbook-help-pages/` | 2026-11-10 | official, via listing playbook capture 2026-10-14 | local file |
| SellerLogic repricer FAQ | https://support.sellerlogic.com/faq/how-do-i-list-an-asin-for-an-fba-and-fbm-product-so-that-they-do-not-interfere-with-each-other | 2026-11-10 | opinion | GET |
| Veeqo, How to Guarantee You Never Oversell (February 1, 2018) | https://www.veeqo.com/blog/prevent-overselling | 2026-11-10 | opinion | GET |
| UpSeller,《库存同步使用指南》 | https://www.upseller.com/zh-CN/doc-article/1253 | 2026-11-10 | opinion | GET |
| AMZ123 Q&A (FBM 配送设置; FBM 导出库存数据; 新店库存限制) | https://www.amz123.com/ask/ShUaMhFq ; …/vf0fisqD ; …/3gr34Gmi | 2026-11-10 | opinion | GET; generic, one mention |
| Chen, Mislove, Wilson, An Empirical Analysis of Algorithmic Pricing on Amazon Marketplace (WWW 2016) | https://www.khoury.northeastern.edu/home/cbw/static/pdf/amazon-www16.pdf | 2026-11-10 | research | GET, PDF text extracted locally |
| Raval, Steering in One Click (December 31, 2023) | https://deveshraval.github.io/buyBox.pdf | 2026-11-10 | research | GET, PDF text extracted locally; abstract, introduction and quoted passages |
| Listing playbook, `research/angles/inventory-and-fulfillment.md` §H–J; `research/method/listing-writes.md` (headings); `research/method/help-page-access.md` §A | local | 2026-11-10 | that seat's read of 2026-10-14 | local file |
| Seller Central help pages listed in *Open questions* (G200955560, G201687550, G201812300, G202072550, G202098380, G8WRJF2N5B787XKQ, GYCAQ9XRL273EVDX, 200332450, G200216110, and four without ids) | https://sellercentral.amazon.com/help/hub/reference/external/<ID> | 2026-11-10 | **unreachable** | plain GET with `?locale=en-US`, `/gp/help/external/<ID>`, `.co.uk` twin: script shell; sell.amazon.com twin 404; web.archive.org no capture for the id tried; content call is a POST (off limits) |
| MCF pricing | https://supplychain.amazon.com/pricing/multichannel-fulfillment | 2026-11-10 | **unreachable** | 404 (guessed URL) |
| Amazon Warehousing and Distribution program page | https://sell.amazon.com/programs/amazon-warehousing-and-distribution | 2026-11-10 | **unreachable** | 404 (guessed URL) |
| Buy with Prime knowledge centre, Fulfillment by Amazon | https://buywithprime.amazon.com/knowledge-center/fulfillment-by-amazon-fba | 2026-11-10 | **unreachable** | 403 |
| Lengow help, `is_inventory_available` | https://help.lengow.com/hc/en-us/articles/22156479838108 | 2026-11-10 | **unreachable** | 403; snippet only; the verifier's retry with a browser user-agent also 403 |
| Linnworks, Sync online sales with quantity updates and buffers (2018-08-31, modified 2025-04-22) | https://www.linnworks.com/blog/sync-online-sales-with-quantity-updates-and-buffers/ | 2026-11-10 | opinion | the seat: 403; the verifier: 200 with a browser user-agent (P5) |
| What is MCF and what are the key features? (Smart Commerce by Amazon, India, Jan 24, 2023) | https://smartcommerce.amazon.in/blog/mcf-what-is-mcf-and-key-features | 2026-11-10 | official | the verifier: GET, text extracted (H5) |

## Verification

Verified 2026-11-10 by the verifier seat. Every source below was fetched again today with a plain GET (developer-docs
`.md` twins, sell.amazon.com, supplychain.amazon.com, sellingpartners.aboutamazon.com, smartcommerce.amazon.in, the
forum threads, the practitioner pages) or opened as a local file (the models at `db2936aa`, the research seat's PDF
text, the listing playbook's help-page captures). No Amazon API host was called; nothing was posted.

**Checked:** all 45 original positions, and about 140 other claims (every operation, report, feed and notification
role against *Role Mappings for SP-API Operations* / *…Types* and the report page's own Roles line; every rate, limit,
enum, path and status from the Listings Items, Fulfillment Outbound (both versions) and Orders 2026-01-01 models;
every date in B9, C1, H2, H10, J2; every quotation in A–J and P1–P8; the two papers' figures). Confirmed as written,
among others: the two copies of quantity and the `fulfillmentAvailability` sentence; the `merge` text, example and
May 28, 2025 date; the `replace` example of *Submit Listings data*; "Only top-level…"; 5/5, 5/10 rates; `pageSize`
max 20; the 1,000-listing ceiling; the 3-hour / 1–6-hour freshness; FAQ 1–5 vs 15–20 minutes, 25,000 SKUs / five per
five minutes, the timestamp ordering; the deprecation schedule's December 3, 2025 and the feed page's July 31, 2025;
`ORDER_STATUS_CHANGE` removed July 29, 2026; Orders v0 removal March 27, 2027; `searchOrders` 0.0056/s burst 20;
Fulfillment Outbound v2026-07-04 launched July 29, 2026, rates 2/30 and `getOffers` 5/30, the status and policy
enums, `Hold` cancelled after 14 days, `FillAll` 24 hours, `BLOCK_AMZL` wording, `channel` max 40; every role in the K
table; the MCF best-practices sentences; the troubleshooting sentences; the External Fulfillment channel list; Easy
Ship's eight stores; the order-handling-capacity, vacation and account-health forum quotations; My Amazon Guy,
SellerActive auto-flip, SellerLogic, UpSeller and Veeqo quotations; Chen et al. Table 1 and Raval's 16% / 46% / 88% /
80%.

**The brief's hardest claims.** (1) Patch shape and live read: confirmed; the file agrees with the listing playbook's
P-inventory-and-fulfillment-2 and states it as a fact rather than a rule. (2) Legacy feed removal: both dates
confirmed; added Amazon's announcement that Seller Central uploads are unaffected. (3) MCF operations, versions,
roles: confirmed, with three omissions filled (below). (4) Automated FBA-to-FBM: the only Amazon statement remains
G1 ("When FBA inventory is available, it is used first. MFN inventory is used after…"), under no product name; "auto-
flip" (SellerActive) and "hybrid fulfillment" (My Amazon Guy) are tools' and practitioners' names. (5) Supply Sources
and External Fulfillment roles: SPI and DTC (Restricted) confirmed; the MLI write's role is now marked not
established (below). (6) Pitfall sources: each re-opened; three inferences re-tagged as the seat's.

**Changes:**

| Where | It said | The source says | Done |
|---|---|---|---|
| A1 | "The same sentence stands on *Listings Items API*" | That page has a different sentence with the same meaning | Quoted the actual sentence; noted agreement with P-inventory-and-fulfillment-2 |
| A4, G1, P-27 | *Manage Amazon Haul…* `updatedAt` 2026-09-09 | `updatedAt` 2026-10-28 (also in the seat's own saved copy) | Date corrected |
| B9, P-12 | Seller Central upload "not established" | Announcement: "does not impact any listings feeds submitted by sellers directly through Seller Central"; June 25, 2025 note also calls July 31 the removal date | Added, with source |
| C3 | FYP report role "not looked up" | PL (report page and Types page) | Filled |
| C5 | "Avoid frequent polling…" as the notification page's | That sentence is on *Understanding Amazon listing status…* | Attribution corrected |
| D4, P-17 | Zero quantity "keeps its SKU and offer" as Amazon's | Not stated; Amazon says restock reactivates and delete removes from all reports | Re-tagged [seat]; P-17 reworded to Amazon's words |
| E1 | Pending order has taken its units, as fact | Inference from A3 + E1 | Tagged [seat] |
| E4, P-20 | Capacity "never stops orders and never changes the quantity" | Posts describe a longer promise; say nothing on quantity; EU: not Prime or Premium | Reworded to what the posts say; added automatic downward adjustment (P-21) |
| E5 | Vacation leaves quantity untouched, as fact | Not in either post | Tagged [seat]; "Stable enough" bullet corrected |
| F2, P-26 | MLI guide excludes only FBA/non-US; disagreement is program page vs Supply Sources page | The MLI guide also lists Seller Central upload and Manage All Inventory; Supply Sources excludes "Sellers who use FBA inventory" | Rewritten: Supply Sources page stands alone against the other two |
| F3, P-23, K | Location write is PL (via `patchListingsItem`) | Both developer pages list adding SPI as an MLI prerequisite | Marked not established; P-23 states the prerequisite; K row added |
| F4 | — | *Manage Amazon Haul…* example patches `DEFAULT` 3 with a location 7 | Tension recorded |
| G2 | G200216110 is "Stop selling / change to Fulfilled by Merchant"; "every practitioner" uses two SKUs | Capture is *Stop selling a product*, nothing on conversion; SellerActive flips one SKU | Corrected; P-29 reworded to name who says it |
| G3 | via listing playbook | Re-read in the capture G201687550-v20 | Quotations confirmed; tag states the capture |
| G4 | Conversion "failing silently for a week" | "for the last week nothing will convert to FBM" | Quoted |
| G5 | — | `GET_MFN_PANEU_OFFER_STATUS`: no Roles line, not on the Types page; five EU stores | Added |
| H2, P-32 | Mapping table | Missing `updateOrderStatus`/`updatePackage` (sandbox-only), `getInvoiceHeaders` (page only), Tracking API grantless and US-only; `getFeatures`/`getFeatureSKU` quote belonged to `getFeatureInventory` | Table corrected; P-47 added |
| H5, P-35 | India hold cap [snippet] | smartcommerce.amazon.in (Jan 24, 2023): two weeks, max 250 units | Read; [official] for India |
| H10 | — | `FULFILLMENT_ORDER_STATUS` payload 1.0 deprecated | Added; P-48 |
| P1 | — | My Amazon Guy: hybrid swap "roughly 15 minutes" | Added as their claim |
| P5 | Linnworks [snippet], 403 | Reached with a browser user-agent | Read; three buffer types; P-49 |
| L | Agreement with `listing-writes.md` asserted from headings | Read B10–B14 and D | Agreements and four differences listed |

**Added:** P-46 to P-49; D5; P10; the L comparison; K rows. **Removed:** no position removed.

**Could not re-open:** Lengow's help article (403 again, browser user-agent too): A7 stays [snippet] and carries no
position. Every Seller Central help page in *Open questions* except G200216110 and G201687550 (read via the listing
playbook's captures). The Buy with Prime page was not retried. The Raval PDF and Chen PDF were checked against the text
the research seat extracted, not downloaded again.

**Gaps filled:** Seller Central effect of the feed deprecation; India hold cap; Linnworks and SellerActive buffers;
MLI's SPI prerequisite; v2026 sandbox-only and deprecated operations; payload deprecation; delete-vs-zero in Seller
Central; the `listing-writes.md` comparison.

**Gaps left** (what someone who has run inventory for a large seller would look for and not find): the Seller Central
help page on converting FBA ↔ FBM and what happens to FBA units on conversion; FBM quantity limits for new sellers or
categories (AMZ123's 新店库存限制 thread was opened by the seat but not mined); whether `quantity` above some maximum is
rejected (schema not read, it needs the API); the Seller Central MCF setting pages and US fee amounts; Sellbrite,
Rithum, 店小秘, 马帮, 易仓 and 领星 on sync intervals; Local Selling / BOPIS and Buy with Prime at an Amazon source;
whether an MCF order's units count under `pendingCustomerOrderQuantity`, and how MCF shipments appear in the ledger;
the effect of a stock-out with an FBM backup, measured.
