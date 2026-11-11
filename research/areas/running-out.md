# Running out of stock and what it costs

Read 2026-11-10 by the research seat.

Tags. **[official]** is Amazon's own words on a page opened in this session with a plain GET, or in the SP-API models
cloned locally at commit `db2936aa` (2026-10-29). **[official, office capture 2026-10-14]** is the text of a Seller
Central help page as another team captured it on 2026-10-14; the capture is a local file read in this session
(`office-mailbox/from-engineering/20261014-1510-listing-playbook-help-pages/`), not a page I opened at Amazon.
**[official, listing playbook 2026-10-14, not re-read]** is a quotation taken from the listing playbook's
`research/angles/inventory-and-fulfillment.md`, which another seat read on 2026-10-14; I did not re-read the page.
**[official, via <who>]** is Amazon's text as a third party quotes it. **[snippet]** is text seen only in a search
result. **[opinion]** is a named practitioner or tool. **[research]** is published research. **[seat]** is my own
inference and enters no skill.

How URLs were reached. Seller Central help pages (`/help/hub/reference/external/<ID>`, `/gp/help/external/<ID>`, the
`.co.uk` twin, `?locale=en-US`) returned only a script shell to a plain GET; their content call is a POST and is off
limits by the lead's ruling of 2026-11-10. web.archive.org copies of the Inventory performance and Restock help pages
were tried and failed (HTTP 502 and connection failures). What did serve text to a plain GET: `developer-docs.amazon.com/sp-api/docs/<page>.md`,
`sell.amazon.com`, `advertising.amazon.com/resources/faq` and `/library/guides/…`, Seller Forums threads under
`sellercentral.amazon.com/seller-forums/discussions/t/<id>`, and Amazon's customer-help mirror at
`digprjsurvey.amazon.com/csad/help/node/<id>`. Forum pages show only relative dates ("3 years ago") in their text,
but each page's HTML carries the post's exact `datePublished`; the verifier replaced the seat's derived years with those
dates (see *Verification*). Practitioner pages (English and Chinese) and research papers were read by three helper streams whose notes are in
`scratch/stock-playbook/running-out/`; each quotation in those notes was copied from a fetched page. The Chinese and
the research helpers stopped on a usage limit after their notes were written through to their closing sections; what
they did not reach is listed in *Open questions*.

## What this covers

- What "out of stock" is in Amazon's data: which quantity is buyable, which units exist and are not buyable, what the
  shopper sees, when an FBA listing turns inactive and how it returns, and what a child's stock-out does to a
  variation family.
- What Amazon itself says a stock-out costs: the Featured Offer, search, ads, the Inventory Performance Index's
  in-stock rate, Subscribe & Save, deals, and the measures Amazon publishes of lost sales and stock-out risk
  (in-stock rate, estimated lost sales, Restock alert, Minimum Inventory Level, days of supply, weeks of cover).
- What practitioners claim about the lasting effect on rank, Best Sellers Rank, ads and relaunch cost, in English and
  in Chinese, with their disagreements; and the tactics they use before, during and after.
- What published research has measured about stock-outs, and what it has not.
- How a stock-out distorts the seller's own data, and how named tools correct for it.
- The facts that decide "when does this SKU run out": which fields count, which do not, and where the 30-day average
  misleads. What a pack adds beyond the door's `/low-stock` template.
- Amazon's own agent skills' bands on stock-outs, recorded and not borrowed.

Owned elsewhere and only cross-referenced:

- `areas/stock-states.md`: the full taxonomy of FBA quantities (reserved, researching, unfulfillable, stranded).
- `areas/holding-costs.md`: the low-inventory-level fee's amounts, bands, exemptions and its 2027 change; storage fees.
- `areas/restock-and-forecast.md`: the Restock Inventory tool, Amazon's demand forecast, lead-time settings.
- `areas/inbound.md`: what arrives when; inbound plan states and receiving time.
- `areas/stuck-stock.md`: stranded, suppressed and researching units.
- `areas/fbm-and-outside-fba.md`: running a seller-fulfilled offer, Multi-Channel Fulfilment, handling time.
- `beyond/programs-and-regions.md`: AWD, Pan-EU, remote fulfilment, programme rules by region.
- `beyond/sellers-tools-and-research.md`: the wider tool survey; this file owns the stock-out literature and only the
  tool behaviour that concerns out-of-stock days.
- `method/sp-api-stock-surface.md`: the operations and reports as a surface; `method/seller-central-only.md`: what has
  no API.

## Amazon's own rules

### A. "Out of stock" in the data: the buyable quantity is one field, and it is not the total

**A1. Fulfillable is the quantity that can be shipped today.** FBA Inventory API model, `InventoryDetails.fulfillableQuantity`:
"The item quantity that can be picked, packed, and shipped." [official] local model
`models/fba-inventory-api-model/fbaInventory.json`, line 787, read 2026-11-10. The notification schema says the same
of its field: `Fulfillable` is the quantity that "can be used to fulfill orders in the given marketplace". [official]
`schemas/notifications/FBAInventoryAvailabilityChangeNotification.json`, read 2026-11-10.

**A2. Units can exist at Amazon and not be buyable.** The same model carries, beside `fulfillableQuantity`:
`inboundWorkingQuantity`, `inboundShippedQuantity`, `inboundReceivingQuantity`; `reservedQuantity` with
`pendingCustomerOrderQuantity`, `pendingTransshipmentQuantity` and `fcProcessingQuantity`; `researchingQuantity`;
`unfulfillableQuantity`; and `totalQuantity`, "The total number of units in an inbound shipment or in Amazon
fulfillment centers." [official] same model, lines 674–848. Amazon's help page *Inventory
Buyability* (GFC63UNUF6LMLK2R): "If units are stranded, reserved, being researched, or unfulfillable, customers won't
be able to buy them". [official, listing playbook 2026-10-14, not re-read]. The taxonomy is `areas/stock-states.md`'s.

**A3. A SKU can therefore read "0 fulfillable" with stock in the network.** The states that produce it, each visible
as its own field: units in fulfilment-centre transfer (`pendingTransshipmentQuantity`; report column "FC transfer"),
units being processed (`fcProcessingQuantity`; "FC Processing"), units held for orders already placed
(`pendingCustomerOrderQuantity`; "Customer Order"), and inbound units in the three inbound states. [official] model
as above; column names from *Fulfillment by Amazon (FBA) Reports*,
https://developer-docs.amazon.com/sp-api/docs/report-type-values-fba (page `updatedAt` 2026-10-13), read 2026-11-10.

**A3a. Units in FC transfer may be buyable; Amazon's own statements disagree (aligned with `areas/stock-states.md` C1–C2,
verifier 2026-11-10).** The help page in A2 says reserved units cannot be bought. An Amazon moderator post
(Topher_Amazon, 2024-08-26, thread `c07904af-be04-432d-8c67-80ab0a46f601`, read by the stock-states seat and its
verifier) says: "Units in the FC transfer status are available for customers to buy. However, customers might be shown
a future ship date if no other units are available in the fulfillment centers for immediate fulfillment." [official,
forum moderator, one post]. The FBA Manage Inventory reports now carry `afn-fc-transfer-quantity` and
`afn-onhand-buyable-quantity` beside `afn-fulfillable-quantity` [official] *Fulfillment by Amazon (FBA) Reports*, read
2026-11-10; the page defines neither column. "0 fulfillable" with units in FC transfer is therefore not shown to be
"not buyable": it rests on one moderator post against one help page.

**A4. Stock can be buyable in one region and not another while the SKU total is above zero.** *Inventory Buyability*:
"Your product may be temporarily unavailable for shipping to certain parts of the country…"; and "When we have
products with limited quantities of inventory in our network … and these products have very low sales volume, there
may be rare situations where the product isn't available for sale to all customers". [official, listing playbook
2026-10-14, not re-read]. No SP-API field read in this session reports availability by shopper location.

**A5. Freshness.** The Restock Inventory report is described as "Content updated in near real-time." [official]
*Fulfillment by Amazon (FBA) Reports*, as above. The listing playbook recorded for the Listings Items API that "The
SLA for stock data freshness is 3 hours" [official, listing playbook 2026-10-14, not re-read]. Amazon's own agent
skill describes its inventory metrics as "~2-day data" [official] Amazon Selling Partner plugin 1.0.0,
`skills/seller-analytics/references/metrics-catalog.md`, local file read 2026-11-10. These are three different
surfaces with three different lags.

### B. What the shopper sees

**B1. Amazon defines the availability messages only for items it sells itself.** *Availability Estimate Definitions*
(Amazon customer help), read 2026-11-10 at https://digprjsurvey.amazon.com/csad/help/node/GM6AEUPCYCFUTYX7 (the
`www.amazon.com/gp/help/customer/display.html?nodeId=GM6AEUPCYCFUTYX7` address returned 403): "The availability
estimates on our website only apply to products shipped and sold by Amazon". Its definitions:

- "In Stock — The item is in stock in at least one fulfillment center…"
- "In stock but may require an extra 1-2 days to process"
- "Usually ships in X-Y days — The item will be ordered from a nearby distributor…"
- "Temporarily Out of Stock — This item is currently not in stock but it is available for ordering. We'll email you
  the expected delivery date as soon as that information is available from our suppliers."
- "Currently unavailable — This item isn't currently available for ordering and it may not be in stock again."

[official]. No Amazon page read in this session defines these messages for a third-party FBA offer. What a seller's
own FBA listing shows when it has no buyable offer is known here only from sellers' transcriptions: "Currently
unavailable. - We don't know when or if this item will be back in stock." [opinion] seller post, Seller Forums EU,
2022-04-05 (P7 below).

**B2. The pricing API carries an offer's availability as a type and a date.** Product Pricing v0,
`DetailedShippingTimeType`: `minimumHours`, `maximumHours`; `availableDate` — "The date when the item will be
available for shipping. Only displayed for items that are not currently available for shipping."; `availabilityType`
with the values `NOW`, `FUTURE_WITHOUT_DATE` ("will be available for shipping on an unknown date in the future") and
`FUTURE_WITH_DATE`. [official] local model `models/product-pricing-api-model/productPricingV0.json`, read 2026-11-10.
This is the only field found that separates "ships now" from "buyable, ships later" for an offer.

### C. The listing: inactive when out of stock, and how it returns

**C1. Out of stock is the first listed reason a listing is inactive.** *Understanding Amazon listing status and
seller-fulfilled inventory management*, https://developer-docs.amazon.com/sp-api/docs/understanding-amazon-listing-status-and-seller-fulfilled-inventory-management
(page `updatedAt` 2026-09-09), read 2026-11-10: the reasons for an Inactive listing begin "Is out of stock…". The
All Listings report "returns the seller listings which are either purchasable or have zero inventory… This report
also contains listings with zero (0) inventory quantity, which are considered inactive. This is to allow for not only
tracking active items but also for restocking items that turn inactive due to low inventory levels." The Inactive
Listings report "includes listings that have zero (0) quantity, listings that are blocked, …suppressed, …not yet
opened, and …past their sale end date". [official].

**C2. Inactive (out of stock) is one of several causes with the same status.** The Inactive report mixes zero
quantity with blocked, suppressed, unopened and expired listings (C1). The Listings Items API separates a listing's
status from its stock: `searchListingsItems` takes a `withoutStatus` filter of `BUYABLE`, and the listing playbook
recorded that `fulfillmentAvailability` in a `getListingsItem` response is the live quantity while
`attributes.fulfillment_availability` is what was last submitted, and that `searchListingsItems` returns at most 1,000
listings. [official] the developer page above for the filter; [official, listing playbook 2026-10-14, not re-read]
for the rest.

**C3. A listing returns when it has a buyable offer again.** Same developer page: "Opening a listing item means
adding a current offer for it. An offer must have a purchasable offer with pricing and a positive fulfillment
availability quantity."; "Reactivate your out of stock listing by updating its inventory levels." [official]. For FBA
the quantity is not the seller's to set: it becomes positive when Amazon has fulfillable units (or sells ahead of
them, section D).

**C4. A product with no buyable offer is not searchable.** *My ASIN is unsearchable* (GHGHDMU4X5K9QGCV): "In order to
be searchable, an ASIN needs a buyable offer… ASINs without a buyable offer are unsearchable"; a change "can take up
to 72 hours to reflect in shopping results". [official, listing playbook 2026-10-14, not re-read]. The condition is
on the ASIN, not the seller: an ASIN with another seller's buyable offer stays searchable when one seller runs out.

### D. Selling on stock that is not yet on the shelf

**D1. In-Stock Head Start exists in the data.** `FBAInventoryAvailabilityChangeNotification`: `FutureSupplyBuyable` —
"The number of units available for customers to find and buy while inventory is on its way to an Amazon fulfillment
center through In-Stock Head Start."; `PendingCustomerOrderInTransit` — "The number of units that customers have
purchased while inventory is on its way to an Amazon fulfillment center through In-Stock Head Start". [official]
`schemas/notifications/FBAInventoryAvailabilityChangeNotification.json`, read 2026-11-10. The FBA Manage Inventory
reports list the columns `afn-reserved-future-supply` and `afn-future-supply-buyable`. [official] *Fulfillment by
Amazon (FBA) Reports*, read 2026-11-10. The FBA Inventory API model (`getInventorySummaries`) has no future-supply
field: a search of `fbaInventory.json` finds none. [official] local model.

**D2. What the programme was when announced.** Amazon's own announcement, News_Amazon, "FBA Products in stock soon?
Make them available now", Seller Forums, `datePublished` 2019-07-25,
https://sellercentral.amazon.com/seller-forums/discussions/t/e061bc46a55f2c54b0a71f8085b7e018, read by the verifier
2026-11-10: "With the new In-Stock Head Start pilot program, Fulfillment by Amazon (FBA) will make your temporarily
out-of-stock products available for customers to find and buy when your shipment is on its way and we are confident
about its arrival date." [official]. The rest of the notice is known through third parties. 2019 US pilot: it "will make your out of
stock products discoverable on Amazon and available for customers to find and buy once your shipment is on it's way
and Amazon are confident about it's arrival date"; eligibility needs a shipment sent with "Amazon Carrier Central,
the Partnered Carrier program (PCP), or Amazon Global Logistics"; "At this time, In-Stock Head Start is enabled only
at the seller level, so you will not be able to choose certain ASINs for the pilot."; "Your fees and Inventory
Performance Index (IPI) score will not be impacted."; units appear in both "Available" and "Inbound". [official, via
ChannelX, 2019-08, https://channelx.world/2019/08/amazon-in-stock-head-start-pilot-program/]; [official, via
Feedvisor, 2019-12-04]; [official, via 观海论商 on AMZ123, 2019-07-29, which pastes the notice in English]. ChannelX
reported the programme "now live" in the UK on 2020-08-12 (https://channelx.world/2020/08/amazon-fba-stock-head-start-now-live-uk/)
[opinion, read by the verifier]. The latest dated trace found: a UK seller on Amazon's forums, 2024-11-20, "the program
works for some of our products, it's not functioning for all of them", naming a "Future Buyable Inventory" figure; an
Amazon staff reply (Dominic_Amazon) answers on the case without describing the programme
(https://sellercentral.amazon.co.uk/seller-forums/discussions/t/7b031785-d195-46be-86ff-a3d501d3d83c) [opinion, with an
Amazon reply]. No Amazon help page for the programme was read, and no 2025–2026 Amazon text was found; whether
enrolment, eligibility or regions have changed is an open question.

**D3. AWD stock counts as buyable when auto-replenishment is on.** Amazon moderator "Topher_Amazon", Seller Forums EU,
2024-07-16, answering what happens when FBA runs out before an AWD replenishment arrives: "If you leave
auto-replenishment enabled, your products are considered in stock and buyable when they're received by AWD."
[official, forum moderator] https://sellercentral-europe.amazon.com/seller-forums/discussions/t/53ae3d00-183c-4f5c-a9a2-3839f81e1bcb
(read by the English helper stream, 2026-11-10). AWD itself is `beyond/programs-and-regions.md`'s.

**D4. The Orders API has a status for pre-orders only.** Orders v0: `Pending` — "The order has been placed but payment
has not been authorized. The order is not ready for shipment…"; `PendingAvailability` applies to pre-orders. [official]
local model `models/orders-api-model/ordersV0.json`, read 2026-11-10.

**D5. An order type for out-of-stock items (gap fill 2026-11-10).** Orders v0 `OrderType` includes `BackOrder`: "An
order that contains items that already have been released in the market but are currently out of stock and will be
available in the future." [official] `ordersV0.json`, line 3560, read by the verifier 2026-11-10. No page read says
whether orders taken through In-Stock Head Start carry this type; that is a question for a real account.

### E. The Featured Offer

**E1. No stock, no Featured Offer.** *Becoming the Featured Offer* (G201687550, v20): "Your offer can't become
featured if you're out of stock. Keep your inventory updated and plan accordingly for things that sell quickly."; "As
of September 2026, Amazon no longer maintains a seller eligibility requirement… make sure your offer is shippable to
the customer's location, ensure that you have inventory in stock, and check Pricing Health". [official, office capture
2026-10-14] local file `G201687550-v20.txt`, read 2026-11-10.

**E2. The Featured Offer percentage counts out-of-stock page views, and other things.** *Business reports glossary*
(G27691, v7): "Featured Offer percentage — The percentage of page views where the Featured Offer… appeared… This
percentage will be less than 100% if the page view occurred when: The product was out of stock. The Featured Offer
would result in the customer purchasing from another seller. Your product was not available for purchase using the
Featured Offer… This is not necessarily an indication of the availability of your product for purchase." [official,
office capture 2026-10-14] local file `G27691-v7.txt`, read 2026-11-10. The Data Kiosk schema's `buyBoxPercentage`:
"The percentage of page views where the buy box (the add to shopping cart link) appeared on the page for customers to
add your product to their cart." [official] `schemas/data-kiosk/analytics_salesAndTraffic_2024_04_24.graphql`.

**E3. Per-offer flags.** Product Pricing v0 `OfferDetail`: `IsBuyBoxWinner` ("There can be up to two Buy Box winners
at any time per ASIN, one that is eligible for Prime and one that is not"), `IsFeaturedMerchant`,
`IsFulfilledByAmazon`, `MyOffer`. [official] local model, read 2026-11-10.

### F. Ads

**F1. A sponsored ad does not show for a product that is out of stock or not the Featured Offer.** *Amazon Ads FAQ*,
https://advertising.amazon.com/resources/faq, read 2026-11-10: "Remember that your product must be in stock and priced
competitively in order to become the Featured Offer… If your product isn't the Featured Offer or is out of stock, your
ad will not display." *New advertiser success guide*, https://advertising.amazon.com/library/guides/new-advertiser-success-guide,
read 2026-11-10: "Keep in mind that if your products aren't presenting the featured offer or are out of stock, your ad
will not display."; "Make sure your products are in stock. Your products need to be in stock to be the featured offer
and eligible for advertising." [official].

**F2. What was not confirmed first-hand.** The sentence "your ads will automatically stop serving if your product is no
longer available to purchase" is quoted from an Amazon advertiser guide by Optmyzr [official, via Optmyzr]; I fetched
the Sponsored Display general-availability blog post a search result attributed it to and did not find the sentence in
the text. The console status text "Your ad is not eligible for impressions because your listing is not in the Buy Box."
is [official, via Portent]. The Amazon Ads help page on ad eligibility (`advertising.amazon.com/help/GQFZA83P55P747BZ`)
is a script shell and was not read. Whether Sponsored Brands and Sponsored Display stop the same way is not stated on
the two Amazon pages read; practitioners say they do not (P9). Ad eligibility as data lives in the Amazon Ads API,
which is not this door; the ads playbook owns it.

### G. The Inventory Performance Index, the in-stock rate and estimated lost sales

**G1. The in-stock rate, as Amazon defines it.** *Inventory performance* (G202174810, v9): "the percent of time your
replenishable FBA ASINs have been in stock during the last 30 days, weighted by the number of units sold for each SKU
in the last 60 days". [official, listing playbook 2026-10-14, not re-read]. An older staff post gives the same
definition and a worked example: "FBA in-stock rate is the percentage of time that replenishable FBA products have
been in stock for the past 30 days, weighted by the number of units sold in the past 60 days."; "[(2x50%) + (3x100%)]
/ (2+3) = 80%". [official] Seller Forums post by SEAmod relaying "the Amazon Business team", `datePublished` 2018-04-18,
https://sellercentral.amazon.com/seller-forums/discussions/t/c7a446a3fd90c44976fabe1b2b84f5a2, read 2026-11-10.

**G2. A low in-stock rate does not lower the IPI score; Amazon has said so in both the old post and the current FAQ.**
Old post: "A low FBA in-stock rate doesn't lower your IPI score, but if you go out of stock on a popular product, your
lost sales represent a missed opportunity to increase your IPI score." [official] SEAmod post as above. Current FAQ
(GZJF4DY2W6MERBAL, v19): "The in-stock rate itself is not a direct input into your IPI score, and a low in-stock rate
does not hurt your score, unless your most popular products consistently go out of stock". [official, listing
playbook 2026-10-14, not re-read]. I found no Amazon page announcing a date on which the in-stock rate was "removed"
from the score; the two statements, years apart, say the same thing. The Minimum Inventory Level announcement (H1)
adds that "Maintaining the Minimum Inventory Level will positively contribute to your IPI score."

**G3. A seller can take a SKU out of the in-stock rate.** "Marking a SKU as not replenishable, by hiding it on the
Restock Inventory page, removes it from your FBA in-stock rate calculation… the SKUs you hide will no longer display
restock recommendations". [official] SEAmod post as above (historical wording; the current help page was not read
first-hand).

**G4. Estimated lost sales: Amazon has published two different definitions at two times.**
- Current, in money: "Estimated FBA lost sales in the last 30 days is equal to the forecasted unit sales on days that
  your products were out of stock multiplied by the average sales price." *Inventory performance* (G202174810, v9).
  [official, listing playbook 2026-10-14, not re-read].
- Older, in units, on the since-removed Inventory In Stock report: "Estimated Lost Sales (Units) The sales run rate for
  the previous 60 days multiplied by the days the product is out of stock… 2 x 15 = 30"; with "In Stock % (over time)
  The percentage of time the product has available inventory over the period…28.1 / 30 = 93.7%" and "Weekly Sales Rate
  When In Stock … (7 x total units sold in the period) / number of days in stock in the period… (7 x 100) / 25 =
  28.00". [official, via a seller's forum post quoting Amazon's help text, 2018-04-11]
  https://sellercentral.amazon.com/seller-forums/discussions/t/ce80b3a0306ed49e5747611185f2bd0e, read 2026-11-10. The
  thread says the report was withdrawn ("all inventory related data can now be found in: MYI for MFN Units; Restock
  Inventory Report for FBA Units").

The first multiplies Amazon's forecast by price; the second multiplied a trailing run rate by days out. Neither is a
count of orders that were lost.

**G5. "Restock today" and the planning guideline.** "The Restock today button shows the number of SKUs for which the
days of supply is less than the restock lead time."; "A good guideline is to maintain enough inventory to cover 30 to
60 days of your expected sales."; excess is "over 90 days of supply based on the forecasted demand". *Inventory
performance* (G202174810, v9). [official, listing playbook 2026-10-14, not re-read]. sell.amazon.com repeats the excess
side: "Amazon considers you to have excess inventory if you have: Over 90 days of supply; At least one unit aged over
90 days; A better ROI opportunity". [official] https://sell.amazon.com/learn/inventory-management, read 2026-11-10.

**G6. A very high sell-through is read by Amazon as a stock-out risk.** IPI FAQ: "A very high sell-through rate can
indicate scarce inventory levels, which can lead to slower customer delivery and out of stocks."; "Sell-through rate
is updated daily and looks at the past 90 days of shipped units and average inventory over that same period."; "Newly
created ASINs in their first 90 days do not affect your IPI score." [official, listing playbook 2026-10-14, not
re-read].

**G7. The Restock report's Alert column has no published list of values on any page I could read.** *Fulfillment by
Amazon (FBA) Reports* lists the Restock Inventory report's columns — Price; Sales last 30 days; Units Sold Last 30
Days; Total Units; Inbound; Available; FC transfer; FC Processing; Customer Order; Unfulfillable; Working; Shipped;
Receiving; Fulfilled by; Total Days of Supply (including units from open shipments); Days of Supply at Amazon
Fulfillment Network; Alert; Recommended replenishment qty; Recommended ship date; Recommended action (US store); Unit
storage size (US, CA, UK, DE, FR, IT, ES) — and says "Provides recommendations on products to restock, suggested order
quantities, and reorder dates. Content updated in near real-time." It gives no values and no definition for Alert.
[official] read 2026-11-10. The only description found is a third party's: "InStock Alert - Shows if there is a Low
Stock or Out of Stock alert for the product in the latest Amazon Report." [opinion] Sellercloud help,
https://help.sellercloud.com/omnichannel-ecommerce/amazons-fba-restock-report/, read 2026-11-10. A search result
attributed to an EcommerceBytes report an Amazon statement that restock recommendations apply when "current inventory
must be zero, or current days of supply must be less than 14 days" [snippet]; EcommerceBytes has ceased publication and
the page could not be read. The criterion matches Amazon's Fulfilled-by-Merchant Restock feature: News_Amazon, "Get
personalized restock recommendations for your inventory", `datePublished` 2025-03-14,
https://sellercentral.amazon.com/seller-forums/discussions/t/33b8ff50-5efb-456d-a2d3-12bcf9b86231, read by the verifier
2026-11-10: recommendations for "your Fulfilled by Merchant listings" cover products meeting "specific criteria,
including active sales in the last three months, projected demand, and current days of supply less than 14 days"
[official]. It is an eligibility rule of an FBM feature, not an FBA alert threshold (as `areas/restock-and-forecast.md`
A6 and `beyond/sellers-tools-and-research.md` B record). The Restock help page (G5QJ5MF6MGBBYDSU) and the Replenishment Alerts page (G200285580)
are unreachable; a search result for the latter described an alert threshold set in units or in weeks of cover, "the
number of weeks of on-hand fulfillable inventory based on your sales over the last 30 days" [snippet].

**G8. Report scope.** Restock Inventory report: "All stores except India (IN)"; "This report can only be requested."
The FBA Manage Inventory Health report: "Not available in the NL, PL, SE, or BE stores." [official] *Fulfillment by
Amazon (FBA) Reports*, read 2026-11-10. Amazon India's own restock page says recommendations "are based on a variety
of factors, which may include customer demand from the fulfilment centre, your sales history, seasonality trend,
historical selling prices and sales volume." [official] sell.amazon.in restock page, read 2026-11-10.

### H. Minimum Inventory Level and the low-inventory-level fee (the cost of running thin)

**H1. Amazon's announcement of the Minimum Inventory Level states a sales figure.** News_Amazon, "Plan FBA inventory
levels using a new metric", Seller Forums, `datePublished` 2023-12-19 (page HTML; re-read by the verifier 2026-11-10),
https://sellercentral.amazon.com/seller-forums/discussions/t/1aa7614a-5542-4529-abe1-ddf452681630,
read 2026-11-10:

- "We've launched a new Minimum Inventory Level metric to help FBA sellers plan inventory levels more effectively,
  improve delivery speeds, and help them to avoid the recently announced low-inventory-level fee."
- "We leverage advanced machine learning models to analyze demand forecasts and replenishment settings and recommend
  the minimum number of units per product that you should have on hand in our fulfillment centers."
- "Maintaining inventory above the Minimum Inventory Level helps you meet customer demand and offer faster delivery
  speeds as products can be distributed across local fulfillment centers closer to customers. Sellers who maintain
  units above the Minimum Inventory Level see a 15% increase in sales over a four-week period on average, though actual
  results may vary."
- "Your IPI score reflects how well you reduce excess inventory, fix stranded listings, and improve sell through.
  Maintaining the Minimum Inventory Level will positively contribute to your IPI score."
- "Restock recommendations will continue to provide you with specific recommended ship-by dates and replenishment
  quantities…"

[official]. The survey's stock notes and the listing playbook both said the 15% figure was on no Amazon page; it is on
this one (the verifier re-read the sentence verbatim on 2026-11-10). The figure is Amazon's own, an average with no
method shown, and it compares sellers who hold the level with those who do not; it is not a measured effect of a
stock-out. The same week a Chinese post words it, reposted by the 雨果网 contributor account 亚马逊开店分享社 (a
"观察员" account, not Amazon's verified account) with the source line 「来源：亚马逊全球开店 微信公众号：AmazonGS」 (Amazon
Global Selling's WeChat account):
「ASIN保持最佳库存水平的卖家，在4周内商品的销售额增长了15％*，而ASIN库存水平过低可能导致曝光量和转化率下降！」 ("sellers whose ASINs
keep the best inventory level saw sales grow 15% in 4 weeks*, and too low a level may reduce exposure and conversion");
the footnote reads 「*数据来源：亚马逊2023 Accelerate」 ("data source: Amazon Accelerate 2023"); and names four states for an ASIN's on-hand level: 「"缺货"、"库存不足"、"健康"
或"过剩"」 (out of stock, low, healthy, excess). It also says what the level counts: 「最低库存水平仅考虑亚马逊配送网络内的现有可售库存…计算方法是将可供销售的库存商品、在运营中心之间转移的商品以及预留商品的总和」 ("the Minimum
Inventory Level considers only on-hand sellable stock in Amazon's network… the sum of sellable units, units in transfer
between fulfilment centres and reserved units"), and 「最低库存水平包含在途库存吗？不包括。」 ("does it include inbound? No");
and that the level is updated "at least weekly". [official, via 亚马逊开店分享社 on 雨果网 reposting AmazonGS, 2023-12-11]
https://www.cifnews.com/article/152685, read by the Chinese helper stream and re-read by the verifier 2026-11-10.

**H2. The fee, as a mechanism only.** The same announcement: "Effective April 1, 2024, the low-inventory-level fee will
apply when both…" long-term (90 days) and short-term (30 days) historical days of supply are below 28 days. The listing
playbook's read of the fee page (GV43F6S76Y9DHYRH, v29) recorded: charged at FNSKU level from 2026-01-15; bands 0–14,
14–21 and 21–28 days; historical days of supply = "average daily inventory units on hand divided by average daily
shipped units"; inbound units excluded; exemptions including a product that "sold less than 20 units in the past 7
days"; and "Minimum Inventory Level is a forward-looking metric measured in units". [official, listing playbook
2026-10-14, not re-read]. Amazon's own 雨果网 account gives the Chinese wording of the formula and the FNSKU change:
「关键变化: FBA低库存水平费将按FNSKU收取，不再按照父ASIN计算。」; 「短期历史供货天数=过去30天内平均每日现货库存商品数量/过去30天内平均每日发货商品数量」.
[official, via the 雨果网 account "亚马逊", source line 「来源：亚马逊」] 2026-01-27, https://www.cifnews.com/article/182908,
re-read by the verifier 2026-11-10. **The 2027 method (aligned with `areas/holding-costs.md` I1–I3, verifier
2026-11-10).** Amazon's letter "Update to US Referral and Fulfillment by Amazon fees for 2027" (Sunny Jain, 2026-11-05,
https://sellingpartners.aboutamazon.com/update-to-us-referral-and-fulfillment-by-amazon-fees-for-2027) says "Today, the
fee is assessed using trailing 30- and 90-day sales"; Amazon Global Selling's China notice, as the holding-costs seat
read it, describes the 2027 method: each week Amazon records an FNSKU's inventory and divides it by average daily units
shipped in the 28 days **before** the assessment and again by the 28 days **after**; the fee is charged only if both
are below 28 days, so it is known only four weeks after the assessment (charged in arrears). [official, as read by the
holding-costs seat 2026-11-10; not re-read here]. The 2027 effective date and amounts are `areas/holding-costs.md`'s.
The FBA Manage Inventory Health report carries `Exempted from Low-Inventory-Level fee?`, `Low-Inventory-Level fee
applied in current week?` and `Last updated date for Historical Days of Supply` [official] *Fulfillment by Amazon (FBA)
Reports*, read 2026-11-10 (gap fill 2026-11-10). Amounts, bands and exemptions are `areas/holding-costs.md`'s and are
read at run time.

**H3. Two facts about the fee that bear on a stock-out.** It reads a backward-looking average of on-hand units, so it
is not a measure of today's cover; and eComEngine states that "Amazon low-inventory-level fees are not charged when a
product is out of stock." [opinion, eComEngine, via the listing playbook 2026-10-14, not re-read]. I found no Amazon
sentence for the second.

**H4. The Prime Day playbook's figures (Amazon's, dated, for an event).** *Prime Day readiness playbook*
(GM2ADTH3XH3A5N57, v4): "For new ASINs or products without recommendations, aim to keep at least 28 days of inventory
based on historical demand."; "Review any Minimum Inventory Level (MIL) Potential Sales Lift estimates…"; "To avoid the
low-inventory level fee, make sure you have 4-6 weeks of inventory available before your deal event. After the event…
maintain at least 28 days". [official, office capture 2026-10-14] local file `GM2ADTH3XH3A5N57-v4.txt`, read
2026-11-10. Amazon Global Selling's Chinese text, reposted by 亚马逊开店分享社 on 雨果网 with the source line 「来源：亚马逊全球开店
微信公众号：AmazonGS」: 「建议卖家至少保持4-8周库存量」 ("keep at least 4–8 weeks of stock"). [official, via 亚马逊开店分享社 on 雨果网
reposting AmazonGS] 2025-09-10, https://www.cifnews.com/article/178630, re-read by the verifier 2026-11-10.

### I. Amazon's cover measures, and where each is defined

| Measure | Where it appears | Definition found | Tag |
|---|---|---|---|
| Historical days of supply (short term 30 days, long term 90 days) | Low-inventory-level fee; Planning report columns `historical-days-of-supply`, short- and long-term | "average daily inventory units on hand divided by average daily shipped units"; inbound excluded | [official, listing playbook 2026-10-14, not re-read]; Chinese wording [official] 雨果网 2026-01-27 |
| Days of supply (forward) | Planning report `days-of-supply`; Restock report "Days of Supply at Amazon Fulfillment Network" and "Total Days of Supply (including units from open shipments)" | Column names only on the developer page; the IPI page ties it to "forecasted demand" (G5) | [official] column names; definition not found first-hand |
| Weeks of cover | Planning report `weeks-of-cover-t30`, `weeks-of-cover-t90` (and `weeks-of-cover` in a later column block) | None on the developer page. Search result for the Replenishment Alerts help page: "the number of weeks of on-hand fulfillable inventory based on your sales over the last 30 days" | [official] column names; [snippet] definition |
| Sell-through | Planning report `sell-through`; IPI | "looks at the past 90 days of shipped units and average inventory over that same period" | [official, listing playbook 2026-10-14, not re-read] |
| Minimum Inventory Level | Planning report `fba-minimum-inventory-level`, `fba-inventory-level-health-status` | "the minimum number of units per product that you should have on hand in our fulfillment centers" (H1); "forward-looking… measured in units" (H2) | [official] forum post; [official, listing playbook, not re-read] |
| In-stock rate | IPI dashboard | G1 | as G1 |

The Planning report's column list (which also carries `units-shipped-t7/t30/t60/t90`, `sales-shipped-last-7/30/60/90-days`,
`alert`, `estimated-excess-quantity`, "Inventory Supply at FBA") is from *Fulfillment by Amazon (FBA) Reports*, read
2026-11-10; the page names the columns and defines none. The historical measures divide by shipped units; the forward
ones use Amazon's forecast. A SKU can therefore show long forward days of supply and short historical days of supply
at once, or the reverse.

### J. Subscribe & Save

**J1. An in-stock rate is an eligibility criterion.** *What is Amazon Subscribe & Save?*, sell.amazon.com blog dated
2025-08-25, https://sell.amazon.com/blog/subscribe-and-save, read 2026-11-10: "To participate in Subscribe & Save, all
sellers need to meet the following eligibility criteria: … Have a strong fulfillment history and in-stock rate greater
than 90%". *Subscribe & Save*, https://sell.amazon.com/programs/subscribe-and-save, read 2026-11-10: "eligible for
Subscribe & Save based on their category, average selling price, sales performance, and fulfillment history and
in-stock rate"; "Keeping products in stock is a key consideration for the Subscribe & Save program. You can monitor
inventory directly from the Subscribe & Save page."; "Eligible FBA products are automatically enrolled at a 0%
seller-funded discount, with Amazon funding a 5% discount." [official]. A staff reply on the forums names the window:
"Trailing 28 days in-stock rate is greater than 90%; Not in a restricted product category; Average selling price is
less than $200; Offer is buyable". [official] Manny_Amazon, Seller Forums, `datePublished` 2024-07-23,
https://sellercentral.amazon.com/seller-forums/discussions/t/9f2139f7-377c-488f-b8dd-d30264645e5e, read 2026-11-10.

**J2. The Replenishment API measures what a stock-out cost the programme.** Replenishment API model 2022-11-07:
`NOT_DELIVERED_DUE_TO_OOS` — "The percentage of items that were not shipped out of the total shipped units over a
period of time due to being out of stock." (`notDeliveredDueToOOS`: "Applicable to `PERFORMANCE` `timePeriodType`");
`LOST_REVENUE_DUE_TO_OOS` — "The revenue that would have been generated had there not been out of stock." `FORECAST`
supports only `TOTAL_SUBSCRIPTIONS_REVENUE` and `SHIPPED_SUBSCRIPTION_UNITS`, and is "supported for sellers but not
for vendors"; 30/60/90-day forecast fields. [official] local model
`models/replenishment-api-model/replenishment-2022-11-07.json`, read 2026-11-10.

**J3. Offer-level state.** Same model. `EligibilityStatus`: `ELIGIBLE`; `INELIGIBLE` ("will not be able to add new
subscriptions and existing subscriptions will be cancelled"); `SUSPENDED` ("…existing subscriptions will be
fulfilled"); `REPLENISHMENT_ONLY_ORDERING` ("…This eligibility status also blocks one-time purchases to preserve
inventory for existing subscriptions."). `deliveriesConditions`: `NEXT_30_DAYS_DELIVERIES_PAUSED_PRICING`,
`NEXT_30_DAYS_DELIVERIES_PAUSED_NON_BUYABLE` ("paused because the offer is not buyable"),
`NEXT_30_DAYS_DELIVERIES_AT_LOW_INVENTORY_RISK_ONLY`, `NEXT_30_DAYS_DELIVERIES_AT_LOW_INVENTORY_RISK`,
`NO_ISSUES_FOR_NEXT_30_DAYS_DELIVERIES`. Offer fields: `inventory` ("The available inventory count for the offer."),
`stockRisk` ("The stock risk level of the offer, indicating the risk of the offer going out of stock.", a free
string with no enumerated values), `forecastDeliveries` (next 15, 30, 60 days). [official].
`REPLENISHMENT_ONLY_ORDERING` means a SKU with units on hand can be closed to one-time buyers by Amazon; on that SKU
"fulfillable above zero" and "buyable by a new customer" are different things.

**J4. Scope and history.** *Replenishment API* guide (page `updatedAt` 2026-09-09), read 2026-11-10: "Currently, the
Subscribe & Save replenishment program is supported."; "available wherever Amazon Subscribe & Save is live… also
available to vendors and Fulfillment by Amazon (FBA) selling partners". The two older reports
`GET_FBA_SNS_FORECAST_DATA` and `GET_FBA_SNS_PERFORMANCE_DATA` were announced for deprecation on 2025-06-25 and
removed on 2025-12-11. [official] *SP-API deprecations* table, read 2026-11-10.

**J5. Stock held for subscriptions is outside "highly available".** `ItemInventoryEventChangeNotification`:
`highlyAvailableInventory` is on-hand stock "…minus units in customer shopping carts or otherwise bound for other
orders (for example, subscribe-and-save orders)." [official] local schema, read 2026-11-10.

### K. Deals and coupons

**K1. Closing a listing cancels its deal for good.** *Amazon deals* (G202111490, v25): "Do not change the status of any
ASINs participating in deals to Closed on the Manage Inventory page. Doing so will cancel any deal currently scheduled
for that ASIN. Canceled deals cannot be reactivated." [official, office capture 2026-10-14] local file
`G202111490-v25.txt`, read 2026-11-10. This bears directly on the "close the listing" tactic (P5).

**K2. Deal selection favours quantity.** *Deals for events* (G202183600, v10) favours deals with "a large available
quantity" in selection. [official, office capture 2026-10-14] local file `G202183600-v10.txt`, read 2026-11-10. The
exact stock requirement for a deal at submission and at run time was not read first-hand in this session; third-party
pages disagree on how many days before a Lightning Deal the stock must be in place (25 hours, seven days) [snippet].

**K3. A coupon is switched off per product when stock is short (gap fill 2026-11-10).** Danny_Amazon, "Coupon error?
Understand Why!", Seller Forums, `datePublished` 2024-08-09,
https://sellercentral.amazon.ca/seller-forums/discussions/t/9d6c58b4-130d-4d60-b6e1-9e573ac8efa6, read by the verifier
2026-11-10: "Approximately six hours before your coupon start time, Amazon's system validates your coupon… These
validation rules are continuously enforced as long as your coupon is active. If one or more of the products in your
coupon don't pass these rules, the coupon offer may be disabled on that product or products, while the coupon remains
active on the rest of the eligible products."; "Inventory Error: If you don't have enough inventory to accommodate the
customer demand that your coupon might generate, the coupon offer will be disabled on the affected product(s). To fix
this, simply send in more inventory and recheck all the product attributes, then recreate the coupon." [official,
forum staff post]. The post gives no quantity for "enough", and says a disabled coupon is recreated, not resumed.

### L. Variations

**L1. A child with no stock drops off the detail page.** *Variation relationship FAQ* (G201951410, v16): a child not
showing on the detail page "typically happens if: The child listing is inactive or has no inventory in Seller
Central"; the parent ASIN "does not have inventory". [official, office capture 2026-10-14] local file
`G201951410-v16.txt`, read 2026-11-10.

**L2. The fee moved from parent to FNSKU.** From 2026 the low-inventory-level fee is assessed per FNSKU, not per parent
ASIN (H2). No Amazon page read says how a child's stock-out affects the search placement of its siblings; the only
evidence is practitioners' (P10).

### M. The sales figures a run-out date is computed from

**M1. Ordered and shipped are separate fields, in both Sales and Traffic views.** Data Kiosk
`analytics_salesAndTraffic_2024_04_24`: `ByAsinSales` and `ByDateSales` each carry `unitsOrdered` and `unitsShipped`
("The number of units shipped for the selected time period."), with B2B twins `unitsOrderedB2B` and `unitsShippedB2B`.
[official] local schema, lines 153–172 and 457–479, read 2026-11-10. The Sales and Traffic report schema carries the
same pair with `sessions`, `buyBoxPercentage` and `unitSessionPercentage`. [official]
`schemas/reports/sellerSalesAndTrafficReport.json`.

**M2. `getOrderMetrics` counts ordered units, with filters.** Sales API: `unitCount` — "The number of units in orders
based on the specified filters."; filters `asin` or `sku` (one, not both), `fulfillmentNetwork` (MFN / AFN),
`buyerType` (B2B / B2C); hourly granularity only within the last 30 days. [official] local model
`models/sales-api-model/sales.json`, read 2026-11-10.

**M3. Amazon's own cover measures use shipped units.** Historical days of supply divides by "average daily shipped
units" (H2); the Planning report's sales columns are `units-shipped-t7/t30/t60/t90` (I). The Restock report's column
is "Units Sold Last 30 Days" with no definition on the developer page. A velocity built on ordered units and Amazon's
days-of-supply figures therefore need not agree, most visibly when orders are pending or stock was short.

**M4. Pending orders already hold stock.** A `Pending` order is placed but not authorised (D4); the units it holds are
in `pendingCustomerOrderQuantity` (A2), not in `fulfillableQuantity`.

### N. Amazon's own agent skills (recorded, not borrowed)

Amazon Selling Partner plugin 1.0.0 (Apache-2.0), local files read 2026-11-10.

**N1. The stock-out skill's arithmetic and bands.** `skills/stockout-prevention/SKILL.md`: a 30-day window,
`avg_daily_units = unitCount / 30`, `days_of_cover = fulfillableQuantity / avg_daily_units`; "CRITICAL — days_of_cover
< 7", "WARNING — 7 ≤ days_of_cover < 21", "HEALTHY — days_of_cover ≥ 21 (do **not** flag these…)"; "Amazon's own
analysis rule is *days of supply < 14 → at risk*… 14–21 is an *early-warning* buffer this skill adds";
`gap_days = shipment_arrives - stockout_date`. It reads an `estimatedDeliveryWindow` from `listInboundPlans`, a field
the survey found absent from that operation's response. It tells the agent to mention "lost sales, BSR/rank recovery,
and that running very lean can trigger the **low-inventory-level fee**", and forbids one tactic: "Do not raise pricing
as an option at all"; "Coming from Amazon, pricing advice carries implications this skill must not create".

**N2. The metric catalogue.** `skills/seller-analytics/references/metrics-catalog.md` lists, for Amazon's own analytics
endpoint (`sellingpartner-ai.amazon.com`, which this research did not call): `FBA_INV_VIS_ONHAND_PMEAN_DOS`,
`FBA_INV_VIS_ONHAND_P90_DOS`, `FBA_INV_VIS_TOTAL_PMEAN_DOS`, `FBA_INV_VIS_TOTAL_P90_DOS`,
`FBA_INV_VIS_RECOMMENDED_MIL_PMEAN_DOS` and `…_P90_DOS`, `FBA_INV_VIS_RESTOCK_ORDER_DATE`, `FBA_INV_RESTOCK_QTY`,
`FBA_FORECAST_N7_P80`, `FBA_FORECAST_N30_P80`, `FBA_FORECAST_N60_P80`, `FBA_UNITS_SHIPPED_T30`, `FBA_AVAILABLE_QTY`,
`FBA_INV_VIS_BOUND_QTY`, `FBA_INV_VIS_CUSTOMER_SHIP_DISABLED_QTY`; and states "Analysis rule: **days of supply < 14 →
at risk of stockout.**" The names show that Amazon computes days of supply at a mean and at a 90th percentile of its
forecast, and a P80 unit forecast at 7, 30 and 60 days.

**N3. The listing skill's shortcut.** `listing-buyability/SKILL.md`: a complete product with an offer that is not
`BUYABLE` is "almost certainly **out of stock**".

**N4. Which of these numbers are on an Amazon page (corrected by the verifier 2026-11-10, aligned with
`areas/restock-and-forecast.md` A6/D4 and `beyond/sellers-tools-and-research.md` B).** The 7-day and 21-day bands are
the skill's own, as it says ("an *early-warning* buffer this skill adds"). As a stock-out-risk rule, "days of supply <
14 → at risk" is on no Amazon help or developer page read. 14 does appear on Amazon pages in two other roles: as an
eligibility criterion of the Fulfilled-by-Merchant Restock feature ("current days of supply less than 14 days",
News_Amazon 2025-03-14, G7), and as a band edge of the low-inventory-level fee (0–14, 14–21, 21–28 days of historical
supply; H2, as the listing playbook read the fee page). Amazon's published figures that I could source are 28 days (the fee, H2; the
Prime Day playbook, H4), 30 to 60 days (G5), 4–6 and 4–8 weeks (H4), 90 days (excess, G5) and the restock lead time
(G5).

### O. Roles for every read named in this file

From *Role Mappings for SP-API Operations* (https://developer-docs.amazon.com/sp-api/docs/role-mappings,
page `updatedAt` 2026-10-28) and *Role Mappings for SP-API Types* (https://developer-docs.amazon.com/sp-api/docs/role-mappings-for-types,
page `updatedAt` 2026-09-09), both read 2026-11-10, each entry extracted from its own block. (The slugs
`role-mappings-for-sp-api-operations` and `…-types` returned "Page Not Found" on the verifier's read; the verifier
re-parsed every row below from the two pages above and found each matches. Restricted roles Amazon also lists, such as
Direct to Consumer Shipping, are left out of the table.) The report-type page's own Roles lines agree: Restock, Manage
Inventory and Reserved reports name Pricing and Amazon Fulfillment; the Manage Inventory Health and both Ledger reports
name Amazon Fulfillment only. PL = Product Listing, PR =
Pricing, BA = Brand Analytics, FA = Finance and Accounting, AF = Amazon Fulfillment (the door's five); IOT = Inventory
and Order Tracking, SPI = Selling Partner Insights, BC = Buyer Communication, BS = Buyer Solicitation (outside the
five).

| Read | Roles Amazon names | Held by the door through |
|---|---|---|
| `getInventorySummaries` (FBA Inventory v1) | AF, PL | AF, PL |
| `getListingsItem`, `searchListingsItems` (Listings Items 2021-08-01) | IOT, PL | PL |
| `getItemOffers`, `getListingOffers`, `getPricing` (Product Pricing v0) | PR, PL | PR, PL |
| `getCompetitiveSummary`, `getFeaturedOfferExpectedPriceBatch` (Product Pricing 2022-05-01) | PR | PR |
| `getOrderMetrics` (Sales v1); `getOrders` (Orders v0); `searchOrders` (Orders 2026-01-01) | AF, BC, BS, FA, IOT, PR, PL, SPI | AF, FA, PR, PL |
| Replenishment `getSellingPartnerMetrics`, `listOfferMetrics`, `listOffers` | BA, IOT | BA |
| Data Kiosk `createQuery` (Sales and Traffic dataset) | BA | BA |
| `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`, `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA`, `GET_FBA_MYI_ALL_INVENTORY_DATA`, `GET_RESERVED_INVENTORY_DATA`, `GET_STRANDED_INVENTORY_UI_DATA` | AF, PR | AF, PR |
| `GET_FBA_INVENTORY_PLANNING_DATA`, `GET_LEDGER_SUMMARY_VIEW_DATA`, `GET_LEDGER_DETAIL_VIEW_DATA`, `GET_AFN_INVENTORY_DATA`, `GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_SALES_DATA` | AF | AF |
| `GET_SALES_AND_TRAFFIC_REPORT` | BA | BA |
| `GET_MERCHANT_LISTINGS_ALL_DATA`, `GET_MERCHANT_LISTINGS_DATA`, `GET_MERCHANT_LISTINGS_INACTIVE_DATA` | IOT, PR, PL | PR, PL |
| `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL` | AF, IOT, PR | AF, PR |
| `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL` | AF, IOT, PR, PL | AF, PR, PL |
| `GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL` | AF, IOT, PR | AF, PR |
| `GET_BRAND_ANALYTICS_SEARCH_QUERY_PERFORMANCE_REPORT`, `GET_BRAND_ANALYTICS_SEARCH_CATALOG_PERFORMANCE_REPORT`, `GET_COUPON_PERFORMANCE_REPORT` | BA | BA |
| `GET_PROMOTION_PERFORMANCE_REPORT` | BA, SPI | BA |
| Notification `FBA_INVENTORY_AVAILABILITY_CHANGES` | AF | AF |
| Notifications `ITEM_INVENTORY_EVENT_CHANGE`, `ITEM_SALES_EVENT_CHANGE`, `DETAIL_PAGE_TRAFFIC_EVENT` | BA | BA |
| Notifications `LISTINGS_ITEM_STATUS_CHANGE`, `LISTINGS_ITEM_MFN_QUANTITY_CHANGE` | PL | PL |
| Notifications `ANY_OFFER_CHANGED`, `PRICING_HEALTH` | PR | PR |
| Notification `ORDER_CHANGE` | AF, IOT | AF |
| Feed `JSON_LISTINGS_FEED` (a write) | IOT, PL | PL |

Every read this file builds on is reachable with one of the five roles. The Amazon Fulfillment role is present on the
test store's application (office-reported, 2026-11-10, one call on the test store), so the reads open to Amazon
Fulfillment only (the Planning and Ledger reports, `FBA_INVENTORY_AVAILABILITY_CHANGES`) are written as readable
today. `POST_FLAT_FILE_INVLOADER_DATA` is not on the types page.

## What practitioners add

Everything in this section is **[opinion]** unless tagged otherwise. English sources were read by the English helper
stream (notes `notes-practitioners-en.md`, entries E1–E76), Chinese sources by the Chinese helper stream
(`notes-practitioners-cn.md`, C1–C66), all on 2026-11-10. 知无不言 hides replies from a logged-out reader, so every
知无不言 entry is an opening post only. Almost none of these authors shows data; where one does, it is said.

### P1. Does a stock-out cost rank beyond the days it lasts? Practitioners disagree, and the few who measured disagree with the majority

**The majority view: yes, within days, and recovery takes weeks.**
- Steven Pope, My Amazon Guy (2026-08-10): "Your keyword positions start sliding after roughly three to five days out
  of stock, and getting them back takes two to four weeks of rebuilt velocity." https://myamazonguy.com/?p=170448
- SellerSprite (2026-04-17): "Even short stockouts (3–5 days) can cause ranking losses that take weeks or months to
  recover."; its own bands "1–2 days: Minimal ranking impact… 3–5 days: Noticeable drop in rankings (10–30 positions);
  recovery possible within 2–4 weeks. 6+ days: Severe damage". It cites "a study by Feedvisor in 2020" (34% of ranking
  position lost after 7 days) with no link; two searches did not find that study.
  https://www.sellersprite.com/en/blog/The-Impact-of-Out-of-Stock-on-Keyword-Rankings
- Repricer.com (2026-08-27): "Organic ranking begins to decay within 24 to 48 hours of a stockout on high-velocity,
  competitive ASINs." https://www.repricer.com/blog/amazon-repricing-stockout/
- Onramp Funds (2026-10-20): "Just one week of being out of stock can result in 4 to 6 weeks of reduced visibility";
  "A 7-day stockout can slash organic rankings by 30–50%"; and a figure that also circulates on My Amazon Guy, "For
  240 sellers analyzed, stockouts led to an average of $18,000 in lost revenue". The page footnotes other blogs; no
  dataset is shown. https://www.onrampfunds.com/blog/real-cost-stockouts-amazon-beyond-lost-sales/
- Chuck Kessler, Canopy Management (2026-06-08): "Frequent stockouts now trigger ranking suppression that persists even
  after you restock." (via the listing playbook, not re-read.)
- Seller Labs (2026-07-03): "A short stockout of 24–48 hours on an otherwise strong listing with a long sales history
  may cause minimal lasting damage. A stockout lasting 5 or more days typically causes measurable rank loss".
- Julian Bonte-Friedheim, 8fig (2024-04-02): "Amazon even starts ranking products lower that aren't sold out and are
  simply running low on inventory." Acadia (2017) offered the same as a hypothesis: "We have seen impressions and
  clicks decline as soon as a product gets hit with this warning."
- 跨境大师兄Peter on 雨果网 (2025-12-22) gives the most numeric curve and the least support: 「断货第1-3天：排名下降10-15%… 断货第4-7天：排名下降30-50%…
  断货第8-14天：排名下降60-80%… 断货15天+：排名下降80-95%」 (days 1–3: rank down 10–15%; 4–7: 30–50%; 8–14: 60–80%; 15+: 80–95%). He
  says he observed 127 cases 「断货后恢复失败」 (of failed recovery after a stock-out), a sample chosen for failure, and shows
  no table. https://www.cifnews.com/article/181907
- 赛狐ERP (2026): 「断货1-2周虽不会触发账户健康指标的正式处罚，但搜索排名和购物车赢得率会受到直接影响。」 (one to two weeks out triggers no
  account-health penalty, but search rank and Buy Box win rate are hit directly).

**The "grace period" in Chinese sources is a number that changes as it is copied.** 藏龙荟 on 雨果网 (2019-06-11):
「亚马逊其实对断货是有3天的时间宽限。即使真的断货了，如果在72小时之内能够补货上架的话，对产品listing的排名和权重是不会有影响的。」 ("Amazon in fact gives a 3-day grace; restock
within 72 hours and rank and weight are unaffected"). 董海温 (2022-03-22) and 出海记事本 (2023-09-19) repeat three days.
K哥聊出海 (2021-09-29) prints the same numbered sentence with 「2周」 (two weeks) in place of three days and then continues
word for word with Moss的精神家园's 2018-02-23 text (「两周之内补货上架以后，你会发生一个神奇的现象，产品的排名没有变化…」); Moss's own
two-week section is a routine of his (lower price, keep the listing "currently unavailable", no FBM offer), not a claim
that Amazon grants a grace period. The verifier re-read all five posts on 2026-11-10; the earliest three-day sentence
found is 藏龙荟's of 2019-06-11 (two searches for an earlier one found none). 鹏城阿兽 (2022-01-19) says 3–7 days by category;
an unsigned AMZ123 page says 7 days. None names an Amazon page. No Amazon page read in this session states any grace
period.

**The relative view.** Kuso王道 on 雨果网 (2018-01-19): 「无论是哪个方式 你排名掉不掉完全是取决于你后面的对手追赶的速度」 ("whichever way, whether your
rank drops depends entirely on how fast the rivals behind you catch up"), with one anecdote of a best-seller that held
first place through 13 days out. T. Brian Jones, Inventory Hero (2026-01-15): "The mechanism is velocity, not a
penalty flag"; "Because Amazon does not document this, treat these as directional patterns, not guarantees." Steven
Pope's other page (2026-06-15) attributes the decline to "Amazon's 180-day sales history window" and rates "0-2 weeks —
Minimal ranking damage", which conflicts with his own "three to five days" above; the 180-day window cites no Amazon
page.

**The measured cases.**
- Dave Bryant, EcomCrew (2021-12-10, updated 2024-09-10): "We looked at five ASINs across three accounts and multiple
  product categories that experienced stock outages within the last year." Conclusions: "Items almost always recover
  their sales rank that existed prior to the stock outage within four weeks after the stock outage"; "There is no
  significant penalty, short term or long term, for being out of stock on a product."; "There is no greater or lesser
  penalty for longer or shorter stock outages." The outages ran "from a couple of days to several months"; the page shows
six per-ASIN captions for its "five ASINs", and its measure is sales rank (Best Sellers Rank) before and after, read
off charts. His explanation of the common belief: "Short-term demand spikes due to
  holidays and seasonality often lead to an unexpected stock outage. When the item comes back in stock, this short
  term spike has disappeared and sellers blame it on being out-of-stock." He hedges for "ultra-competitive
  categories". One caption reads "The item never recovered its historical sales rank", and two others say the item "never
  recovered the sales rank bump from the preceding two weeks". https://www.ecomcrew.com/amazon-stockout-effects/
- Franz Jordan for Sellics (2017-03-14), one product: "Following his immediate restock, the rankings were predictably
  worse than before going out of stock. Critically, a week after the product was in stock again, the keyword rankings
  overall for the product had improved significantly."; "only a handful of sales following the restock was necessary
  to prompt Amazon's ranking algorithm to bring the ranking of the product back to where it was". The measure is the
  rankings of the product's top three keywords; the seller ran a Sponsored Products campaign at once on restock, "with
  82% of sales generated by Sponsored Products" in the first week, so the recovery is not separable from that push.
  https://www.skubana.com/out-of-stock-vs-price-hike/ (now redirects to extensiv.com; re-read by the verifier 2026-11-10)
- Jeevanantham Kailasam, DataWeave (2022-06-30), one CPG customer's products: "when products that ranked between 1-10
  went out of stock for just 1 day, their rank fell by over 28%. After 3+ days of being out of stock, their rank fell
  by 83%"; for ranks 10–20, 17% after one day. The page does not say how many products, whether "rank" is search
  position or BSR, or whether it was read during the outage or after restock; it measures the fall, not the recovery.
  https://dataweave.com/blog/amazon-stock-out-impact-on-ecommerce
- Profitero (2020-11-16; UK, brands selling to Amazon as vendors): "it takes an average of 9-10 days to recover search
  placement when a product is out of stock for 2+ days on both Amazon.co.uk and Tesco.com."; "brands lose, on average,
  62% of their sales on Amazon.co.uk when stock rates drop below 30% versus sales at a 90% in-stock rate." The report
  is behind a form; method unknown. The page at thegrocer.co.uk that the helper read returned 404 on the verifier's
  re-read (2026-11-10), so these figures rest on the helper's notes. SPS Commerce cites the same source as 42% and "4 days to regain full sales volumes
  after being out of stock for 1 day".
- A 知无不言 poster (2023-03-16), one product out about a month: 「补货后…第一天出了5单（该产品断货前日均10单左右），通过各个插件查询的大词自然位都在12-16左右，自然位并未产生明显下降…
  第二天自然位开始迅速下降，在25-35之间徘徊」 (ads were left to stop by themselves during the gap and the top-of-search bid raised from 80% to 120% on restock;
  on the first day back the head keyword's organic position was 12–16 against 10–15 before,
  "no clear drop"; on the second day it fell to 25–35 and stayed near 30, with conversion at about 3% against 5–6%
  before). The position held through the month out and fell after the offer returned and converted worse.
  https://www.wearesellers.com/question/71542
- Hello哥的宝藏部落 on 知无不言 (2022-08-15), analysing another member's charts for one 14.99-dollar product out about
  four weeks: weekly sessions 534 before, 28 at the bottom, 375 five weeks after restock; revenue per visitor 4.01
  before and about 2.5 after; ad conversion above 25% before and under 20% after; ACOS doubled. He adds that in a
  crowded market 「基本上重新续上货之后，跟重新推一个新品没有太大的区别了」 ("restocking is little different from launching anew"), while for a
  differentiated or protected product 「整体影响没有那么大」 ("the overall effect is not that large").
  https://www.wearesellers.com/question/62937
- A seller on the EU forums (2020-06-25) after about three months out: ads lifted "my sales rank from 250,000 to
  21,000" while the product "doesn't appear at all in any of the first 7 pages" for its main term. Best Sellers Rank
  came back in a day; keyword position did not.
- Kaijie on 知无不言 (2020-07-22), children out about 20 days, reviews intact: ACOS under 30% before and near 50% after;
  ad conversion about 11% before and 6.36% after.

**What survives, by these accounts.** Reviews and listing age (r/FulfillmentByAmazon thread read on a mirror,
2026-01-15: "After a long stockout, momentum is gone but it's not a negative. You're basically restarting with
advantages like reviews and age."). 夕木运营笔记本 (2026-01-30): 「断货后你的关键词排名会丢，订单会没有，但是之前积累的权重还在（只是在断货期间无法叠加）」 ("keyword rank
and orders go, but the accumulated weight remains; it just cannot add up during the gap"). Against that, 大美电商
(2022-12-28) puts listing weight at 「基本可以趋近于0」 ("close to zero") after two weeks.

**Scope limits practitioners themselves state.**
- Only-seller listings. SPS Commerce (formerly the SoStocked blog): "When you run out of stock (inventory), it hurts
  your listing's ranking if you are the only seller."; on a shared listing "those sales simply get redistributed among
  the remaining four sellers. The listing itself sees zero net impact".
- Seasonal products. Regan跨境 (2025-12-15): 「强季节性产品断货 1-5 个月都没关系，只要在旺季前 1 个月补货、启动推广」 (a strongly seasonal product can
  be out for 1–5 months without harm if restocked a month before its season); he says "data shows" and shows none.
- New listings. An answer on the UK forums (2025-05-12): "new listings aren't penalized as heavily as established
  ones"; a 2017 雨果问答 answer says the same.
- Marketplace. One 知无不言 poster (2021-08-30): 「之前一直做的都是欧洲站，即使断货一两周也能很快恢复断货前的状态。今年接触的美国站，感觉美国站一旦断货，影响都特别大」 (on the
  European stores one or two weeks out recovered quickly; on the US store a stock-out hits much harder). No second
  source.
- Repeats. alvin8868 on 知无不言 (2020-08-11): a two-year-old product "after several stock-outs this year" had not
  recovered six weeks after the last.

**Honeymoon.** Only Ken Zhou, My Amazon Guy (2026-02-14) addresses it: "Amazon's honeymoon period only applies to
brand-new listings"; changing the offer release date "provides no benefit for items returning to stock". Several
Chinese writers recommend the opposite route for a long gap: a new listing, then a variation merge to carry reviews
(Moss 2018; 董海温 2022; 深深深情 2022; 大美电商 2022 "after about a month"; Regan 2025 "over 3 weeks"). None reports a
measured result, and whether that merge is within Amazon's variation policy is not this file's to judge.

### P2. How long recovery takes, as claimed

"About one week" with promotions (Acadia, 2017, sellers' reports); a week (Sellics case); 9–10 days (Profitero); two
weeks (Acadia's beauty case; 日落大道 on 知无不言 for a high-ranked product with deals, 「基本可以一到两周就能回到之前的销量」); "at least
about 15 days" (藏龙荟); within four weeks (EcomCrew); two to four weeks (My Amazon Guy, SellerSprite); four to six weeks
or 30–60 days (Onramp); 42 days (SellerSprite's unnamed case); five weeks and still short (Seller Labs' unnamed case);
"a couple months" (a seller on the CA forums, 2024-10-18); Peter's curve of 70% by day 7 and 85–95% by day 14. No
source states a recovery time as a fixed multiple of the stock-out's length; the nearest are Onramp's one week to four
to six weeks and SPS Commerce's four days per day out (citing Profitero).

The cost of recovery relative to lost sales is priced three ways: about 14% of the total in sellerboard's worked
example ("The lost units account for roughly 80% of the damage"; the recovery line is labelled "indicative"); "can
equal or exceed the direct missed margin" (Inventory Hero, whose footnote says "Amazon does not publish a recovery
multiplier"); and 2–5 times (Onramp, footnoted to other blogs).

### P3. Before the stock-out: slow down, speed up, or leave alone

日落大道 on 知无不言 (2023-04-08) names the four modes: 「需要判断产品到底是减速/加速/正常速度/停售？」 (slow down, speed up, normal speed, or
stop selling).

**Raise price to slow sales.** For, in small steps: Ken Zhou, My Amazon Guy ("in small increments of no more than 10%
at a time. Wait 1-2 days between increases and monitor the Buy Box"; "Jumping more than 10% in a single change can
trigger Amazon to remove your Buy Box"); Samuel Clifford, BellaVix (below 21 days of supply); SPS Commerce ("subtle
price increases"); Repricer.com (a rule that adds $0.25 every four hours below 30 units); 日落大道 (5% steps, after
withdrawing coupon and promotions first, not far above the market median); 跨境大师兄Peter (5–8%, three to five days
before); 夕木运营笔记本 (5–10% for a 10–15 day gap, less if conversion falls more than 10–20%; her case of 7.99 to 9.99 at
once went badly); Hello哥 (1–2 dollars every two days up to the average of similar items, restoring the price if
conversion halves); 老魏 (「单次小幅上涨，观察之后再涨」, small rise, watch, rise again); an unsigned AMZ123 page (under 3% a step);
Regan跨境 (10–20%).

Against: Sellics' case — "Contrary to the common belief, we found that it's generally better to go out of stock than
to (drastically) raise prices", from a seller who went from 19.90 to 49.90 over four weeks; its rule is "if you have a
huge gap between restocking, the better option is to keep the price stable and let the product go out of stock.
However, if you only need to bridge your stock levels for a few days, it would not harm your rankings terribly if you
raised your prices very slightly." Helium 10's Weekly Buzz (2021-12-09): "they try to slow down their sales velocity by
doing things such as turning off PPC, raising the price, things like that. Now, this is completely not advisable…
Usually, you do not lose too much of your page ranking when going outta stock… So if you are close to running out
inventory, just keep things the way they are." 董海温 (2022-03-22): 「一旦你进行了提价或者取消促销活动等行为，listing的权重会慢慢开始下滑… 若不做任何操作的话，短暂性的断货，按照亚马逊的算法链接权重依旧是保持在最高位的」
(raise price or cancel promotions and the weight starts to slide; do nothing and a brief stock-out leaves it at its
peak). 8fig: raising "too much and leaving this raise in place for too long can negatively affect your Amazon ranking
more than simply running out of stock would." SPS Commerce, on another page of the same site: "it's not a great idea
to slow down your sales".

Evidence that it may not even slow sales: 小学逊 on 知无不言 (2019-08-16), 「连续3次提价，销量还是不减」 (three rises in a row and sales
did not fall). Evidence that slowing fails to prevent the gap: two 知无不言 posters (2023-08-28; 2026-01-13) raised
price and cut ads and still ran out.

Amazon's plugin forbids its agent the price lever (N1). Amazon's fair-pricing policy is the constraint SellerEngine
names ("be sure to adhere to fair pricing and gouging rules"); the policy itself is not this file's.

**Cut ads.** Pause all: Ken Zhou; SellerEngine; 8fig. Throttle and keep branded and high-converting terms: BellaVix
("Below 30 Days of Supply… Start reducing bids on high-volume keywords and pause non-essential campaigns"; "Below 21
Days of Supply… Pull back significantly on spend"); Inventory Hero ("Reduce spend as days of cover falls toward your
lead time"); Eva; 夕木 (「切勿直接关闭所有广告」, never switch off all ads; lower core bids 5–10%); Regan (5–10 dollars a day on core
terms). Do not: Helium 10 (above); Ad Badger ("Longstanding campaigns, anecdotally, perform better"). A reader of
跟着阿杜学跨境电商 (2022-11-30) switched ads off with a few dozen units left and 「发现自己的产品排名和销量暴跌」 (rank and sales plunged).
Dave Bryant's reasoning on the order: "it's assumed that raising prices has a more negative effect on ranking than
reducing or eliminating PPC because PPC sales are not weighted as equally as organic sales for organic rankings."
intelliRANK (2026-09-02) gives a test for a planned campaign: "if this campaign doubles my sales velocity, how many
days of stock do I have left? If the answer is fewer than your supplier lead time plus FBA processing time, the
campaign will cause a stockout before new inventory arrives." SPS Commerce: coupons and ad spend can "buy your way
into a stockout".

**Other throttles.** 大美电商 names 「关闭各种促销活动、限制购买、减少广告和预算、提高价格」 (end promotions, limit purchase quantity, cut ads,
raise price). No page read describes a maximum order quantity or pausing Subscribe & Save as a stock-stretching tactic
in any detail.

**Speed up.** Moss (2018) and 大美电商's 「冲销量关链接」 ("sprint, then close") push sales harder into the stock-out and then
go dark; 日落大道: 「断货前通过超高转化和流量来让亚马逊认为你是一个很好的产品，在断货回归后你的自然排名也会相对来说恢复的更快」 (very high conversion and traffic before the gap makes
organic rank return faster). Asserted, not measured.

### P4. During the stock-out: seller-fulfilled backup offer

For: Steven Pope ("An Amazon FBM backup offer on the same ASIN is what keeps your best sellers buyable while that late
stock clears receiving"; a second SKU on the ASIN, priced "above FBA by your extra shipping cost", with "an honest
handling time"; "drop the FBM quantity to zero instead of closing the offer" when FBA returns); SPS Commerce for a
short gap ("turning on FBM… on the condition that you are capable of fulfilling your orders in the required time");
Fast Brands; AMZ Prep; 老魏 (for three to five days, priced about 5 dollars above FBA, the orders shipped later by
Multi-Channel Fulfilment once stock lands: 「三五天的时间差客户一般感受不到」, "buyers rarely notice a 3–5 day lag"); 跨境Andy;
橙子的小婷婷; Peter (「FBM模式维持"生命体征"（每天2-3单）」, FBM to keep "vital signs", two or three orders a day). The Chinese "for"
side has a second reason that is not rank: an ASIN left at "currently unavailable" 「别人可能把链接捡过去当僵尸」 (may be picked up
by others as a zombie listing and altered).

Against: Moss (「一定不能去FBM跟卖」, "never attach an FBM offer", because non-FBA conversion is far lower); Regan
(「自发货转化率低，会拉低链接整体转化，导致大类排名下滑」, FBM converts poorly and drags down the listing); a 2017 雨果问答 answer (for three or four
days out, rank returns in a day or two and an FBM offer would lower conversion). A tried-and-failed report: a 知无不言
poster (2023-08-28) whose FBM offer drew ad clicks and no orders. A seller on the CA forums (2024-10-18): "While the
unit was never officially 'out of stock', we did not have any 'Prime' inventory for 4-5 days. I'm fairly certain that
this is what killed our listing." Steven Pope himself: "Expect a measurable conversion dip while the FBM offer carries
the listing". SPS Commerce for a long gap: "not fulfilling your FBM orders on time will hurt your account more than a
stockout."

Whether the backup stays live while FBA has stock is disputed: live always (Fast Brands: "As long as you have items in
inventory at Amazon FBA warehouse, your Amazon FBA offers will automatically 'Win the Buy Box'"; Pope: "featured-offer
share stays in the family either way") against kept at quantity zero (SKU.io's FBM Backup Mode: a live backup "can
steal the Buy Box while FBA still has stock"; it publishes the quantity "within one sync cycle (about 15 minutes) of
FBA showing empty" and notes that FBA "available" often lags reserved and inbound units). Running the offer itself is
`areas/fbm-and-outside-fba.md`'s.

### P5. During the stock-out: close the listing, or leave it

Close, to "freeze" rank: SPS Commerce ("let it run out of stock and then close that listing. This technique will allow
you to, for the most part, lock in your current page rank", for a gap "under 3 weeks" on one page and for a long gap
on another); Omar Deryan, OJ Digital ("The ranking is put on hold when you close a listing"); Helium 10's Weekly Buzz
("sometimes that can help"); Ken Zhou ("consider closing it to potentially 'freeze' your BSR", for a standalone
listing only: "Closing a variation in a parent-child family does not preserve BSR"); Hello哥 (a closed listing draws
no visits that cannot convert); 奋斗的青年 (who calls it 「很有争议」, "very disputed"); Zach的进化笔记; 大美电商. Hello哥 and
another 知无不言 poster give a mechanism worth knowing whatever one thinks of the tactic: returned units are
re-shelved, 「有1-2个库存，结果广告重新激活，一堆人进来，但是只能成交1-2单，转化率直线下滑」 (one or two units in stock, the ads reactivate, many visitors,
one or two sales, conversion collapses).

Leave it: a seller on the EU forums (2023-01-21), "You can temporarily close a listing, but all that will achieve, is
no sales and loss of rank."; another thread (2021-03-07), "i dont think it would make much difference"; a UK forums
answer (2025-05-12), "keep the listing active rather than closing it temporarily"; Moss (leave it at "currently
unavailable"). IG PPC (2023-04-04) lists a third practice it has heard of — getting the listing suppressed on purpose
by breaking a listing rule — which is recorded as said and is against Amazon's listing rules by its own description.

Nobody on either side cites an Amazon page or shows a comparison. Amazon's own stated consequence of closing is on
deals (K1).

### P6. Selling on inbound stock

Practitioners contradict each other on whether it is possible. "Amazon does not allow this" (Ken Zhou, on pre-orders
while inventory is in transit); "Amazon does not have a native backorder status for FBA listings" (AMZ Prep). Against
that: the In-Stock Head Start descriptions of 2019–2020 (Feedvisor, Seller Snap, ShippingEasy, 观海论商); a seller on the
EU forums (2022-10-05) — "I had an instance last month where I was out of stock and amazon activated the listing
before receiving my shipment but on this occasion it is just staying inactive"; Ken Zhou's own "check-in limbo,
sometimes showing as 'Available in X days'"; a 知无不言 poster (2021-08-30) whose listing sat in 「漫长的预售状态长达两周」 (a
pre-sale state for two weeks) after a week out; an unsigned AMZ123 answer describing an offer "Restock Date" field in
the listing editor; Boardfy (in the past tense) on "Temporarily out of stock" offers that held the Buy Box; and
夕木's note that with pre-order holding the Buy Box Sponsored Products keep serving at low conversion. Seller Snap:
"The In-Stock Head Start feature is developed for products that infrequently go out of stock, and not for regular
inventory replenishment cycles." The data fields in D1 show the programme's units exist in 2026; nothing read says
how a seller controls it now.

### P7. What the shopper and the seller see

A seller's transcription of the customer page (EU forums, 2022-04-05), at a time Seller Central showed the listing
Active: "Currently unavailable. - We don't know when or if this item will be back in stock." Repricer.com: "If you were
the only FBA seller: The Buy Box disappears. The listing shows 'Currently unavailable' or, if FBM sellers are present,
Amazon shows them in the Other Sellers section without a featured Buy Box."

### P8. After restock

Hard and at once: Steven Pope ("Raising bids by 25% to 50% and applying Top of Search placement"); Repricer.com
("Reactivation pricing should be 3% to 5% below market for 14 days"); 奋斗的青年 (budget three times the daily average,
bids 50% above suggested); 老魏 (cut price, paid for by the margin earned before the gap); Hello哥 (a 20–30% coupon
scheduled to start as stock lands); 夕木 (20–35%, never 50%). Gradual: Seller Labs ("Resume campaigns gradually after
the inventory is fully restored"; pitfall: "Immediately returning to pre-stockout budgets and bids"). Wait first:
Peter (「D1-D3：只观察，不干预」, days 1–3 observe only), who calls the immediate price cut with a coupon and a fourfold
budget the fatal mistake. Organic first: a reply on the EU forums. Costs reported from the discount route: alvin8868's
numbers 「恢复价格后，所有数据又是猛跌」 (collapsed when the price was restored), and a 2026-01-13 poster whose repeated deals
meant 「个别 SKU 划线价已经消失」 (some SKUs lost their strike-through price). 董海温 and 深深深情 say the same budget and bids buy
less after the gap; no English source claims ad "history" is lost in a stock-out (Seller Labs: "expect a short
learning period").

Air freight to shorten the gap: Inventory Hero ("a bridge air shipment for a strong SKU is often worth it precisely
because it shortens the rank damage"); eComEngine; 跨境Andy (express, 3–5 days, for high-price fast sellers); SoStocked's
"Express Lead Time" splits a shipment "so that some of it's coming by air"; 领星 splits the suggested quantity across
shipping methods by transit time. 深深深情 doubts the pay-off: 「补货过去之后还能够像之前一样接着销售的概率非常小」 (the chance sales resume as
before is very small). 橙子的小婷婷 sends the restock to a fulfilment centre near where orders peak, for shorter receiving.

### P9. Ads during the stock-out

Sponsored Products stop on their own, by every tool that documents it: Optmyzr ("Sponsored Products and Sponsored
Display do pause on their own. When the ASIN goes out of stock, it stops being the Featured Offer"); m19; Seller Labs;
Acadia ("Amazon will show both your campaign and ad group as running, but with your product ineligible"); 雨果网's help
page (「当产品断货的时候，广告会自动暂停。因为断货的产品没有了购物车」); 赛狐. Sponsored Brands do not: Ad Badger ("SB campaigns, unlike Sponsored
Product campaigns, will keep running, even when the product is out of stock"); Profit Whales (they "will proceed with
driving traffic to 3P offers"); Optmyzr ("as long as one featured ASIN is still in stock, the whole campaign keeps
running"; "Amazon DSP doesn't get this protection at all"); 夕木 (「即使断货，SB/SD 广告仍可能正常展示并产生点击费用」). Optmyzr and 夕木
disagree on Sponsored Display. Acadia observed a "Product Display campaign kept its eligible status for a number of
hours". Writers who say ads "keep spending" on an out-of-stock listing (Inventory Hero, sellerboard's blog) do not say
which ad type they mean. 鹏城阿兽 leaves Sponsored Products on through the gap so they restart by themselves when stock
lands at night.

### P10. Variations

newbeeseller on 知无不言 (2022-11-15), four children, the best seller (about 10 a day against 2–3) sold out on the 12th:
「从大概从13号开始…在自然搜索位，搜不到这4个变体中的任何一个了…现在是前7页完全搜不到」 (from the 13th none of the four children could be found organically for
the main keyword; before, one of them was on page 1 to 3). 日落大道: when the main child runs out, listing conversion
falls and that child's traffic entry is lost, and if no sibling can take it he closes the whole listing. 一味君: it
depends on the child's share of traffic and orders. An unsigned AMZ123 page: a child that is not the best seller
running out leaves the others' rank unaffected. Ken Zhou: "Keep one listing variation live so the parent holds its
Best Seller Rank." All assertion or single cases.

### P11. Subscribe & Save

Seller Labs: "stockouts on SnS orders cause Amazon to skip that delivery, costing you the revenue and weakening the
habit you've built". Connor Mulholland, Jarvio: "Amazon monitors your stock levels and may remove S&S eligibility if
you frequently stock out". Whether a missed delivery cancels the subscription or holds it was seen both ways in search
results only [snippet]; the model's `EligibilityStatus` texts (J3) are the first-hand statement.

### P12. How tools treat out-of-stock days in a sales velocity

| Tool | What its own help text says | Read |
|---|---|---|
| Inventory Planner (Sage) | "When stockouts are included in the calculation, the number of sales stays the same, while the number of days decreases." Example: 150 units in a month with 15 days out gives 9.38 a day against 4.84. On by default; to be switched off "if you allow overselling". It "cannot import stock history from your platform". | 2026-11-10 |
| sellerboard | "Days when the product was out of stock are excluded, so velocity reflects real demand rather than stock limitations."; weighted over 3/7/30/60/180 days. Its "Missed Profit" column "estimates profit lost to stockouts over the trailing 90 days". | 2026-11-10 |
| SoStocked | Imputes: "replace out of stock days with a daily average of what you would have sold if you were in stock". A day counts by default at "ZERO inventory AND if your sales drop below 30% of your daily average sales", switchable to OR. It reads "Amazon's Inventory Ledger Report" to find the days. A whole velocity period out of stock is disabled. Caution: with little stock sent, "the stockout tool averages… could over-inflate your velocity." | 2026-11-10 |
| RestockPro (eComEngine) | Optional "Adjusted Velocity… increased to account for out of stock periods": 2 a day in stock half the time becomes 4. | 2026-11-10 |
| Connect Books | "Avg Daily Qty leaves out days you were out of stock." | 2026-11-10 |
| Inventory Forecasting Hero | "A stockout day is a day when a product was completely unavailable for sale due to zero inventory, and no sales happened on that day."; a zero-stock day with sales is "a valid sales day". | 2026-11-10 |
| Gorilla ROI | Counts days out from its own stored snapshots: "Amazon does not provide this calculation natively." | 2026-11-10 |
| 赛狐ERP | 「排除断货天数：若当天因FBA库存为0导致日销量为0,则为断货。公式为：x天日均 = x天日销量/(x-n); n为断货天数」 (a day with zero sales because FBA stock was zero is a stock-out day; x-day average = x-day sales ÷ (x − n)). All windows drop the latest two days. Default weights 7-day 50%, 14-day 30%, 30-day 20%. | 2026-11-10 |
| 领星ERP | 「若开启了历史销量排除断货数据，天数=历史时间段天数-断货天数」 (with the switch on, days = period days − stock-out days). Also 「必断货量」: demand "that no shipping method can reach in time" can be left out of the suggested quantity. Days of cover on the 7-day average, with and without FBA inbound. | 2026-11-10 |
| 积加ERP | Projects a stock-out date and interval from on-hand, in-transit and ordered quantities with arrival dates (红绿线); the daily figure is a seller-set planning number, by season if wanted; no exclusion rule found. Its 7-day average includes Multi-Channel orders. | 2026-11-10 |
| 易仓 | Weighted 3/7/14/30-day shipments with weights chosen by trend; a coefficient that scales past days down and a multiple that scales future days up; no stock-out exclusion found. | 2026-11-10 |
| 优麦云, 船长BI, 店小秘, 马帮 | Seller-set or weighted daily sales on the pages read; no stock-out correction found. 店小秘 subtracts 「预估缺货量」, demand that cannot be served before goods arrive. | 2026-11-10 |
| Jungle Scout, Helium 10 | Help pages unreachable (HTTP 403). | — |

Three methods are in use — drop the days from the denominator, impute an average for them, or do nothing — and four
definitions of an out-of-stock day (zero stock; zero stock and zero sales; zero sales because of zero stock; zero
stock and/or sales under a share of average). Two sources of the day count: Amazon's Inventory Ledger, or the tool's
own daily snapshots, which begin only when the store is connected. Inventory Hero adds days "the listing existed but
could not be bought" (stranded or suppressed) to the count; SupplyKick adds days when ads were paused or Buy Box share
was lost as distorted days.

Lost-sales arithmetic, as practitioners state it: "Lost sales = stockout days x baseline daily velocity", the baseline
being "the two to four weeks before you ran out, excluding any earlier out-of-stock days" (Inventory Hero). An Amazon
Global Selling post (reposted by 亚马逊开店分享社 on 雨果网 from AmazonGS, 2025-09-10, cifnews 178630) puts one money figure
on days out: a steam-cleaner seller whose top listing was out five days on
Prime Day 2024, 「直接损失近50万销售额」 ("a direct loss of nearly 500,000 in sales", currency not stated).

### P13. Cover thresholds practitioners and tools use (theirs, each)

"Keep around 60 days of inventory on hand" (Jungle Scout, via the listing playbook, not re-read); alert "at 45 days
rather than at your reorder point" (Ken Zhou); 30 and 21 days of supply as ad-throttle points (BellaVix); pause an ad
"If inventory units < 50 OR if Days on hand < 15 days" (SPS Commerce's automation example); 夕木's sheet turns red at 75
days of cover and holds two weeks of sales as safety stock; Regan, at least 6 weeks; Peter, at least 30 days; 跨境Andy,
at least twice normal monthly sales; 优麦云 under 30 days replenish, 30–60 watch, 60 or more ample; 赛狐 15–30 safety days
plus 20–30% in peak; mjzj's unsigned page, red at 7 days and yellow at 14. A seller quoted by 雨果网 (2024-03-28) on what
the fee did to that rhythm: 「我一般都是一批货剩一点库存的时候下一批海运刚好衔接上，剩一点的时候可能就维持2-3周的库存。我可没办法在一批货卖的尾声的时候永远维持4周以上。」 ("I time each sea
shipment to land as the last lot runs down to two or three weeks. I cannot hold over four weeks at the tail of every
lot.")

## Published research

Read by the research helper stream on 2026-11-10 (`notes-research.md`, S1–S57); each entry there says whether the full
text or only the abstract was opened. All **[research]**.

**No study measures what practitioners argue about.** No peer-reviewed paper, working paper or Amazon-authored paper
found measures how a marketplace seller's organic search position or Best Sellers Rank behaves after restocking, or
how long recovery takes. Statements about a lasting ranking penalty rest on practitioner observation.

**Nearest evidence on Amazon.**
- Etumnu, Chenarides & Jaenicke (2025), *Agribusiness*, DOI 10.1002/agr.22051 (abstract only): Amazon grocery in five
  countries, "more than 290,000 distinct grocery products"; "when products are unavailable for a 90-day period, average
  sales rankings across all seller types are 14%–67% higher, indicating lower sales performance." A cross-product
  association, partly mechanical, with no recovery analysis and no search position.
- Raval (2023), working paper "Steering in one click", full text read: a logit model of Buy Box assignment on Keepa
  data from 2020–2021; "For the entire sample, an offer being in stock provides the same increase in utility as a 16%
  reduction in price." A same-moment effect, observational.
- Etumnu & Malone (2024), *Agribusiness*, DOI 10.1002/agr.21978 (abstract): "maintaining low current product prices,
  low sales ranks, and minimal out-of-stock percentages are crucial in becoming a BuyBox seller."
- Lee & Musolff (2021 draft), full text: "26% of consumers only consider offers recommended by the platform".
- He, Hollenbeck & Proserpio (2022), *Marketing Science*, working-paper text read: Amazon keyword position "may have a
  high degree of inertia. After an increase in sales and ratings cause a product's keyword rank to improve it does not
  decline quickly even when sales are decreasing." The products were in stock throughout; the decline came from fading
  fake-review campaigns, so this is not evidence that position survives a stock-out.
- Chevalier & Goolsbee (2003), NBER w9085: sales rank is close to a power-law function of sales (books, 2001); six
  copies bought in ten minutes moved a book from rank 14,468 to 2,854. A rank change is not a proportional sales
  change.
- Cabral & Xu (2021), *Economic Inquiry*, full text: on masks and sanitiser in early 2020, "When Amazon stocks out,
  entrants increase price by the equivalent of 178% of 2019's price, whereas the incumbents' increase corresponds to
  56.7%." What other offers on a listing do when the main offer is out.
- Cui, Zhang & Bassamboo (2019), *Management Science*: a randomised experiment on Amazon lightning deals; "a 10%
  increase in past claims leads to a 2.08% increase in cart add-ins in the next hour." About a visible claimed bar,
  deliberately kept away from actual stock-outs.

**Off-marketplace, real purchase behaviour.**
- Anderson, Fitzsimons & Simester (2006), *Management Science* 52(11), full text: a US mail-order catalogue, 22,921
  customers. "The catalog earned revenue on 86% of the items ordered that were in stock at the time of the order. The
  conversion rate dropped to 62% if the item was out of stock"; conversion on other items in the order fell from 83.1%
  to 71.2%; "If all the items ordered by a customer during the treatment period were out of stock, posttreatment demand
  was approximately 22% lower"; "the percentage loss in long-run profits is similar in magnitude to the percentage loss
  in short-run profits (19% versus 17%)". Discounts offered for the wait "were the least profitable of the five
  responses". The retailer owned the customer; a marketplace seller mostly does not.
- Jing & Lewis (2011), *Journal of Marketing Research* (abstract): at an online grocer, "stockout rates have a dramatic
  but nonlinear impact on the seller's profitability."
- Craig, DeHoratius & Raman (2016), *M&SOM*: for a supplier selling to retailers, "a one percentage point increase in
  fill rate, measured over the prior year, is associated with a statistically significant 11% increase in current
  retailer demand". Business buyers, not consumers.
- Gruen, Corsten & Bharadwaj (2002), an industry-funded report on store shelves: "The overall average OOS rate
  worldwide is estimated at 8.3 percent"; shoppers' stated responses "Buy Item at Another Store 31%", "Substitute —
  Different Brand 26%", "Substitute — Same Brand 19%", "Delay Purchase 15%", "Do not Purchase Item 9%". Grocery
  shelves in 2002; not Amazon figures. Zinn & Liu (2008) found stated intent "a rather poor indicator when the
  consumer intends to delay the search."

**Low-stock messages: the sign is mixed.** Calvo, Cui & Wagner (2023), *M&SOM* (abstract; the retailer is unnamed): a
last-five-units disclosure "increases hourly sales—they grow by 13.6%—but these products are more likely to be
returned—product return rates increase by 17.0%." Park et al. (2020), *Journal of Operations Management* (abstract):
such messages "can decrease daily sales by an average of 17.60%" on durable goods. Cachon, Gallino & Olivares (2019):
more depth of an identical item did not raise sales at car dealerships; more variety did.

**Censored demand: sales understate demand when stock runs out, and Amazon's own forecasters say so.**
- Wecker (1978), *Management Science*: the forecasting bias depends "on the frequency of stockouts, the coefficient of
  variation of demand, and the serial correlation of demand."
- Anupindi, Dada & Gupta (1998): "Sales of items that stock-out are right-censored, while sales of other items are
  inflated because of substitutions." Conlon & Mortimer (2013): "the closest substitute experiences about a three
  percent increase in its sales when the focal product stocks out"; and aggregation hides it, "approximately 17 percent
  of the data come from periods during which a stock-out occurred, versus 35 percent when the data are aggregated at
  the daily level."
- Besbes & Muharremoglu (2013): the cost of censoring "almost disappears as soon as a lost sales indicator (that
  records whether demand was censored or not) becomes available". Jain, Rudi & Wang (2015): "the information contained
  in the timing of sales occurrences is fully captured by a single number—the timing of stock-out."
- Seeger, Salinas & Flunkert (2016), NeurIPS, authors at Amazon: "When out of stock, an item cannot be sold (zt = 0),
  yet may still elicit considerable customer demand."; "If an item is not in stock at day t, the data zt = 0 is
  explained away, and the corresponding likelihood term should be dropped."; "ignoring the out of stock signal leads to
  systematic underbias".
- Salinas et al. (2020), DeepAR, authors at Amazon: not modelling out-of-stock periods "can, in the best case, lead to
  systematic forecast underbias, and, in a worst case in the larger supply chain context, can lead to a disastrous
  downward spiral where an out-of-stock situation leads to a lower demand forecast, lower re-ordering and more
  out-of-stock-situations."
- Böse et al. (2017), VLDB, authors at Amazon: "Note that this is an approximation as demand is actually partially
  unobserved: orders for an item are subject to the item's availability." This system takes orders as its demand
  target and names the approximation; it does not state that out-of-stock days are dropped.

The verifier re-opened the three Amazon papers' full texts on 2026-11-10 and found each quotation verbatim (Seeger et
al.: "If an item is not in stock at day t, the data zt = 0 is explained away, and the corresponding likelihood term
should be dropped"; "It is obvious that ignoring the out of stock signal leads to systematic underbias"). Of the three,
only Seeger et al. state that the out-of-stock day is treated as missing (its likelihood term dropped); DeepAR's
authors name the bias of not modelling it; Böse et al. name the approximation. These papers describe Amazon's retail
forecasting research. No page read says how the forecast behind a seller's
Restock recommendations or Minimum Inventory Level treats the seller's own out-of-stock days.

**Assumed, not measured, in the papers found.** That displayed stock raises demand (a modelling premise in
Balakrishnan et al. 2004); that a discount for waiting recaptures demand profitably (Bhargava et al. 2006, a model;
Anderson et al. measured the opposite).

## Stable enough for a skill

Each line points at the section that carries its source.

1. The buyable FBA quantity is `fulfillableQuantity`; reserved, inbound, researching and unfulfillable units are
   separate fields and are not buyable; `totalQuantity` is not a buyable figure. (A1–A3)
2. A SKU can be unavailable to some shoppers by region while its fulfillable quantity is above zero. (A4)
3. Units Amazon sells ahead of receipt through In-Stock Head Start are a separate quantity, visible in the
   availability notification and the Manage Inventory reports and absent from `getInventorySummaries`. (D1)
4. With AWD auto-replenishment on, Amazon treats a product as in stock once AWD has received it. (D3)
5. An FBA listing with no buyable offer is Inactive (out of stock); the same status covers blocked, suppressed,
   unopened and expired listings. An ASIN with no buyable offer from any seller is not searchable. (C1, C2, C4)
6. Amazon states that an out-of-stock offer cannot be the Featured Offer and that a sponsored ad does not display for
   a product that is out of stock or not the Featured Offer. (E1, F1)
7. The Featured Offer percentage falls for reasons other than stock. (E2)
7a. Units in FC transfer are buyable by one Amazon moderator post and not buyable by the help page's "reserved"
    sentence; the Manage Inventory reports carry an on-hand-buyable column. (A3a)
8. Amazon's in-stock rate is a 30-day share of time in stock weighted by 60 days of units sold, over replenishable FBA
   SKUs; Amazon says a low rate does not lower the IPI score. (G1, G2)
9. Amazon's estimated lost sales is its forecast for the out-of-stock days times an average price, not a count. (G4)
10. Amazon's historical days of supply divides on-hand units by shipped units and excludes inbound; its forward days
    of supply uses its forecast. The two can disagree for one SKU. (H2, I)
11. Amazon's Minimum Inventory Level is a per-product unit figure from its forecast and the seller's replenishment
    settings; Amazon's announcement attached a 15% four-week sales figure to holding it, as an average with no method.
    (H1)
12. Subscribe & Save eligibility includes an in-stock rate above 90% (trailing 28 days per an Amazon staff reply); the
    Replenishment API reports units not delivered and revenue lost to stock-outs, and an offer state in which Amazon
    blocks one-time purchases to keep stock for subscribers. (J1–J3)
13. Closing a listing cancels its scheduled deal, and a cancelled deal cannot be reactivated; a coupon is disabled on a
    product whose stock Amazon judges short, and is recreated, not resumed. (K1, K3)
14. Ordered units and shipped units are separate fields; Amazon's cover measures use shipped. Pending orders hold
    units outside the fulfillable quantity. (M1–M4)
15. A sales average over days when the SKU could not be bought understates demand; a forecasting paper by Amazon's
    researchers (Seeger et al. 2016) drops such a day's zero as unobserved, and two others name the bias. Tools differ in whether and how they correct for it. (Research; P12)
16. No Amazon page and no published study measures a lasting search or sales-rank penalty after a stock-out;
    practitioners' measured cases disagree with one another. (P1; Research)
17. Amazon publishes no grace period for a stock-out; the three-day and two-week figures in circulation come from
    practitioner pages that cite no source. (P1)
18. The 7- and 21-day bands in Amazon's agent skill are the skill's own; its "days of supply < 14 → at risk" rule is on
    no Amazon help or developer page read, where 14 appears only as an FBM Restock eligibility criterion and a fee band
    edge. (N4, G7)

## What cx must read at run time

**R1. Buyable and non-buyable units per SKU: `getInventorySummaries` with details.** Role: Amazon Fulfillment or
Product Listing. Fields: `fulfillableQuantity`; `reservedQuantity` and its three parts; the three inbound quantities;
`researchingQuantity`; `unfulfillableQuantity`; `totalQuantity`. Rate and paging facts are the door's and the listing
playbook's (50 SKUs a call; default 2 requests a second; a `startDateTime` filter misses inbound-only changes — not
re-read). Pitfalls: no future-supply field (D1); no per-region availability (A4); one row per seller SKU, so an ASIN
with two FBA SKUs has two rows.

**R2. The same quantities with In-Stock Head Start units: `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` or
`GET_FBA_MYI_ALL_INVENTORY_DATA`.** Role: Amazon Fulfillment or Pricing. Columns: `afn-fulfillable-quantity`,
`afn-reserved-quantity`, `afn-inbound-working-quantity`, `afn-inbound-shipped-quantity`,
`afn-inbound-receiving-quantity`, `afn-reserved-future-supply`, `afn-future-supply-buyable`, `afn-fc-transfer-quantity`,
`afn-onhand-buyable-quantity` (the last two undefined on the page; A3a). Pitfall: third parties' account of the 2019
pilot says head-start units show in both Available and Inbound (D2), so summing columns can count a unit twice; this
needs a check on a real account. The notification schema's example carries `FutureSupplyBuyable` 10 against 15 units
shipped or receiving, which is consistent with head-start units being a subset of inbound, but an example is not a
rule.

**R3. Amazon's own view of risk per SKU: `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`.** Role: Amazon Fulfillment or
Pricing. Columns: Available; FC transfer; FC Processing; Customer Order; Working, Shipped, Receiving; Units Sold Last
30 Days; Days of Supply at Amazon Fulfillment Network; Total Days of Supply (including units from open shipments);
Alert; Recommended replenishment qty; Recommended ship date. Freshness: "near real-time"; request only. Scope: all
stores except India. Pitfalls: the Alert column's values are undocumented on any page read (G7), and no skill sentence
can name them until they are seen in real output; a SKU the seller has hidden as not replenishable shows no recommendation
(G3). The tool's logic is `areas/restock-and-forecast.md`'s.

**R4. Amazon's cover measures per SKU: `GET_FBA_INVENTORY_PLANNING_DATA`.** Role: Amazon Fulfillment only. Columns:
`units-shipped-t7/t30/t60/t90`, `days-of-supply`, `historical-days-of-supply` (and the short- and long-term columns),
`weeks-of-cover-t30`, `weeks-of-cover-t90`, `sell-through`, `fba-minimum-inventory-level`,
`fba-inventory-level-health-status`, `alert`, `Recommended ship-in quantity`, `Recommended ship-in date`, `Exempted
from Low-Inventory-Level fee?`, `Low-Inventory-Level fee applied in current week?`, `Last updated date for Historical
Days of Supply`, `is-seasonal-in-next-3-months` and the season columns, `sales-rank`. Scope: not available in the NL,
PL, SE or BE stores; "Attributes vary by store", Brazil returns a reduced set. Pitfall: the
developer page defines none of these columns; the definitions in section I are from help pages not read first-hand.

**R5. Days out of stock, after the fact: `GET_LEDGER_SUMMARY_VIEW_DATA` aggregated by day.** Role: Amazon Fulfillment
only. Column: `Ending Warehouse Balance` per day, FNSKU and disposition; a day whose sellable ending balance is zero
is a day that ended with nothing on the shelf (SoStocked's help text describes this same filter). Pitfalls: the report
"can return empty data if invalid `dataStartTime`/`dataEndTime` is passed along with `aggregatedByTimePeriod` filter
values"; an end-of-day balance does not say when in the day stock ran out, nor whether units on hand were reserved or
in transfer and so not buyable; whether the balance is per country or per fulfilment centre depends on the
aggregation chosen. No report gives a ready count of out-of-stock days.

**R6. Whether the offer is buyable and featured now: `getListingsItem` (status and live `fulfillmentAvailability`) and
`getItemOffers` / `getListingOffers`.** Roles: Product Listing for the first; Pricing or Product Listing for the
second. Fields: listing status including `BUYABLE`; `OfferDetail.IsBuyBoxWinner`, `IsFeaturedMerchant`,
`IsFulfilledByAmazon`, `MyOffer`; `DetailedShippingTimeType.availabilityType` (`NOW`, `FUTURE_WITH_DATE`,
`FUTURE_WITHOUT_DATE`) and `availableDate`. Pitfalls: a non-buyable status has causes other than stock (C2); an ASIN
with both an FBA and an FBM SKU of the same seller has two offers; "up to two Buy Box winners at any time per ASIN".

**R7. Units sold per day: one of three sources that do not count the same thing.**
- `getOrderMetrics` — any of Pricing, Product Listing, Finance and Accounting, Amazon Fulfillment. `unitCount` is
  ordered units; filter by `sku` or `asin`, `fulfillmentNetwork`, `buyerType`. Default rate 0.5 a second, burst 15.
- Sales and Traffic (`GET_SALES_AND_TRAFFIC_REPORT`, or Data Kiosk `analytics_salesAndTraffic_2024_04_24`) — Brand
  Analytics. `unitsOrdered`, `unitsShipped`, the B2B twins, `sessions`, `buyBoxPercentage`. By date for the account or
  by ASIN; the by-ASIN view is at ASIN grain, not seller-SKU grain.
- `GET_FBA_INVENTORY_PLANNING_DATA` (`units-shipped-t7/t30/t60/t90`) or the Restock report ("Units Sold Last 30
  Days") — roles as R3 and R4. Windowed totals, FBA only.
Pitfalls: ordered units include orders later cancelled and pending orders; an ASIN-level figure includes the seller's
FBM offer and every FBA SKU on that ASIN; a B2B bulk order is one day's spike; the window may contain days the SKU
could not be bought (R5, R8).

**R8. A second sign of days the offer could not be bought: sessions with a low Featured Offer percentage.** Sales and
Traffic by ASIN and day, `sessions` and `buyBoxPercentage`. Role: Brand Analytics. Pitfall: the percentage falls for
reasons other than stock (E2), and it is at ASIN grain.

**R9. Subscribe & Save exposure: Replenishment API `getSellingPartnerMetrics`, `listOfferMetrics`, `listOffers`.**
Role: Brand Analytics. Metrics `NOT_DELIVERED_DUE_TO_OOS`, `LOST_REVENUE_DUE_TO_OOS` (performance periods only);
offer fields `eligibility`, `deliveriesConditions`, `inventory`, `stockRisk`, `forecastDeliveries`. Default rate 1 a
second for each. Pitfall: `stockRisk` is a free string whose values are not enumerated in the model.

**R10. Events instead of polling.** `FBA_INVENTORY_AVAILABILITY_CHANGES` (Amazon Fulfillment): "sent whenever there is
a change in the Fulfillment By Amazon (FBA) inventory quantities… includes a snapshot of the FBA inventory in all
eligible Amazon stores in a particular region"; carries `Fulfillable`, the inbound and reserved breakdowns,
`FutureSupplyBuyable` and `PendingCustomerOrderInTransit`. `LISTINGS_ITEM_STATUS_CHANGE` (Product Listing).
`ANY_OFFER_CHANGED` (Pricing). `ITEM_INVENTORY_EVENT_CHANGE` (Brand Analytics), with `highlyAvailableInventory`.
Subscriptions and destinations are the door's.

**R11. Listings that are inactive: `GET_MERCHANT_LISTINGS_INACTIVE_DATA` and `GET_MERCHANT_LISTINGS_ALL_DATA`.** Roles:
Pricing or Product Listing. Pitfall: zero quantity is one of five reasons in the inactive report (C1).

**R12. Rates and thresholds that are Amazon's and change.** The low-inventory-level fee's bands, amounts and
exemptions: `areas/holding-costs.md`, read from the fee page and the fee reports at run time. The Subscribe & Save
in-stock criterion (90%, trailing 28 days as of the pages read 2026-11-10): sell.amazon.com/programs/subscribe-and-save
and the Seller Central Subscribe & Save page. The Minimum Inventory Level per SKU: `fba-minimum-inventory-level` in R4.

**What a pack adds beyond the door's `/low-stock` template.** The template asks which FBA listings "will run out of
stock within ${1:-14} days at the rate they sold over the last 30 days" and to show "the units available and inbound,
the units sold a day, and the day it runs out". The facts in this file that the template does not carry: which
quantity is buyable and which are not (A); that inbound has three states and none is a date (the dates are
`areas/inbound.md`'s); that the 30-day rate is biased down by days out of stock and by days without the Featured
Offer, and biased up by a deal or a bulk order (R5, R7, R8; Research); that ordered and shipped differ and Amazon's own
cover figures use shipped (M3); that Amazon publishes its own days of supply, alert and Minimum Inventory Level for
the same SKU, built on its forecast, not on the trailing rate (R3, R4); the ASIN-versus-SKU grain (R7); and what
Amazon says a stock-out costs (E, F, J, K). The 14 in the template is a default of the door's prompt, not a figure
from an Amazon page.

## Reads that need a role outside the five

Nothing this file builds on needs a role outside the five. For completeness:

- **Amazon Warehousing and Distribution role** — the AWD inventory operations. They would show the AWD units that,
  with auto-replenishment on, Amazon counts as in stock (D3). No position here depends on reading them;
  `beyond/programs-and-regions.md` owns AWD.
- **Inventory and Order Tracking** — named beside the listings, orders and replenishment reads, each of which is also
  open to one of the five roles. It opens nothing further for this file.
- **Selling Partner Insights** — named beside `GET_PROMOTION_PERFORMANCE_REPORT` and the order reads, each also open
  to one of the five.
- **Not SP-API at all:** ad eligibility and serving status per advertised product are in the Amazon Ads API (the ads
  playbook's door). Amazon's analytics endpoint `sellingpartner-ai.amazon.com`, which serves the metric ids in N2
  (days of supply at mean and P90, P80 forecasts, restock order date), is not an SP-API host; this research did not
  call it and builds nothing on it.

## Only in Seller Central

As far as I could establish, by searching the cloned models and schemas for "lost sales", "in-stock rate", "instock"
and "head start", and by reading the report and notification type pages:

- **The IPI dashboard's FBA in-stock rate and estimated lost sales.** No model, report schema or dataset carries
  either; the only hits for lost revenue are the Replenishment API's Subscribe & Save metrics. A per-SKU in-stock share
  can be rebuilt from the daily ledger (R5), with Amazon's weighting applied by hand; Amazon's forecast-based lost-sales
  figure cannot.
- **The "Restock today" count and the Minimum Inventory Level's "Potential Sales Lift" estimate** (named in the Prime
  Day playbook, H4). The Planning report carries the level and a health status, not the lift.
- **Hiding a SKU as not replenishable** on the Restock Inventory page (G3), and the **Replenishment Alerts** settings
  (G7).
- **In-Stock Head Start enrolment or pause.** The units are visible as data (D1); no operation that switches the
  programme was found.
- **The Subscribe & Save page's inventory view** that sell.amazon.com mentions (J1); the API carries the metrics (R9),
  not the page.
- **The customer-facing availability message** for the seller's own offer. The pricing API gives `availabilityType`
  and a date (B2), not the words shown.
- **A history of the Featured Offer per SKU.** `buyBoxPercentage` is by ASIN and day.

`method/seller-central-only.md` owns the general list.

## The seller's choices

Each is the seller's. What each changes is stated; none is picked.

1. **Which quantity counts as cover.** Fulfillable only gives the earliest run-out date and flags SKUs whose stock is
   in transfer or processing and will be buyable without any action. Adding FC transfer follows the moderator post
   that calls those units buyable (A3a) and Amazon's own Minimum Inventory Level, which counts transfer and reserved
   units as on hand (H1); adding FC processing assumes those units return before the shelf empties. Adding inbound assumes an arrival date. Adding AWD or 3PL
   stock assumes it can reach FBA in time (Inventory Hero counts only "units that are actually deliverable to FBA
   within your lead time window").
2. **Which sales figure is the rate.** Ordered units react first and include cancellations and pending orders; shipped
   units match Amazon's own cover measures and lag. ASIN grain mixes the seller's SKUs and channels; SKU grain does
   not.
3. **Which window, and how weighted.** A short window follows a trend and a deal alike; a long one smooths both and
   carries old stock-outs. Tools ship 7/14/30 blends (赛狐 50/30/20), 3/7/30/60/180 (sellerboard), seven periods from 2
   to 180 days (SoStocked), a trend-dependent weighting (易仓), or the seller's own figure by season (积加). Amazon's
   plugin divides 30 days by 30.
4. **What to do with days the SKU could not be bought.** Leave them in (the rate understates demand and, by the DeepAR
   authors' account, can spiral); drop them from the denominator; or impute an average. Dropping or imputing on little
   in-stock history can overstate demand (SoStocked's own caution). The definition of such a day is itself a choice
   (P12).
5. **Whether to count days without the Featured Offer, with ads paused, or under a deal as normal days.** Each moves
   the rate; SupplyKick treats the first two as distorted.
6. **How much cover to hold.** More cover costs storage and capital and risks excess (Amazon's 90 days); less risks
   the run-out and the low-inventory-level fee (Amazon's 28 days). Amazon's guideline, tools' defaults and
   practitioners' figures differ (G5, H4, P13). `areas/holding-costs.md` and `areas/restock-and-forecast.md` carry the
   other side of the trade.
7. **Before a run-out that cannot be avoided: slow sales, leave them, or speed them.** Raising price lengthens the days
   in stock and, by the Sellics case, Helium 10 and 董海温, may cost rank before the stock is gone; it also meets
   Amazon's fair-pricing policy and can lose the Featured Offer. Cutting ads lowers sales that practitioners believe
   weigh less in rank, and campaigns restart slowly by some accounts. Leaving everything keeps rank and conversion to
   the last unit and makes the gap longer. Speeding up is Moss's and 大美电商's practice, unmeasured.
8. **During the gap: a seller-fulfilled offer, or none.** An offer keeps the ASIN buyable, searchable and eligible for
   Sponsored Products; it converts worse without Prime delivery, needs the seller able to ship on time, and by some
   accounts lowers the listing's conversion. `areas/fbm-and-outside-fba.md` owns the mechanics.
9. **During the gap: close the listing, or leave it inactive.** Closing stops stray returned units from reopening the
   offer and its ads on one or two units; it cancels any scheduled deal for good (Amazon's rule); the claim that it
   preserves rank has no evidence on either side.
10. **Whether to rely on Amazon selling ahead of receipt.** In-Stock Head Start and AWD auto-replenishment can keep an
    offer buyable with nothing on the FBA shelf; sellers report it happening unpredictably.
11. **Air or express for part of the next shipment.** It shortens the gap at a freight cost; whether the shorter gap
    repays it depends on a rank effect nobody has measured.
12. **After restock: discount and ad push, gradual return, or wait and watch.** Deep discounts are reported to recover
    sales and to cost the reference price and a second fall when the price returns.
13. **For a variation family, when one child runs out:** leave the family open, move ads to a sibling, or close the
    family. Practitioners' reports conflict (P10).
14. **Whether a SKU belongs in the in-stock picture at all.** A SKU being discontinued or sold through on purpose is
    not a stock-out to prevent; Amazon lets the seller hide it from restock recommendations and the in-stock rate.

## Open questions

For a first run on a real account:

1. What values does the Restock report's `Alert` column take, and what does the Planning report's `alert` column
   take? Neither is documented on a page I could read.
2. Do In-Stock Head Start units appear in both `afn-fulfillable-quantity` and the inbound columns, as the 2019
   coverage says, or only in `afn-future-supply-buyable`? Does `getInventorySummaries.fulfillableQuantity` include
   them?
3. What does `getListingsItem` return for an FBA SKU with zero fulfillable and inbound stock: status, issues, and
   `fulfillmentAvailability`? What does `getItemOffers` return for an offer selling ahead of receipt
   (`availabilityType`, `availableDate`)?
4. What strings does the Replenishment API's `stockRisk` return?
5. At what grain does the daily ledger summary report zero: does a SKU with all units in FC transfer show a zero
   sellable ending balance?
6. How far apart are `unitsOrdered` and `unitsShipped` over 30 days on a real account, and "Units Sold Last 30 Days"
   in the Restock report against both?
7. Does `fba-inventory-level-health-status` use the four states of Amazon's Chinese post (out of stock, low, healthy,
   excess)?

For the office:

8. Help pages I could not read first-hand, with ids: Inventory performance (G202174810); IPI FAQ (GZJF4DY2W6MERBAL);
   Restock Inventory (G5QJ5MF6MGBBYDSU); Replenishment Alerts (G200285580); Low-inventory-level fee
   (GV43F6S76Y9DHYRH); Inventory Buyability (GFC63UNUF6LMLK2R); My ASIN is unsearchable (GHGHDMU4X5K9QGCV); FBA
   inventory overview (GTMXYZN64UJL7TT6); the FBA Subscribe & Save help page and the In-Stock Head Start help page
   (ids not found); Amazon Ads help GQFZA83P55P747BZ (ad eligibility); Amazon customer help GM6AEUPCYCFUTYX7 on
   amazon.com (read on the mirror instead). Read through office captures of 2026-10-14, not at Amazon: G201687550,
   G27691, G201951410, G202111490, G202183600, GM2ADTH3XH3A5N57.
9. Is In-Stock Head Start still offered, where, and how is it switched? Amazon announced the US pilot on 2019-07-25; a
   UK seller reported it working for some products on 2024-11-20; no 2025–2026 Amazon text was found; the data fields
   remain in the models.
10. Does Amazon define the availability messages for third-party FBA offers anywhere? The customer page covers only
    items "shipped and sold by Amazon".
11. The exact stock requirements for deals at submission and at run time, and what happens to a running deal when
    stock reaches zero, were not read first-hand. For coupons, Amazon's staff post (K3) says the coupon is disabled on a
    product without "enough inventory", with no quantity.
12. The 14-day "at risk" rule in Amazon's plugin: is it on any Amazon help page? The snippet in G7 matches the FBM
    Restock feature's eligibility criterion (2025-03-14), not an FBA rule.
13. The 2027 low-inventory-level method is recorded from `areas/holding-costs.md` (H2); the 2027 fee page
    (GFU8NTVGHP2JQLCR) was not read by either seat.
14. Gaps left by the helper streams, which stopped on a usage limit: 知无不言 replies (login-gated); help text for
    Helium 10, Jungle Scout and Pacvue (HTTP 403); 马帮's help centre (script shell); full texts of Etumnu et al. 2025,
    Jing & Lewis 2011, Calvo et al. 2023 and Wecker 1978 (abstracts only; the verifier found no open copy either); no Chinese practitioner page on Amazon's estimated lost
    sales or the Restock alert was found; reddit.com was read only through a mirror.

## Positions

Scope: the positions on FBA quantities, listing status, the Featured Offer, ads and the SP-API models are not tied to
one store unless a scope is stated. Help-page quotations are from the US Seller Central pages.

**What "out of stock" is**

**P-running-out-1.** Amazon defines an FBA SKU's `fulfillableQuantity` as "The item quantity that can be picked,
packed, and shipped"; it is the buyable quantity. [official] FBA Inventory API model (`fbaInventory.json`);
*FBAInventoryAvailabilityChangeNotification* schema. (A1)

**P-running-out-2.** Reserved, inbound, researching and unfulfillable units are separate fields beside the fulfillable
quantity, and Amazon's help says customers cannot buy units that are "stranded, reserved, being researched, or
unfulfillable". [official] FBA Inventory API model; [official, listing playbook 2026-10-14, not re-read] *Inventory
Buyability* (GFC63UNUF6LMLK2R). (A2)

**P-running-out-3.** An FBA SKU can show zero fulfillable units while units sit in fulfilment-centre transfer, in
fulfilment-centre processing, held for pending customer orders, or inbound; each of those is its own field in
`getInventorySummaries` and its own column in the Restock report. [official] FBA Inventory API model; *Fulfillment by
Amazon (FBA) Reports*. (A3)

**P-running-out-4.** Amazon states that a product "may be temporarily unavailable for shipping to certain parts of the
country" while the seller has stock; no SP-API field read reports availability by shopper location. [official, listing
playbook 2026-10-14, not re-read] *Inventory Buyability* (GFC63UNUF6LMLK2R). (A4)

**P-running-out-5.** Amazon's customer-help definitions of "In Stock", "Temporarily Out of Stock" and "Currently
unavailable" are stated to "only apply to products shipped and sold by Amazon"; no Amazon page read defines the
messages for a third-party FBA offer. [official] *Availability Estimate Definitions* (GM6AEUPCYCFUTYX7, read on
Amazon's mirror). (B1)

**P-running-out-6.** The Product Pricing API reports an offer's shipping availability as `availabilityType` (`NOW`,
`FUTURE_WITH_DATE`, `FUTURE_WITHOUT_DATE`) with an `availableDate` shown only for offers not currently available for
shipping. [official] Product Pricing v0 model (`productPricingV0.json`). (B2)

**P-running-out-7.** Amazon lists "out of stock" as a reason a listing is Inactive, and the Inactive Listings report
mixes zero-quantity listings with blocked, suppressed, unopened and expired ones, so Inactive alone does not mean out
of stock. [official] *Understanding Amazon listing status and seller-fulfilled inventory management*. (C1, C2)

**P-running-out-8.** Amazon says an out-of-stock listing is reactivated "by updating its inventory levels", and that
an open offer needs "a purchasable offer with pricing and a positive fulfillment availability quantity". [official]
*Understanding Amazon listing status and seller-fulfilled inventory management*. (C3)

**P-running-out-9.** Amazon states that "ASINs without a buyable offer are unsearchable" and that a change "can take
up to 72 hours to reflect in shopping results"; the condition is on the ASIN, so another seller's buyable offer keeps
it searchable. [official, listing playbook 2026-10-14, not re-read] *My ASIN is unsearchable* (GHGHDMU4X5K9QGCV). (C4)

**P-running-out-10.** Units Amazon offers for sale ahead of receipt through In-Stock Head Start are reported as
`FutureSupplyBuyable` and `PendingCustomerOrderInTransit` in the FBA inventory availability notification and as
`afn-future-supply-buyable` and `afn-reserved-future-supply` in the Manage Inventory reports; the
`getInventorySummaries` model has no such field. [official] *FBAInventoryAvailabilityChangeNotification* schema;
*Fulfillment by Amazon (FBA) Reports*; FBA Inventory API model. (D1)

**P-running-out-11.** Amazon announced In-Stock Head Start on 2019-07-25 as a US pilot that makes "temporarily
out-of-stock products available for customers to find and buy when your shipment is on its way and we are confident
about its arrival date"; its terms (seller-level enrolment; shipments by Carrier Central, the Partnered Carrier
programme or Amazon Global Logistics) are known through third parties, and no Amazon text of 2025–2026 on it was found.
[official] News_Amazon, 2019-07-25; [official, via ChannelX 2019-08; via Feedvisor 2019-12-04; via 观海论商 2019-07-29];
[opinion] UK seller post 2024-11-20. (D2)

**P-running-out-12.** An Amazon forum moderator stated on 2024-07-16 that with AWD auto-replenishment enabled
"products are considered in stock and buyable when they're received by AWD". [official, forum moderator]
Topher_Amazon, Seller Forums EU. (D3)

**What Amazon says a stock-out costs**

**P-running-out-13.** Amazon states "Your offer can't become featured if you're out of stock". [official, office
capture 2026-10-14] *Becoming the Featured Offer* (G201687550, v20). (E1)

**P-running-out-14.** The Featured Offer percentage in Business Reports falls below 100% when the product was out of
stock and also for other reasons, and Amazon says it "is not necessarily an indication of the availability of your
product for purchase"; the figure is by ASIN, not by seller SKU. [official, office capture 2026-10-14] *Business
reports glossary* (G27691, v7); [official] Data Kiosk Sales and Traffic schema. (E2)

**P-running-out-15.** Amazon Ads states "If your product isn't the Featured Offer or is out of stock, your ad will not
display." [official] *Amazon Ads FAQ*; *New advertiser success guide*. (F1)

**P-running-out-16.** The two Amazon Ads pages read do not say whether Sponsored Brands and Sponsored Display stop in
the same way; tools and practitioners say Sponsored Products stop on their own and Sponsored Brands keep serving, and
they disagree on Sponsored Display. [official] *Amazon Ads FAQ*; [opinion] Optmyzr, Ad Badger, Profit Whales,
夕木运营笔记本. (F2, P9)

**P-running-out-17.** Amazon defines the FBA in-stock rate as the percentage of time replenishable FBA products were
in stock in the last 30 days, weighted by units sold in the last 60 days. [official] Seller Forums post by SEAmod
relaying the Amazon Business team; [official, listing playbook 2026-10-14, not re-read] *Inventory performance*
(G202174810, v9). (G1)

**P-running-out-18.** Amazon states that a low in-stock rate "does not hurt" the IPI score "unless your most popular
products consistently go out of stock"; an older Amazon post says the same, and no Amazon page read gives a date on
which the rate left the score. [official] SEAmod post; [official, listing playbook 2026-10-14, not re-read] IPI FAQ
(GZJF4DY2W6MERBAL, v19). (G2)

**P-running-out-19.** By Amazon's older post, hiding a SKU on the Restock Inventory page marks it not replenishable,
removes it from the in-stock rate and stops its restock recommendations. [official] SEAmod post (historical wording).
(G3)

**P-running-out-20.** Amazon's "estimated FBA lost sales in the last 30 days" is its forecast unit sales for the days
out of stock multiplied by the average sales price; an earlier Amazon report defined estimated lost sales in units as
the 60-day run rate times days out. Neither counts lost orders. [official, listing playbook 2026-10-14, not re-read]
*Inventory performance* (G202174810, v9); [official, via a seller's forum post, 2018-04-11] Inventory In Stock report
help text. (G4)

**P-running-out-21.** Amazon's inventory-performance page says "Restock today" counts SKUs whose days of supply is
less than the restock lead time, gives "30 to 60 days of your expected sales" as a guideline, and calls stock over 90
days of forecast supply excess; these are Amazon's figures as read on 2026-10-14. [official, listing playbook
2026-10-14, not re-read] *Inventory performance* (G202174810, v9); [official] sell.amazon.com *Inventory management*.
(G5)

**P-running-out-22.** The Restock Inventory report carries Amazon's per-SKU days of supply (at Amazon, and including
open shipments), an Alert, a recommended quantity and a recommended ship date; it is available in all stores except
India, and the developer page lists no values for Alert. [official] *Fulfillment by Amazon (FBA) Reports*. (G7, G8)

**P-running-out-23.** The FBA Manage Inventory Health report carries `days-of-supply`, `historical-days-of-supply`,
`weeks-of-cover-t30`, `weeks-of-cover-t90`, `sell-through`, `fba-minimum-inventory-level` and
`fba-inventory-level-health-status`; the developer page defines none of them, and the report is not available in the
NL, PL, SE or BE stores. [official] *Fulfillment by Amazon (FBA) Reports*. (I, G8)

**P-running-out-24.** Amazon describes the Minimum Inventory Level as "the minimum number of units per product that
you should have on hand in our fulfillment centers", derived from its demand forecasts and the seller's replenishment
settings, and stated in its announcement of 2023-12-19 that sellers above it "see a 15% increase in sales over a
four-week period on average, though actual results may vary"; the Chinese version footnotes the figure to Amazon
Accelerate 2023. The level counts on-hand sellable, FC-transfer and reserved units and not inbound. [official]
News_Amazon, "Plan FBA inventory levels using a new metric"; [official, via 亚马逊开店分享社 on 雨果网 reposting
AmazonGS, 2023-12-11]. (H1)

**P-running-out-25.** Amazon's historical days of supply is average daily units on hand divided by average daily
shipped units, excludes inbound units, and is what the low-inventory-level fee reads through 2026 (below 28 days on both the 30-day and 90-day measure, per
FNSKU from 2026-01-15); Amazon's 2027 method divides weekly recorded inventory by shipments in the 28 days before and
the 28 days after the assessment, both below 28 days, so a fee is known only four weeks after it. Amounts, dates and
exemptions are read at run time and belong to `areas/holding-costs.md`. [official] News_Amazon announcement 2023-12-19;
[official, via the 雨果网 account "亚马逊"] 2026-01-27; [official, listing playbook 2026-10-14, not re-read] fee page
(GV43F6S76Y9DHYRH, v29); [official, as read by the holding-costs seat] 2027 letter and China notice. (H2)

**P-running-out-26.** Amazon's historical days of supply looks back at shipped units and its forward days of supply
rests on its forecast, so one SKU can read short on one and long on the other. [official] sources as positions 25 and
21. (I)

**P-running-out-27.** Amazon's Prime Day readiness playbook gives, for an event, "at least 28 days of inventory" for
products without recommendations and "4-6 weeks of inventory available before your deal event"; these are Amazon's
event guidance as captured on 2026-10-14. [official, office capture 2026-10-14] *Prime Day readiness playbook*
(GM2ADTH3XH3A5N57, v4). (H4)

**P-running-out-28.** Amazon lists an in-stock rate greater than 90% among Subscribe & Save eligibility criteria, and
an Amazon staff reply gives the window as the trailing 28 days. [official] sell.amazon.com *What is Amazon Subscribe &
Save?* (2025-08-25); Manny_Amazon, Seller Forums. (J1)

**P-running-out-29.** The Replenishment API reports, for Subscribe & Save, the share of units not delivered because of
out of stock (`NOT_DELIVERED_DUE_TO_OOS`) and "The revenue that would have been generated had there not been out of
stock" (`LOST_REVENUE_DUE_TO_OOS`), for past periods only; it is the only SP-API surface found that puts a figure on
revenue lost to a stock-out. [official] Replenishment API model 2022-11-07. (J2)

**P-running-out-30.** A Subscribe & Save offer can be in the state `REPLENISHMENT_ONLY_ORDERING`, in which Amazon
"blocks one-time purchases to preserve inventory for existing subscriptions", and can carry delivery conditions that
say deliveries are paused because the offer is not buyable or are at low-inventory risk. [official] Replenishment API
model 2022-11-07. (J3)

**P-running-out-31.** The report types `GET_FBA_SNS_FORECAST_DATA` and `GET_FBA_SNS_PERFORMANCE_DATA` were removed on
2025-12-11; the Replenishment API carries those figures. [official] *SP-API deprecations*; *Replenishment API* guide.
(J4)

**P-running-out-32.** Amazon states that setting an ASIN in a deal to Closed "will cancel any deal currently scheduled
for that ASIN" and that "Canceled deals cannot be reactivated." [official, office capture 2026-10-14] *Amazon deals*
(G202111490, v25). (K1)

**P-running-out-33.** Amazon states that a child listing that "is inactive or has no inventory" typically does not
show on the detail page; no Amazon page read says what a child's stock-out does to its siblings' search placement.
[official, office capture 2026-10-14] *Variation relationship FAQ* (G201951410, v16). (L1, L2)

**The data a run-out date rests on**

**P-running-out-34.** Sales and Traffic data carries `unitsOrdered` and `unitsShipped` as separate fields, by date and
by ASIN; `getOrderMetrics.unitCount` counts units in orders. [official] Data Kiosk schema
`analytics_salesAndTraffic_2024_04_24`; Sales API model. (M1, M2)

**P-running-out-35.** Amazon's own cover measures are built on shipped units (historical days of supply; the Planning
report's `units-shipped-t7/t30/t60/t90`), so a rate built on ordered units need not agree with them. [official]
*Fulfillment by Amazon (FBA) Reports*; sources as position 25. (M3)

**P-running-out-36.** Units held for orders placed but not yet authorised are counted in
`pendingCustomerOrderQuantity`, outside the fulfillable quantity. [official] FBA Inventory API model; Orders v0 model.
(M4)

**P-running-out-37.** No report read gives a count of days out of stock; the Inventory Ledger summary report gives an
`Ending Warehouse Balance` per day from which zero-balance days can be counted, and an end-of-day balance says neither
when in the day stock ran out nor whether units on hand were buyable. [official] *Fulfillment by Amazon (FBA)
Reports*; [opinion] SoStocked help, Gorilla ROI. (R5, P12)

**P-running-out-38.** The IPI dashboard's in-stock rate and estimated lost sales appear in no SP-API model, report
schema or Data Kiosk schema in the models at commit `db2936aa`. [official] local models, searched 2026-11-10. (Only in
Seller Central)

**P-running-out-39.** Every operation, report, notification and dataset named in this file is open to at least one of
Product Listing, Pricing, Brand Analytics, Finance and Accounting or Amazon Fulfillment; the Planning and Ledger
reports are open to Amazon Fulfillment only, and Sales and Traffic and the Replenishment API to Brand Analytics.
[official] *Role Mappings for SP-API Operations* (2026-10-28); *Role Mappings for SP-API Types* (2026-09-09). (O)

**P-running-out-40.** A sales average taken over days when a SKU could not be bought understates demand; a forecasting
paper by Amazon's researchers states that on an out-of-stock day "the data zt = 0 is explained away, and the
corresponding likelihood term should be dropped" and that "ignoring the out of stock signal leads to systematic
underbias"; DeepAR's authors warn of a "downward spiral". These describe Amazon's retail forecasting research, not the
forecast behind a seller's Restock figures. [research] Seeger, Salinas & Flunkert 2016 (full text); Salinas et al.
2020 (full text); Böse et al. 2017 (full text); Wecker 1978 (abstract). (Published research)

**P-running-out-41.** Tools differ on out-of-stock days: Inventory Planner, sellerboard, Connect Books, 赛狐 and 领星
remove them from the divisor, SoStocked imputes an average for them, RestockPro scales velocity by the in-stock share
as an option, and the pages read for 积加, 易仓, 优麦云, 船长BI, 店小秘 and 马帮 show no correction; they also define an
out-of-stock day in four different ways. [opinion] each tool's help text, read 2026-11-10. (P12)

**What a stock-out does afterwards**

**P-running-out-42.** No Amazon page read states a ranking consequence of a stock-out beyond losing the Featured
Offer, ad display and searchability while no offer is buyable, and none states a grace period. [official] pages in
sections C, E, F. (C4, E1, F1, P1)

**P-running-out-43.** No published study found measures a marketplace seller's search position or Best Sellers Rank
after restocking; the nearest Amazon evidence is an association of 90-day unavailability with 14%–67% worse sales
rank in grocery and a Buy Box model in which being in stock is worth a 16% price cut. [research] Etumnu, Chenarides &
Jaenicke 2025 (abstract only); Raval 2023. (Published research)

**P-running-out-44.** Practitioners who published measurements disagree: EcomCrew (five ASINs, outages of days to
months, Best Sellers Rank read off charts) found sales rank "almost always" back within four weeks and "no significant
penalty", while one item "never recovered its historical sales rank"; a Sellics case (one product, top three keywords,
with a Sponsored Products push at restock) found keyword rankings back a week after restock; DataWeave reports rank falls of 28% after one day and 83% after three for one customer's top-ten
products; Profitero reports 9–10 days to recover search placement for UK vendor brands. [opinion] Dave Bryant,
EcomCrew; Franz Jordan, Sellics; DataWeave; Profitero. (P1)

**P-running-out-45.** Most practitioner pages state that rank falls within three to seven days out of stock and takes
two to six weeks to recover, without showing data; the figures differ from page to page. [opinion] My Amazon Guy,
SellerSprite, Repricer.com, Onramp Funds, Seller Labs, 跨境大师兄Peter. (P1, P2)

**P-running-out-46.** The "three-day grace period" in Chinese practitioner writing cites no Amazon page; the earliest
copy found is 藏龙荟's (2019-06-11), and a 2021 post prints the same sentence with "two weeks", spliced onto Moss的精神家园's
2018 text, which describes his own routine for a gap under two weeks, not a grace period. [opinion] 藏龙荟 2019-06-11;
董海温 2022-03-22; 出海记事本 2023-09-19; K哥聊出海 2021-09-29; Moss的精神家园 2018-02-23. (P1)

**P-running-out-47.** Single cases report that Best Sellers Rank and keyword position recover differently: one seller
regained sales rank with ads while absent from the first seven result pages, and one product held its keyword position
through a month out of stock and lost it in the days after restock as conversion ran lower. [opinion] seller on
Seller Forums EU, 2020-06-25; anonymous poster on 知无不言, 2023-03-16. (P1)

**P-running-out-48.** In a mail-order field study, conversion on an ordered item fell from 86% to 62% when it was out
of stock, and customers whose whole order was out of stock bought about 22% less afterwards; the setting is a
catalogue retailer, not Amazon. [research] Anderson, Fitzsimons & Simester 2006. (Published research)

**Tactics, as practitioners' practice**

**P-running-out-49.** Practitioners disagree on raising price before a stock-out: My Amazon Guy, BellaVix, 老魏,
日落大道 and others raise in small steps; Sellics' case, Helium 10 and 董海温 say to leave the price and let the product
run out. Amazon's own agent skill bars its agent from raising price as an option. [official] Amazon Selling Partner
plugin 1.0.0, `stockout-prevention`; [opinion] as named. (P3, N1)

**P-running-out-50.** Practitioners disagree on a seller-fulfilled backup offer during the gap: My Amazon Guy, 老魏
and SPS Commerce (for a short gap) use one; Moss and Regan跨境 say its lower conversion harms the listing; and those
who use one disagree on keeping it live while FBA has stock. [opinion] as named; SKU.io; Fast Brands. (P4)

**P-running-out-51.** The claim that closing an out-of-stock listing "freezes" its rank is asserted by SPS Commerce,
OJ Digital, My Amazon Guy and several Chinese writers and denied by sellers on Amazon's forums; neither side shows a
comparison. [opinion] as named. (P5)

**P-running-out-52.** Practitioners report that a returned unit re-shelved during a stock-out reopens the offer and
its Sponsored Products ads on one or two units. [opinion] Hello哥的宝藏部落 and another poster on 知无不言. (P5)

**P-running-out-53.** Reports on a variation family conflict: one seller lost organic placement for all four children
the day after the best-selling child sold out, while others say a minor child's stock-out leaves its siblings
unaffected. [opinion] newbeeseller on 知无不言, 2022-11-15; 日落大道; an unsigned AMZ123 page. (P10)

**P-running-out-54.** Estimates of recovery cost against lost sales range from about one-seventh of the total
(sellerboard's worked example) to two to five times the lost sales (Onramp Funds); Inventory Hero notes that "Amazon
does not publish a recovery multiplier". [opinion] sellerboard blog; Inventory Hero; Onramp Funds. (P2)

**P-running-out-55.** Cover thresholds in circulation are each their author's: 60 days (Jungle Scout), 45 days (Ken
Zhou), 30 and 21 days (BellaVix), 6 weeks (Regan跨境), 75 days (夕木运营笔记本), 30/60 days (优麦云). [opinion] as named.
(P13)

**Amazon's agent skills**

**P-running-out-56.** Amazon's Selling Partner plugin 1.0.0 divides 30 days of ordered units by 30, divides the
fulfillable quantity by that, and bands the result at 7 and 21 days, which it calls its own buffer; it calls "days of
supply < 14" Amazon's analysis rule. No Amazon help or developer page read states that rule; the only "14 days of
supply" on an Amazon page read is an eligibility criterion of the Fulfilled-by-Merchant Restock feature (2025-03-14),
and 14 and 21 are band edges of the low-inventory-level fee. [official] News_Amazon, 2025-03-14. [official] Amazon Selling Partner plugin 1.0.0 (`stockout-prevention/SKILL.md`,
`seller-analytics/references/metrics-catalog.md`). (N1, N2, N4, G7)

**P-running-out-57.** The plugin's metric catalogue names Amazon-computed days of supply at a mean and a 90th
percentile and P80 unit forecasts at 7, 30 and 60 days, served from `sellingpartner-ai.amazon.com`, which is not an
SP-API host. [official] Amazon Selling Partner plugin 1.0.0, `metrics-catalog.md`. (N2)

**Added by the verifier, 2026-11-10**

**P-running-out-58.** Amazon's help page says reserved units cannot be bought, while an Amazon moderator post
(2024-08-26) says units in FC transfer "are available for customers to buy" with a possible future ship date; the
Manage Inventory reports carry `afn-fc-transfer-quantity` and `afn-onhand-buyable-quantity`, undefined on the page.
[official, forum moderator] Topher_Amazon 2024-08-26; [official, listing playbook 2026-10-14, not re-read] *Inventory
Buyability*; [official] *Fulfillment by Amazon (FBA) Reports*. (A3a)

**P-running-out-59.** Amazon validates a coupon about six hours before it starts and keeps validating it while active;
a product without "enough inventory to accommodate the customer demand that your coupon might generate" has the coupon
disabled, and the coupon is recreated, not resumed. No quantity is published. [official, forum staff post]
Danny_Amazon, 2024-08-09. (K3)

**P-running-out-60.** Orders v0 has an order type `BackOrder` for items "currently out of stock and will be available
in the future". [official] Orders v0 model. (D5)

**P-running-out-61.** The FBA Manage Inventory Health report carries, per SKU, whether it is exempt from the
low-inventory-level fee and whether the fee was applied in the current week, with the date its historical days of
supply was last updated. [official] *Fulfillment by Amazon (FBA) Reports*. (H2, R4)

**The seat's own (no source; enters no skill)**

- The disagreement between the "lasting penalty" majority and the measured cases may be partly a difference of
  measure: Best Sellers Rank follows recent sales and returns with them, while keyword position depends on conversion
  after the return. Two single cases point that way; nothing establishes it.
- A day with zero fulfillable units is not always a day the SKU could not be bought (In-Stock Head Start, AWD
  auto-replenishment, the seller's own FBM offer), and a day with fulfillable units is not always a buyable day
  (regional unavailability, Subscribe & Save's replenishment-only state, a suppressed listing). A count of
  out-of-stock days from the ledger is therefore an approximation in both directions.
- Amazon's 15% figure for the Minimum Inventory Level probably reflects faster delivery promises from deeper stock as
  much as avoided stock-outs; the announcement ties it to delivery speed, gives no method, and the Chinese version
  footnotes it to an Amazon Accelerate 2023 talk. It also compares sellers who hold the level with those who do not,
  which is a selection, not an experiment.
- Because the low-inventory-level fee looks back and is reported not to be charged while a product is out of stock, a
  SKU returning from a stock-out with a small first shipment is the case most likely to pay it; one 知无不言 post is
  consistent with that.
- The 14-day default in the door's `/low-stock` template and the 14-day rule in Amazon's plugin look like the same
  convention; I found no Amazon page behind either.
- If the forecast behind Restock recommendations treats a seller's out-of-stock days as Amazon's papers describe,
  Amazon's days of supply would be less biased by a past stock-out than a trailing average is. No page says it does.

## Pages read

All read 2026-11-10 unless a different read is stated. "Local" means a file on disk read in this session.

**Amazon's pages and files**

| Page | URL or path | Date read | Tag | Reached how / unreachable |
|---|---|---|---|---|
| Fulfillment by Amazon (FBA) Reports | https://developer-docs.amazon.com/sp-api/docs/report-type-values-fba | 2026-11-10 | [official] | plain GET of the `.md` form |
| Understanding Amazon listing status and seller-fulfilled inventory management | https://developer-docs.amazon.com/sp-api/docs/understanding-amazon-listing-status-and-seller-fulfilled-inventory-management | 2026-11-10 | [official] | plain GET |
| Replenishment API (guide) | https://developer-docs.amazon.com/sp-api/docs/replenishment-api | 2026-11-10 | [official] | plain GET |
| Analytics Reports; Inventory Reports (report type values) | https://developer-docs.amazon.com/sp-api/docs/report-type-values-analytics ; …/report-type-values-inventory | 2026-11-10 | [official] | plain GET |
| Notification Type Values | https://developer-docs.amazon.com/sp-api/docs/notification-type-values | 2026-11-10 | [official] | plain GET |
| Role Mappings for SP-API Operations | https://developer-docs.amazon.com/sp-api/docs/role-mappings (`updatedAt` 2026-10-28) | 2026-11-10 | [official] | plain GET of the `.md` form; the seat's slug `role-mappings-for-sp-api-operations` returned "Page Not Found" on the verifier's read |
| Role Mappings for SP-API Types | https://developer-docs.amazon.com/sp-api/docs/role-mappings-for-types (`updatedAt` 2026-09-09) | 2026-11-10 | [official] | plain GET of the `.md` form; the seat's slug `role-mappings-for-sp-api-types` returned "Page Not Found" on the verifier's read |
| SP-API deprecations; SP-API release notes | https://developer-docs.amazon.com/sp-api/docs/sp-api-deprecations ; …/sp-api-release-notes | 2026-11-10 | [official] | plain GET |
| SP-API models at commit `db2936aa`: FBA Inventory, Replenishment 2022-11-07, Product Pricing v0, Sales, Orders v0; notification schemas; Data Kiosk and report schemas | `scratch/sp-api-plugins/models/` | 2026-11-10 | [official] | local |
| Amazon Selling Partner plugin 1.0.0: `stockout-prevention`, `listing-buyability`, `seller-analytics` metric catalogue | `scratch/sp-api-plugins/amazon-plugin-zip/` | 2026-11-10 | [official] | local |
| The door's `/low-stock` template | `packages/cx-amazon-sp-api-305/prompts/low-stock.md` | 2026-11-10 | local file | local |
| Availability Estimate Definitions (GM6AEUPCYCFUTYX7) | https://digprjsurvey.amazon.com/csad/help/node/GM6AEUPCYCFUTYX7 | 2026-11-10 | [official] | plain GET of Amazon's mirror; the amazon.com address returned 403 |
| Amazon Ads FAQ | https://advertising.amazon.com/resources/faq | 2026-11-10 | [official] | plain GET |
| New advertiser success guide | https://advertising.amazon.com/library/guides/new-advertiser-success-guide | 2026-11-10 | [official] | plain GET |
| Announcing general availability of Sponsored Display | https://advertising.amazon.com/blog/announcing-general-availability-of-sponsored-display | 2026-11-10 | [official] | plain GET; the sentence a snippet attributed to it was not in the text |
| What is Amazon Subscribe & Save? (2025-08-25) | https://sell.amazon.com/blog/subscribe-and-save | 2026-11-10 | [official] | plain GET |
| Subscribe & Save (programme page) | https://sell.amazon.com/programs/subscribe-and-save | 2026-11-10 | [official] | plain GET |
| Inventory management | https://sell.amazon.com/learn/inventory-management | 2026-11-10 | [official] | plain GET |
| Amazon India restock page | sell.amazon.in (restock inventory blog) | 2026-11-10 | [official] | plain GET |
| News_Amazon, "Plan FBA inventory levels using a new metric" (`datePublished` 2023-12-19) | https://sellercentral.amazon.com/seller-forums/discussions/t/1aa7614a-5542-4529-abe1-ddf452681630 | 2026-11-10 | [official] | plain GET; re-read by the verifier |
| SEAmod, FBA in-stock rate post (`datePublished` 2018-04-18) | https://sellercentral.amazon.com/seller-forums/discussions/t/c7a446a3fd90c44976fabe1b2b84f5a2 | 2026-11-10 | [official] | plain GET |
| Manny_Amazon, Subscribe & Save eligibility reply (`datePublished` 2024-07-23) | https://sellercentral.amazon.com/seller-forums/discussions/t/9f2139f7-377c-488f-b8dd-d30264645e5e | 2026-11-10 | [official] | plain GET |
| "Inventory In Stock Report" thread (2018-04-11) | https://sellercentral.amazon.com/seller-forums/discussions/t/ce80b3a0306ed49e5747611185f2bd0e | 2026-11-10 | [official, via a seller's forum post] | plain GET |
| Topher_Amazon on AWD auto-replenishment (2024-07-16) | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/53ae3d00-183c-4f5c-a9a2-3839f81e1bcb | 2026-11-10 | [official, forum moderator] | plain GET |
| 亚马逊开店分享社, Minimum Inventory Level post (2023-12-11) | https://www.cifnews.com/article/152685 | 2026-11-10 | [official, via 亚马逊开店分享社, a 雨果网 contributor ("观察员") account, reposting AmazonGS] | plain GET |
| 亚马逊, low-inventory-level fee by FNSKU (2026-01-27) | https://www.cifnews.com/article/182908 | 2026-11-10 | [official, via the 雨果网 account "亚马逊", source line 「来源：亚马逊」] | plain GET |
| 亚马逊开店分享社, peak-season stock post (2025-09-10) | https://www.cifnews.com/article/178630 | 2026-11-10 | [official, via 亚马逊开店分享社 reposting AmazonGS] | plain GET |
| Becoming the Featured Offer (G201687550, v20) | office capture `G201687550-v20` | 2026-11-10 (capture 2026-10-14) | [official, office capture] | local |
| Business reports glossary (G27691, v7) | office capture `G27691-v7` | 2026-11-10 (capture 2026-10-14) | [official, office capture] | local |
| Variation relationship FAQ (G201951410, v16) | office capture `G201951410-v16` | 2026-11-10 (capture 2026-10-14) | [official, office capture] | local |
| Amazon deals (G202111490, v25) | office capture `G202111490-v25` | 2026-11-10 (capture 2026-10-14) | [official, office capture] | local |
| Deals for events (G202183600, v10) | office capture `G202183600-v10` | 2026-11-10 (capture 2026-10-14) | [official, office capture] | local |
| Prime Day readiness playbook (GM2ADTH3XH3A5N57, v4) | office capture `GM2ADTH3XH3A5N57-v4` | 2026-11-10 (capture 2026-10-14) | [official, office capture] | local |
| My ASIN is unsearchable (GHGHDMU4X5K9QGCV, v6) | quotations taken from the listing playbook | 2026-10-14 (that seat) | [official, listing playbook, not re-read] | another seat's file |
| Listing playbook, `research/angles/inventory-and-fulfillment.md` | `packages/cx-listing-playbook/research/angles/inventory-and-fulfillment.md` | 2026-11-10 | another seat's read of 2026-10-14 | local |
| Survey stock notes | `scratch/sp-api-plugins/03-job-stock.md` | 2026-11-10 | starting material | local |
| Inventory performance (G202174810) | https://sellercentral.amazon.com/help/hub/reference/external/G202174810 | — | **unreachable** | script shell to GET, also with `?locale=en-US`, `/gp/help/external/`, the `.co.uk` twin; web.archive.org returned 502 |
| IPI FAQ (GZJF4DY2W6MERBAL) | …/external/GZJF4DY2W6MERBAL | — | **unreachable** | script shell |
| Restock Inventory (G5QJ5MF6MGBBYDSU) | …/external/G5QJ5MF6MGBBYDSU | — | **unreachable** | script shell; web.archive.org failed |
| Replenishment Alerts (G200285580) | …/external/G200285580 | — | **unreachable** | script shell; one search snippet only |
| Low-inventory-level fee (GV43F6S76Y9DHYRH) | …/external/GV43F6S76Y9DHYRH | — | **unreachable** | script shell |
| Inventory Buyability (GFC63UNUF6LMLK2R) | …/external/GFC63UNUF6LMLK2R | — | **unreachable** | script shell |
| FBA inventory overview (GTMXYZN64UJL7TT6) | …/external/GTMXYZN64UJL7TT6 | — | **unreachable** | script shell |
| FBA Subscribe & Save help page; In-Stock Head Start help page | ids not found | — | **unreachable** | no address found that serves text |
| Amazon Ads help, ad eligibility (GQFZA83P55P747BZ) | https://advertising.amazon.com/help/GQFZA83P55P747BZ | — | **unreachable** | script shell |
| aboutamazon page on the 2027 fee change | the seat's address returned 404; the letter is at https://sellingpartners.aboutamazon.com/update-to-us-referral-and-fulfillment-by-amazon-fees-for-2027 (read by the holding-costs seat) | — | **unreachable** to this seat | 404; method taken from `areas/holding-costs.md` |
| EcommerceBytes report quoting a restock criterion | — | — | **unreachable** | site no longer publishes; snippet only |
| News_Amazon, "FBA Products in stock soon? Make them available now" (`datePublished` 2019-07-25) | https://sellercentral.amazon.com/seller-forums/discussions/t/e061bc46a55f2c54b0a71f8085b7e018 | 2026-11-10 | [official] | plain GET by the verifier |
| News_Amazon, "Get personalized restock recommendations for your inventory" (`datePublished` 2025-03-14) | https://sellercentral.amazon.com/seller-forums/discussions/t/33b8ff50-5efb-456d-a2d3-12bcf9b86231 | 2026-11-10 | [official] | plain GET by the verifier |
| Danny_Amazon, "Coupon error? Understand Why!" (`datePublished` 2024-08-09) | https://sellercentral.amazon.ca/seller-forums/discussions/t/9d6c58b4-130d-4d60-b6e1-9e573ac8efa6 | 2026-11-10 | [official, forum staff post] | plain GET by the verifier |
| UK seller, "Assistance Needed with the In-Stock Head Start Program", with a Dominic_Amazon reply (`datePublished` 2024-11-20) | https://sellercentral.amazon.co.uk/seller-forums/discussions/t/7b031785-d195-46be-86ff-a3d501d3d83c | 2026-11-10 | [opinion, with an Amazon reply] | plain GET by the verifier |
| ChannelX, "Amazon FBA In-Stock Head Start now live in UK" (2020-08-12) | https://channelx.world/2020/08/amazon-fba-stock-head-start-now-live-uk/ | 2026-11-10 | [opinion] | plain GET by the verifier |
| Topher_Amazon on the three reserved parts (2024-08-26), read by `areas/stock-states.md` | https://sellercentral.amazon.co.uk/seller-forums/discussions/t/c07904af-be04-432d-8c67-80ab0a46f601 | 2026-11-10 | [official, forum moderator] | not re-read here; quoted from the verified sibling file |

**Third parties quoting Amazon, and practitioner and tool pages**

Entry numbers are those of the scratch notes (`notes-practitioners-en.md`, `notes-practitioners-cn.md`), which hold
the quotations. All [opinion] unless the row says it quotes Amazon.

| Page | URL | Date read | Tag | Reached how / unreachable |
|---|---|---|---|---|
| E1: Steven Pope, My Amazon Guy (agency), "Did You Experience a Sudden Amazon Ranking Drop? Here's How to Recover Sales Velocity Fast" (published 2026-06-15, modified 2026-06-16) | https://myamazonguy.com/inventory-management/recover-sudden-amazon-ranking-drop/ | 2026-11-10 | [opinion] | plain GET |
| E2: T. Brian Jones (co-founder/CTO), Inventory Hero (tool), "Out of Stock and Amazon Ranking: What Really Happens" (published 2026-01-15, modified 2026-02-26) | https://www.inventoryhero.ai/blog/out-of-stock-amazon-ranking | 2026-11-10 | [opinion] | plain GET |
| E3: T. Brian Jones, Inventory Hero, "The Real Cost of a Stockout on Amazon FBA, Fully Priced" (published 2026-01-15, modified 2026-02-22) | https://www.inventoryhero.ai/blog/cost-of-stockout-amazon | 2026-11-10 | [opinion] | plain GET |
| E4: SellerSprite (tool; unsigned), "The Impact of Out-of-Stock on Keyword Rankings" (published 2026-04-17) | https://www.sellersprite.com/en/blog/The-Impact-of-Out-of-Stock-on-Keyword-Rankings | 2026-11-10 | [opinion] | plain GET |
| E5: Repricer.com (tool; unsigned), "What Happens to Your Amazon Repricer During a Stockout" (dated 2026-08-27) | https://www.repricer.com/blog/amazon-repricing-stockout/ | 2026-11-10 | [opinion] | plain GET |
| E6: Onramp Funds (lender; unsigned), "The Real Cost of Stockouts on Amazon (Beyond Lost Sales)" (published 2026-10-20, modified 2026-10-23) | https://www.onrampfunds.com/blog/real-cost-stockouts-amazon-beyond-lost-sales/ | 2026-11-10 | [opinion] | plain GET |
| E7: "Team Acadia" (agency; post originally on the Bobsled Marketing blog), "How inventory stockouts impact your ad campaigns on Amazon" (published 2017-07-06, modified 2025-04-02) | https://acadia.io/inventory-stockout/ | 2026-11-10 | [opinion] | plain GET |
| E8: Jeevanantham Kailasam, DataWeave (retail analytics vendor), "How short term Stockouts on Amazon can have a long-term impact on your eCommerce business" (2022-06-30) | https://dataweave.com/blog/amazon-stock-out-impact-on-ecommerce | 2026-11-10 | [opinion] | plain GET |
| E9: SellerEngine (tool; unsigned), "What to Do When Running Out of FBA Inventory and How to Avoid Stockouts" (2023-04-11) | https://sellerengine.com/what-to-do-when-running-out-of-fba-inventory-and-how-to-avoid-stockouts/ | 2026-11-10 | [opinion] | plain GET |
| E10: Steven Pope, My Amazon Guy, "What to Do If You Miss the Amazon FBA Cutoff for Q4" (search title: "Don't Know What to Do If You Miss the Amazon FBA Cutoff? Try This FBM Failover") (published 2026-10-26, modified 2026-10-27) | https://myamazonguy.com/?p=177711 | 2026-11-10 | [opinion] | plain GET |
| E11: Steven Pope, My Amazon Guy, "How to Run Amazon FBA and FBM Together in 2026" (search title: "…Without Losing Rank") (published 2026-08-10, modified 2026-09-15) | https://myamazonguy.com/?p=170448 | 2026-11-10 | [opinion] | plain GET |
| E12: "The SPS Commerce Team" on The Supply Chain Source (SPS Commerce; this is the former SoStocked blog article — `sostocked.com/stockout/` redirects within sostocked.com, and the search engine returned this page for SoStocked queries; the page text itself does not name SoStocked or Chelsea Cohen), "What Is A Stockout + 9 Ways To Avoid It" ("Last Updated March 6, 2026") | https://www.spscommerce.com/community/articles/stockout | 2026-11-10 | [opinion] | plain GET |
| E13: "The SPS Commerce Team" (former SoStocked article, first-person voice), "Inventory-Minded Marketing For Amazon Sellers" ("Last Updated March 6, 2026") | https://www.spscommerce.com/community/articles/inventory-minded-marketing | 2026-11-10 | [opinion] | plain GET |
| E14: Samuel Clifford, BellaVix (agency), "How Amazon PPC Causes Stockouts and What Sellers Must Do to Prevent Them" (published 2026-04-28, modified 2026-06-01) | https://www.bellavix.com/how-amazon-ppc-causes-stockouts-and-what-sellers-must-do-to-prevent-them/ | 2026-11-10 | [opinion] | plain GET |
| E15: Aly Sams, Inventory Planner by Sage (help centre), "Stockouts" (modified 2026-01-29) | https://help.inventory-planner.com/en/articles/2242706-stockouts | 2026-11-10 | [opinion] | plain GET |
| E16: "CustomerSuccess", Store Builder — Inventory Forecasting Hero (help centre; Shopify-first tool, included for its day-level rule), "Understanding Out-of-Stock Logic in Inventory Forecasting Hero (IFH)" (2025-12-05) | https://intercom.help/storebuilder/en/articles/13016500-understanding-out-of-stock-logic-in-inventory-forecasting-hero-ifh | 2026-11-10 | [opinion] | plain GET |
| E17: T. Brian Jones, Inventory Hero, "Stockout Days: What They Are and Why They Matter on FBA" (published 2026-01-15, modified 2026-02-27) | https://www.inventoryhero.ai/blog/stockout-days | 2026-11-10 | [opinion] | plain GET |
| E18: T. Brian Jones, Inventory Hero, "How to Calculate Lost Sales from an Amazon Stockout" (published 2026-01-15, modified 2026-02-23) | https://www.inventoryhero.ai/blog/calculate-lost-sales | 2026-11-10 | [opinion] | plain GET |
| E19: Dave Bryant, EcomCrew (seller/educator), "The Effect of ASIN Stockouts on Amazon Product Rankings" (published 2021-12-10, "Last Updated: September 10, 2024") | https://www.ecomcrew.com/amazon-stockout-effects/ | 2026-11-10 | [opinion] | plain GET |
| E20: Franz Jordan (byline; writes as Sellics — "At Sellics, we…"), on the Skubana blog (page title now reads "Extensiv"), "Out-of-Stock vs Price Hike: Which Is Better On Amazon?" (published 2017-03-14, modified 2025-12-08) | https://www.skubana.com/out-of-stock-vs-price-hike/ | 2026-11-10 | [opinion] | plain GET; now redirects to extensiv.com/blog/out-of-stock-vs-price-hike; re-read by the verifier |
| E21: Profitero (analytics vendor), paid whitepaper page in The Grocer, "The implications of going out of stock are much bigger than you think" (2020-11-16) | https://www.thegrocer.co.uk/whitepapers/the-implications-of-going-out-of-stock-are-much-bigger-than-you-think/650325.article | 2026-11-10 | [opinion] | plain GET by the helper; **404** on the verifier's re-read 2026-11-10 |
| E22: r/FulfillmentByAmazon thread, read through a third-party snapshot mirror ("Reddit Sentiment Analyzer", snapshot dated 2026-01-15), thread question: "Have you successfully recovered a dead ASIN after long stockouts?" (snapshot 2026-01-15) | https://reddit.sentinel-team.org/posts/1qbyr3n/snapshots/2026-01-15T06%3A41%3A22.067049Z | 2026-11-10 | [opinion] | plain GET |
| E23: Seller Labs (tool; unsigned knowledge base), "Listing Ranking Decay: Why Your Top Sellers Slowly Drop" (published 2026-07-03, modified 2026-08-01) | https://www.sellerlabs.com/knowledge-base/listing-ranking-decay-why-your-top-sellers-slowly-drop/ | 2026-11-10 | [opinion] | plain GET |
| E24: Optmyzr (ad tool; unsigned), "How to Pause Amazon Ads Automatically When Inventory Runs Low" (none shown) | https://www.optmyzr.com/blog/pause-amazon-ads-automatically-low-inventory/ | 2026-11-10 | [opinion] | plain GET |
| E25: Ken Zhou, My Amazon Guy, "Stockouts on Amazon and How to Handle Them Right" (search title: "How to Handle Stockouts on Amazon Without Losing Rankings") (published 2026-02-14) | https://myamazonguy.com/inventory-management/stockouts-on-amazon/ | 2026-11-10 | [opinion] | plain GET |
| E26: "The SPS Commerce Team" (former SoStocked article), "Amazon Inventory Answers" (none shown on the fetched text) | https://www.spscommerce.com/community/articles/amazon-inventory-answers | 2026-11-10 | [opinion] | plain GET |
| E27: "The SPS Commerce Team" (former SoStocked article), "Amazon Inventory Impact On Ranking Products" (none shown) | https://www.spscommerce.com/community/articles/amazon-inventory-impact-on-ranking-products | 2026-11-10 | [opinion] | plain GET |
| E28: SKU.io Product Team (tool docs), "FBM Backup Mode — keep your Amazon offer alive through FBA stockouts" (2026-07-16) | https://docs.sku.io/release-notes/2026/07/16/fbm-backup-mode | 2026-11-10 | [opinion] | plain GET |
| E28b: AMZ Prep (3PL; staff byline Joel den Boer shown on page), "Backorder vs Out of Stock: What the Difference Means for Ecommerce Sellers" (published 2026-07-14, modified 2026-09-22) | https://amzprep.com/backorder-vs-out-of-stock/ | 2026-11-10 | [opinion] | plain GET |
| E29: Feedvisor (tool; byline shows "IT"), "Inside Amazon’s In-Stock Head Start and Storage and Replenishment Services" (published 2019-12-04, modified 2022-07-06) | https://feedvisor.com/resources/amazon-shipping-fba/inside-amazons-in-stock-head-start-and-storage-and-replenishment-services/ | 2026-11-10 | [official, via Feedvisor] | plain GET |
| E30: Nel Ayala, Seller Snap (repricer), "How Amazon In-Stock Head Start Helps You Get Ahead of Your Competition" (published 2020-12-22, modified 2025-06-10) | https://sellersnap.io/amazon-in-stock-head-start-benefits/ | 2026-11-10 | [official, via Seller Snap] | plain GET |
| E31: Rob Zaleski, ShippingEasy, "How to Still Sell Out-of-Stock FBA Inventory on Amazon" (published 2019-09-18, modified 2020-06-29) | https://shippingeasy.com/?p=34030 | 2026-11-10 | [opinion] | plain GET |
| E32: Canopy Management (agency; unsigned), "Amazon Rolls Out New Inventory Planning Metric for FBA Sellers" (published 2024-01-09, modified 2025-05-07) | https://canopymanagement.com/amazons-new-inventory-planning-metric/ | 2026-11-10 | [opinion] | plain GET |
| E33: "Alex S", sellerboard (help centre), "Inventory planner" (published 2025-12-04, modified 2026-02-24) | https://help.sellerboard.com/?p=3397 | 2026-11-10 | [opinion] | plain GET |
| E34: "Olivia", sellerboard (blog), "How to Avoid Stockouts on Amazon: A Complete System Using sellerboard" (2026-08-05) | https://blog.sellerboard.com/2026/08/05/how-to-avoid-stockouts-on-amazon-a-complete-system-using-sellerboard/ | 2026-11-10 | [opinion] | plain GET |
| E35: SoStocked Knowledge Base (unsigned help article), "Removing Stock-Outs from Your Forecast" (none shown) | https://help.sostocked.com/article/108-13-advanced-how-to-remove-stock-outs | 2026-11-10 | [opinion] | plain GET |
| E36: SoStocked Knowledge Base, "Inventory Ledger (Stockout Periods)" (none shown) | https://help.sostocked.com/article/308-inventory-ledger-stockout-periods | 2026-11-10 | [opinion] | plain GET |
| E37: SoStocked Knowledge Base (video transcript, first person), "6. Set up Your Forecasts" (none shown) | https://help.sostocked.com/article/106-forecasting-overview | 2026-11-10 | [opinion] | plain GET |
| E38: m19 (ad tool help centre; unsigned), "ASINs status issues" (none shown) | https://help.m19.com/asin-status-issue | 2026-11-10 | [opinion] | plain GET |
| E39: Seller Labs (unsigned knowledge base), "How Inventory Impacts Amazon PPC Performance" (published 2026-05-05, modified 2026-07-29) | https://www.sellerlabs.com/knowledge-base/how-inventory-impacts-amazon-ppc-performance/ | 2026-11-10 | [opinion] | plain GET |
| E40: Gloria Steiner, Perpetua (help centre), "Red Dot Errors and Ads Not Serving" (2024-03-06) | https://help.perpetua.io/en/articles/3151158-red-dot-errors-and-ads-not-serving | 2026-11-10 | [opinion] | plain GET |
| E41: Portent (agency; unsigned), "Why Your Sponsored Product Ads are “Ineligible”" (none shown) | https://portent.com/blog/ppc/why-your-sponsored-product-ads-are-ineligible.htm | 2026-11-10 | [opinion] | plain GET |
| E42: Helium 10 (tool), Weekly Buzz podcast transcript; episode "hosted by Helium 10’s Brand Evangelist Lem Turner", with Bradley Sutton closing, "Helium 10 Buzz 12/08/21: Amazon Logistics, Your Questions Answered, & the New Amazon Anomaly Tracker" (2021-12-09 (modified 2021-12-16)) | https://www.helium10.com/podcast/weekly-buzz-12-8-21/ | 2026-11-10 | [opinion] | plain GET |
| E43: "Isaac", IG PPC (agency), "What to do when you are running out of stock on Amazon" (published 2023-04-04, modified 2024-08-21) | https://igppc.com/?p=13784 | 2026-11-10 | [opinion] | plain GET |
| E44: Julian Bonte-Friedheim, 8fig (funding), "How and why running out of stock hurts your Amazon ranking" (published 2024-04-02, modified 2024-11-06) | https://www.8fig.co/?p=1446 | 2026-11-10 | [opinion] | plain GET |
| E45: Julian Bonte-Friedheim (same byline as E44) on the eComEngine blog, "How to Avoid Stockouts During Peak Selling Periods" (published 2023-08-22, updated 2025-03-19) | https://www.ecomengine.com/blog/running-out-of-stock-amazon | 2026-11-10 | [opinion] | plain GET |
| E46: Kristen Hicks, eComEngine, "How to Avoid Amazon Out of Stock Situations" (published 2023-03-14, updated 2024-09-11) | https://www.ecomengine.com/blog/amazon-out-of-stock | 2026-11-10 | [opinion] | plain GET |
| E47: Ken Zhou, My Amazon Guy, "Avoid Stockouts and Overstock: Amazon Inventory Management" (published 2024-07-30, modified 2026-10-31) | https://myamazonguy.com/articles/selling-on-amazon/amazon-stockouts-and-overstock/ | 2026-11-10 | [opinion] | plain GET |
| E48: Omar Deryan, OJ Digital Solutions (agency), "Amazon Close Listing (Complete Guide to do it Properly") | https://ojdigitalsolutions.com/amazon-close-listing/ | 2026-11-10 | [opinion] | plain GET |
| E49: Rachel Hoover Canto, eComEngine, "Close Listing vs. Delete Listing on Amazon: What's the Difference?" (published 2024-08-06, updated 2024-11-01) | https://ecomengine.com/sell-on-amazon/close-vs-delete-listing | 2026-11-10 | [opinion] | plain GET |
| E50: Amazon Seller Forums (EU), thread "What to when running low on stock FBA?" (seller replies; forum handles not recorded), 2023-01-21 () | https://sellercentral-europe.amazon.com/forums/t/what-to-when-running-low-on-stock-fba/573195 | 2026-11-10 | [opinion] | plain GET |
| E51: Amazon Seller Forums (EU), thread "Out of stock vs Close listing", thread metadata 2021-03-07 () | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/663acbf6f1e619ad3a42c97698f0a92c | 2026-11-10 | [opinion] | plain GET |
| E52: Amazon Seller Forums (CA), thread "Sales Peaked and Plummuted (hear me out)", 2024-10-18 () | https://sellercentral.amazon.ca/seller-forums/discussions/t/4dc51b19-f302-4e54-b2b0-a5be7f50a395 | 2026-11-10 | [opinion] | plain GET |
| E53: Amazon Seller Forums (UK), thread "Is There Any Risk in Leaving My FBA Listing \"Out of Stock\" for Over a Month?", 2025-05-12 () | https://sellercentral.amazon.co.uk/seller-forums/discussions/t/325a7953-2c57-4e7a-8abe-6a7241518cbe | 2026-11-10 | [opinion] | plain GET |
| E54: Amazon Seller Forums (EU), thread "Keeping an out of stock listing active (FBA)", 2022-10-05 () | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/b3e023183b6dda02ebe9e2b5cf4adf0f | 2026-11-10 | [opinion] | plain GET |
| E55: Amazon Seller Forums (EU), thread "Seller Central showing product 'Active' but out of stock for customers?", 2022-04-05 () | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/1876949d02a8c42bdaebdd4df1e5b147 | 2026-11-10 | [opinion] | plain GET |
| E56: Amazon Seller Forums (US), thread "Inventory In Stock Report" (a seller pasting Amazon's field definitions for a report that was later removed), 2018-04-11 () | https://sellercentral.amazon.com/forums/t/inventory-in-stock-report/396641 | 2026-11-10 | [opinion] | plain GET |
| E57: Amazon Seller Forums (EU), thread "FBA inventory runs out but AWD inventory available" — reply by an Amazon forum moderator ("Topher_Amazon"), 2024-07-16 () | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/53ae3d00-183c-4f5c-a9a2-3839f81e1bcb | 2026-11-10 | [opinion] | plain GET |
| E58: Daniel Hannig, SellerLogic (tool), "Amazon Warehousing and Distribution (AWD) Explained" (published 2025-09-24, modified 2026-10-06) | https://www.sellerlogic.com/en/blog/amazon-awd/ | 2026-11-10 | [opinion] | plain GET |
| E59: Supply Chain Dive (trade press; byline not captured), "How Amazon sellers are navigating capacity constraints" (2024-11-07) | https://supplychaindive.com/news/amazon-inbound-fulfillment-AWD-capacity-issues/732189 | 2026-11-10 | [opinion] | plain GET |
| E60: Fast Brands (agency blog; unsigned), "How to add Seller Fulfilled offers to your existing Amazon FBA listings while they are out-of-stock?" (none shown) | https://fastbrands.eu/post/how-to-add-seller-fulfilled-offers-to-your-existing-amazon-fba-listings-while-they-are-out-of-stock | 2026-11-10 | [opinion] | plain GET |
| E61: Boardfy (repricer; unsigned), "Amazon Temporarily Out of Stock: What Price to Set" (published 2023-04-20, modified 2026-10-28) | https://www.boardfy.com/amazons-new-strategy-temporarily-out-of-stock | 2026-11-10 | [opinion] | plain GET |
| E62: "The Badger", Ad Badger (ad tool), "When do you Pause Amazon Advertising Campaigns?" (published 2021-09-09, modified 2026-10-29) | https://adbadger.com/?p=5269 | 2026-11-10 | [opinion] | plain GET |
| E63: Profit Whales (agency) guest post on Payability, "Advertising Out-of-Stock Items: Tactics You Can Use Now" (published 2021-11-29, modified 2022-04-22) | https://payability.com/blog/advertising-out-of-stock-items-tactics-you-can-use-now | 2026-11-10 | [opinion] | plain GET |
| E64: SPS Commerce Team (unsigned; cites Profitero), "Inventory-Aware Amazon PPC: Stop Wasting Ad Spend on Low-Stock Products" (none shown) | https://www.spscommerce.com/community/articles/inventory-aware-amazon-ppc-reduce-wasted-ad-spend | 2026-11-10 | [opinion] | plain GET |
| E65: T. Brian Jones, Inventory Hero, "PPC Inventory Planning: Don't Advertise a Stockout" (published 2026-01-15, modified 2026-06-21) | https://www.inventoryhero.ai/blog/ppc-inventory-planning | 2026-11-10 | [opinion] | plain GET |
| E66: "intelliRANK" guest post on eComEngine, "Spend Less, Profit More: PPC and Inventory Strategy For Amazon Sellers" (2026-09-02) | https://www.ecomengine.com/blog/amazon-ppc-inventory-strategy | 2026-11-10 | [opinion] | plain GET |
| E67: "Hai Mag", Eva (tool/agency), "When to Stop Amazon PPC Spending" (2026-10-30) | https://eva.guru/answers/when-to-stop-amazon-ppc/ | 2026-11-10 | [opinion] | plain GET |
| E68: Colleen Quattlebaum, eComEngine (RestockPro), "Stay in Stock: Amazon Restock Calculator" (published 2015-10-21, updated 2023-12-20) | https://www.ecomengine.com/blog/amazon-restock-calculator | 2026-11-10 | [opinion] | plain GET |
| E69: eComEngine, RestockPro help (unsigned), "How are Suggested Ship and Order, On Order, and Restock Needed Quantities Calculated in RestockPro?" (none shown) | https://www.ecomengine.com/migration/help/suggested-quantity-calculation | 2026-11-10 | [opinion] | plain GET |
| E70: Connect Books (accounting/inventory tool help centre; unsigned), "FBA Restock Inventory Report Explained" (2026-10-29) | https://help.connectbooks.com/en/articles/9528971-restock-inventory-report-explained | 2026-11-10 | [opinion] | plain GET |
| E71: Seller Labs (unsigned knowledge base), "Subscribe & Save Strategy: Stickiness as a Growth Lever" (published 2026-06-01, modified 2026-08-03) | https://www.sellerlabs.com/knowledge-base/subscribe-save-strategy-stickiness-as-a-growth-lever/ | 2026-11-10 | [opinion] | plain GET |
| E72: Connor Mulholland, Jarvio (tool), "How to Build a Replenishable Product Strategy on Amazon" (2026-03-04) | https://jarvio.io/blog/amazon-replenishable-product-strategy | 2026-11-10 | [opinion] | plain GET |
| E73: Amazon Seller Forums (EU), thread "I'm being punished for running out of stock. How do I recover?", thread metadata 2020-06-25 () | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/3956f291b46daa3e95456bac669feef1 | 2026-11-10 | [opinion] | plain GET |
| E74: SupplyKick (agency; unsigned), "Amazon Inventory Forecasting: How to Plan FBA Stock" (published 2021-05-06, modified 2026-09-14) | https://www.supplykick.com/blog/amazon-inventory-forecasting | 2026-11-10 | [opinion] | plain GET |
| E75: Gorilla ROI (spreadsheet data tool; unsigned), "Amazon FBA Inventory Out of Stock Report" (none shown) | https://www.gorillaroi.com/amazon-seller-central-reports/inventory-oos | 2026-11-10 | [opinion] | plain GET |
| E76: Andrew Erickson, Inventory Hero, "Amazon FBA Stockout Prevention: A Seller's Playbook for Never Going to Zero" (published 2026-01-15, modified 2026-05-23) | https://www.inventoryhero.ai/blog/amazon-fba-stockout-prevention | 2026-11-10 | [opinion] | plain GET |
| C1: Kuso王道 (观察员), 雨果网 cifnews, 亚马逊断货后，Listing权重变化及逻辑分析 (2018-01-19) | https://www.cifnews.com/article/32350 | 2026-11-10 | [opinion] | plain GET |
| C2: 藏龙荟跨境电商 (观察员; credited source 跨境电商人成长日记), 雨果网, 亚马逊如何补救断货的产品排名？断货有哪些运营手段来减少损失？ (2019-06-11) | https://www.cifnews.com/article/45337 | 2026-11-10 | [opinion] | plain GET |
| C3: 董海温 (观察员; bio: 12年亚马逊运营操盘手经验), 雨果网, 亚马逊断货太久，链接还能救吗？这些断货补救的措施，你知道几个 (2022-03-22) | https://www.cifnews.com/article/119284 | 2026-11-10 | [opinion] | plain GET |
| C4: 出海记事本 (观察员), 雨果网, 亚马逊断货几天会有什么影响，亚马逊断货后怎么重新做推广 (2023-09-19) | https://www.cifnews.com/article/149674 | 2026-11-10 | [opinion] | plain GET |
| C5: K哥聊出海 (观察员; credited source 跨境工具人的king), 雨果网, 亚马逊断货应对方案及补救方法 (2021-09-29) | https://www.cifnews.com/article/107530 | 2026-11-10 | [opinion] | plain GET |
| C6: Moss的精神家园 (观察员; WeChat GoodLookingMoss), 雨果网, 亚马逊断货如何避免Listing受到影响？教你断货排名反而还上升 (2018-02-23) | https://www.cifnews.com/article/33135 | 2026-11-10 | [opinion] | plain GET |
| C7: 跨境大师兄Peter (观察员; bio: 18人团队跨境年销1亿美元), 雨果网, 亚马逊断货后如何起死回生？ (2025-12-22) | https://www.cifnews.com/article/181907 | 2026-11-10 | [opinion] | plain GET |
| C8: 大美电商·全球跨境店铺管家 (服务商), 雨果网, 亚马逊Listing断货后，该如何快速激活恢复销量？ (2022-12-28) | https://www.cifnews.com/article/138103 | 2026-11-10 | [opinion] | plain GET |
| C9: 鹏城阿兽, AMZ123, Day 111 关于老品断货该不该关广告，广告组权重到底有多少？… (2022-01-19) | https://www.amz123.com/t/dGSYjjH9 | 2026-11-10 | [opinion] | plain GET |
| C10: Regan跨境, AMZ123, 黑五爆单断货后如何快速恢复销量！ (2025-11-28) | https://www.amz123.com/t/M1GURPTt | 2026-11-10 | [opinion] | plain GET |
| C11: Regan跨境, AMZ123, 亚马逊断货后如何快速恢复权重 (2025-12-15) | https://www.amz123.com/t/xqkFI2a6 | 2026-11-10 | [opinion] | plain GET |
| C12: 跨境知识搬运工 (观察员), 雨果网, 断货之后，怎样重新拉动listing的销量？ (2020-08-25) | https://www.cifnews.com/article/75787 | 2026-11-10 | [opinion] | plain GET |
| C13: 老魏 / 跨境电商赢商荟, AMZ123, 【老魏聊电商】断货之后，如何重新拉动Listing的销量？ (2017-11-16) | https://www.amz123.com/t/huJCZ1mK | 2026-11-10 | [opinion] | plain GET |
| C14: 雨果问答, multiple answerers (handles on the page include 三不大师, 高手007, 落花无意, 帝国时代, 波楼牛 and others; which handle wrote which answer was not captured), 【每日一问】亚马逊旺季库存缺货要怎么办？缺货对排名的影响有多大？ (2017-08-21 to 2017-10-17) | https://www.cifnews.com/ask/question/20818 | 2026-11-10 | [opinion] | plain GET |
| C15: AMZ123 `/ask/` (unsigned, stitched), 亚马逊断货后怎么重新推(亚马逊产品断货会影响什么) (2024-05-02) | https://www.amz123.com/ask/s2zKjTir | 2026-11-10 | [opinion] | plain GET |
| C16: AMZ123 `/ask/` (unsigned), 亚马逊补货限制 (2024-05-11) | https://www.amz123.com/ask/Nq8kP7Of | 2026-11-10 | [opinion] | plain GET |
| C17: 赛狐ERP (vendor blog), 亚马逊断货怎么办？2026年跨境卖家全链路补救方案 (dates on page 2026-06-25 … 2026-10-27) | https://www.sellfox.com/blog/article/ymx-dh-sellfox | 2026-11-10 | [opinion] | plain GET |
| C18: 易仓科技 ECCANG (vendor news), 亚马逊FBA库存管理及如何运用ECCANG ERP备货 (2021-10-09) | https://www.eccang.com/news/2300 | 2026-11-10 | [opinion] | plain GET |
| C19: Moss的精神家园, 雨果网 (same page as C6), 2018-02-23 () | https://www.cifnews.com/article/33135 | 2026-11-10 | [opinion] | plain GET |
| C20: 跨境大师兄Peter, 雨果网 (same page as C7), 2025-12-22 () | https://www.cifnews.com/article/181907 | 2026-11-10 | [opinion] | plain GET |
| C21: 大美电商, 雨果网 (same page as C8), 2022-12-28 () | https://www.cifnews.com/article/138103 | 2026-11-10 | [opinion] | plain GET |
| C22: 董海温, 雨果网 (same page as C3), 2022-03-22 () | https://www.cifnews.com/article/119284 | 2026-11-10 | [opinion] | plain GET |
| C23: 跨境Andy, 知无不言, FBA断货了，如何把伤害降到最低？下面几招和大家分享 (2019-12-04 (last activity 2020-04-02)) | https://www.wearesellers.com/question/14838 | 2026-11-10 | [opinion] | plain GET |
| C24: Regan跨境, AMZ123 (same page as C11), 2025-12-15 () | https://www.amz123.com/t/xqkFI2a6 | 2026-11-10 | [opinion] | plain GET |
| C25: 夕木运营笔记本, AMZ123, 亚马逊断货全周期应对方案 (2026-01-30) | https://www.amz123.com/t/QUggCinH | 2026-11-10 | [opinion] | plain GET |
| C26: 老魏 / 跨境电商赢商荟, 知无不言, 求助：热卖的Listing遭遇断货，我该怎么办？ (2020-02-13) | https://www.wearesellers.com/question/16144 | 2026-11-10 | [opinion] | plain GET |
| C27: Hello哥的宝藏部落, 知无不言, 亚马逊Listing断货后如何快速冲击恢复排名？此方法大卖也在用（建议收藏） (2022-08-15 (last activity 2025-03-26)) | https://www.wearesellers.com/question/62937 | 2026-11-10 | [opinion] | plain GET |
| C28: 日落大道, 知无不言, 运营技能干货分享贴:产品要断货怎么办，怎么恢复到断货前的排名？第四波更新 (2023-04-08 (last activity 2024-07-24)) | https://www.wearesellers.com/question/72571 | 2026-11-10 | [opinion] | plain GET |
| C29: Zach的进化笔记, 知无不言, 产品断货前应该做什么动作？断货后应该怎么调整？ (2023-10-23 (last activity 2024-03-07)) | https://www.wearesellers.com/question/83099 | 2026-11-10 | [opinion] | plain GET |
| C30: 奋斗的青年, 知无不言, 亚马逊产品断货后如何快速恢复销量：… (2022-01-19 (last activity 2023-01-06)) | https://www.wearesellers.com/question/52259 | 2026-11-10 | [opinion] | plain GET |
| C31: 橙子的小婷婷, 知无不言, 亚马逊Listing销量暴涨供不应求，排名暴跌怎么应对 (2023-09-22) | https://www.wearesellers.com/question/81837 | 2026-11-10 | [opinion] | plain GET |
| C32: Netease, 知无不言, 亚马逊停售和断货哪个影响大呢？ (2021-07-22) | https://www.wearesellers.com/question/41104 | 2026-11-10 | [opinion] | plain GET |
| C33: 深深深情, 知无不言, listing断货后应怎样应对：分享以下两个方法… (2022-01-14) | https://www.wearesellers.com/question/52000 | 2026-11-10 | [opinion] | plain GET |
| C34: 跟着阿杜学跨境电商, AMZ123, 黑五网一活动日过后，如何避免产品断货的同时让排名掉太多？ (2022-11-30) | https://www.amz123.com/t/lxS2bm17 | 2026-11-10 | [opinion] | plain GET |
| C35: 卖家之家 mjzj.com (no author or date shown; reads as machine-written: 「我结合2025年最新行业数据和实操案例」), 亚马逊产品马上断货的应对策略 (no date) | https://m.mjzj.com/article/eh2qr2ebsfeo | 2026-11-10 | [opinion] | plain GET |
| C36: AMZ123 `/ask/` (unsigned), 亚马逊怎么进行预售？怎么使用库存预售功能？ (2024-09-13) | https://www.amz123.com/ask/2zqpRY8m | 2026-11-10 | [opinion] | plain GET |
| C37: AMZ123 `/ask/` (unsigned), fba产品断货率控制在多少以内 (2024-04-09) | https://www.amz123.com/ask/4JS9NfCc | 2026-11-10 | [opinion] | plain GET |
| C38: 观海论商 / 跨境电商赢商荟, AMZ123, 喜大普奔！亚马逊推出应对FBA库存缺货新计划 (2019-07-29) | https://www.amz123.com/t/OuA00iCk | 2026-11-10 | [opinion] | plain GET |
| C39: AMZ123 `/ask/` (unsigned), 亚马逊物流到什么状态货物会开售 (2024-03-27) | https://www.amz123.com/ask/BE4pykeu | 2026-11-10 | [opinion] | plain GET |
| C40: 小学逊, 知无不言, 即将面临断货一周，请问各位大神有什么方法将影响减至最低！！！ (2019-08-16 (last activity 2021-04-28)) | https://www.wearesellers.com/question/12461 | 2026-11-10 | [opinion] | plain GET |
| C41: newbeeseller, 知无不言, 不知道为啥链接疑似被突然降权，4个变体 … 变体A就在12号断货。其他3个变体为何都搜不到了？… (2022-11-15 (last activity 2022-11-21)) | https://www.wearesellers.com/question/67042 | 2026-11-10 | [opinion] | plain GET |
| C42: Kaijie, 知无不言, 因之前FBA爆仓子体断货,补货后排名和转化率都达不到断货前水平,求解!! (2020-07-22 (last activity 2021-01-19)) | https://www.wearesellers.com/question/21870 | 2026-11-10 | [opinion] | plain GET |
| C43: 一味君, 知无不言, 多变体产品，一个广告打了其中两个变体，要是其中一个变体断货了不进行补货，对流量影响大吗？ (2022-03-20) | https://www.wearesellers.com/question/54942 | 2026-11-10 | [opinion] | plain GET |
| C44: 赛狐ERP SellFox, help centre, 补货建议 (赛狐ERP补货建议怎么设置?) (dates on page 2023年8月30 / 2025年4月27) | https://www.sellfox.com/help/features/restocking-suggestions | 2026-11-10 | [opinion] | plain GET |
| C45: 领星ERP Lingxing, help centre, 领星ERP补货建议视频讲解 (no date shown) | https://www.lingxing.com/help/article/replenishmentAadvice | 2026-11-10 | [opinion] | plain GET |
| C46: 积加ERP (Gerpgo / 积加), help centre, 红绿线 (2025-03-09) | https://help.jijiaerp.com/docs/ADakGUcz | 2026-11-10 | [opinion] | plain GET |
| C47: 易仓科技 ECCANG, training deck (肖忍忍), FBA断货预警 (2020-09-25) | https://www.eccang.com/upload/file/20200926/1601086994_9.pdf | 2026-11-10 | [opinion] | plain GET |
| C48: 优麦云 SellerSpace, help centre, 断货积压不断？别急！这就教你如何科学备货！ (2023-09-19) | https://www.sellerspace.com/help/operations/prepare-inventory-scientifically | 2026-11-10 | [opinion] | plain GET |
| C49: 船长BI CaptainBI, manual, 库存列表—船长手册 (no date) | https://m.captainbi.com/amz_faq_list-49.html | 2026-11-10 | [opinion] | plain GET |
| C50: 店小秘 Dianxiaomi, help centre, 采购＞采购建议＞海外仓备货建议 (no date) | https://help.dianxiaomi.com/pre/getContent.htm?id=2293 | 2026-11-10 | [opinion] | plain GET |
| C51: 马帮ERP, news page, 亚马逊卖家如何做好库存管理？ (2022-09-05) | https://www.mabangerp.com/main_newsDetail.htm?id=29060 | 2026-11-10 | [opinion] | plain GET |
| C52: anonymous poster, 知无不言, 新品期表现好, 开售两周后断货，恢复在售后转化率依然保持在20-30%，但流量怎么也上不去……求支招 (2021-08-30 (last activity 2021-09-30)) | https://www.wearesellers.com/question/43574 | 2026-11-10 | [opinion] | plain GET |
| C53: anonymous poster, 知无不言, 想和大家讨论一下断货前的处理问题和到货后的推广节奏问题… (2023-03-16 (last activity 2023-04-13)) | https://www.wearesellers.com/question/71542 | 2026-11-10 | [opinion] | plain GET |
| C54: anonymous poster, 知无不言, # 案例分析 # 上架三个月的新品自从断货之后，到货在卖数据就不好了… (2023-08-28 (last activity 2023-10-13)) | https://www.wearesellers.com/question/80451 | 2026-11-10 | [opinion] | plain GET |
| C55: Hello哥的宝藏部落, 知无不言 (same page as C27), 2022-08-15 () | https://www.wearesellers.com/question/62937 | 2026-11-10 | [opinion] | plain GET |
| C56: WeAreSellers (reposted on AMZ123), 美国站爆单日出300+稳居前20，断货1周后折扣恢复销量，排名仍滑至50开外，求办法！ (2026-01-13) | https://www.amz123.com/t/aDSRtGJ7 | 2026-11-10 | [opinion] | plain GET |
| C57: alvin8868, 知无不言, 断货后再也回不去了 折腾一个半月的时间，数据还在变差 (2020-08-11) | https://www.wearesellers.com/question/22743 | 2026-11-10 | [opinion] | plain GET |
| C58: anonymous poster, 知无不言, 断货10多天如何重新恢复单量和排名？… (2023-08-28 (last activity 2024-12-20)) | https://www.wearesellers.com/question/80441 | 2026-11-10 | [opinion] | plain GET |
| C59: Frual (case credited to service firm 巧豚豚), 知无不言, 高客单产品断货后，有什么白帽打法快速拉升自然流量，恢复排名？ (2025-07-12 (last activity 2026-03-23)) | https://www.wearesellers.com/question/107496 | 2026-11-10 | [opinion] | plain GET |
| C60: 亚马逊开店分享社 (观察员 contributor account reposting AmazonGS), 雨果网, 1个优化动作=124%增长！亚马逊卖家从断货到爆单的逆袭秘诀 (2025-09-10) | https://www.cifnews.com/article/178630 | 2026-11-10 | [official, via 亚马逊开店分享社 reposting AmazonGS] | plain GET |
| C61: 如果你也听说1234, 知无不言, 关于"低库存水平费用"收取的巨大逻辑漏洞，希望亚马逊的工作人员能刷到... (2025-02-20 (last activity 2026-01-27)) | https://www.wearesellers.com/question/102368 | 2026-11-10 | [opinion] | plain GET |
| C62: 雨果网的朋友们 (观察员, 雨果精选), 雨果网, 4月1日，亚马逊FBA库存新政正式实施 (2024-03-28) | https://www.cifnews.com/article/156707 | 2026-11-10 | [opinion] | plain GET |
| C63: 亚马逊 (the platform's own 雨果 account), 速查！2026年FBA低库存水平费与AWD费率更新 (2026-01-27) | https://www.cifnews.com/article/182908 | 2026-11-10 | [official, via the 雨果网 account "亚马逊"] | plain GET |
| C64: 亚马逊开店分享社 (观察员 contributor account reposting AmazonGS), 雨果网, 上新！亚马逊库存报告新增两个重要指标，预测未来40周商品需求，提升销售表现 (2023-12-11) | https://www.cifnews.com/article/152685 | 2026-11-10 | [official, via 亚马逊开店分享社 reposting AmazonGS] | plain GET |
| C65: 跨境有道, AMZ123, subscribe & save 订购省计划 原理&操作 (2024-08-09) | https://www.amz123.com/t/CJxvPovr | 2026-11-10 | [opinion] | plain GET |
| C66: 雨果跨境 help (unsigned), 亚马逊产品断货之后，广告需要暂停吗 (page dates 2020–2025) | https://www.cifnews.com/help/jjthw | 2026-11-10 | [opinion] | plain GET |

**Research**

Entry numbers are those of `notes-research.md`, which records for each whether the full text or the abstract was read.

| Paper | URL | Date read | Tag | Reached how / unreachable |
|---|---|---|---|---|
| S1: Gruen, Corsten & Bharadwaj (2002), *Retail Out-of-Stocks: A Worldwide Examination of Extent, Causes and Consumer Responses* | https://www.supplychain247.com/images/pdfs/GMA_2002_Worldwide_OOS_Study.pdf | 2026-11-10 | [research] | full text (PDF above), executive summary and the sales-loss chapter read. |
| S2: Corsten & Gruen (2003), "Desperately seeking shelf availability: an examination of the extent, the causes, and the efforts to address retail out-of-stocks" | https://doi.org/10.1108/09590550310507731 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S3: Corsten & Gruen (2004), "Stock-Outs Cause Walkouts" | OpenAlex record (University of St.Gallen repository; *Harvard Business Review*, no DOI) | 2026-11-10 | [research] | repository one-line summary only (OpenAlex). |
| S4: Emmelhainz, Emmelhainz & Stock (1991), "Consumer responses to retail stock-outs" | none (*Journal of Retailing* 67(2)); known only through S21 and S5, which cite it | 2026-11-10 | [research] | **not opened**: no abstract in Crossref, no open copy found; figures second-hand only |
| S5: Verbeke, Farris & Thurik (1998), "Consumer response to the preferred brand out-of-stock situation" | https://doi.org/10.1108/03090569810243640 ; https://personal.eur.nl/thurik/Research/Articles/Consumer%20response%20to%20the%20preferred%20brand%20out-of-stock%20situation.pdf | 2026-11-10 | [research] | abstract (OpenAlex) + full text (author PDF, |
| S6: Campo, Gijsbrechts & Nisol (2000), "Towards understanding consumer response to stock-outs" | https://doi.org/10.1016/S0022-4359(00)00026-9 | 2026-11-10 | [research] | abstract (Tilburg University research portal page). |
| S7: Fitzsimons (2000), "Consumer Response to Stockouts" | https://doi.org/10.1086/314323 | 2026-11-10 | [research] | abstract (OpenAlex; the stored abstract is cut off mid-sentence). |
| S8: Zinn & Liu (2001), "Consumer response to retail stockouts" | https://doi.org/10.1002/j.2158-1592.2001.tb00159.x | 2026-11-10 | [research] | abstract (OpenAlex). |
| S9: Zinn & Liu (2008), "A comparison of actual and intended consumer behavior in response to retail stockouts" | https://doi.org/10.1002/j.2158-1592.2008.tb00090.x | 2026-11-10 | [research] | abstract (OpenAlex). |
| S10: Sloot, Verhoef & Franses (2005), "The impact of brand equity and the hedonic level of products on consumer stock-out reactions" | https://doi.org/10.1016/j.jretai.2005.01.001 ; https://repub.eur.nl/pub/257/erimrs20021125174407.pdf | 2026-11-10 | [research] | abstract of the published article (Erasmus RePub page) + full text of the 2002 working paper. |
| S11: van Woensel, van Donselaar, Broekmeulen & Fransoo (2007), "Consumer responses to shelf out-of-stocks of perishable products" | https://doi.org/10.1108/09600030710840822 | 2026-11-10 | [research] | abstract (Crossref). |
| S12: Anupindi, Dada & Gupta (1998), "Estimation of consumer demand with stock-out based substitution: An application to vending machine products" | https://doi.org/10.1287/mksc.17.4.406 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S13: Kök & Fisher (2007), "Demand estimation and assortment optimization under substitution: Methodology and application" | https://doi.org/10.1287/opre.1070.0409 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S14: Musalem, Olivares, Bradlow, Terwiesch & Corsten (2010), "Structural estimation of the effect of out-of-stocks" | https://doi.org/10.1287/mnsc.1100.1170 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S15: Vulcano, van Ryzin & Ratliff (2012), "Estimating primary demand for substitutable products from sales transaction data" | https://doi.org/10.1287/opre.1110.1012 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S16: Conlon & Mortimer (2013), "Demand estimation under incomplete product availability" | https://doi.org/10.1257/mic.5.4.1 ; https://www.nber.org/system/files/working_papers/w14315/w14315.pdf | 2026-11-10 | [research] | abstract (OpenAlex) + full text of NBER w14315. |
| S17: Che, Chen & Chen (2012), "Investigating effects of out-of-stock on consumer stockkeeping unit choice" | https://doi.org/10.1509/jmr.09.0528 | 2026-11-10 | [research] | abstract (Crossref). |
| S18: Kalyanam, Borle & Boatwright (2007), "Deconstructing each item's category contribution" | https://doi.org/10.1287/mksc.1070.0270 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S19: Breugelmans, Campo & Gijsbrechts (2006), "Opportunities for active stock-out management in online stores: The impact of the stock-out policy on online stock-out reactions" | https://doi.org/10.1016/j.jretai.2006.05.001 | 2026-11-10 | [research] | abstract (Maastricht University research page; and the working-paper abstract on EconPapers, Univ. of Antwerp WP 2005005). |
| S20: Jing & Lewis (2011), "Stockouts in online retailing" | https://doi.org/10.1509/jmkr.48.2.342 | 2026-11-10 | [research] | abstract (OpenAlex and Crossref). No open full text found. |
| S21: Anderson, Fitzsimons & Simester (2006), "Measuring and mitigating the costs of stockouts" | https://doi.org/10.1287/mnsc.1060.0577 ; https://www.kellogg.northwestern.edu/faculty/anderson_e/htm/personalpage_files/Papers/Measuring_and_Mitigating_the_Costs_of_Stockouts.pdf | 2026-11-10 | [research] | full text (author copy, |
| S22: Kim & Lennon (2011), "Consumer response to online apparel stockouts" | https://doi.org/10.1002/mar.20383 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S23: Dadzie & Winston (2007), "Consumer response to stock-out in the online supply chain" | https://doi.org/10.1108/09600030710723309 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S24: Peinkofer, Esper, Smith & Williams (2015), "Assessing the impact of price promotions on consumer response to online stockouts" | https://doi.org/10.1111/jbl.12095 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S25: Peinkofer, Esper & Howlett (2016), "Hurry! Sale ends soon: The impact of limited inventory availability disclosure on consumer responses to online stockouts" | https://doi.org/10.1111/jbl.12136 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S26: Peterson, Kim & Jeong (2019), "Out-of-stock, sold out, or unavailable? Framing a product outage in online retailing" | https://doi.org/10.1002/mar.21309 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S27: Sampaio & Sampaio (2015), "Managerial response to stockouts: the effect of remedies on consumer behavior" | https://doi.org/10.1590/0103-6513.156113 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S28: Craig, DeHoratius & Raman (2016), "The impact of supplier inventory service level on retailer demand" | https://doi.org/10.1287/msom.2016.0582 ; https://www.hbs.edu/ris/Publication%20Files/11-034_e1d4f7ab-7e3a-4b10-8d6c-d5c2ab8b4c9b.pdf | 2026-11-10 | [research] | abstract (Crossref) + full text of the HBS working paper. |
| S29: Olivares & Cachon (2009), "Competing retailers and inventory: An empirical investigation of General Motors' dealerships in isolated U.S. markets" | https://doi.org/10.1287/mnsc.1090.1050 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S30: Cachon, Gallino & Olivares (2019), "Does adding inventory increase sales? Evidence of a scarcity effect in U.S. automobile dealerships" | https://doi.org/10.1287/mnsc.2017.3014 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S31: Balakrishnan, Pangburn & Stavrulaki (2004), "“Stack them high, let 'em fly”: Lot-sizing policies when inventories stimulate demand" | https://doi.org/10.1287/mnsc.1040.0228 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S32: Cui, Zhang & Bassamboo (2019), "Learning from inventory availability information: Evidence from field experiments on Amazon" | https://doi.org/10.1287/mnsc.2017.2950 ; https://utdserv.utdallas.edu/jindal/files/2022/03/achal_bassamboo_paper.pdf | 2026-11-10 | [research] | abstract of the published version (Crossref/OpenAlex) + full text of the earlier working-paper version titled "…Field Evidence from Amazon". The published version reports "two randomized field experiments"; the working paper… |
| S33: Park, Rabinovich, Tang & Yin (2020), "The impact of disclosing inventory-scarcity messages on sales in online retailing" | https://doi.org/10.1002/joom.1082 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S34: Calvo, Cui & Wagner (2023), "Disclosing product availability in online retail" | https://doi.org/10.1287/msom.2020.0882 | 2026-11-10 | [research] | abstract (Crossref). |
| S35: Etumnu, Chenarides & Jaenicke (2025), "Grocery stockouts and seller performance in Amazon's marketplaces" | https://doi.org/10.1002/agr.22051 | 2026-11-10 | [research] | abstract only (OpenAlex; Semantic Scholar). Publisher full text returned HTTP 403; ResearchGate 403; no open copy found. |
| S36: Etumnu & Malone (2024), "An empirical examination of BuyBox assignments in online grocery retail" | https://doi.org/10.1002/agr.21978 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S37: Raval (2023), "Steering in one click: Platform self-preferencing in the Amazon Buy Box" | https://deveshraval.github.io/buyBox.pdf | 2026-11-10 | [research] | full text (PDF above). |
| S38: Chen, Mislove & Wilson (2016), "An empirical analysis of algorithmic pricing on Amazon Marketplace" | https://doi.org/10.1145/2872427.2883089 ; https://mislove.org/publications/Amazon-WWW.pdf | 2026-11-10 | [research] | full text (PDF above). |
| S39: Lee & Musolff (2021), "Entry into two-sided markets shaped by platform-guided search" | https://conference.nber.org/confer/2022/DTs22/judy1.pdf | 2026-11-10 | [research] | full text of that draft (searched and read at the quoted passages). |
| S40: He, Hollenbeck & Proserpio (2022), "The market for fake reviews" | https://doi.org/10.1287/mksc.2022.1353 ; https://mpra.ub.uni-muenchen.de/105507/1/MPRA_paper_105507.pdf | 2026-11-10 | [research] | full text of the January 2021 working paper. Crossref's abstract for the published version is one sentence. |
| S41: Chevalier & Goolsbee (2003), "Measuring prices and price competition online: Amazon and Barnes and Noble" | https://www.nber.org/system/files/working_papers/w9085/w9085.pdf | 2026-11-10 | [research] | full text of the NBER working paper. |
| S42: Zhu & Liu (2018), "Competing with complementors: An empirical look at Amazon.com" | https://doi.org/10.1002/smj.2932 | 2026-11-10 | [research] | abstract (Crossref) + full text of the January 2015 draft (Mack Institute copy). |
| S43: Farronato, Fradkin & MacKay (2023), "Self-preferencing at Amazon: Evidence from search rankings" | https://doi.org/10.1257/pandp.20231068 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S44: Cabral & Xu (2021), "Seller reputation and price gouging: Evidence from the COVID-19 pandemic" | https://doi.org/10.1111/ecin.12993 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC8251445/ | 2026-11-10 | [research] | full text (PubMed Central copy, |
| S45: Cavallo & Kryvtsov (2023), "What can stockouts tell us about inflation? Evidence from online micro data" | https://doi.org/10.1016/j.jinteco.2023.103769 ; https://www.nber.org/system/files/working_papers/w29209/w29209.pdf | 2026-11-10 | [research] | abstract (OpenAlex) + full text of NBER w29209. |
| S46: Wecker (1978), "Predicting demand from sales data in the presence of stockouts" | https://doi.org/10.1287/mnsc.24.10.1043 | 2026-11-10 | [research] | abstract (Crossref). |
| S47: Nahmias (1994), "Demand estimation in lost sales inventory systems" | https://doi.org/10.1002/1520-6750(199410)41:6<739::AID-NAV3220410605>3.0.CO;2-A | 2026-11-10 | [research] | abstract (OpenAlex). |
| S48: Agrawal & Smith (1996), "Estimating negative binomial demand for retail inventory management with unobservable lost sales" | https://doi.org/10.1002/(SICI)1520-6750(199609)43:6<839::AID-NAV4>3.0.CO;2-5 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S49: Lau & Lau (1996), "Estimating the demand distributions of single-period items having frequent stockouts" | https://doi.org/10.1016/0377-2217(95)00134-4 | 2026-11-10 | [research] | Crossref record only; no abstract available. Content `[not re-read]`. |
| S50: Huh, Levi, Rusmevichientong & Orlin (2011), "Adaptive data-driven inventory control with censored demand based on Kaplan-Meier estimator" | https://doi.org/10.1287/opre.1100.0906 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S51: Besbes & Muharremoglu (2013), "On implications of demand censoring in the newsvendor problem" | https://doi.org/10.1287/mnsc.1120.1654 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S52: Jain, Rudi & Wang (2015), "Demand estimation and ordering under censoring: Stock-out timing is (almost) all you need" | https://doi.org/10.1287/opre.2014.1326 | 2026-11-10 | [research] | abstract (OpenAlex). |
| S53: Seeger, Salinas & Flunkert (2016), "Bayesian intermittent demand forecasting for large inventories" (Amazon) | https://proceedings.neurips.cc/paper_files/paper/2016/file/03255088ed63354a54e0e5ed957e9008-Paper.pdf | 2026-11-10 | [research] | full text. re-opened by the verifier 2026-11-10 and the quotations found |
| S54: Böse, Flunkert, Gasthaus, Januschowski, Lange, Salinas, Schelter, Seeger & Wang (2017), "Probabilistic demand forecasting at scale" (Amazon) | https://doi.org/10.14778/3137765.3137775 ; https://www.vldb.org/pvldb/vol10/p1694-schelter.pdf | 2026-11-10 | [research] | full text. re-opened by the verifier 2026-11-10 and the quotations found |
| S55: Salinas, Flunkert, Gasthaus & Januschowski (2020), "DeepAR: Probabilistic forecasting with autoregressive recurrent networks" (Amazon) | https://doi.org/10.1016/j.ijforecast.2019.07.001 ; https://arxiv.org/abs/1704.04110 | 2026-11-10 | [research] | full text of the arXiv version; re-opened by the verifier 2026-11-10 and the quotation found |
| S56: Wen, Torkkola, Narayanaswamy & Madeka (2017), "A multi-horizon quantile recurrent forecaster" (Amazon) | https://arxiv.org/abs/1711.11053 | 2026-11-10 | [research] | full text. |
| S57: Bhargava, Sun & Xu (2006), "Stockout compensation: Joint inventory and price optimization in electronic retailing" | https://doi.org/10.1287/ijoc.1040.0091 | 2026-11-10 | [research] | abstract (OpenAlex). |

**Third-party pages that could not be read**

| Page | URL | Date read | Tag | Reached how / unreachable |
|---|---|---|---|---|
| Jungle Scout help, Inventory Manager calculations | https://support.junglescout.com/hc/en-us/articles/30529000072087-Inventory-Manager-Calculations-and-Sales-History | — | **unreachable** | HTTP 403 |
| Helium 10 help, Inventory Manager restock recommendations | https://kb.helium10.com/hc/en-us/articles/360060376193-How-Does-the-Helium-10-Inventory-Manager-Calculate-My-Restock-Recommendations | — | **unreachable** | HTTP 403 (challenge page) |
| Pacvue, weeks of cover | https://pacvue.com/blog/weeks-of-cover-preventing-out-of-stock-inventory-lost-sales-and-seo-ranking/ | — | **unreachable** | HTTP 403 (challenge page) |
| My Amazon Guy podcast on In-Stock Head Start | https://podcast.myamazonguy.com/915508/9340861 | — | **unreachable** | connection failed |
| 知无不言 replies under every thread cited | https://www.wearesellers.com/ | — | **unreachable** | replies hidden from a logged-out reader; opening posts read |
| 马帮 help centre | — | — | **unreachable** | script shell |
| reddit.com | — | — | **unreachable** | not fetched; one thread read on a third-party mirror (E22) |
| Full texts of several papers (Etumnu et al. 2025; Jing & Lewis 2011; Calvo et al. 2023; others) | see `notes-research.md`, section (c) | — | **unreachable** | publisher paywalls; abstracts read |
| web.archive.org captures of Seller Central help pages | https://web.archive.org/ | — | **unreachable** | HTTP 502 and connection failures on 2026-11-10 |

## Verification

Verified 2026-11-10 by the verifier seat, against sources re-opened that day: Amazon pages and forum posts by plain GET
(each forum post's `datePublished` read from its HTML), the developer pages' `.md` forms, the local SP-API models at
`db2936aa`, Amazon's plugin files, the office captures of 2026-10-14, the three Amazon forecasting papers' full texts
(PDFs read with macOS PDFKit), and a sample of practitioner pages. Scratch copies are in
`scratch/stock-playbook/running-out/verify/`.

**Scope of the check.** All 57 positions were checked; about 95 other claims (figures, dates, field names, enums,
columns, report scopes, roles, quotations) were re-opened at their source. Every role in section O was re-parsed from
Amazon's two role-mapping pages and matches; every report's Roles line on the report-type page agrees. Positions
corrected: 7 (P-running-out-11, -24, -25, -40, -44, -46, -56), plus the stable lines 13, 15 and 18 and a new stable
line 7a.
Positions removed: none. Positions added: 4 (-58 to -61). No position carried an instruction to cx.

**Changes that matter, by claim.**

- *The 15% Minimum Inventory Level figure (H1, P-24).* Confirmed verbatim on Amazon's forum post: "Sellers who
  maintain units above the Minimum Inventory Level see a 15% increase in sales over a four-week period on average,
  though actual results may vary." The post's `datePublished` is 2023-12-19 (the seat had derived "December 2023").
  The survey and the listing playbook were wrong to say no Amazon page carries it. The Chinese post (cifnews 152685,
  2023-12-11) is by 亚马逊开店分享社, a 雨果网 contributor ("观察员") account, reposting Amazon Global Selling's WeChat
  (AmazonGS): tag lowered from [official] to [official, via …]. Its footnote, which the seat said was not captured,
  reads 「*数据来源：亚马逊2023 Accelerate」. The same post says the level counts sellable, FC-transfer and reserved units
  and excludes inbound (added to H1 and P-24).
- *Lasting rank penalty (P1, P-42 to -45).* No Amazon page or published study read measures one: confirmed. EcomCrew
  (published 2021-12-10, updated 2024-09-10): five ASINs across three accounts, outages "from a couple of days to
  several months", Best Sellers Rank read before and after from charts; six per-item captions appear, one item "never
  recovered its historical sales rank" and two never regained the pre-outage bump. Sellics (2017-03-14, now on
  extensiv.com): one product, rankings of its top three keywords, with a Sponsored Products push at restock that made
  82% of first-week sales, so the one-week recovery is not separable from that push. Both added to P1 and P-44.
- *The Chinese grace period (P1, P-46).* All five posts re-read. 藏龙荟 2019-06-11 has the three-day sentence; 董海温
  2022 and 出海记事本 2023 repeat it; K哥聊出海 2021-09-29 prints it with 「2周」 and then copies Moss的精神家园's
  2018-02-23 two-week section word for word. Moss's section is his own routine, not a grace-period claim. No earlier
  three-day copy was found in two searches; 藏龙荟 2019 is the earliest found, not proven the first.
- *Amazon's forecasting papers (Research, P-40, stable line 15).* Quotations found verbatim in Seeger et al. 2016,
  Salinas et al. (DeepAR) and Böse et al. 2017. Only Seeger et al. treat the out-of-stock day as missing (likelihood
  term dropped); DeepAR names the underbias and "downward spiral"; Böse et al. call orders an approximation of
  demand. The file said all three "treat such days as missing"; reworded.
- *Plugin bands (N4, P-56, stable line 18).* Aligned with `beyond/sellers-tools-and-research.md` and
  `areas/restock-and-forecast.md`: the only "14 days of supply" on an Amazon page read is the FBM Restock feature's
  eligibility criterion (News_Amazon 2025-03-14, re-read: "current days of supply less than 14 days"), and 14/21 are
  low-inventory-level fee band edges. The EcommerceBytes snippet in G7 matches the FBM criterion. The file had said the
  14 was on no Amazon page.
- *Lost revenue only in the Replenishment API (P-29).* Confirmed for seller surfaces: a search of all models and
  schemas finds `LOST_REVENUE_DUE_TO_OOS` only there. Vendor-only surfaces carry out-of-stock measures
  (`procurableProductOutOfStockRate` in the vendor inventory report and Data Kiosk vendor analytics; the vendor
  forecasting report's P70/P80/P90 "will not run out of stock" units); none is a lost-revenue figure and none applies to
  a seller.
- *In-Stock Head Start (D1, D2, P-10, P-11, R2).* Amazon's own announcement is now read first-hand (News_Amazon
  2019-07-25). The latest trace is a UK seller post of 2024-11-20 saying it works for some products. No 2025–2026
  Amazon text found; whether it is still offered stays open. Double counting: the notification example (10 future-supply
  buyable against 15 shipped or receiving) is consistent with a subset of inbound; the 2019 "both Available and
  Inbound" line is pilot-era third-party text. Both stay open for a real account.
- *Sibling alignment.* The 2027 low-inventory-level method now follows `areas/holding-costs.md` I1–I3 (28 days of
  shipments before and after the assessment; both below 28 days; charged in arrears); the seat had quoted only the
  survey. The FC-transfer buyability (A3a, P-58, seller's choice 1) now follows `areas/stock-states.md` C1–C2, and it
  rests on one moderator post against one help page. The Manage Inventory reports' `afn-fc-transfer-quantity` and
  `afn-onhand-buyable-quantity`, missing from R2, were added.
- *Forum dates.* SEAmod's in-stock-rate post is 2018-04-18 (was "9 years ago"); Manny_Amazon's Subscribe & Save
  reply is 2024-07-23 (was "2 years ago"); Topher_Amazon's AWD reply (2024-07-16) and the Inventory In Stock thread
  (2018-04-11) are confirmed.
- *Tags lowered.* cifnews 152685 and 178630 → [official, via 亚马逊开店分享社 reposting AmazonGS]; cifnews 182908 →
  [official, via the 雨果网 account "亚马逊"]; Pages read rows C60, C63 and C64 were tagged [opinion] while the body
  called them [official], and are now the "via" tag; E29 and E30 read "[official, via]" with no name, now named.
- *Smaller corrections.* `totalQuantity`'s definition was re-read in the model (line 848: "The total number of units in
  an inbound shipment or in Amazon fulfillment centers."). 跨境大师兄Peter's 127 cases are cases of failed recovery
  (a chosen sample). The 知无不言 case of 2023-03-16 left its ads running and raised its top-of-search bid on restock.
  The Profitero page (thegrocer.co.uk) now returns 404, so its figures rest on the helper's notes. The role pages'
  slugs used by the seat now return "Page Not Found"; the live slugs are `role-mappings` and `role-mappings-for-types`.
- *Pages read.* The 41 research rows that read "see notes" were rebuilt from `notes-research.md`. All 57 research rows
  now carry the DOI or open URL and what was opened. The script had also mislabelled S20 (Jing & Lewis) as "full text"
  when only the abstract was read, and that is corrected. No practitioner row read "see notes". Six rows were added for
  the pages the verifier read.

**Gap fills (2026-11-10).** D5 (Orders v0 `BackOrder` order type); K3 (coupon stock validation, Danny_Amazon
2024-08-09); the Manage Inventory Health report's fee-exemption, fee-applied and last-updated columns (H2, R4, P-61);
the Minimum Inventory Level's on-hand composition (H1); In-Stock Head Start's first-hand announcement and latest trace
(D2).

**Not re-opened, and why.** Help pages behind the script shell (the list in Open questions 8), per the lead's ruling;
the listing playbook's quotations and the office captures were checked against the local capture files (E1, E2, K1,
K2, L1, H4: all found) but not at Amazon. Practitioner pages were spot-checked (My Amazon Guy ?p=170448, SellerSprite,
DataWeave, Onramp Funds, 跨境大师兄Peter, 知无不言 71542, 62937 and 67042, EcomCrew, Sellics: all quotations found);
the rest of E1–E76 and C1–C66 rest on the helpers' notes. Papers other than S53–S55 were not re-opened.

**Gaps left.** The Restock report's `Alert` values and the Planning report's `alert` values (one more search found no
Amazon list); `stockRisk` strings (none in the model, nor in Amazon's SDK repositories on GitHub); deal stock rules at
submission and run time (third parties disagree: 25 hours or seven days); the 2027 fee page GFU8NTVGHP2JQLCR; Helium 10,
Jungle Scout and Pacvue help centres (not retried); 知无不言 replies behind the login; open full texts of Etumnu et al.
2025, Jing & Lewis 2011, Calvo et al. 2023 and Wecker 1978 (none found); whether In-Stock Head Start still runs in 2026.

**Duplication noted, left as is.** P-26 restates part of P-25, and P-35 restates M3. Pages read lists some pages twice
under different helper entry numbers (C6/C19, C7/C20, C8/C21, C3/C22, C11/C24, C27/C55), each marked "same page".
