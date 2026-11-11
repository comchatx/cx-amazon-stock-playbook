# Placement, exits, AWD and the peak fee

## Inbound placement

- The US inbound placement service fee has applied since 2024-03-01 (C29).
- Amazon-optimized splits carry no fee when each item ships in a minimum number of identical cartons or pallets, and minimal splits, generally one location, carry the highest fee, which varies by location (C29).
- Partial splits have been unavailable for standard-size products since 2025-02-20 (C29).
- The fee is charged after receipt on the actual inbound location and received quantities, so the figure at shipment creation is an estimate; the lag is in Amazon's 2024 letter (C29).
- For a plan, the fee is `listPlacementOptions` `fees` (Fulfillment Inbound 2024-03-20, Amazon Fulfillment); the charge is in Finances; the rate table is help page GC3Q44PBK8BXQW3Z, which this research could not read (C29).
- Through the API a placement option's fee or discount is a figure quoted on the option, set at creation, and confirming an option cannot be reversed (I15).
- The European rate card and the Japanese announcements read carry no inbound placement service fee and no inbound defect fee; "placement" in the EU card refers only to Pan-EU stock placement (C30).
- For the EU, UK, Japan and Canada no equivalent of the placement fee was found (C30).
- Inbound as a position: ../stock-inbound/SKILL.md.

## Removal, disposal and liquidation

- US removal and disposal fees are charged per unit as each unit is removed or disposed of, at unchanged rates, for orders created from 2026-03-01; the UK made the same change from 2026-05-01 (C31).
- The per-unit fee as processed is the `removal-fee` column of `GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA`, which Pricing or Amazon Fulfillment opens (C31, C39).
- The fee table is help page G5FKTA8LXU4TZPD5, which this research could not read, and the Europe rate card (C31).
- Liquidation in Canada and Europe costs a referral fee on gross recovery plus a per-item processing fee, on the Europe rate card and the Canadian News post (C32).
- Amazon staff gave a typical US recovery as a small share of the product's value; US proceeds and fee are Finances v0 `FBALiquidationEvent` (C32).
- Every way out and what is permanent: ../stuck-stock/SKILL.md.

## AWD

- AWD's bill has three parts: storage per cubic foot per month, processing per box, and transportation per cubic foot (US) (C20).
- The AWD rate page is help page GAYG62Q3MPE6STFS, which this research could not read; AWD charges as billed are in Finances (C20).
- The AWD waiver on FBA fees: references/low-inventory.md.
- AWD's 2027 storage by age: references/2027.md.

## The peak fulfilment fee

- The peak fulfilment fee is a fulfilment fee over a period Amazon posts each year; the period was the same in 2023–24 and 2026–27 (C35).
- In the US it covers FBA, Remote Fulfillment with FBA, MCF and Buy with Prime; in Europe only selected UK and German orders, not oversize, Low-Price FBA or orders delivered to other EU countries (C35).
- The period is in that year's News_Amazon holiday post on the store's seller forum: for 2026, the US post *Holiday 2026: Same fees, same eligibility, earlier deadlines*, https://sellercentral.amazon.com/seller-forums/discussions/t/3e31fbb7-04e0-4ed4-873e-f74b1052e2ff, and the UK post *Peak season 2026*, https://sellercentral.amazon.co.uk/seller-forums/discussions/t/d8c34b0b-86ed-4aec-9b0a-8be6eabb8fb0 (C35).
- The amounts are on the Europe rate card and the store's pricing page (C35).
