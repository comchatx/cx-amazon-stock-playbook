# What only Seller Central shows

Read 2026-11-10 by the research seat. Verified 2026-11-10 by the verifier (changes are listed in *Verification*).

Tags: **[official]** is Amazon's own words on a page opened in this session, or in a local copy of Amazon's models and
documentation; **[official, via IF]** is a Seller Central help page quoted in the listing playbook's
`research/angles/inventory-and-fulfillment.md`, read by that seat on 2026-10-14 and **not re-read here**; **[official,
via <who>]** and **[snippet]** are Amazon's words seen only in a third party's quotation or a search result;
**[opinion]** names who says it; **[seat]** is this seat's inference and enters no skill.

How pages were reached. Seller Central help pages returned a script shell to a plain GET in every form tried
(`/help/hub/reference/external/<ID>?locale=en-US`, `/gp/help/external/<ID>`, the `.co.uk` twin); the help hub's
content call is a POST and was not made; a text-reader proxy and web.archive.org captures of help pages were refused
by this session's permission layer and were not retried. So **no Seller Central help page was read first-hand**
(they are listed in *Open questions*). What was read by plain GET: Amazon's seller-forum threads
(`sellercentral.amazon.*/seller-forums/discussions/t/<id>`, whose text is in the HTML), `sell.amazon.com`, the SP-API
documentation as Markdown (`developer-docs.amazon/sp-api/docs/<page>.md`), and practitioners' pages. The SP-API
models and schemas were read locally at commit `db2936aa` (2026-10-29) under
`scratch/sp-api-plugins/models/` (`models/` and `schemas/`); Amazon's Selling Partner plugin 1.0.0 was read from its
extracted files under `scratch/sp-api-plugins/amazon-plugin-zip/`; its host was never called.

What "no API carries it" means in this file. It is evidence by absence, of three kinds, named beside each item:
**(m)** a case-insensitive search for the field's words across every JSON model and every report, Data Kiosk,
notification and feed schema in the clone returned nothing relevant; **(r)** the *Report Type Values* pages (FBA,
Inventory, the general list) name no report with that content; **(n)** the release notes name no such launch through
the entry of 2026-11-04 (the research seat read through 2026-10-28; the verifier re-read the page as updated
2026-11-04). A search of the models and schemas alone misses the flat-file reports' columns: two of this file's
first-draft absences (the storage utilization ratio, the inbound performance rows) were broken by the *FBA Reports*
page, and a third (the capacity reservation charge) by a model field spelt without the word "fee". The FBA flat-file reports have no schema in the clone, so for them the evidence is the column list on the
*FBA Reports* page (r), not (m). Absence in documents is not proof about a live account: a first run can still find a
column the page does not list.

## What this covers

- The stock facts and settings a seller sees in Seller Central that no SP-API operation, report or Data Kiosk
  dataset returns, item by item, with the nearest proxy an API does carry and that proxy's role.
- For each item: what the page is (as far as Amazon's reachable words say), the evidence of absence, whether a
  download exists, and whether Amazon's own Selling Partner connector exposes it.
- Items the starting material called Seller-Central-only that the models show are **in** the API (carrier quotes,
  appointment slots, item labels, placement options, the entered cost of goods).
- Other ways the data leaves Seller Central (ERP sub-accounts and browser extensions, Seller Assistant, the
  Business Solutions Agreement's Agent Policy), as facts about what exists.
- What overlaps with the listing playbook's `method/seller-central-only-tools.md`.

Owned elsewhere and only cross-referenced: the meaning and rules of each program and fee (`areas/*`,
`beyond/programs-and-regions.md`); the API surface tables, with every operation's rate and parameters
(`method/sp-api-stock-surface.md`). This file states a rule of a program only as far as needed to say what the page
shows.

## Amazon's own rules

### A. Inventory Performance Index (IPI)

A1. What the dashboard shows [official, via IF D3, help page G202174810 v9, read there 2026-10-14]. Four parts:
excess inventory, 90-day sell-through, stranded inventory, in-stock rate. "We consider an item to be excess if it has
over 90 days of supply based on the forecasted demand." In-stock rate is "the percent of time your replenishable FBA
ASINs have been in stock during the last 30 days, weighted by the number of units sold for each SKU in the last 60
days". "Estimated FBA lost sales in the last 30 days is equal to the forecasted unit sales on days that your
products were out of stock multiplied by the average sales price."

A2. Who has a score [official, via IF D4, help page GZJF4DY2W6MERBAL v19]. Professional plan only. "If you are new
to FBA or have not been active in the past 13 weeks, you may not have an IPI score". "Newly created ASINs in their
first 90 days do not affect your IPI score." "The in-stock rate itself is not a direct input into your IPI score…".
"Sell-through rate is updated daily and looks at the past 90 days of shipped units and average inventory over that
same period." "We will inform you four to eight weeks before the new period limit goes into effect what the IPI
threshold will be."

A3. Threshold history, from Amazon's forum announcements opened this session [official]:

| Announcement | Store | What it says |
|---|---|---|
| "IPI threshold change for FBA storage limits and new overage fee", News_Amazon, sellercentral-europe forum, 2020 | UK/EU | "We have raised the IPI threshold requirement for storage limits from 350 to 400 as of May 14, 2020 (week 20). If you had an IPI score of 400 or more as of week 20, you will receive unlimited storage for Q3." and "If you have an IPI score of less than 400 as of week 26 (June 21), your potential storage limits will apply from July 1 through Sept. 30." |
| "Inventory Performance Index threshold will change to 450", News_Amazon, sellercentral.amazon.com forum, December 2020 | US | "If your IPI is 450 or above in week 51 of 2020, starting January 1, 2021, you will not be subject to storage volume limits. If your IPI is below 450 in week 51 of 2020, you will continue to be subject to storage volume limits. We will notify you of your next period limits, which will go into effect on February 1, 2021." |

Two further steps were seen only in search results and are **[snippet]**: a US notice of October 2019 ("Effective
January 1, 2020, we are changing the IPI threshold for storage limits to 400 (previously 350)"), a US threshold of
500 for 2020-08-16 to 2020-12-31, and a return to 400 from 2022-01-01 ("With this IPI change, less than 10% of
sellers will have storage volume limits", via EcommerceBytes 2021-12-21, page not readable this session).

A4. The pattern in A3 is a **measurement week** and an **effective date**: the score in a named week decides the
limit for a later period. That mechanism belonged to the quarterly storage-limit system, which Amazon replaced on
2023-03-01 (B1). In the monthly capacity system Amazon's reachable words say only that the limit "is influenced by
your IPI score, as well as other factors" (B1, B2) and that estimates "may vary up or down based on how efficiently
you are using capacity, as measured by your Inventory Performance Index (IPI) score". No Amazon page opened in this
session states a current numeric threshold, and the listing playbook's read of the capacity page (2026-10-14) found
none on it either. The current threshold, if one applies to an account, is on that account's Inventory Performance
dashboard.

A5. No API field carries the score or its parts. (m) No hit for `inventory performance`, `IPI`, `ipiScore`,
`sell-through`, `excess` as an account measure in any seller model or schema (the only hits are the vendor
analytics dataset and the vendor inventory report). The Data Kiosk seller analytics schema
(`schemas/data-kiosk/analytics_sellerAnalytics_2025_03_31.graphql`, type `Lending`, line 466) carries one stock
figure, `totalFbaInventoryValue` ("Total worth of seller's inventory stored in FBA warehouses based on 15-day average
selling price"), and no IPI, excess, stranded or sell-through field; the sales-and-traffic schema carries no stock
figure. The per-SKU columns `sell-through` and `estimated-excess-quantity` are in the planning report (R1); they are
SKU figures, not the account's score. (n) No release note. The connector's metric catalogue (H2) has no IPI metric.

### B. Capacity limits and Capacity Manager

B1. The system [official]. "Simplifying FBA capacity limits for your business", News_Amazon, sellercentral.amazon.com
forum, January 2023: "Effective March 1, 2023, we're replacing the weekly restock limit and quarterly storage limit
with a single monthly capacity limit per storage type". "Capacity limits for the upcoming month will be announced in
the third full week of each month via the Capacity Monitor in Seller Central and an email notification." "In
addition to your upcoming monthly capacity limit, we'll provide estimated limits for the following two months". "We'll
set capacity limits and measure your inventory usage by volume … we'll continue to show inventory usage in units and
provide an estimate of how many units your capacity limits permit." "Like restock limits today, capacity limits
consider inventory that is on-hand in Amazon's fulfillment centers and shipments you've created that have not yet
arrived." "Overage fees are calculated based on the highest estimated or confirmed limit that we provided for the
given period." "You can view your capacity limit … as well as your estimated limits, in the FBA dashboard." The same
text is in Amazon's blog post "Amazon announces new streamlined FBA capacity management system" (Dharmesh Mehta,
sell.amazon.com, 2023-01-17) and in the "Ask Amazon" Q&A of 2023-03-14 (Kelly_Amazon).

B2. Two Amazon pages disagree on when the limit is announced. The 2023 announcement says "the third full week of
each month"; the help page as read by the listing playbook on 2026-10-14 says "Capacity limits are typically
announced during the fourth week of the month." [official, via IF D1, GAFNWEYTJUV2GBFC v22]. The help page is the
later text. Other facts from that read: "You'll receive one capacity limit for each storage type per month.";
"Individual selling accounts have a capacity limit of 15 cubic feet"; "New professional selling accounts (active in
FBA for less than 39 weeks) don't receive FBA capacity limits."; "If your on-hand inventory plus shipments on the way
to our fulfillment centers exceeds your capacity limit, you'll be blocked from creating new shipments to Amazon.";
"Capacity cannot be transferred or exchanged between storage types."; "Removal orders are reflected in your capacity
usage within 24 hours of the order being created, even if the order is still in Pending status."

B3. Capacity Manager [official]. The 2023 announcement: "you can request additional capacity based on a reservation
fee that you specify. Requests are granted objectively, starting with the highest reservation fee per cubic foot
until all capacity available under this program has been allocated. When your request is granted, the reservation fee
is offset by performance credits that you earn from the sales you generate using the extra capacity. Performance
credits are designed to offset up to 100% of your reservation fee". Dominic_Amazon, "Refresher: FBA Capacity Limits &
How They Work" (forum): "Tell us how much additional capacity you want, and when / Set the maximum reservation fee
that you're willing to pay … We'll assess fulfillment center capacity regularly (typically twice per week) and grant
requests as capacity is available." TaylorR_Amazon, reply in "FBA Capacity Limits and Fees" (forum, 2024): "No
upfront payment is required and if your request is granted, you'll earn a $0.15 performance credit for every dollar
of sales that you generate using additional capacity." The credit rate is a dated figure; the live one is on the
Capacity Manager page.

B4. Amazon's public FBA page still uses the older word. `sell.amazon.com/fulfillment-by-amazon`, read 2026-11-10:
"Restock limits help you determine how much inventory you can ship into our fulfillment network … If you exceed your
restock limit, you may see an increase in your storage costs." The Seller Central help page and the 2023
announcement say "capacity limit". Both are recorded; the word a seller uses may be either.

B5. No API read of the limit, the estimates, the usage, a request or a credit. (m) `storage limit`, `capacity
limit`, `reservation fee`, `performance credit`, `capacity manager`, `capacity monitor` return nothing. `capacity`
otherwise appears in other senses (an AWD preferred region that "depends on warehouse capacity availability",
service-slot and carrier capacity), with **one exception the research seat missed**: Finances v0 carries
`CapacityReservationBillingEventList` (`models/finances-api-model/financesV0.json:2043, 3092`), "An event related to
a capacity reservation billing charge", with `TransactionType` ("The transaction type. For example, FBA Inventory
Fee."), `PostedDate`, `Description` and `TransactionAmount`. The release notes of 2023-01-25 announce it: "New
financial event type: `CapacityReservationBillingEventList` allows you to retrieve details related to a Capacity
Reservation Billing charge." So the **money charged** for a capacity reservation is readable after the fact
(`listFinancialEvents`; R12); the request, its reservation fee per cubic foot as bid, its state and the credits earned
are not. The model does not say whether the amount is net of performance credits. (r) The one report that names a
limit is the overage report, after the fact (R2). (n) No other capacity entry in the release notes through the entry
of 2026-11-04. The connector's catalogue has no capacity metric (H2).

### C. Restock Inventory settings, minimum inventory level, the restock block

C1. The inputs a seller sets [official]. "Take advantage of restock recommendation in Send to Amazon", News_Amazon,
sellercentral.amazon.co.uk forum, 2024: "Restock recommendations will be available during the shipment creation
process starting May 9, 2024 … You can also provide SKU-level details for the following parameters to personalize the
recommendations: Lead time / Minimum order quantity / Replenishment frequency / Case pack quantity". The Australian
twin: "This feature gives you SKU-level recommendations on quantity to send in based on the historic performance on
four input factors, being, lead time, minimum order quantity, replenishment frequency and case pack quantity … Note:
These recommendations are a guide o[nly]". Amazon's default values for these inputs were not found on any reachable
page.

C2. What the report carries of them. The *FBA Reports* page (`developer-docs.amazon/sp-api/docs/report-type-values-fba`)
lists for the Restock Inventory report (`GET_FBA_INVENTORY_PLANNING_DATA`'s sibling
`GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`) the columns `Supplier`, `Supplier part no.`, `Recommended
replenishment qty`, `Recommended ship date`, `Recommended action (available in the US store)` and `Unit storage size`,
and **no lead-time, minimum-order, replenishment-frequency or case-pack column**. So the report returns the
recommendation and not the settings that shaped it; two sellers with the same sales and different settings get
different recommendations with nothing in the file to say why. The planning report carries `supplier` and
`fba-minimum-inventory-level`.

C3. Minimum inventory level [official, via IF E, GV43F6S76Y9DHYRH v29]: "Minimum Inventory Level is a
forward-looking metric measured in units". It is Amazon's figure, not a seller setting; the planning report column
`fba-minimum-inventory-level` carries it (R1), and the connector exposes a recommended-MIL metric in days of supply
(H2).

C4. A maximum inventory level exists and blocks replenishment; it is shown on the Restock Inventory page. Seller
post in "AWD to FBA blocked SKUS" (forum, 2024) quoting the Seller Central message: "This product has a maximum
inventory level and exceeds the allowed quantity. View the maximum inventory level on the Restock Inventory page."
[official, via a seller's quotation of the UI]. Bryce_Amazon in "You already have high days of supply for this ASIN
in our fulfillment centers…" (forum, 2024) [official]: "We may temporarily restrict shipment creation for certain
products … These restrictions may apply to hazardous materials exceeding quantity limits, products undergoing
dangerous goods classification, or items with excess inventory levels … We actively monitor inventory levels on a
daily basis and adjust the restrictions accordingly … You can check your FBA Inventory page where inventory health
status and total days of supply based on projected demand is displayed for each product." (m) No `maximum inventory`
field in any model or schema, and neither report page lists such a column.

### D. Automated settings and value-recovery programs

D1. Automated removal of aged fulfillable stock [official]. "Automatic removal of your aging inventory starts April
15", News_Amazon, 2022: "Starting April 15, 2022, the following inventory will be removed automatically, unless you
opt out: Units that have been in fulfillment centers for more than 365 days and that are subject to long-term storage
fees / Units of ASINs that haven't sold in six or more consecutive months and that have been in fulfillment centers
for more than 180 days. You can recover value from these units through liquidation or have your inventory returned to
you by providing a valid return address in your Automated fulfillable inventory settings. If you don't provide a
return address, your inventory will be automatically donated, recycled, or disposed of. On the settings page, select
Disable to opt out … Automatic removals will occur monthly". This is a 2022 text; the current ages are the help
page's (not read).

D2. Unfulfillable stock, UK and EU [official]. "Unfulfillable FBA inventory to be removed after 23 days",
News_Amazon, sellercentral-europe forum, 2024: "Starting September 16, 2024, if you haven't enabled automated
unfulfillable settings in the UK or EU, we will dispose of or donate unfulfillable inventory after 23 days' notice
instead of 30 … Once we create a disposal order after 23 days' notice, it can't be cancelled." For the US a search
result quotes the help page "Remove inventory automatically" (G200678710): "Amazon has enabled the automated
unfulfillable settings and grayed-out the Disable option. It is not possible to opt out of the automated
unfulfillable settings." **[snippet]**; the page itself returned a shell.

D3. Liquidations and Donations defaults, US and Canada [official]. "Enrollment changes for FBA Liquidations and
Donations programs", News_Amazon, sellercentral.amazon.com forum, 2025 (the Canadian forum carries the same text):
"On September 30, 2025, we'll update the enrollment process for the US and Canada … The FBA Liquidations program …
will become the default option for your unsold inventory. If you haven't configured your automated fulfillable
settings and automated unfulfillable settings, you'll automatically be enrolled in the Liquidations program. You can
still opt out of the Liquidations program at any time. The FBA Donations program … will become mandatory. As of
September 30, 2025, you won't be able to opt out. If you've previously opted out, you will be re-enrolled." A search
result shows a later correction by Amazon ("The changes described below apply to the US only. The FBA Liquidations
and Donations programs are unchanged in Canada. Also, the change to the US FBA Donations program has been delayed
until October 30, 2025.") The verifier re-opened both forum threads on 2026-11-10: neither the US thread (published
2025-08-22) nor the Canadian one carries the correction. The correction's full text is on the Sellers Ask Sellers
mirror of the notice (`sellersasksellers.com/t/…/6434`, opened 2026-11-10): "The changes described below apply to the
US only. The FBA Liquidations and Donations programs are unchanged in Canada. Also, the change to the US FBA Donations
program has been delayed until October 30, 2025. We apologize for the erroneous email and any confusion that it may
have caused. The corrected message is as follows: On September 30, 2025, the FBA Liquidations program …" **[official,
via Sellers Ask Sellers]**. So Amazon's forum text and Amazon's corrected e-mail as mirrored disagree; both are
recorded, and the corrected one is the later.

D4. Grade and Resell [official]. "Give returns a second life with FBA Grade and Resell", sell.amazon.com blog,
2025-09-11: "After you enroll in Grade and Resell, eligible FBA returns are inspected to see if they can be relisted
with one of four Used conditions: "Like New," "Very Good," "Good," or "Acceptable.""

D5. Barcode choice [official]. "Commingling practices will end effective March 31, 2026", News_Amazon,
sellercentral.amazon.com forum, late 2025: "The following requirements will go into effect for inventory shipped on
or after March 31, 2026: Brand owners with the Brand Representative selling role in Amazon Brand Registry will no
longer need to apply Amazon barcode stickers to prevent commingling for products that already have manufacturer
barcodes … Resellers (not enrolled in Amazon Brand Registry as a Brand Representative selling role) will now be
required to use Amazon barcode stickers for products even if they have a manufacturer barcode … For products that do
not have a manufacturer barcode, both brand owners and resellers will need to use Amazon Barcode stickers."

D6. What the API reads or changes of D1–D5.
- No operation reads or sets the automated fulfillable or unfulfillable settings, the liquidation or donation
  enrolment, or a return address for automated removals: (m) no hit for `automated removal`, `auto-removal`,
  `donat`, `grade and resell`, `repackag`; (r) no report lists them; (n) no release note.
- Their **results** are readable: removal orders and shipments (R5), liquidation proceeds in Finances v0
  `FBALiquidationEvent` (`LiquidationProceedsAmount`, `LiquidationFeeAmount`; the model says "This event is used only
  in the US marketplace"), the stranded report's `Date-to-take-auto-removal` column (R4).
- Barcode: `getItemEligibilityPreview` (FBA Inbound Eligibility v1, role **AF**) takes program `INBOUND` or
  `COMMINGLING` ("Using the manufacturer barcode for FBA inventory tracking.") and returns reason codes; the model's
  2026 state still names the program `COMMINGLING` after the 2026-03-31 change. Inbound plans carry `labelOwner`
  per item (`AMAZON`, `SELLER`, `NONE`). The account-level barcode preference itself has no read.
- A removal order can be **created** by feed `POST_FLAT_FILE_FBA_CREATE_REMOVAL` (role **AF** on *Role Mappings for
  SP-API Types*); that is a write this file only names.

### E. Reimbursement, manufacturing cost, cases

E1. The policy and the page [official]. "Update to the FBA inventory reimbursement policy", News_Amazon,
sellercentral.amazon.com forum (updated 2024-12-19): "Effective March 10, 2025, we'll reimburse you based on the
product manufacturing cost of the affected inventory. "Manufacturing cost" means your cost to source a product from a
manufacturer, wholesaler, reseller, or produce the item if you are the manufacturer. It excludes costs such as
shipping, handling, customs duties, or other costs." "You can provide your manufacturing costs directly. If you don't
provide your own costs, we'll automatically apply our estimate which you can change when you're ready." "you can view
and manage manufacturing costs in the Inventory Defect and Reimbursement portal starting in late January using a new
Manage Your Manufacturing Cost page." "We now offer automatic reimbursements for items lost in our fulfillment
centers". Practitioners report the start moved to 2025-03-31 [opinion, Seller Labs and others, via search result;
not opened].

E2. The entered cost **is** read back by an API. Data Kiosk economics schema
(`schemas/data-kiosk/analytics_economics_2024_03_15.graphql`), type `PerUnitCost`: `costOfGoodsSold`, "Cost to
manufacture or acquire the product. This value is provided by the seller…", with "Fields in this type will be null if
not provided by the seller." Whether this field is the same number as the one on *Manage Your Manufacturing Cost*, or
the one entered in the Revenue Calculator or the economics page, is not stated in the schema and is an open question.
Role: the *Data Kiosk API* page lists Brand Analytics as the required role of every operation and says "Each field
available with Data Kiosk requires a certain role"; Amazon's changelog entry *Correction: Data Kiosk role
requirements* says "The Economics dataset requires the Selling Partner Insights role" [official, both re-opened
2026-11-10; the two statements disagree]. On the stricter reading this read is outside the five roles, so no position
rests on cx being able to make it. The release notes of 2026-09-30 add: "Updated the Analytics Economics dataset with
deal, coupon, removal, disposal, and fuel fees." The same schema's `economicsSimulation` query takes
`shipmentLeadTime` and `unitPerCarton` as inputs to an AWD or SIPP simulation; they are request inputs with Amazon's
defaults ("Default value is 1 week", "20 units per carton"), not a read of the seller's Restock settings.

E3. Cases. Support API 2025-02-01 (launched 2026-09-30 per the release notes; "available in all Amazon stores",
sellers only): `listCases`, `getCase`, `listContacts`; role **Selling Partner Support (Restricted)**, outside the
five. It returns case id, status (`RESOLVED`, `TRANSFERRED`, `PENDING_MERCHANT_ACTION`, `PENDING_AMAZON_ACTION`),
subject, dates, and contacts by channel with e-mail content, attachments, call notes and chat transcript. It has no
operation that opens a case or files a claim, and `listCases` is itself a POST. The Inventory Defect and
Reimbursement portal's claim state has no read; the result of a claim is the reimbursements report (R6).

### F. Shipment-level pages

F1. In the API, contrary to parts of the starting material. Fulfillment Inbound 2024-03-20 (all operations role
**AF**): `listTransportationOptions` returns, per option, `shippingSolution` (`AMAZON_PARTNERED_CARRIER`,
`USE_YOUR_OWN_CARRIER`), `shippingMode`, `carrier`, a `quote` ("The estimated shipping cost associated with the
transportation option", with `cost`, `expiration`, `voidableUntil`) and a `carrierAppointment`;
`listPlacementOptions` returns each placement option's `fees`, `discounts`, `expiration` and `status`;
`getSelfShipAppointmentSlots` / `scheduleSelfShipAppointment` handle self-ship appointments;
`createMarketplaceItemLabels` "creates labels for a list of MSKUs"; `listItemComplianceDetails` returns tax details
per MSKU; `getDeliveryChallanDocument` is India only. The model states the void window: "The window for Amazon
Partnered Carriers is 24 hours for Small Parcel Delivery (SPD) and one hour for Less-Than-Truckload (LTL)". Amazon's
own plugin adds two limits of the API path: "Case-packed not supported | Use Send to Amazon (STA) in Seller Central"
and that its transport tools work "only … for shipments created via these API tools" (plugin
`fba-inbound-management/references`, read locally).

F2. Not in the API. (m) No hit for `Global Logistics` or `Carrier Central`, or for `remeasur`. **Inbound performance
is in a report, which the research seat missed**: the *FBA Reports* page lists the FBA Inbound Performance Report,
`GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA` (roles **PR or AF**; "Contains inbound shipment problems by product
and shipment. Content updated daily."), with columns `issue-reported-date`, `shipment-creation-date`,
`fba-shipment-id`, `fba-carton-id`, `fulfillment-center-id`, `sku`, `fnsku`, `asin`, `problem-type`,
`problem-quantity`, `expected-quantity`, `received-quantity`, `performance-measurement-unit`, `coaching-level`,
`fee-type`, `currency`, `fee-total`, `problem-level`, `alert-status` (R13). What stays on the page is any
account-level rate or summary the Inbound Performance page shows beyond these rows; no model or report names one. Dangerous-goods documents: the only `SDS` hit is a reason text
in FBA Inbound Eligibility; there is no upload operation. The placement **default** (which inbound placement option
an account prefers) has no read; the options and fees offered for one plan do (F1).

F3. Remeasurement. KJ_Amazon, reply in a sellercentral.amazon.co.uk forum thread (2024) [official]: "how to request
a remeasurement: type "remeasure" into the search box and follow the instructions in the widget. There is a monthly
remeasurement request limit". The help page as read by the listing playbook [official, via IF G11, G6WAEPTECPT2JUH3
v11]: "typically takes 10 days"; an item "can only be remeasured twice within the preceding 60 days"; requests go
"through the Remeasure FBA products and confirm fees widget". The figure of 20 requests a month appears only in a
seller's post and a search result [snippet].

### G. Fees shown on dashboards

G1. In an API. The planning report (R1) carries the low-inventory-level fee's inputs and flags: per the listing
playbook's read of the fee page [official, via IF E], `fba-minimum-inventory-level`,
`fba-inventory-level-health-status`, "Exempted from Low-Inventory-Level fee?", "Low-Inventory-Level fee applied in
current week?" and short- and long-term historical days of supply. Data Kiosk economics names fee types including
`LOW_INVENTORY_LEVEL_FEE`, `STORAGE_UTILIZATION_SURCHARGE` ("Monthly Inventory Storage Fee Storage Utilization
Surcharge") and `PAN_EU_OVERSIZE_FEE`. The overage report (R2) carries the charged overage.

G2. The storage utilization ratio **is in a report** (corrected by the verifier; the research seat had it as
absent). TaylorR_Amazon (forum, 2024) [official]: "The storage utilization ratio is the ratio of your average daily
inventory volume stored divided by the average daily shipped volume during the past 13 weeks." The *FBA Reports* page
lists, for the FBA Storage Fees Report `GET_FBA_STORAGE_FEE_CHARGES_DATA` (roles **PR or AF**; "Contains estimated
monthly inventory storage fees for each ASIN"), the columns `storage_utilization_ratio`,
`storage_utilization_ratio_units`, `base_rate`, `utilization_surcharge_rate`, `avg_qty_for_sus`, `est_vol_for_sus`,
`est_base_msf`, `est_sus`, beside `month_of_charge`, `storage_rate`, `average_quantity_on_hand` and
`estimated_monthly_storage_fee` (R14). The page does not say whether the ratio on a row is the account's ratio
repeated per ASIN or something narrower; that is for a first run. (m) In the models and schemas `utilization` appears
only as the Data Kiosk fee type name above, which is why a schema-only search misses the report column. What has no
API read under this heading: the Fee Explainer and the Revenue Calculator. The survey records that the surcharge ends on 2027-02-01 (not re-read here). The Product Fees API
v0 (`getMyFeesEstimates`, role **PR or PL**) takes no storage input and returns referral, closing and fulfilment
fees [official, via IF G5–G7; request fields `IsAmazonFulfilled`, `OptionalFulfillmentProgram`]: it does not estimate
storage. (m) No hit for `fee explainer` or `revenue calculator`; those are pages, with no operation behind them that
the models show.

### H. Forecasts, the connector, Seller Assistant

H1. No seller-side FBA demand forecast in SP-API. (m) `forecast` appears only in vendor reports and in the
Replenishment (Subscribe & Save) API; the release notes record that `GET_FBA_SNS_FORECAST_DATA` was removed. The
planning and restock reports carry results that rest on Amazon's forecast (days of supply, recommended quantity)
without the forecast itself.

H2. Amazon's Selling Partner connector does expose forecast figures. Plugin 1.0.0, `skills/seller-analytics`, read
locally [official]: tools `analytics_getMetricMetadata` and `analytics_getMetricData` over domains named
`Threep_Inventory`, `Threep_Traffic`, `Threep_Sales`; metrics include `FBA_FORECAST_N7_P80`, `FBA_FORECAST_N30_P80`,
`FBA_FORECAST_N60_P80`, `FBA_INV_VIS_ONHAND_PMEAN_DOS` / `_P90_DOS`, `FBA_INV_VIS_TOTAL_PMEAN_DOS` / `_P90_DOS`,
`FBA_INV_VIS_RESTOCK_ORDER_DATE`, `FBA_INV_RESTOCK_QTY`, `FBA_INV_VIS_RECOMMENDED_MIL_PMEAN_DOS` / `_P90_DOS`,
`FBA_INV_HIL_ZONE`. The skill says "Data is delayed ~2 days", "Note (private beta)" on the `Threep_` names, and "Not
every metric in this catalog is exposed to every seller". The catalogue has no IPI, capacity, storage-utilization or
settings metric. The plugin also states that "there is **no `reports` tool** exposed" on the connector and that it
has no case tool; it reaches Seller Assistant through two create-then-poll tools. The connector is a separate door
from SP-API (OAuth through Seller Central, "limited to the tools your Seller Central roles allow"); the listing
playbook records it as announced at Accelerate 2026 "in Quick and in beta with Claude" for US stores (not re-read).

H3. Seller Assistant answers are AI answers. The listing playbook's `seller-central-only-tools.md` quotes Amazon:
"AI is experimental and can make mistakes…" (not re-read). A capacity or IPI figure a seller relays from Seller
Assistant is that kind of answer, not a page read.

### I. AWD and Supply Chain Services

I1. In the API. AWD 2024-05-09: 21 operations including `listInventory`, `listInboundShipments`,
`listReplenishmentOrders`, `createReplenishmentOrder`, `getReplenishmentOrder`. *Role Mappings for SP-API Operations*
gives `listInventory` and `listInboundShipments` the role **Amazon Warehousing and Distribution** (outside the five;
NA only); the replenishment-order operations are in the model but **not on the role page** as read.

I2. Not in the API. The auto-replenishment switch and its state: (m) no `auto-replenish` hit; `AUTO` in the AWD
model is only the confirmation mode of a manual replenishment order. Amazon describes the feature publicly
(`sell.amazon.com/programs/warehousing`, read 2026-11-10): "Auto-replenishment relies on a proprietary data-science
model that monitors the inventory levels in Prime-ready fulfillment centers and triggers replenishments … If you
leave auto-replenishment enabled, your products are considered in stock and buyable when they're received by AWD, and
we manage your replenishments so you don't have to worry about Fulfillment by Amazon (FBA) capacity limits."
`sell.amazon.com/programs/supply-chain`: "With auto-replenishment, you never have to worry about FBA capacity limits
or low-inventory charges." The AWD "blocked SKUs" tab (C4) and the Supply Chain dashboard have no read.

### J. Account-level blocks

J1. Amazon restricts shipment creation per product for dangerous-goods quantity, dangerous-goods classification in
progress, and excess inventory (C4, Bryce_Amazon). The API shows the symptom at two points: `getItemEligibilityPreview`
(role **AF**) returns an ineligibility reason before a plan, and an inbound plan operation fails with an error. No
operation lists an account's current restrictions or their cause; (m) no hit for `inbound block`, `policy hold`.
`getListingsRestrictions` (role **PL**) answers a different question (whether the account may list the ASIN in a
condition). The Action Items API (launched 2026-10-28; role **Selling Partner Insights**, outside the five) documents
two item types, `AFN_CROSS_STORE_EXPANSION` and `LISTING_SUPPRESSED`, neither a stock block (survey; the
documentation page was re-read for the launch date and role only).

### K. Regional

K1. Pan-EU has an API read. *Inventory Reports* page: `GET_PAN_EU_OFFER_STATUS`, "Pan-European Eligibility: FBA
ASINs", roles Inventory and Order Tracking, **Pricing**, **Amazon Fulfillment**, Direct to Consumer Shipping
(Restricted); stores ES, UK, FR, DE, IT; columns include `Enrol`, `Pan-EU status`, `Enrollment Date`, per-country
offer status and `Date Pan-EU expires`. *Role Mappings for SP-API Types* adds **Product Listing** to that role
list. The account's programme enrolment and the allowed storage countries are
settings with no read found. `GET_REMOTE_FULFILLMENT_ELIGIBILITY` (roles **AF** or Inventory and Order Tracking)
reads per-ASIN Remote Fulfillment eligibility; the Remote Fulfillment enrolment settings have no read found.

### L. Amazon's terms on automated access

L1. Amazon's notice, read first-hand by the verifier [official]. "Business Solutions Agreement updates effective
March 4, 2026", News_Amazon, sellercentral.amazon.com forum, published 2026-02-17
(`…/seller-forums/discussions/t/84e3f6b1-42f7-4cf3-a189-a5cc8d78d838`, opened 2026-11-10): "Effective March 4, 2026,
we're updating the Amazon Services Business Solutions Agreement (BSA) and including a new Agent Policy with new
requirements for AI usage and automated systems". "AI and machine learning restrictions: We'll add BSA restrictions
on using Amazon materials or services for AI development with enhanced protection against reverse engineering."
"Agent restriction and new Agent Policy: We'll add requirements for the use of automated software or AI agents to
access Amazon Services, and we may restrict their access in certain instances under the BSA and new Agent Policy. All
AI agents must do the following: Clearly identify themselves as automated systems / Comply with the new Agent Policy
at all times / Cease access if Amazon requests". "your continued use of Selling Services after the effective date
constitutes acceptance of these changes." The notice links to the agreement's change page and to the Agent Policy
page; both are Seller Central pages that return a script shell (the Business Solutions Agreement, help id G1791,
tried in both URL forms on 2026-11-10), so **the agreement's and the policy's own text were not read**. The section
numbers come from a practitioner [opinion: Canopy Management, opened 2026-11-10]: "a new Agent Policy, introduced in
Section 19 of the agreement" and "new Section 4.2 restricts using Amazon materials or services to develop or improve
AI and machine learning models"; Canopy's reading that "standard fulfillment automation likely qualifies" as an Agent
is Canopy's. PPC Land (opened 2026-11-10) restates the notice. The notice does not say how an agent identifies
itself, and does not say whether a seller's own agent calling SP-API through an authorised application is an "Agent"
in the policy's sense.

## What practitioners add

P1. Gerpgo (积加) reads capacity from Seller Central through a seller sub-account, not through the API and not, on
its own page, through a browser extension. Help page "FBA库容" (`help.jijiaerp.com/docs/cOmfrT3w`, modified
2025-03-20, opened 2026-11-10): "抓取相应亚马逊后台FBA库容统计，每天8点，12点，16点、21点更新一次" (it scrapes the
FBA capacity figures from the Amazon back end, refreshed at 08:00, 12:00, 16:00 and 21:00 each day) and "如果子账号
登录正常，但是库容同步有问题，需要确认子账号是否授权了管理库容的权限" (if the sub-account logs in normally but
capacity does not sync, check that the sub-account was granted the manage-capacity permission). The page still
describes six storage types and ASIN-level inbound limits, wording of the pre-2023 system. [opinion: Gerpgo]

P2. Browser extensions that read Seller Central for an ERP exist as a class. 易仓 (Eccang)'s Chrome extension
describes itself: "进入Amazon卖家后台，即可自动抓取交易和流量数据" (enter the Amazon seller back end and it
captures transaction and traffic data automatically) [snippet; the store page did not render]. Search found no
statement that a named extension reads capacity or IPI. [opinion: Eccang]

P3. Gerpgo says of partnered carriers and AGL in its Send to Amazon flow "(亚马逊未提供API)" (Amazon provides no
API), per the survey's read of Gerpgo's help (not re-read). The 2024-03-20 inbound model returns partnered-carrier
options with quotes (F1); `Global Logistics` has no hit. So the statement holds for AGL and not, on the model's
evidence, for partnered-carrier quotes. [opinion: Gerpgo; the comparison is F1]

P4. IPI threshold figures in vendor blogs disagree: 400 (Seller Labs, SellerApp), 350 from 2026-01-01 (Nova
Analytics, 2025-12-04: "Q1 2026 capacity limits announced with new IPI threshold of 350 (down from 400)" and
"Capacity Manager bidding opens January 2 for additional space at $0.35-$0.75/cubic foot"). None cites an Amazon page
that could be opened; Nova's quarterly framing does not match Amazon's monthly system (B1). [opinion: each named]

P5. My Amazon Guy (2025) reports further account settings under the FBA settings menu ("returnless resolutions,
item evaluation, and … the ownership of damaged inventory") and that "The defaults are not always optimized for a
seller's profitability or control." [opinion: My Amazon Guy]

P6. Capacity Manager in practice, from the listing playbook's practitioner notes (eComEngine, AMZ Prep; not
re-read): requests can stay pending until they expire, and limits were cut for some accounts ahead of Q4. A seller
in Amazon's forum (2024): "We recently saw a significant decline in our capacity limit for November, but it doubles
again in December." [opinion: each named]

## Published research

None found on this subject. The question here is what a platform exposes through which door; the search turned up
vendor and practitioner writing only.

## Stable enough for a skill

- The score, the limit, the estimates, the usage and Capacity Manager requests live on Seller Central pages with no
  API read; the charge for a granted reservation is a Finances v0 event (A5, B5).
- The storage utilization ratio is a column of the FBA Storage Fees report, and inbound problems with their coaching
  level and fee are rows of the FBA Inbound Performance report (G2, F2).
- The Restock report returns a recommendation and not the lead time, minimum order quantity, replenishment
  frequency or case pack that shaped it (C1, C2).
- Automated-removal, liquidation, donation and barcode settings have no read; their results do (D6).
- The limit's announcement is by Capacity Monitor and e-mail, monthly, with two further months estimated (B1, B2).
- Partnered-carrier quotes, placement fees, self-ship appointments and item labels are in the inbound API (F1).
- A seller-provided cost of goods is a field of Data Kiosk economics, under a role Amazon's pages disagree on (E2).
- Pan-EU per-ASIN status has a report (K1).
- A figure relayed from Seller Assistant is an AI answer (H3).
- How a seller's page fact reaches cx: a file kept as downloaded, else a screenshot, else typed, each with its
  as-of date (the listing playbook's established method; see *Overlap*).

## What cx must read at run time

These are the proxies. Roles are from *Role Mappings for SP-API Operations* (page updated 2026-10-28) and *Role
Mappings for SP-API Types* (page updated 2026-09-09), read as Markdown on 2026-11-10.

R1. `GET_FBA_INVENTORY_PLANNING_DATA`. Role **AF** only. Carries `fba-minimum-inventory-level`,
`fba-inventory-level-health-status`, the low-inventory-level fee flags, historical days of supply, age buckets,
`sell-through`, `estimated-excess-quantity`, `storage-type`, `storage-volume`, `supplier`. "Not available in the NL,
PL, SE, or BE stores"; "Attributes vary by store". Proxy for: the Inventory Health and FBA Inventory pages, the LIL fee dashboard. Pitfall: it has the
per-SKU inputs of excess and sell-through, not the account's IPI score, and nobody outside Amazon has the formula.

R2. `GET_FBA_OVERAGE_FEE_CHARGES_DATA`. Role **AF** only. Columns `charged_date`, `country_code`, `storage_type`,
`charge_rate`, `storage_usage_volume`, `storage_limit_volume`, `overage_volume`, `volume_unit`, `charged_fee_amount`,
`currency_code`. Proxy for: the capacity limit. Pitfall: a row exists only after an overage was charged, so an
account within its limit gets no limit from it; and overage is counted on on-hand stock while the shipment block
counts on-hand plus inbound (B1, B2).

R3. `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`. Role **AF or PR**. "All stores except India (IN)". Proxy for:
the Restock Inventory page. Pitfall: C2; `Recommended action` is US only; `Unit storage size` is "available in the
US, CA, UK, DE, FR, IT, and ES stores".

R4. `GET_STRANDED_INVENTORY_UI_DATA`. Role **AF or PR**. Carries `Date-to-take-auto-removal`. Proxy for: Fix
stranded inventory and the effect of the stranded auto-removal setting. Pitfall: the date shows what will happen,
not which setting the seller chose.

R5. `GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA` and `GET_FBA_FULFILLMENT_REMOVAL_SHIPMENT_DETAIL_DATA`. Role
**AF or PR**. Carry `order-source`, `order-type`, `order-status`, `disposition`, quantities, `removal-fee`;
`removal-order-type`. Proxy for: automated removals, liquidations, disposals after the fact. Pitfall: the page lists
the columns, not their values; whether `order-type` or `order-source` distinguishes an automated order, a
liquidation or a donation is for a first run. `GET_FBA_RECOMMENDED_REMOVAL_DATA` (role **AF or PR**) is the proxy
for what the next automated removal would take.

R6. `GET_FBA_REIMBURSEMENTS_DATA`. Role **AF or PR**. Columns include `approval-date`, `reimbursement-id`,
`case-id`, `reason`, `amount-per-unit`, `quantity-reimbursed-cash`, `quantity-reimbursed-inventory`. Proxy for: the
reimbursement portal's outcomes; `case-id` ties a row to a case without the restricted Support role. Finances
2024-06-19 `listTransactions`, role **FA**, carries the money side; Finances v0 `listFinancialEvents` (role **FA**;
the role page also lists Amazon Fulfillment "(NA, FE only)") returns `FBALiquidationEventList` (US only), liquidation
proceeds and fees, and removal events whose `TransactionType` the model documents with the one value
`WHOLESALE_LIQUIDATION`.

R7. `getItemEligibilityPreview`, FBA Inbound Eligibility v1. Role **AF**. Proxy for: a per-ASIN inbound block and
the manufacturer-barcode eligibility. Pitfall: it answers for one ASIN and one program at a time and names a reason
code, not the account restriction behind it.

R8. Fulfillment Inbound 2024-03-20 `listTransportationOptions`, `listPlacementOptions`,
`getSelfShipAppointmentSlots`, `listInboundPlans`, `getShipment`. Role **AF**. These are first-hand, not proxies,
for a plan created through the API; quotes and placement options expire (`expiration`). Pitfall: F1's two limits
from Amazon's plugin.

R9. `GET_PAN_EU_OFFER_STATUS`. Role **AF, PR or PL** (also Inventory and Order Tracking, Direct to Consumer
Shipping).
ES, UK, FR, DE, IT stores. `GET_REMOTE_FULFILLMENT_ELIGIBILITY`: role **AF** (or Inventory and Order Tracking).

R10. `getInventorySummaries`, FBA Inventory v1. Role **AF or PL**. Proxy for usage in units only; capacity is
measured in volume, and no API returns the account's volume used against its limit.

R11. `getMyFeesEstimates`, Product Fees v0. Role **PR or PL**. Not a storage estimate (G2).

R12 (gap fill 2026-11-10). Finances v0 `listFinancialEvents`, `CapacityReservationBillingEventList`. Role **FA**
(the role page also lists Amazon Fulfillment for NA and FE, and Account Information Service Provider for the EU).
Fields `TransactionType`, `PostedDate`, `Description`, `TransactionAmount`. Proxy for: what a granted Capacity
Manager reservation cost. Pitfall: an event exists only after a charge posts; it carries no storage type, volume,
period or bid, and the model does not say whether performance credits are netted. Whether Finances 2024-06-19
`listTransactions` carries the same charge, and under which transaction type, is not stated in its model.

R13 (gap fill 2026-11-10). `GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA`, FBA Inbound Performance Report. Role
**AF or PR**. Request only; "Content updated daily". Columns in F2. First-hand for inbound problems per shipment and
product (`problem-type`, `coaching-level`, `fee-total`, `alert-status`). Pitfall: the page lists columns, not their
values.

R14 (gap fill 2026-11-10). `GET_FBA_STORAGE_FEE_CHARGES_DATA`, FBA Storage Fees Report. Role **AF or PR**. "This
report can be requested or scheduled." Carries `storage_utilization_ratio`, `utilization_surcharge_rate`, `est_sus`,
`month_of_charge` per ASIN and fulfilment centre. First-hand for the ratio a month's storage fee was charged at.
Pitfall: it is by month of charge, so it shows the ratio after the fact; G2's open point on what the per-row ratio
is.

R15 (gap fill 2026-11-10). Fulfillment Outbound 2020-07-01 `getFeatures`, `getFeatureInventory`, `getFeatureSKU`.
Role **AF**. "Returns a list of features available for Multi-Channel Fulfillment orders in the marketplace you
specify, and whether the seller for which you made the call is enrolled for each feature" (example features
`BLANK_BOX`, `BLOCK_AMZL`, with `sellerEligible`). First-hand for which multi-channel features an account has; the
three operations are absent from the 2026-07-04 version of the model, which has nine order operations only.

## Reads that need a role outside the five

Nothing above is built on these.

- **Selling Partner Insights**: Data Kiosk economics, if the changelog's statement is the true one (E2), which
  would open the seller-entered `costOfGoodsSold` and the fee types of G1; Action Items (`listActionItems`,
  `getActionItem`), which today document no stock item; `GET_V2_SELLER_PERFORMANCE_REPORT`; notification
  `ACCOUNT_STATUS_CHANGED`.
- **Selling Partner Support (Restricted)**: Support API `listCases`, `getCase`, `listContacts` (E3): the case log
  with its correspondence; it reads cases and opens none.
- **Amazon Warehousing and Distribution**: AWD `listInventory`, `listInboundShipments` (NA only); the
  replenishment-order operations' role is unstated on the page (I1).
- **Inventory and Order Tracking**: an alternative role for `GET_PAN_EU_OFFER_STATUS`,
  `GET_REMOTE_FULFILLMENT_ELIGIBILITY` and the Replenishment API's metrics; it opens nothing the five do not already
  open for those reads.

## Only in Seller Central

Each row: the item; what a seller could hand over; the proxy; how absence was established. "Download" states only
what a reachable Amazon source confirmed; where none did, the cell says so, and the handoff is a screenshot or typed
figures with the date seen.

| Item | What a seller would paste or export for cx | API proxy and role | Evidence no API carries it |
|---|---|---|---|
| IPI score, its four parts, the account's threshold and measurement week | Inventory Performance dashboard: screenshot or typed score and date. No download confirmed. | Per-SKU inputs in R1 (AF) | (m) (r) (n); sales-and-traffic schema has only `totalFbaInventoryValue`; connector catalogue has none (A5) |
| Capacity limit this month, two months' estimates, usage by storage type | Capacity Monitor on the FBA dashboard, or Amazon's monthly e-mail. No download confirmed. | R2 after an overage (AF); units only in R10 (AF or PL) | (m) (r) (n) (B5) |
| Capacity Manager requests, reservation fee as bid, performance credits | Capacity Manager page | The posted charge only: Finances v0 `CapacityReservationBillingEventList` (FA), R12 | (m): no `reservation fee`, `performance credit`; the event has an amount and a description, no request (B5) |
| Restock settings: lead time, minimum order quantity, replenishment frequency, case pack | The seller's own values, typed, or the SKU settings as shown | R3 returns the recommendation only (AF or PR) | (r): column list (C2); (m) |
| Maximum inventory level and the per-product restock block | Restock Inventory page; the block message | R7 (AF) shows a reason per ASIN | (m) (r) (C4) |
| Automated fulfillable and unfulfillable settings; liquidation and donation enrolment; return address | Settings → Fulfillment by Amazon, typed or screenshot | Results in R4, R5, R6 | (m) (r) (n) (D6) |
| Barcode preference | Same settings page | `getItemEligibilityPreview` `COMMINGLING` (AF); `labelOwner` in plans (AF) | (m): no account-level field |
| Grade and Resell, Liquidations, Donations dashboards | The dashboards; no download confirmed | Removal reports (AF or PR); `FBALiquidationEvent` (FA, US only) | (m) (r): no report names these programs |
| Manage Your Manufacturing Cost; claim state in the Inventory Defect and Reimbursement portal | The cost file or page; claim status typed | Outcomes in R6; `costOfGoodsSold` in Data Kiosk economics (role disputed, E2) | (m): no claim object outside the Support API |
| Case log | — | Support API, restricted role | It is in an API, outside the five (E3) |
| Remeasurement request and its result | The widget's confirmation; the result shows later in catalog dimensions and fee reports | None for the request | (m): no `remeasur` |
| AGL bookings; Carrier Central appointments; dangerous-goods document upload; placement default | The pages | Plan-level options and quotes in R8 (AF) | (m): no `Global Logistics`, `Carrier Central`; no upload operation (F2) |
| Inbound performance page | — | In a report: `GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA` (AF or PR), R13 | It is in an API (F2); only an account-level summary, if the page shows one, has no read |
| Amazon's demand forecast per SKU | — | Results only in R1, R3; the connector exposes `FBA_FORECAST_N7/N30/N60_P80` (H2) | (m): `forecast` only in vendor and Subscribe & Save models |
| Storage utilization ratio | — | In a report: `storage_utilization_ratio` in `GET_FBA_STORAGE_FEE_CHARGES_DATA` (AF or PR), R14 | It is in an API, by month of charge (G2) |
| Fee Explainer; Revenue Calculator with storage | The page's output | R11 has no storage (PR or PL); Fee Preview and economics datasets carry fees charged or previewed | (m) |
| AWD auto-replenishment switch, blocked-SKU tab, Supply Chain dashboard | The AWD pages | AWD API (role outside the five) | (m): no `auto-replenish` (I2) |
| Account restrictions and their cause | The notice or Account Health page | R7 symptom (AF) | (m) (J1) |
| Pan-EU and Remote Fulfillment enrolment settings | The programme pages | Per-ASIN status in R9 | No settings read found; per-ASIN read exists (K1) |
| Multi-channel fulfilment settings | The MCF settings page | Feature enrolment per marketplace: `getFeatures` (AF), R15 | (m): no other settings read |

Not established in this session, either way, because no Amazon page on them could be read: whether Seller Central
offers a native scheduled e-mail delivery of fulfilment reports (search found only third-party schedulers and the
notification preference for report availability; the Reports API has `createReportSchedule`, whose roles include AF,
FA, PR and PL; and the *FBA Reports* page marks some reports, the Storage Fees report among them, "can be requested or
scheduled", which is the API's schedule, not Seller Central's). A search on 2026-11-10 returned Amazon's help page
*Order Reports* (G651) as saying recurring order reports can be scheduled, and an EcommerceBytes item saying Amazon
added scheduling to the FBA fulfilment reports page; both **[snippet]**, neither opened. Also not established: the
Outlet page (`outlet` has no hit in any seller model, report page or release note, so there is no read; what the page
shows is unread); repackaging and refurbishment settings (same: no hit, page unread); the aged inventory page beyond
the planning report; which Seller Central pages offer a download and in what format (no reachable Amazon page says).
Multi-channel fulfilment has one read, R15.

### Overlap with the listing playbook

`cx-listing-playbook/research/method/seller-central-only-tools.md` (read in full; its pages were read by that seat
on 2026-10-14) covers listing tools only: Manage Your Experiments, listing-quality queues, Seller Assistant, A+
analytics, Business Reports, Voice of the Customer, the Category Listings Report. It names no stock item, so no fact
here repeats one there. What carries over is its method: a page fact reaches cx as a file kept as downloaded, else a
screenshot, else typed, with the date it was true; Seller Assistant's answers are AI answers Amazon says to verify;
and the Selling Partner connector is a separate, beta door. Its Data Kiosk schema list and this file's agree.

## The seller's choices

- Whether to give cx the page facts at all, and how fresh: a capacity limit typed in the fourth week of the month
  is the month's; an IPI score moves weekly.
- Which role set the door holds: adding Selling Partner Insights or the restricted Support role would open the
  reads listed above; that is an application and consent decision, not a research one.
- Whether to enter manufacturing cost or leave Amazon's estimate (E1); it changes what a lost unit is reimbursed
  at, and what `costOfGoodsSold` returns.
- The automated settings themselves (return, liquidate, dispose; opt-out where one exists) and the barcode route
  where the seller is a brand owner (D1–D5).
- The Restock inputs (C1): leaving Amazon's defaults or entering their own changes the recommendation the report
  returns.
- Whether to bid for capacity, and at what reservation fee (B3).
- Whether an ERP reads Seller Central through a sub-account or extension on their behalf, under the Agent Policy
  (L1, P1, P2).

## Open questions

Help pages not read first-hand (all returned a script shell): FBA capacity limits GAFNWEYTJUV2GBFC; Inventory
performance G202174810; IPI FAQ GZJF4DY2W6MERBAL; FBA dashboard GPDFH32J7DYNM378; Q4 playbook G4QH4XCRWUXRJBLY;
Remove inventory automatically G200678710; FBA Donations programme VCFMKLPUTBXE7L5; FBA Liquidations terms
G201507460; stranded inventory G201436600 and GKQ8DGGU529BJJ7E; low-inventory-level fee GV43F6S76Y9DHYRH; storage
utilization surcharge G3EDYEF6KUCFQTNM; Fee and Economics Preview GQNVDV46U9JQ25HY; remeasurement G6WAEPTECPT2JUH3;
and, with ids not found, Capacity Manager, Restock Inventory settings, Automated fulfillable inventory removal, FBA
inventory required removals, Value-recovery services, FBA barcode choice and labeling FAQ, Pan-European FBA
enrolment, Remote Fulfillment, the Business Solutions Agreement and its Agent Policy.

For a first run on a real account, or for the office:

1. Is there a current numeric IPI threshold on the dashboard, for which marketplaces, and with what measurement
   week? Vendor figures conflict (P4).
2. Which pages offer a download (Capacity Monitor, Inventory Performance, Restock settings, Manage Your
   Manufacturing Cost, the value-recovery dashboards), and in what format?
3. Do `order-type` / `order-source` in the removal reports tell an automated removal, a liquidation and a donation
   apart? Amazon's page lists the columns and no values. SellerSpace's help (search result, not opened) lists four
   removal order types, "Return, Dispose, Donate, and Liquidate" [snippet; opinion: SellerSpace]; none names a value
   for an Amazon-initiated order.
4. Is `costOfGoodsSold` in Data Kiosk economics the Manage Your Manufacturing Cost figure, and which role does the
   dataset in fact require?
5. Amazon's corrected Liquidations and Donations message (US only; Donations from 2025-10-30) is read only through a
   mirror, and Amazon's own forum threads still carry the uncorrected text (D3); what do the help pages
   VCFMKLPUTBXE7L5 and G201507460 say today?
6. Is `CapacityReservationBillingEvent`'s amount net of performance credits, does a credit post as its own event,
   and does Finances 2024-06-19 carry the same charge (B5, R12)?
6a. Is `storage_utilization_ratio` in the Storage Fees report the account's ratio repeated on each row (G2)?
7. Does Seller Central schedule reports by e-mail natively?
8. Which roles do the AWD replenishment-order operations need?
9. The exact text of the Agent Policy, and what it requires of a seller's own agent reading Seller Central pages.
10. Does the connector's `Threep_Inventory` forecast reach a given seller, and for which stores?

## Positions

- **P-seller-central-only-1.** No SP-API operation, report or Data Kiosk dataset returns an account's Inventory
  Performance Index score, its four parts as account measures, or its threshold; the score is on the Inventory
  Performance dashboard, and the planning report's `sell-through` and `estimated-excess-quantity` are per-SKU figures.
  Sources: models and schemas at `db2936aa`, *FBA Reports* and *Inventory Reports* pages, release notes, read
  2026-11-10; §A5.
- **P-seller-central-only-2.** Amazon's historical IPI thresholds were tied to a named measurement week and a later
  effective date (400 from week 20 of 2020 in the UK and EU; 450 in week 51 of 2020 for 2021-01-01 in the US); these
  belong to the quarterly storage-limit system that ended on 2023-03-01, and no Amazon page read on 2026-11-10 states
  a current number. Sources: News_Amazon forum announcements; §A3, §A4.
- **P-seller-central-only-3.** Since 2023-03-01 Amazon sets one monthly FBA capacity limit per storage type, in
  volume, announced through the Capacity Monitor in Seller Central and an e-mail, with estimates for the two following
  months; the limit, the estimates and the usage against them have no API read. Sources: News_Amazon "Simplifying FBA
  capacity limits for your business"; models and report pages; §B1, §B5.
- **P-seller-central-only-4.** Amazon's pages disagree on when the monthly limit is announced: "the third full week
  of each month" (announcement of January 2023) and "typically … the fourth week of the month" (help page
  GAFNWEYTJUV2GBFC as read 2026-10-14 by the listing playbook, not re-read). Sources: as named; §B2.
- **P-seller-central-only-5.** The only report that names a capacity limit is `GET_FBA_OVERAGE_FEE_CHARGES_DATA`
  (`storage_limit_volume`, role Amazon Fulfillment), which Amazon describes as overage fees for inventory "that
  exceeds your storage limits"; a row therefore presupposes an overage. Sources: *FBA Reports* page, *Role Mappings
  for SP-API Types*; §R2.
- **P-seller-central-only-6.** Amazon states that overage fees count on-hand inventory "not including open
  shipments", while the limit that blocks new shipments counts on-hand inventory plus shipments created and not yet
  arrived. Sources: News_Amazon 2023 announcement; help page via the listing playbook (not re-read); §B1, §B2.
- **P-seller-central-only-7.** Capacity Manager requests name a maximum reservation fee and are granted "starting
  with the highest reservation fee per cubic foot"; performance credits "are designed to offset up to 100%" of the
  fee; the requests, bids and credits have no API read, and the credit rate ($0.15 per dollar of sales in a 2024
  Amazon forum reply) is a dated figure whose live value is on the Capacity Manager page. Sources: News_Amazon 2023;
  TaylorR_Amazon; models; §B3, §B5.
- **P-seller-central-only-8.** Amazon's restock recommendation takes four seller inputs per SKU (lead time, minimum
  order quantity, replenishment frequency, case pack quantity); the Restock Inventory report's documented columns
  carry the recommendation and the supplier fields and none of the four. Sources: News_Amazon forum notices (UK, AU),
  *FBA Reports* page; §C1, §C2.
- **P-seller-central-only-9.** Amazon restricts shipment creation per product for excess inventory and for
  dangerous-goods reasons and adjusts the restrictions daily; the maximum inventory level is shown on the Restock
  Inventory page and in no API, where only an eligibility reason or a plan error shows. Sources: Bryce_Amazon forum
  reply; the UI message as quoted by a seller; models; §C4, §J1.
- **P-seller-central-only-10.** The automated fulfillable and unfulfillable removal settings, the Liquidations and
  Donations enrolment and the barcode preference have no API read or write; what they caused is readable in the
  removal order and shipment reports (role Amazon Fulfillment or Pricing), the stranded report's
  `Date-to-take-auto-removal`, and Finances v0 `FBALiquidationEvent` (US only; role Finance and Accounting). Sources:
  models, *FBA Reports* page, role pages; §D6.
- **P-seller-central-only-11.** Amazon's forum notice of 2025-08-22 says that from 2025-09-30, in the US and Canada,
  a seller who has not configured automated settings is enrolled in FBA Liquidations by default with an opt-out and
  FBA Donations becomes mandatory; Amazon's corrected message, read only through the Sellers Ask Sellers mirror, says
  the changes apply to the US only, Canada is unchanged, and the US Donations change was delayed to 2025-10-30.
  Sources: News_Amazon forum notice (US and CA threads, uncorrected as of 2026-11-10); Sellers Ask Sellers mirror;
  §D3.
- **P-seller-central-only-12.** For inventory shipped on or after 2026-03-31, Amazon lets Brand Registry brand owners
  with the Brand Representative role use manufacturer barcodes without Amazon stickers and requires Amazon barcode
  stickers from resellers; the SP-API eligibility program is still named `COMMINGLING` in the models of 2026-10-29.
  Sources: News_Amazon forum notice; `fbaInbound.json`; §D5, §D6.
- **P-seller-central-only-13.** From 2025-03-10 (as announced on Amazon's forum, updated 2024-12-19) Amazon reimburses
  lost or damaged FBA inventory at the manufacturing cost, which excludes shipping, handling and customs duties, using
  its own estimate unless the seller enters a cost on the Manage Your Manufacturing Cost page; the outcome of a
  reimbursement is in `GET_FBA_REIMBURSEMENTS_DATA` (role Amazon Fulfillment or Pricing), whose `case-id` column names
  the case. Sources: News_Amazon forum notice; *FBA Reports* page; §E1, §R6.
- **P-seller-central-only-14.** Removed by the verifier: it rested wholly on the Support API, whose role (Selling
  Partner Support, restricted) is outside the five. The fact stays in §E3 and in *Reads that need a role outside the
  five*.
- **P-seller-central-only-15.** Partnered-carrier options with quotes, placement options with fees, self-ship
  appointment slots and item labels are returned by the Fulfillment Inbound API 2024-03-20 (role Amazon Fulfillment)
  for plans created through it; Amazon Global Logistics bookings, Carrier Central, remeasurement requests and
  dangerous-goods document upload appear in no model. Sources: `fulfillmentInbound_2024-03-20.json`, role page; §F1,
  §F2.
- **P-seller-central-only-16.** A remeasurement is requested through a Seller Central widget and Amazon states there
  is a monthly request limit; no API files or tracks one. Sources: KJ_Amazon forum reply; help page via the listing
  playbook (not re-read); models; §F3.
- **P-seller-central-only-17.** The Product Fees API (role Pricing or Product Listing) takes no storage input; Amazon
  defines the storage utilization ratio as average daily volume stored over average daily volume shipped in the past
  13 weeks, and the FBA Storage Fees report `GET_FBA_STORAGE_FEE_CHARGES_DATA` (role Amazon Fulfillment or Pricing)
  lists `storage_utilization_ratio` and `utilization_surcharge_rate` among its columns, by month of charge. Sources:
  TaylorR_Amazon; *FBA Reports* page; listing playbook's read of the fees model (not re-read); §G2, §R14.
- **P-seller-central-only-18.** SP-API has no seller-side FBA demand forecast; Amazon's Selling Partner connector
  lists forecast metrics (`FBA_FORECAST_N7_P80`, `N30`, `N60`) and inventory-health metrics in a private-beta
  catalogue, with data "delayed ~2 days", no IPI or capacity metric, and no reports tool. Sources: models; plugin
  1.0.0 `skills/seller-analytics`; §H1, §H2.
- **P-seller-central-only-19.** No model, report or release note carries AWD's auto-replenishment setting or its
  blocked-SKU list; the AWD API itself needs a role outside the five. Sources: AWD model, role page,
  sell.amazon.com; §I1, §I2.
- **P-seller-central-only-20.** Pan-EU per-ASIN enrolment status is readable (`GET_PAN_EU_OFFER_STATUS`; roles
  include Pricing, Product Listing and Amazon Fulfillment; ES, UK, FR, DE, IT), and per-ASIN Remote Fulfillment
  eligibility is readable for US offers (`GET_REMOTE_FULFILLMENT_ELIGIBILITY`; role Amazon Fulfillment); no read of
  either programme's account settings was found. Sources: *Inventory Reports* and *FBA Reports* pages, role page;
  §K1.
- **P-seller-central-only-21.** Gerpgo (积加) states that its capacity report is scraped from Seller Central four
  times a day through a seller sub-account holding the manage-capacity permission (their practice). Source: Gerpgo
  help page "FBA库容", modified 2025-03-20; §P1.
- **P-seller-central-only-22.** Amazon's notice of 2026-02-17 says that from 2026-03-04 the Business Solutions
  Agreement carries an Agent Policy with "requirements for the use of automated software or AI agents to access Amazon
  Services", that all AI agents "Clearly identify themselves as automated systems", comply with the Agent Policy and
  "Cease access if Amazon requests", and that Amazon "may restrict their access"; the agreement's and the policy's own
  text were not read. Sources: News_Amazon "Business Solutions Agreement updates effective March 4, 2026"; §L1.
- **P-seller-central-only-23.** (added by the verifier) Inbound shipment problems are readable per shipment and
  product in the FBA Inbound Performance Report, `GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA` (role Amazon
  Fulfillment or Pricing), whose columns include `problem-type`, `coaching-level`, `fee-type`, `fee-total` and
  `alert-status`. Sources: *FBA Reports* page, *Role Mappings for SP-API Types*; §F2, §R13.
- **P-seller-central-only-24.** (added by the verifier) Finances v0 returns `CapacityReservationBillingEventList`,
  "An event related to a capacity reservation billing charge", with a transaction type, posted date, description and
  amount (role Finance and Accounting); it is the charge after the fact and carries no request, bid, volume or
  storage type. Sources: `financesV0.json`; release notes of 2023-01-25; role page; §B5, §R12.
- **P-seller-central-only-25.** (added by the verifier) Fulfillment Outbound 2020-07-01 `getFeatures` (role Amazon
  Fulfillment) returns the Multi-Channel Fulfillment features of a marketplace and whether the seller is enrolled in
  each; the operation is not in the 2026-07-04 version of the model. Sources: `fulfillmentOutbound_2020-07-01.json`,
  `fulfillmentOutbound_2026-07-04.json`, role page; §R15.

The seat's own (no source; enters no skill):

- The page facts a stock skill most needs from the seller are few: the month's capacity limit and estimates per
  storage type, the IPI score, the four Restock inputs where they differ from default, and the automated settings.
  Everything else has a workable proxy.
- A typed capacity limit can be cross-checked against `storage_limit_volume` only in a month with an overage, so in
  practice it cannot be checked.
- The connector, not SP-API, is where Amazon is putting its forecast figures; if it leaves beta it changes this
  file more than any SP-API release would.
- Gerpgo's wording (six storage types, ASIN limits) suggests its page predates 2023; what it scrapes today is
  unverified.

## Pages read

| Page | URL | Date read | Tag | Reached how / unreachable |
|---|---|---|---|---|
| Simplifying FBA capacity limits for your business (News_Amazon) | https://sellercentral.amazon.com/seller-forums/discussions/t/27d116c68a0af696c2abce9f47d67131 | 2026-11-10 | official | GET |
| Ask Amazon: Simplified FBA capacity limits Q&A (Kelly_Amazon) | https://sellercentral.amazon.com/seller-forums/discussions/t/3c9cef3c-530b-4846-a3b3-a855ed62f241 | 2026-11-10 | official | GET |
| Refresher: FBA Capacity Limits & How They Work (Dominic_Amazon) | https://sellercentral.amazon.com/seller-forums/discussions/t/7dd1b421-5863-46c8-a88a-ba2cdcabad94 | 2026-11-10 | official | GET, read in part |
| FBA Capacity Limits and Fees (TaylorR_Amazon reply) | https://sellercentral.amazon.com/seller-forums/discussions/t/2b80fe3a-a0b0-4f7a-aa5d-269de36ed948 | 2026-11-10 | official (reply), opinion (seller) | GET |
| Amazon announces new streamlined FBA capacity management system | https://sell.amazon.com/blog/announcements/fba-capacity | 2026-11-10 | official | GET |
| Inventory Performance Index threshold will change to 450 | https://sellercentral.amazon.com/forums/t/inventory-performance-index-threshold-will-change-to-450/755699 | 2026-11-10 | official | GET |
| IPI threshold change for FBA storage limits and new overage fee | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/befc961d25121b91d2136392756ac66a | 2026-11-10 | official | GET |
| Take advantage of restock recommendation in Send to Amazon | https://sellercentral.amazon.co.uk/seller-forums/discussions/t/42f1aae6-db61-4198-be0f-80c9408e4caa | 2026-11-10 | official | GET |
| New Fulfilment by Amazon restock recommendation feature in Send to Amazon | https://sellercentral.amazon.com.au/seller-forums/discussions/t/6358ccd6-2bb5-41bb-8fa4-90ad98948e7f | 2026-11-10 | official | GET |
| Automatic removal of your aging inventory starts April 15 | https://sellercentral.amazon.com/seller-forums/discussions/t/7f56696bda4cdf112a856f319860e02b | 2026-11-10 | official | GET |
| Unfulfillable FBA inventory to be removed after 23 days | https://sellercentral-europe.amazon.com/seller-forums/discussions/t/b3d3cac6-0736-4c6c-9d64-8f21acb3eb2d | 2026-11-10 | official | GET |
| Enrollment changes for FBA Liquidations and Donations programs (US) | https://sellercentral.amazon.com/seller-forums/discussions/t/8a402163-2acc-41b0-b4ea-fe6c9b763856 | 2026-11-10 | official | GET |
| Enrolment changes for FBA Liquidations and Donations programs (CA) | https://sellercentral.amazon.ca/seller-forums/discussions/t/faf1e3b4-9d24-4bda-97ec-0928f92e478f | 2026-11-10 | official | GET |
| Commingling practices will end effective March 31, 2026 | https://sellercentral.amazon.com/seller-forums/discussions/t/106d0747-e5c6-44d8-86f3-7669f11238fe | 2026-11-10 | official | GET |
| Update to the FBA inventory reimbursement policy | https://sellercentral.amazon.com/seller-forums/discussions/t/68864b6f-0ab8-41ef-be18-069c33df6336 | 2026-11-10 | official | GET |
| You already have high days of supply for this ASIN… (Bryce_Amazon reply) | https://sellercentral.amazon.com/seller-forums/discussions/t/aa4ec534-b230-4a4f-92fe-b0b6fc9bc392 | 2026-11-10 | official (reply) | GET |
| AWD to FBA blocked SKUS | https://sellercentral.amazon.com/seller-forums/discussions/t/5c324ac8-a3b8-4c3f-957a-ae382f8a3768 | 2026-11-10 | opinion (seller quoting the UI) | GET |
| Wrong FBA fulfillment fees… (KJ_Amazon reply on remeasurement) | https://sellercentral.amazon.co.uk/seller-forums/discussions/t/958851b3-3d11-4dec-950d-7644e6206869 | 2026-11-10 | official (reply) | GET |
| Give returns a second life with FBA Grade and Resell | https://sell.amazon.com/blog/announcements/fba-grade-and-resell | 2026-11-10 | official | GET |
| Fulfillment by Amazon | https://sell.amazon.com/fulfillment-by-amazon | 2026-11-10 | official | GET |
| Amazon Warehousing and Distribution | https://sell.amazon.com/programs/warehousing | 2026-11-10 | official | GET |
| Amazon Supply Chain Services | https://sell.amazon.com/programs/supply-chain | 2026-11-10 | official | GET |
| Role Mappings for SP-API Operations; for SP-API Types | https://developer-docs.amazon/sp-api/docs/role-mappings.md ; …/role-mappings-for-types.md | 2026-11-10 | official | GET (Markdown) |
| FBA Reports; Inventory Reports; Report Type Values | https://developer-docs.amazon/sp-api/docs/report-type-values-fba.md ; …-inventory.md ; …/report-type-values.md | 2026-11-10 | official | GET (Markdown) |
| SP-API release notes; deprecations; Support API; Data Kiosk API; Action Items API; notification type values | https://developer-docs.amazon/sp-api/docs/sp-api-release-notes.md and siblings | 2026-11-10 | official | GET (Markdown) |
| SP-API models and schemas, commit db2936aa | local clone `scratch/sp-api-plugins/models/` | 2026-11-10 | official | local |
| Selling Partner plugin 1.0.0 skills | local `scratch/sp-api-plugins/amazon-plugin-zip/` | 2026-11-10 | official | local; host not called |
| Listing playbook: inventory-and-fulfillment.md; seller-central-only-tools.md; help-page-access.md | local `packages/cx-listing-playbook/research/` | 2026-11-10 | that seat's read of 2026-10-14 | local |
| Survey 03-job-stock.md, 03-tools-cn.md | local `scratch/sp-api-plugins/` | 2026-11-10 | starting material | local, in part |
| Gerpgo help: FBA库容 | https://help.jijiaerp.com/docs/cOmfrT3w | 2026-11-10 | opinion | GET |
| Canopy Management: Amazon's New AI Rules Go Live March 4 | https://canopymanagement.com/amazon-bsa-agent-policy-march-2026/ | 2026-11-10 | opinion; official via | GET |
| PPC Land: Amazon's new AI agent rules… | https://ppc.land/amazons-new-ai-agent-rules-shake-up-sellers-before-march-4-deadline/ | 2026-11-10 | opinion; official via | GET |
| Nova Analytics: Amazon FBA Capacity Limits Reset | https://novadata.io/resources/news/amazon-fba-capacity-limits-q1-2026-reset | 2026-11-10 | opinion | GET |
| My Amazon Guy: FBA Liquidations and Donations Policy Changes in 2025 | https://myamazonguy.com/news/fba-liquidations-and-donations/ | 2026-11-10 | opinion | GET, read in part |
| Business Solutions Agreement updates effective March 4, 2026 (News_Amazon, published 2026-02-17) | https://sellercentral.amazon.com/seller-forums/discussions/t/84e3f6b1-42f7-4cf3-a189-a5cc8d78d838 | 2026-11-10 (verifier) | official | GET |
| Correction: Data Kiosk role requirements; Data Kiosk API page | https://developer-docs.amazon.com/sp-api/changelog/correction-data-kiosk-role-requirements ; …/docs/data-kiosk-api.md | 2026-11-10 (verifier) | official | GET |
| Sellers Ask Sellers mirror of the corrected Liquidations/Donations message | https://sellersasksellers.com/t/enrollment-changes-for-fba-liquidations-and-donations-programs/6434 | 2026-11-10 (verifier) | official, via Sellers Ask Sellers | GET; the text is in the page's embedded data |
| Business Solutions Agreement (G1791); Agent Policy page | https://sellercentral.amazon.com/gp/help/external/G1791 and /help/hub/reference/external/G1791 | 2026-11-10 (verifier) | — | **unreachable**: script shell |
| FBA Removals reports attributes; FBA Inventory reports attributes | https://developer-docs.amazon.com/sp-api/docs/fba-removals-reports-attributes(.md) | 2026-11-10 (verifier) | — | **unreachable** as Markdown: served the site's HTML shell, no attribute text |
| Seller Central help pages (ids in *Open questions*) | https://sellercentral.amazon.com/help/hub/reference/external/<ID> and /gp/help/external/<ID> | 2026-11-10 | — | **unreachable**: script shell on .com (both forms, `?locale=en-US`) and .co.uk; content POST off limits; reader proxy and web.archive.org captures refused by the session's permission layer |
| sell.amazon.com guessed program pages (inventory-management, liquidations, grade-and-resell, donations, capacity-management, outlet, remote-fulfillment; sell.amazon.co.uk pan-european-fba) | — | 2026-11-10 | — | **unreachable**: 404 on guessed URLs |
| EcommerceBytes 2021-12-21 and 2023-12-20 | https://www.ecommercebytes.com/2021/12/21/… ; /2023/12/20/… | 2026-11-10 | snippet only | **unreachable**: served a 5 KB challenge page |
| Eccang Chrome extension | chrome.google.com/webstore/detail/ec-amztool/… | 2026-11-10 | snippet only | **unreachable**: store page did not render |

## Verification

Verified 2026-11-10 by the verifier. Checked: 22 positions and about 95 other claims (quotations, column lists,
enums, model lines, roles, dates). Method: every forum thread, sell.amazon.com page and practitioner page in *Pages
read* was fetched again by plain GET and the quoted sentence searched for; the *FBA Reports*, *Inventory Reports*,
*Report Type Values*, release notes, deprecations, notification type values, both role-mapping pages, the Data Kiosk,
Support and Action Items pages were fetched as Markdown; model and schema lines were re-opened locally at `db2936aa`.
No Amazon API host was called and no POST made.

Absences re-tested (case-insensitive `grep -rliE` over `models/` and `schemas/`, then the same terms over the report
pages, release notes and notification page): `inventory.?performance|ipi|ipiScore`; `sell.?through`; `excess`;
`storage.?limit|capacity.?limit|restock.?limit`; `reservation.?fee|performance.?credit|capacity.?manager|capacity.?monitor`;
`capacity`; `lead.?time`; `case.?pack|reorder|replenishment.?frequency|minimum.?order`;
`maximum.?inventory|minimum.?inventory`; `auto.?remov|automated.?(un)?fulfillable|donat|grade.?and.?resell|repackag|refurbish|liquidat`;
`global.?logistics|carrier.?central|remeasur`; `utili[sz]ation`; `forecast`; `auto.?replen`; `outlet`;
`manufacturing.?cost|costOfGoods|cogs`; `stranded`; `in.?stock.?rate`; `commingl|labelOwner`; `pan.?eu|remote.?fulfil`;
`defect.?rate`; `SDS`. Held: IPI, capacity limit and usage, Restock inputs, maximum inventory level, automated
settings and enrolments, AGL, Carrier Central, remeasurement, seller-side forecast, AWD auto-replenishment, Outlet.

Absences broken, and what was done:

- **Storage utilization ratio** (§G2, table, old position 17). The file said no API returns the ratio. The *FBA
  Reports* page lists `storage_utilization_ratio`, `storage_utilization_ratio_units`, `utilization_surcharge_rate`
  and `est_sus` in `GET_FBA_STORAGE_FEE_CHARGES_DATA` (AF or PR). §G2 rewritten, R14 added, table row and position 17
  corrected.
- **Inbound performance** (§F2, table). The file said no inbound performance measure exists. The page lists the FBA
  Inbound Performance Report `GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA` (AF or PR). §F2 rewritten, R13 and
  position 23 added, table row split.
- **Capacity reservation charge** (§B5, table, open question 6). The file said `reservation fee` returned nothing and
  that a Finances appearance was unverified. `financesV0.json:3092` defines `CapacityReservationBillingEvent`; release
  notes 2023-01-25 announce it. §B5 rewritten, R12 and position 24 added, table row corrected. The limit, usage,
  request and credits remain absent.
- **Multi-channel fulfilment settings** (was "not established"). `getFeatures` / `getFeatureInventory` /
  `getFeatureSKU` (AF) read feature enrolment. R15, a table row and position 25 added.

Other changes, by position or section:

- Positions: all were already numbered `P-seller-central-only-N`; put into the sibling files' list form
  (`- **P-…-N.** …`).
- P1: added that the planning report's `sell-through` and `estimated-excess-quantity` are per-SKU. §A5 said the
  `totalFbaInventoryValue` field is in the sales-and-traffic schema; it is in
  `analytics_sellerAnalytics_2025_03_31.graphql` (type `Lending`); corrected.
- P3: "none of these figures has an API read" narrowed to the limit, estimates and usage.
- P5: "has rows only after an overage fee was charged" is an inference from the report's description; reworded to
  quote the description.
- P7: "is read on the Capacity Manager page" reworded as a dated figure with its live source.
- P11: the correction was a snippet; now read in full on the Sellers Ask Sellers mirror and tagged
  [official, via Sellers Ask Sellers]. Both Amazon forum threads re-opened: still uncorrected. Position restated to
  give both texts.
- P13: the `costOfGoodsSold` clause removed from the position, because Amazon's changelog gives the Economics dataset
  the Selling Partner Insights role (outside the five). The schema fact is confirmed (`PerUnitCost.costOfGoodsSold`,
  "This value is provided by the seller", null when not provided) and stays in §E2, whose tag was raised from
  [official, via IF] to [official] after both role statements were re-opened. Replaced by the reimbursements report
  and its `case-id` column.
- P14: removed as a position (rests wholly on a restricted role outside the five); the fact stays in §E3.
- P16: "limited per month and per item" narrowed to the monthly limit KJ_Amazon states; the per-item rule is the
  listing playbook's read, not re-read.
- P19: reworded so it does not rest on the AWD API (role outside the five).
- P20: Product Listing added to the Pan-EU report's roles (*Role Mappings for SP-API Types*); Remote Fulfillment
  eligibility added with its scope (US offers, NARF).
- P22: was [official, via Canopy and PPC Land]. Amazon's own notice was found and read; position now quotes it, tagged
  [official]. Section numbers 19 and 4.2 stay Canopy's [opinion].
- §R1, §R3, §R6, §R9: column and store-scope details added from the pages; `listFinancialEvents` roles stated.

Confirmed as written (the three claims that contradict the starting material): Fulfillment Inbound 2024-03-20 has
`listTransportationOptions` (with `AMAZON_PARTNERED_CARRIER`, `quote`, `voidableUntil`, `carrierAppointment`),
`listPlacementOptions`, `getSelfShipAppointmentSlots`, `scheduleSelfShipAppointment`, `createMarketplaceItemLabels`,
all Amazon Fulfillment on the role page; `costOfGoodsSold` is in the economics schema as quoted; Gerpgo's page says
"抓取相应亚马逊后台FBA库容统计，每天8点，12点，16点、21点更新一次" and names the sub-account permission, and nowhere on that
page names a browser extension for capacity (its page metadata gives modified 2025-03-20). Also confirmed: every
forum quotation in A3, B1, B3, C1, C4, D1, D2, D5, E1, F3, G2; the sell.amazon.com quotations; the plugin's metric
names and limits; the Support API's three operations, enum and role; AWD's 21 operations, of which 11 are on the role
page and the replenishment-order and outbound operations are not; launch dates of the Support API (2026-09-30) and
Action Items API (2026-10-28).

Could not re-open: every Seller Central help page (script shell; content call off limits), so all
[official, via IF] quotations stand on the listing playbook's read of 2026-10-14; the Business Solutions Agreement
and Agent Policy text; EcommerceBytes (challenge page); Eccang's extension page; Seller Labs on the 2025-03-31
reimbursement start; the survey's note that the storage utilization surcharge ends 2027-02-01; Gerpgo's "(亚马逊未提供API)"
line in §P3 (survey's read). The developer-docs attribute pages for removal reports served no text.

Gaps the research seat named: closed: the Liquidations/Donations correction (through a mirror); Amazon's own
words on automated access (the notice; not the agreement); MCF settings (one read). Not closed: a current numeric IPI
threshold (searches on 2026-11-10 returned vendor pages only, saying 400 or 350; no Amazon page); which pages offer a
download and in what format; the removal reports' `order-type` / `order-source` values (Amazon's page lists none;
SellerSpace's four types are a snippet); native scheduled e-mail reports (two snippets, neither opened); Outlet,
repackaging, Pan-EU and Remote Fulfillment settings pages (no read exists in the models; what the pages show is
unread).

Gaps an experienced operator would still find: the Inventory Ledger reports as the reconciliation proxy for the
shipment-reconciliation page (owned by the surface file, not named here); the Account Health page's FBA-specific
policy items; the FBA dashboard's "FBA Opportunities" cards; Seller Central user-permission names a sub-account needs
for each page; the Japanese, Indian and Brazilian twins of the capacity and IPI rules.
