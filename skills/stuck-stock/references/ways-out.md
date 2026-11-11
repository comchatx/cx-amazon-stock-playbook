# Ways out: removal, disposal, liquidation, donation, Grade and Resell

- How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.

## The settings no API reaches

- The automated stranded, unfulfillable and fulfillable settings, the Liquidations and Donations enrolment and the barcode preference can be neither read nor changed through any SP-API operation, report or feed found (S15).
- These settings decide removals and disposals that happen without a seller's order (S15).
- What they caused is read in the removal order and shipment reports, the stranded report's `Date-to-take-auto-removal`, and Finances v0 `FBALiquidationEvent` (S15).
- Whether `order-type` and `order-source` in the removal reports tell an automated removal, a liquidation and a donation apart was read in Amazon's documents and not yet seen on a live store (S15).

## Creating a removal

- A removal order is created through the SP-API only by the feed `POST_FLAT_FILE_FBA_CREATE_REMOVAL` (Amazon Fulfillment; NA, EU, FE), live in 2026, with sandbox scenarios added on 2026-09-30 (S18).
- Amazon's page does not list the feed's allowed `RemovalDisposition` values; whether it can create a disposal and a liquidation was read in Amazon's documents and not yet seen on a live store (S18).
- The removal order detail report gives, per order line, requested, cancelled, disposed, shipped and in-process quantities and the removal fee (S18).
- The removal shipment report excludes cancelled and disposed items (S18).
- Both reports need Pricing or Amazon Fulfillment (S18).
- The removal and disposal fee rule and where it is read: ../stock-cost/SKILL.md (C31).

## What is permanent

- A removal order can be cancelled only while in Planning status, which lasts hours (S17).
- An order Amazon creates (a required removal, an automated removal, a disposal after notice) cannot be cancelled (S17).
- No API operation cancels a removal (S17).
- A liquidation order cannot be cancelled (S19).
- A UK or EU disposal after notice cannot be cancelled (S14).

## How long a removal takes

- Amazon's stated removal processing times differ by store and season, run from days to months at peak plus carrier time, and removal orders are worked behind customer orders in peak season (S16).
- Practitioners report removals taking many months (S16).
- No page states a current figure; the time each order took is read from `GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA` (`order-status`, dates) and `GET_FBA_FULFILLMENT_REMOVAL_SHIPMENT_DETAIL_DATA` (S16).

## Liquidation

- Amazon states that liquidators pay a gross recovery value, a fraction of the product's value, from which Amazon takes a per-item processing fee and a referral fee (S19, C32).
- Amazon states a payment period for the proceeds (S19).
- Storage and the aged surcharge stop at submission (S19, C2).
- Dave Bryant and Cathy 跨境服务 report net recovery below Amazon's stated gross range (their practice) (S19).
- US proceeds and fee are read in Finances v0 `FBALiquidationEvent`; Canada and Europe's terms are on the Europe rate card PDF linked from each `sell.amazon.<tld>/pricing` page and the store's News post (S19).
- Hazmat, recalled inventory, face masks, jewellery and expired, defective or warehouse-damaged items are not eligible for FBA Liquidations (S20).
- Finances v0 carries `FBALiquidationEvent` (proceeds and fee, by original removal order id), "used only in the US marketplace" (S22).
- Finances v0 carries `RemovalShipmentEvent` with transaction type `WHOLESALE_LIQUIDATION` (S22).
- `listFinancialEvents` needs Finance and Accounting (S22).
- Whether liquidation orders appear in the removal detail report, and where proceeds show outside the US, was read in Amazon's documents and not yet seen on a live store (S22).

## Liquidations and Donations by default: where Amazon contradicts itself

- Amazon's forum notice posted 2025-08-22 says that from 2025-09-30, in the US and Canada, a seller who has configured neither automated setting is enrolled in FBA Liquidations by default, with opt-out possible (S21).
- The same notice says FBA Donations is mandatory with no opt-out (S21).
- A "corrected" text, read only through the Sellers Ask Sellers mirror, says US only, Canada unchanged, and US Donations from 2025-10-30 (S21).
- Amazon's own US and Canadian threads still carry the 2025-08-22 text (S21).

## Donation

- A disposal is donated where the product is eligible (S23).
- Charities may not resell donated goods (S23).
- Amazon gives no tax advice on donations (S23).

## Grade and Resell

- FBA Grade and Resell grades eligible customer returns and relists them as used in one of four conditions (S24).
- It does not apply to unsold new stock (S24).
- Amazon opened it to all US FBA sellers in 2024; some third parties describe US enrolment as by invitation, seen only in search results (S24).
- On 2025-02-24 Amazon listed it as available in the UK (since 2021), France, Germany, Italy, Spain, the Czech Republic and Poland (S24).
