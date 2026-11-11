# Programs and regions: where a store's stock can serve, and special stock

What each program charges, by store: ../../stock-cost/SKILL.md.

## Europe: Pan-European FBA

- In Pan-European FBA the seller enables countries for storage, and Amazon moves stock between them "at its own discretion and at any time", so where a unit sits is Amazon's decision, not the seller's (G1).
- The countries in the program are on *Pan-European FBA* on sell.amazon.co.uk and each EU store's twin (G1, G2).
- Pan-EU status is per ASIN and depends on active offers in a required list of stores (G2).
- The required list is a dated value of Amazon's that has changed before (2020, 2025, 2026), most recently by Amazon's post of 2026-08-21 adding the Netherlands and Belgium; the current list is read on *Pan-European FBA* (G2).
- Pan-EU enrolment, per-store offer status and the date Pan-EU status expires are read per SKU from `GET_PAN_EU_OFFER_STATUS`, on the *Inventory Reports* page, for ES, UK, FR, DE and IT (G4).
- That report's layout still carries UK and Small-and-Light columns that are not statements about the 2026 program, and no read of the program's account settings was found (G4).
- Storing stock in an EU country other than the home store creates VAT reporting there; Amazon states this on the Pan-EU page (G3).
- By practitioners' reading, the same applies to the Central Europe Programme's Poland and Czech Republic (G3).
- Two developers report (2023-09-22, 2024-04-11) that under Pan-European FBA `getInventorySummaries` returns the same sum for each participating EU marketplace, the UK excluded, so adding those marketplaces multiplies the stock (W18).
- Amazon's guide does not mention it, and the repeated sum was read in developers' reports and not yet seen on a live store (W18).
- `GET_AFN_INVENTORY_DATA_BY_COUNTRY` gives the quantity available for local fulfilment per country in Europe, and movement between European countries is read from the Inventory Ledger (W19).

## The UK and the EU

- The UK and the EU are separate FBA networks (G5).
- UK stock serves EU customers, and the reverse, only through Remote Fulfilment or through stock the seller imports and stores on the other side (G5).
- Remote Fulfilment is price-capped, makes the customer or Amazon the importer, and shows the product as an import (G5).
- Amazon's 2026 UK–EU program page states a price cap on Remote Fulfilment ASINs, while its older EFN handbook states no cap and gives a VAT threshold above which the customer is importer of record; no Amazon page read reconciles the two (G6).
- Both figures are on *Sell across UK and EU borders* on sell.amazon.co.uk and in the handbook (G6).

## North America and Brazil

- Remote Fulfillment with FBA sells US FBA stock on Amazon.ca, Amazon.com.mx and Amazon.com.br, with the customer as importer of record (G8).
- Its returns go back to US stock, its fees replace US FBA fees and use the referral fee of the store of sale, and while enrolled a seller-fulfilled offer cannot share a SKU with an FBA offer (G8).
- It applies to North America and Brazil unified accounts with US FBA and FBA Export enabled; the terms are on *Remote Fulfillment with FBA* on sell.amazon.com (G8).
- Whether a Remote Fulfillment US SKU appears under the CA and MX marketplaces in the inventory reads was read in Amazon's documents and not yet seen on a live store (G8).
- An offer on Amazon.ca or Amazon.com.mx draws on US stock "unless the item is already in a fulfillment center in Canada or Mexico", so local stock comes first (G9).
- That is Amazon's statement of 2020-09-29 and the only one found; how local and remote stock take turns in 2026 was read in Amazon's documents and not yet seen on a live store (G9).
- Remote Fulfillment eligibility is per ASIN, changes over time, and is read for US offers from `GET_REMOTE_FULFILLMENT_ELIGIBILITY`, which has no destination-store column (G10).
- The unified account is one account over four stores, not one pool: stock sent to Canada, Mexico or Brazil is separate stock the seller imports (G11).
- Local FBA in Brazil is open only to accounts with Brazil as reporting country or registered on Amazon.com.br (G11).

## Other stores

- Japan, Australia, India, the UAE and Saudi Arabia are separate selling accounts with their own FBA stock (G12).
- No Amazon page read lets stock in one of them serve another; a UAE-to-Saudi remote lane is reported only by the press (2025-08-28) (G12).
- The stock age at which an aged or long-term charge starts differs by store beyond the US and European rule, and is read on the store's pricing page and, as applied, in `GET_FBA_FULFILLMENT_LONGTERM_STORAGE_FEE_CHARGES_DATA` (`surcharge-age-tier`) where that report serves the store (G13).
- In Japan and Australia two of Amazon's own pages per store disagree on that age (G13).
- In Australia, after Amazon's notice the seller has a set number of days to create a removal order for unfulfillable stock, after which Amazon disposes of it unless automated removal settings are set; the period is in News_Amazon AU's post of 2025-05-14 (G14).
- In India Amazon may dispose of or return a damaged unit if the seller has not chosen within a set period, stated in the FBA FAQ on sell.amazon.in (G14).
- Stock can sit in the seller's own building under Amazon's systems: FBA Onsite in Brazil (restricted, by invitation, domestic orders) (G22).
- In India, under Seller Flex, Amazon "manages a portion of the seller's warehouse as an Amazon fulfilment center", priced as its own channel since 2026-09-07 (G22).

## AWD and GWD

- AWD quantities (on hand, inbound to AWD, available to distribute, reserved for a replenishment order, and `replenishmentQuantity`, "in transit from AWD and has not yet been received at FBA") come from `listInventory` (W38).
- Every AWD operation on Amazon's role page needs the Amazon Warehousing and Distribution role, which the door's five roles do not include, and is documented for the US store (W38).
- The AWD model's 21 operations include ten (outbound, replenishment orders, label page types) with no role on the page (W38).
- No FBA report type on Amazon's SP-API page has an AWD column (W39).
- Amazon's AWD Inventory report, which shows AWD and FBA stock together, is a Seller Central download (W39).
- No model, report or release note carries AWD's auto-replenishment setting or its blocked-SKU list (W39).
- Amazon states that with AWD auto-replenishment enabled a product is "considered in stock and buyable" when AWD receives it, with a later delivery promise than a unit already at a fulfilment centre (W40).
- Under manual replenishment only stock in transit to FBA counts (W40).
- Which FBA field shows the AWD units Amazon calls in stock and buyable, and whether a replenishment appears as FBA inbound, was read in Amazon's documents and not yet seen on a live store (W40).
- AWD is a separate upstream pool: stock moves from AWD to FBA and never back ("You can't move inventory from FBA to AWD because items are stored differently"; unsupported as of 2024-08-21) (W41).
- AWD does no unit labelling, and AWD and FBA shipments cannot share a truckload (W41).
- AWD serves the US, and DE, FR, IT, ES and the UK since 2026-08-20 (W41).
- What AWD accepts by unit size and weight is a dated value: from 2026-07-31 units must be sortable, by help page GGTMT4PTMUMHDS6B's wording as an Amazon moderator quoted it in 2026-07, the limit Amazon also stated on 2024-04-26 (G15).
- Amazon China's AWD page states a larger per-ASIN limit, and the figures on the US AWD blog are a box limit (G15).
- The help page is one this research could not read, and `checkInboundEligibility` needs the Amazon Warehousing and Distribution role, which the five do not include (G15).
- Global Warehousing and Distribution stores stock in Shenzhen, Shanghai and Ningbo for replenishment into the US network, and no SP-API field for GWD stock was found (W42).

## Dangerous goods, meltables and expiry

- Dangerous goods are excluded from every cross-border remote program read: Remote Fulfilment UK–EU, and Remote Fulfillment with FBA to CA, MX and BR (G7).
- The US AWD blog says lithium-ion batteries are not supported at AWD, while Amazon China's AWD page admits listed lithium batteries from 2026-04; Amazon's two pages disagree (G7).
- Dangerous-goods classification can freeze stock already in a fulfilment centre: under review a product cannot be sold or inbounded, and a product classed unfulfillable is disposed of (G18).
- Meltable stock has a closed season in US and Canadian fulfilment centres whose dates Amazon sets each year (G16).
- For 2026, a notice of 2026-03-09 closed meltable inbound and set disposal for a fee, and a notice of 2026-08-28 reopened it by product type (G16).
- That year's window is in that year's meltable posts on the store's seller forum (2026: fd0e75cd… and a46c87eb… on `sellercentral.amazon.com/seller-forums`), and no operation states it (G16).
- AWD does not take meltables (G16).
- Expiry-dated stock must arrive with a minimum remaining life in US FBA and a longer one at AWD, and Amazon removes units a set number of days ahead of the date, by region (G17).
- Those figures are on the help page *Expiration dates on FBA products* G201003420, which this research could not read; they are known through an Amazon moderator's posts (2023-11-22, 2026-03-31) and ScanPower's restatement of 2024-09-10 (G17).
- Amazon treats best-by, use-by and sell-by dates as expiry dates, does not return units marked for disposal, and says a small number of consumable categories differ without naming them (G17).
- A unit past its date or whose date cannot be confirmed becomes unsellable, and once pulled it shows in `getInventorySummaries` `expiredQuantity` (G17, W16).

## Brand and compliance holds

- For a Transparency-enrolled ASIN, FBA scans codes when units arrive (G19).
- Amazon's 2024 notices to resellers say units without a valid code "cannot be sold and will be marked as "unfulfillable"", with removal or disposal as the remedy (G19).
- Transparency protection starts only after the brand passes Amazon's operational performance review, in the US, CA, DE, FR, IT, ES, UK, AU, IN and JP stores (G19).
- GPSR applies to EU stores and Northern Ireland, not Great Britain, from 2024-12-13; Amazon deactivates non-compliant offers, and a moderator's answer for non-compliant FBA stock was its removal (G20).
- In Germany, listings without a validated LUCID packaging number are blocked, since 2022-06-15 (G20).
- In France, a seller without an EPR number is enrolled in Pay on Behalf and the fees are debited from the account (G20).

## Programs that are not stock pools

- Small and Light no longer exists: the US closed it on 2023-08-29, Europe on 2023-09-26, and its API was removed in 2023 and 2024 (G21).
- Low-Price FBA is a fee rate by price, not a program or a stock pool (G21).

## Returns and ownership

- Since 2026 the extended holiday return window is annual in the US, so units sold in the holiday season can re-enter stock after it; the dates are in that year's returns-window post on the store's seller forum (G23).
- Third-party sellers keep ownership of their FBA stock, while a vendor's units bought on purchase order are Amazon's inventory, so a hybrid brand's two offers on one ASIN draw on two owners' stock (G24).

## When Amazon's pages disagree

- On 2026-11-10 the sell.amazon.com and gs.amazon.cn overview pages lagged on Pan-EU, Remote Fulfillment and AWD; the store's own program page and the newest dated announcement are the later texts (G25).
