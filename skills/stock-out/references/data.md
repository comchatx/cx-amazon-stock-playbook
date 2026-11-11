# What out of stock is in Amazon's data

## Fields and reports

- An FBA SKU can show zero fulfillable units while units sit in fulfilment-centre transfer, in fulfilment-centre processing, held for pending customer orders, or inbound (O1).
- Each of those is its own field in `getInventorySummaries` and its own column in `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT` (O1).
- Whether reserved and fulfilment-centre transfer units can be bought is stated two ways by Amazon: ../../stock-position/SKILL.md (W10).
- Amazon's *Inventory Buyability* page, as the listing playbook's seat read it on 2026-10-14, states that a product "may be temporarily unavailable for shipping to certain parts of the country" while the seller has stock (O2).
- No SP-API field read reports availability by shopper location (O2).
- Amazon's customer-help definitions of "In Stock", "Temporarily Out of Stock" and "Currently unavailable" "only apply to products shipped and sold by Amazon", read on Amazon's mirror of page GM6AEUPCYCFUTYX7 (O3).
- No Amazon page read defines those messages for a third-party FBA offer (O3).
- The Product Pricing API reports an offer's shipping availability as `availabilityType` (`NOW`, `FUTURE_WITH_DATE`, `FUTURE_WITHOUT_DATE`), with `availableDate` only for an offer not currently available for shipping, read in Amazon's documents and not yet seen on a live store (O4).
- Orders v0 has an order type `BackOrder` for items "currently out of stock and will be available in the future", read in Amazon's documents and not yet seen on a live store (O4).
- Amazon lists "out of stock" as a reason a listing is Inactive and says it is reactivated "by updating its inventory levels" (O5).
- An open offer needs "a purchasable offer with pricing and a positive fulfillment availability quantity" (O5).
- `GET_MERCHANT_LISTINGS_INACTIVE_DATA` mixes zero-quantity listings with blocked, suppressed, not-yet-opened and expired ones, so Inactive alone does not mean out of stock (O5).
- What `getListingsItem` returns for an FBA SKU with zero fulfillable and inbound stock was read in Amazon's documents and not yet seen on a live store (O5).
- No report read gives a count of days out of stock (O17).
- The daily `Ending Warehouse Balance` of `GET_LEDGER_SUMMARY_VIEW_DATA` lets zero-balance days be counted, read in Amazon's documents and not yet seen on a live store (O17).
- An end-of-day balance says neither when in the day stock ran out nor whether the units on hand were buyable (O17).
- The role each read needs: ../../stock-position/SKILL.md.

## Amazon's in-stock and lost-sales figures

- Amazon defines the FBA in-stock rate as the percentage of time replenishable FBA products were in stock in the last 30 days, weighted by units sold in the last 60 days, in a SEAmod post of 2018-04-18 and on *Inventory performance* G202174810 as the listing seat read it on 2026-10-14 (O11).
- Amazon's IPI FAQ GZJF4DY2W6MERBAL, as the listing seat read it on 2026-10-14, says a low in-stock rate "does not hurt" the IPI score "unless your most popular products consistently go out of stock" (O11).
- By Amazon's older post, hiding a SKU on the Restock Inventory page marks it not replenishable, removes it from the rate and stops its restock recommendations (O11).
- Amazon's "estimated FBA lost sales in the last 30 days" is its forecast unit sales for the days out of stock times the average sales price, on *Inventory performance* as the listing seat read it on 2026-10-14 (O12).
- An earlier Amazon report, quoted in a seller's forum post of 2018-04-11, defined lost sales in units as the 60-day run rate times days out (O12).
- Neither definition counts lost orders (O12).
- Neither the in-stock rate nor estimated lost sales appears in any SP-API model, report schema or Data Kiosk schema read (O12).
- The Featured Offer percentage in Business Reports falls below full when the product was out of stock and for other reasons, and Amazon says it "is not necessarily an indication of the availability of your product for purchase", in *Business reports glossary* G27691 as the office captured it on 2026-10-14 (O9).
- That figure is by ASIN, not by SKU (O9).

## Subscribe & Save: the Replenishment API

- The Replenishment API, on the Brand Analytics role, is Subscribe & Save, not FBA restock (O14).
- It returns per-offer `inventory`, `stockRisk`, delivery conditions, forecast deliveries and out-of-stock metrics for past periods only (O14).
- Its out-of-stock metrics include `NOT_DELIVERED_DUE_TO_OOS` and `LOST_REVENUE_DUE_TO_OOS`, "The revenue that would have been generated had there not been out of stock" (O14).
- It is the only seller-side SP-API surface found that puts a figure on revenue lost to a stock-out (O14).
- The values `stockRisk` takes were read in Amazon's documents and not yet seen on a live store (O14).
- Sellers' stores in the API: US, CA, ES, UK, FR, IT, IN, DE, JP (O14).
- `GET_FBA_SNS_FORECAST_DATA` and `GET_FBA_SNS_PERFORMANCE_DATA` were removed on 2025-12-11 (O14).
